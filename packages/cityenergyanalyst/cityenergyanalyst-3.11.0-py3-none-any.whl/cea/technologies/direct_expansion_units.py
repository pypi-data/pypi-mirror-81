# -*- coding: utf-8 -*-
"""
direct expansion units
"""





import numpy as np

from cea.analysis.costs.equations import calc_capex_annualized
from cea.constants import HEAT_CAPACITY_OF_WATER_JPERKGK

__author__ = "Shanshan Hsieh"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Shanshan Hsieh"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"

# FIXME: this model is simplified, and required update
PRICE_DX_PER_W = 1.6  # USD FIXME: to be moved to database


# operation costs

def calc_cop_DX(Q_load_W):
    cop = 2.3

    return cop


def calc_DX(mdot_kgpers, T_sup_K, T_re_K):
    if np.isclose(mdot_kgpers, 0.0):
        q_chw_W = 0.0
        wdot_W = 0.0
    else:
        q_chw_W = mdot_kgpers * HEAT_CAPACITY_OF_WATER_JPERKGK * (T_re_K - T_sup_K)

        cop_DX = calc_cop_DX(q_chw_W)

        wdot_W = q_chw_W / cop_DX

    return wdot_W, q_chw_W


# investment and maintenance costs

def calc_Cinv_DX(Q_design_W):
    """
    Assume the same cost as gas boilers.
    :type Q_design_W : float
    :param Q_design_W: Design Load of Boiler in [W]
    :rtype InvCa : float
    :returns InvCa: Annualized investment costs in CHF/a including Maintenance Cost
    """
    Capex_a_DX_USD = 0
    Opex_fixed_DX_USD = 0
    Capex_DX_USD = 0

    if Q_design_W > 0:
        InvC = Q_design_W * PRICE_DX_PER_W
        Inv_IR = 5
        Inv_LT = 25
        Inv_OM = 5 / 100

        Capex_a_DX_USD = calc_capex_annualized(InvC, Inv_IR, Inv_LT)
        Opex_fixed_DX_USD = InvC * Inv_OM
        Capex_DX_USD = InvC

    return Capex_a_DX_USD, Opex_fixed_DX_USD, Capex_DX_USD
