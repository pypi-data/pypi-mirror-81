# Copyright(c) 2020 Jake Fowler
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import clr
import System as dotnet
import System.Collections.Generic as dotnet_cols_gen
import pathlib as pl

clr.AddReference(str(pl.Path('cmdty_storage/lib/Cmdty.Core.Simulation')))
import Cmdty.Core.Simulation as net_sim
import Cmdty.Storage as net_cs

import pandas as pd
import numpy as np
from datetime import datetime, date
import typing as tp
from cmdty_storage import utils, CmdtyStorage
from cmdty_storage import time_func as tf
import math

FactorCorrsType = tp.Optional[tp.Union[float, np.ndarray]]

class MultiFactorSpotSim:

    def __init__(self,
                 freq: str,
                 factors: tp.Iterable[tp.Tuple[float, utils.CurveType]],
                 factor_corrs: FactorCorrsType,
                 current_date: tp.Union[datetime, date, str, pd.Period],
                 fwd_curve: utils.CurveType,
                 sim_periods: tp.Iterable[tp.Union[pd.Period, datetime, date, str]],
                 seed: tp.Optional[int] = None
                 # time_func: Callable[[Union[datetime, date], Union[datetime, date]], float] TODO add this back in
                 ):
        factor_corrs = _validate_multi_factor_params(factors, factor_corrs)
        if freq not in utils.FREQ_TO_PERIOD_TYPE:
            raise ValueError("freq parameter value of '{}' not supported. The allowable values can be found in the "
                             "keys of the dict curves.FREQ_TO_PERIOD_TYPE.".format(freq))

        time_period_type = utils.FREQ_TO_PERIOD_TYPE[freq]

        net_multi_factor_params = _create_net_multi_factor_params(factor_corrs, factors, time_period_type)
        net_forward_curve = utils.curve_to_net_dict(fwd_curve, time_period_type)
        net_current_date = utils.py_date_like_to_net_datetime(current_date)
        net_time_func = dotnet.Func[dotnet.DateTime, dotnet.DateTime, dotnet.Double](net_sim.TimeFunctions.Act365)
        net_sim_periods = dotnet_cols_gen.List[time_period_type]()
        [net_sim_periods.Add(utils.from_datetime_like(p, time_period_type)) for p in sim_periods]

        if seed is None:
            mt_rand = net_sim.MersenneTwisterGenerator()
        else:
            mt_rand = net_sim.MersenneTwisterGenerator(seed)
        mt_rand = net_sim.INormalGenerator(mt_rand)

        self._net_simulator = net_sim.MultiFactor.MultiFactorSpotPriceSimulator[time_period_type](
            net_multi_factor_params, net_current_date, net_forward_curve, net_sim_periods, net_time_func, mt_rand)
        self._sim_periods = [_to_pd_period(freq, p) for p in sim_periods]
        self._freq = freq

    def simulate(self, num_sims: int) -> pd.DataFrame:
        net_sim_results = self._net_simulator.Simulate(num_sims)
        spot_sim_array = utils.as_numpy_array(net_sim_results.SpotPrices)
        spot_sim_array.resize((net_sim_results.NumSteps, net_sim_results.NumSims))
        period_index = pd.PeriodIndex(data=self._sim_periods, freq=self._freq)
        return pd.DataFrame(data=spot_sim_array, index=period_index)


def _to_pd_period(freq: str, date_like: tp.Union[pd.Period, datetime, date, str]) -> pd.Period:
    if isinstance(date_like, pd.Period):
        return date_like
    return pd.Period(date_like, freq=freq)


def _create_net_multi_factor_params(factor_corrs, factors, time_period_type):
    net_factors = dotnet_cols_gen.List[net_sim.MultiFactor.Factor[time_period_type]]()
    for mean_reversion, vol_curve in factors:
        net_vol_curve = utils.curve_to_net_dict(vol_curve, time_period_type)
        net_factors.Add(net_sim.MultiFactor.Factor[time_period_type](mean_reversion, net_vol_curve))
    net_factor_corrs = utils.as_net_array(factor_corrs)
    net_multi_factor_params = net_sim.MultiFactor.MultiFactorParameters[time_period_type](net_factor_corrs,
                                                                                          *net_factors)
    return net_multi_factor_params


