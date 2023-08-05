# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2012-2020 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>.

"""
Module :mod:`~openquake.hazardlib.calc.gmf` exports
:func:`ground_motion_fields`.
"""
import time
import numpy
import scipy.stats

from openquake.hazardlib.const import StdDev
from openquake.hazardlib.gsim.base import ContextMaker
from openquake.hazardlib.gsim.multi import MultiGMPE
from openquake.hazardlib.imt import from_string

U32 = numpy.uint32
F32 = numpy.float32


class CorrelationButNoInterIntraStdDevs(Exception):
    def __init__(self, corr, gsim):
        self.corr = corr
        self.gsim = gsim

    def __str__(self):
        return '''\
You cannot use the correlation model %s with the GSIM %s, \
that defines only the total standard deviation. If you want to use a \
correlation model you have to select a GMPE that provides the inter and \
intra event standard deviations.''' % (
            self.corr.__class__.__name__, self.gsim.__class__.__name__)


def rvs(distribution, *size):
    array = distribution.rvs(size)
    return array


def to_imt_unit_values(vals, imt):
    """
    Exponentiate the values unless the IMT is MMI
    """
    if str(imt) == 'MMI':
        return vals
    return numpy.exp(vals)


class GmfComputer(object):
    """
    Given an earthquake rupture, the ground motion field computer computes
    ground shaking over a set of sites, by randomly sampling a ground
    shaking intensity model.

    :param rupture:
        Rupture to calculate ground motion fields radiated from.

    :param :class:`openquake.hazardlib.site.SiteCollection` sitecol:
        a complete SiteCollection

    :param imts:
        a sorted list of Intensity Measure Type strings

    :param cmaker:
        a :class:`openquake.hazardlib.gsim.base.ContextMaker` instance

    :param truncation_level:
        Float, number of standard deviations for truncation of the intensity
        distribution, or ``None``.

    :param correlation_model:
        Instance of correlation model object. See
        :mod:`openquake.hazardlib.correlation`. Can be ``None``, in which
        case non-correlated ground motion fields are calculated.
        Correlation model is not used if ``truncation_level`` is zero.

    :param amplifier:
        None or an instance of Amplifier
    """
    # The GmfComputer is called from the OpenQuake Engine. In that case
    # the rupture is an higher level containing a
    # :class:`openquake.hazardlib.source.rupture.Rupture` instance as an
    # attribute. Then the `.compute(gsim, num_events)` method is called and
    # a matrix of size (I, N, E) is returned, where I is the number of
    # IMTs, N the number of affected sites and E the number of events. The
    # seed is extracted from the underlying rupture.
    def __init__(self, rupture, sitecol, imts, cmaker,
                 truncation_level=None, correlation_model=None,
                 amplifier=None, sec_perils=()):
        if len(sitecol) == 0:
            raise ValueError('No sites')
        elif len(imts) == 0:
            raise ValueError('No IMTs')
        elif len(cmaker.gsims) == 0:
            raise ValueError('No GSIMs')
        self.imts = [from_string(imt) for imt in imts]
        self.gsims = sorted(cmaker.gsims)
        self.truncation_level = truncation_level
        self.correlation_model = correlation_model
        self.amplifier = amplifier
        self.sec_perils = sec_perils
        # `rupture` is an EBRupture instance in the engine
        if hasattr(rupture, 'source_id'):
            self.ebrupture = rupture
            self.source_id = rupture.source_id  # the underlying source
            self.e0 = rupture.e0
            rupture = rupture.rupture  # the underlying rupture
        else:  # in the hazardlib tests
            self.source_id = '?'
            self.e0 = 0
        self.seed = rupture.rup_id
        self.rctx, self.sctx, self.dctx = cmaker.make_contexts(
            sitecol, rupture)
        self.sids = self.sctx.sids
        if correlation_model:  # store the filtered sitecol
            self.sites = sitecol.complete.filtered(self.sids)
        self.offset = 0  # can be overridden by the engine

    def compute_all(self, min_iml, rlzs_by_gsim, sig_eps=None):
        """
        :returns: [(sid, eid, gmv), ...], dt
        """
        t0 = time.time()
        sids = self.sids
        eids_by_rlz = self.ebrupture.get_eids_by_rlz(rlzs_by_gsim, self.offset)
        mag = self.ebrupture.rupture.mag
        data = []
        No = sum(len(sp.outputs) for sp in self.sec_perils)
        for gs, rlzs in rlzs_by_gsim.items():
            num_events = sum(len(eids_by_rlz[rlzi]) for rlzi in rlzs)
            # NB: the trick for performance is to keep the call to
            # compute.compute outside of the loop over the realizations
            # it is better to have few calls producing big arrays
            array, sig, eps = self.compute(gs, num_events)
            array = array.transpose(1, 0, 2)  # from M, N, E to N, M, E
            for i, miniml in enumerate(min_iml):  # gmv < minimum
                arr = array[:, i, :]
                arr[arr < miniml] = 0
            n = 0
            for rlzi in rlzs:
                eids = eids_by_rlz[rlzi] + self.e0
                e = len(eids)
                for ei, eid in enumerate(eids):
                    gmfa = array[:, :, n + ei]  # shape (N, M)
                    tot = gmfa.sum(axis=0)  # shape (M,)
                    if not tot.sum():
                        continue
                    if sig_eps is not None:
                        tup = tuple([eid, rlzi] + list(sig[:, n + ei]) +
                                    list(eps[:, n + ei]))
                        sig_eps.append(tup)
                    sp_out = numpy.zeros((No,) + gmfa.shape)  # No, N, M
                    for m, imt in enumerate(self.imts):
                        o = 0
                        for sp in self.sec_perils:
                            o1 = o + len(sp.outputs)
                            sp_out[o:o1, :, m] = sp.compute(
                                mag, imt, gmfa[:, m], self.sctx)
                            o = o1
                    for i, gmv in enumerate(gmfa):
                        if gmv.sum():
                            if No:
                                data.append((sids[i], eid, gmv) +
                                            tuple(sp_out[:, i, :]))
                            else:
                                data.append((sids[i], eid, gmv))
                        # gmv can be zero due to the minimum_intensity, coming
                        # from the job.ini or from the vulnerability functions
                n += e
        dt = F32, (len(min_iml),)
        dtlist = [('sid', U32), ('eid', U32), ('gmv', dt)] + [
            (out, dt) for sp in self.sec_perils for out in sp.outputs]
        d = numpy.array(data, dtlist)
        return d, time.time() - t0

    def compute(self, gsim, num_events):
        """
        :param gsim: a GSIM instance
        :param num_events: the number of seismic events
        :returns:
            a 32 bit array of shape (num_imts, num_sites, num_events) and
            two arrays with shape (num_imts, num_events): sig for stddev_inter
            and eps for the random part
        """
        result = numpy.zeros((len(self.imts), len(self.sids), num_events), F32)
        sig = numpy.zeros((len(self.imts), num_events), F32)
        eps = numpy.zeros((len(self.imts), num_events), F32)
        numpy.random.seed(self.seed)
        for imti, imt in enumerate(self.imts):
            if isinstance(gsim, MultiGMPE):
                gs = gsim[str(imt)]  # MultiGMPE
            else:
                gs = gsim  # regular GMPE
            try:
                result[imti], sig[imti], eps[imti] = self._compute(
                     gs, num_events, imt)
            except Exception as exc:
                raise exc.__class__(
                    '%s for %s, %s, source_id=%s' %
                    (exc, gs, imt, self.source_id)
                ).with_traceback(exc.__traceback__)
        if self.amplifier:
            self.amplifier.amplify_gmfs(
                self.sctx.ampcode, result, self.imts, self.seed)
        return result, sig, eps

    def _compute(self, gsim, num_events, imt):
        """
        :param gsim: a GSIM instance
        :param num_events: the number of seismic events
        :param imt: an IMT instance
        :returns: (gmf(num_sites, num_events), stddev_inter(num_events),
                   epsilons(num_events))
        """
        dctx = self.dctx.roundup(gsim.minimum_distance)
        if self.truncation_level == 0:
            if self.correlation_model:
                raise ValueError('truncation_level=0 requires '
                                 'no correlation model')
            mean, _stddevs = gsim.get_mean_and_stddevs(
                self.sctx, self.rctx, dctx, imt, stddev_types=[])
            gmf = to_imt_unit_values(mean, imt)
            gmf.shape += (1, )
            gmf = gmf.repeat(num_events, axis=1)
            return (gmf,
                    numpy.zeros(num_events, F32),
                    numpy.zeros(num_events, F32))
        elif self.truncation_level is None:
            distribution = scipy.stats.norm()
        else:
            assert self.truncation_level > 0, self.truncation_level
            distribution = scipy.stats.truncnorm(
                - self.truncation_level, self.truncation_level)

        num_sids = len(self.sids)
        if gsim.DEFINED_FOR_STANDARD_DEVIATION_TYPES == {StdDev.TOTAL}:
            # If the GSIM provides only total standard deviation, we need
            # to compute mean and total standard deviation at the sites
            # of interest.
            # In this case, we also assume no correlation model is used.
            if self.correlation_model:
                raise CorrelationButNoInterIntraStdDevs(
                    self.correlation_model, gsim)

            mean, [stddev_total] = gsim.get_mean_and_stddevs(
                self.sctx, self.rctx, dctx, imt, [StdDev.TOTAL])
            stddev_total = stddev_total.reshape(stddev_total.shape + (1, ))
            mean = mean.reshape(mean.shape + (1, ))

            total_residual = stddev_total * rvs(
                distribution, num_sids, num_events)
            gmf = to_imt_unit_values(mean + total_residual, imt)
            stdi = numpy.nan
            epsilons = numpy.empty(num_events, F32)
            epsilons.fill(numpy.nan)
        else:
            mean, [stddev_inter, stddev_intra] = gsim.get_mean_and_stddevs(
                self.sctx, self.rctx, dctx, imt,
                [StdDev.INTER_EVENT, StdDev.INTRA_EVENT])
            stddev_intra = stddev_intra.reshape(stddev_intra.shape + (1, ))
            stddev_inter = stddev_inter.reshape(stddev_inter.shape + (1, ))
            mean = mean.reshape(mean.shape + (1, ))
            intra_residual = stddev_intra * rvs(
                distribution, num_sids, num_events)

            if self.correlation_model is not None:
                intra_residual = self.correlation_model.apply_correlation(
                    self.sites, imt, intra_residual, stddev_intra)
                sh = intra_residual.shape
                if len(sh) == 1:  # a vector
                    intra_residual = intra_residual.reshape(sh + (1,))

            epsilons = rvs(distribution, num_events)
            inter_residual = stddev_inter * epsilons

            gmf = to_imt_unit_values(
                mean + intra_residual + inter_residual, imt)
            stdi = stddev_inter.max(axis=0)
        return gmf, stdi, epsilons