def _validate_multi_factor_params(  # TODO unit test validation fails
        factors: tp.Iterable[tp.Tuple[float, utils.CurveType]],
        factor_corrs: FactorCorrsType) -> np.ndarray:
    factors_len = len(factors)
    if factors_len == 0:
        raise ValueError("factors cannot be empty.")
    if factors_len == 1 and factor_corrs is None:
        factor_corrs = np.array([[1.0]])
    if factors_len == 2 and (isinstance(factor_corrs, float) or isinstance(factor_corrs, int)):
        factor_corrs = np.array([[1.0, float(factor_corrs)],
                                 [float(factor_corrs), 1.0]])

    if factor_corrs.ndim != 2:
        raise ValueError("Factor correlation matrix is not 2-dimensional.")
    corr_shape = factor_corrs.shape
    if corr_shape[0] != corr_shape[1]:
        raise ValueError("Factor correlation matrix is not square.")
    if factor_corrs.dtype != np.float64:
        factor_corrs = factor_corrs.astype(np.float64)
    for (i, j), corr in np.ndenumerate(factor_corrs):
        if i == j:
            if not np.isclose([corr], [1.0]):
                raise ValueError("Factor correlation on diagonal position ({i}, {j}) value of {corr} not valid as not "
                                 "equal to 1.").format(i=i, j=j, corr=corr)
        else:
            if not -1 <= corr <= 1:
                raise ValueError("Factor correlation in position ({i}, {j}) value of {corr} not valid as not in the "
                                 "interval [-1, 1]".format(i=i, j=j, corr=corr))
    num_factors = corr_shape[0]
    if factors_len != num_factors:
        raise ValueError("factors and factor_corrs are of inconsistent sizes.")
    for idx, (mr, vol) in enumerate(factors):
        if mr < 0.0:
            raise ValueError("Mean reversion value of {mr} for factor at index {idx} not valid as is negative.".format(
                mr=mr, idx=idx))
    return factor_corrs


# TODO convert to common key types for vol curve and fwd contracts
class MultiFactorModel:
    _corr_tolerance = 1E-10  # TODO more scientific way of finding this.
    _factors: tp.List[tp.Tuple[float, utils.CurveType]]
    _factor_corrs: FactorCorrsType
    _time_func: utils.TimeFunctionType

    def __init__(self,
                 freq: str,
                 factors: tp.Iterable[tp.Tuple[float, utils.CurveType]],
                 factor_corrs: FactorCorrsType = None,
                 time_func: tp.Optional[utils.TimeFunctionType] = None):
        self._factor_corrs = _validate_multi_factor_params(factors, factor_corrs)
        self._factors = list(factors)
        self._time_func = tf.act_365 if time_func is None else time_func

    def integrated_covar(self,
                         obs_start: utils.TimePeriodSpecType,
                         obs_end: utils.TimePeriodSpecType,
                         fwd_contract_1: utils.ForwardPointType,
                         fwd_contract_2: utils.ForwardPointType) -> float:
        obs_start_t = 0.0
        obs_end_t = self._time_func(obs_start, obs_end)
        if obs_end_t < 0.0:
            raise ValueError("obs_end cannot be before obs_start.")
        fwd_1_t = self._time_func(obs_start, fwd_contract_1)
        fwd_2_t = self._time_func(obs_start, fwd_contract_2)

        cov = 0.0
        for (i, j), corr in np.ndenumerate(self._factor_corrs):
            mr_i, vol_curve_i = self._factors[i]
            vol_i = self._get_factor_vol(i, fwd_contract_1,
                                         vol_curve_i)  # TODO if converted to nested loop vol_i could be looked up less
            mr_j, vol_curve_j = self._factors[j]
            vol_j = self._get_factor_vol(j, fwd_contract_2, vol_curve_j)
            cov += vol_i * vol_j * self._factor_corrs[i, j] * math.exp(-mr_i * fwd_1_t - mr_j * fwd_2_t) * \
                   self._cont_ext(-obs_start_t, -obs_end_t, mr_i + mr_j)
        return cov

    def integrated_variance(self,
                            obs_start: utils.TimePeriodSpecType,
                            obs_end: utils.TimePeriodSpecType,
                            fwd_contract: utils.ForwardPointType) -> float:
        return self.integrated_covar(obs_start, obs_end, fwd_contract, fwd_contract)

    def integrated_stan_dev(self,
                            obs_start: utils.TimePeriodSpecType,
                            obs_end: utils.TimePeriodSpecType,
                            fwd_contract: utils.ForwardPointType) -> float:
        return math.sqrt(self.integrated_covar(obs_start, obs_end, fwd_contract, fwd_contract))

    def integrated_vol(self,
                       val_date: utils.TimePeriodSpecType,
                       expiry: utils.TimePeriodSpecType,
                       fwd_contract: utils.ForwardPointType) -> float:
        time_to_expiry = self._time_func(val_date, expiry)
        if time_to_expiry <= 0:
            raise ValueError("val_date must be before expiry.")
        return math.sqrt(self.integrated_covar(val_date, expiry, fwd_contract, fwd_contract) / time_to_expiry)

    def integrated_corr(self,
                        obs_start: utils.TimePeriodSpecType,
                        obs_end: utils.TimePeriodSpecType,
                        fwd_contract_1: utils.ForwardPointType,
                        fwd_contract_2: utils.ForwardPointType) -> float:
        covariance = self.integrated_covar(obs_start, obs_end, fwd_contract_1, fwd_contract_2)
        variance_1 = self.integrated_variance(obs_start, obs_end, fwd_contract_1)
        variance_2 = self.integrated_variance(obs_start, obs_end, fwd_contract_2)
        corr = covariance / math.sqrt(variance_1 * variance_2)
        if 1.0 < corr < (1.0 + self._corr_tolerance):
            return 1.0
        if (-1.0 - self._corr_tolerance) < corr < -1:
            return -1.0
        return corr

    @staticmethod
    def _cont_ext(c1, c2, x) -> float:
        if x == 0.0:
            return c1 - c2
        return (math.exp(-x * c2) - math.exp(-x * c1)) / x

    @staticmethod
    def _get_factor_vol(factor_num, fwd_contract, vol_curve) -> float:
        vol = vol_curve.get(fwd_contract, None)
        if vol is None:
            raise ValueError(
                "No point in vol curve of factor {factor_num} for fwd_contract_1 value of {fwd}.".format(
                    factor_num=factor_num, fwd=fwd_contract))
        return vol


class MultiFactorValuationResults(tp.NamedTuple):
    npv: float


def multi_factor_value(cmdty_storage: CmdtyStorage,
                       val_date: utils.TimePeriodSpecType,
                       inventory: float,
                       fwd_curve: pd.Series,
                       interest_rates: pd.Series,
                       settlement_rule: tp.Callable[[pd.Period], date],
                       factors: tp.Iterable[tp.Tuple[float, utils.CurveType]],
                       factor_corrs: FactorCorrsType,
                       num_sims: int,
                       seed: tp.Optional[int] = None,
                       regress_poly_degree: int = 2,
                       regress_cross_products: bool = True,
                       num_inventory_grid_points: int = 100,
                       numerical_tolerance: float = 1E-12
                       ) -> MultiFactorValuationResults:
    factor_corrs = _validate_multi_factor_params(factors, factor_corrs)
    if cmdty_storage.freq != fwd_curve.index.freqstr:
        raise ValueError("cmdty_storage and forward_curve have different frequencies.")

    time_period_type = utils.FREQ_TO_PERIOD_TYPE[cmdty_storage.freq]
    net_multi_factor_params = _create_net_multi_factor_params(factor_corrs, factors, time_period_type)
    net_forward_curve = utils.series_to_double_time_series(fwd_curve, time_period_type)
    net_current_period = utils.from_datetime_like(val_date, time_period_type)
    net_grid_calc = net_cs.FixedSpacingStateSpaceGridCalc.CreateForFixedNumberOfPointsOnGlobalInventoryRange[
        time_period_type](cmdty_storage.net_storage, num_inventory_grid_points)
    net_settlement_rule = utils.wrap_settle_for_dotnet(settlement_rule, cmdty_storage.freq)
    net_interest_rate_time_series = utils.series_to_double_time_series(interest_rates, utils.FREQ_TO_PERIOD_TYPE['D'])
    net_discount_func = net_cs.StorageHelper.CreateAct65ContCompDiscounterFromSeries(net_interest_rate_time_series)

    net_val_results = net_cs.LsmcStorageValuation.Calculate[time_period_type](net_current_period,
                                                                              inventory, net_forward_curve,
                                                                              cmdty_storage.net_storage,
                                                                              net_settlement_rule, net_discount_func,
                                                                              net_grid_calc, numerical_tolerance,
                                                                              net_multi_factor_params, num_sims, seed,
                                                                              regress_poly_degree,
                                                                              regress_cross_products)
    return MultiFactorValuationResults(net_val_results.Npv)