# this is not used in the engine; it is still useful for usage in IPython
# when demonstrating hazardlib capabilities
def ground_motion_fields(rupture, sites, imts, gsim, truncation_level,
                         realizations, correlation_model=None, seed=None):
    """
    Given an earthquake rupture, the ground motion field calculator computes
    ground shaking over a set of sites, by randomly sampling a ground shaking
    intensity model. A ground motion field represents a possible 'realization'
    of the ground shaking due to an earthquake rupture.

    .. note::

     This calculator is using random numbers. In order to reproduce the
     same results numpy random numbers generator needs to be seeded, see
     http://docs.scipy.org/doc/numpy/reference/generated/numpy.random.seed.html

    :param openquake.hazardlib.source.rupture.Rupture rupture:
        Rupture to calculate ground motion fields radiated from.
    :param openquake.hazardlib.site.SiteCollection sites:
        Sites of interest to calculate GMFs.
    :param imts:
        List of intensity measure type objects (see
        :mod:`openquake.hazardlib.imt`).
    :param gsim:
        Ground-shaking intensity model, instance of subclass of either
        :class:`~openquake.hazardlib.gsim.base.GMPE` or
        :class:`~openquake.hazardlib.gsim.base.IPE`.
    :param truncation_level:
        Float, number of standard deviations for truncation of the intensity
        distribution, or ``None``.
    :param realizations:
        Integer number of GMF realizations to compute.
    :param correlation_model:
        Instance of correlation model object. See
        :mod:`openquake.hazardlib.correlation`. Can be ``None``, in which case
        non-correlated ground motion fields are calculated. Correlation model
        is not used if ``truncation_level`` is zero.
    :param int seed:
        The seed used in the numpy random number generator
    :returns:
        Dictionary mapping intensity measure type objects (same
        as in parameter ``imts``) to 2d numpy arrays of floats,
        representing different realizations of ground shaking intensity
        for all sites in the collection. First dimension represents
        sites and second one is for realizations.
    """
    cmaker = ContextMaker(rupture.tectonic_region_type, [gsim])
    rupture.rup_id = seed
    gc = GmfComputer(rupture, sites, [str(imt) for imt in imts],
                     cmaker, truncation_level, correlation_model)
    res, _sig, _eps = gc.compute(gsim, realizations)
    return {imt: res[imti] for imti, imt in enumerate(gc.imts)}
