# -*- coding: utf-8 -*-
"""
refrigeration loads
"""



import numpy as np
import pandas as pd
from cea.technologies import heatpumps
from cea.constants import HOURS_IN_YEAR
from cea.demand.constants import T_C_REF_SUP_0, T_C_REF_RE_0

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca", "Martin Mosteiro", "Gabriel Happle"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def has_refrigeration_load(bpr):
    """
    Checks if building has a hot water system

    :param bpr: BuildingPropertiesRow
    :type bpr: cea.demand.building_properties.BuildingPropertiesRow
    :return: True or False
    :rtype: bool
        """

    if bpr.internal_loads['Qcre_Wm2'] > 0:
        return True
    else:
        return False


def calc_Qcre_sys(bpr, tsd, schedules):
    # calculate refrigeration loads
    tsd['Qcre'] = schedules['Qcre_W'] * -1.0  # cooling loads are negative
    # calculate distribution losses for refrigeration loads analogously to space cooling distribution losses
    Y = bpr.building_systems['Y'][0]
    Lv = bpr.building_systems['Lv']
    Qcre_d_ls = ((T_C_REF_SUP_0 + T_C_REF_RE_0) / 2.0 - tsd['T_ext']) * (tsd['Qcre'] / np.nanmin(tsd['Qcre'])) * (Lv * Y)

    # calculate system loads for data center
    tsd['Qcre_sys'] = abs(tsd['Qcre'] + Qcre_d_ls) #make sure you get the right mcpcre positive
    # writing values to tsd, replacing function and np.vectorize call with simple for loop
    tsd['mcpcre_sys'], tsd['Tcre_sys_re'], tsd['Tcre_sys_sup'] =\
        np.vectorize(calc_refrigeration_temperature_and_massflow)(tsd['Qcre_sys'])

    return tsd


def calc_refrigeration_temperature_and_massflow(Qcre_sys):
    """
    Calculate refrigeration supply and return temperatures and massflows based on the refrigeration load
    This function is intended to be used in np.vectorize form
    :param Qcre_sys: refrigeration load including losses
    :return: refrigeration massflow, refrigeration supply temperature, refrigeration return temperature
    """

    if Qcre_sys > 0.0:
        Tcre_sys_re = T_C_REF_RE_0
        Tcre_sys_sup = T_C_REF_SUP_0
        mcpcre_sys = Qcre_sys / (T_C_REF_RE_0 - T_C_REF_SUP_0)
    else:
        mcpcre_sys = 0.0
        Tcre_sys_re = np.nan
        Tcre_sys_sup = np.nan

    return mcpcre_sys, Tcre_sys_re, Tcre_sys_sup


def calc_Qref(locator, bpr, tsd):
    """
    it calculates final loads
    """
    # GET SYSTEMS EFFICIENCIES
    energy_source = bpr.supply["source_cs"]
    scale_technology = bpr.supply["scale_cs"]
    efficiency_average_year = bpr.supply["eff_cs"]
    if scale_technology == "BUILDING":
        if energy_source == "GRID":
            t_source = (tsd['T_ext'] + 273)
            # heat pump energy
            tsd['E_cre'] = np.vectorize(heatpumps.HP_air_air)(tsd['mcpcre_sys'], (tsd['Tcre_sys_sup'] + 273),
                                                                (tsd['Tcre_sys_re'] + 273), t_source)
            # final to district is zero
            tsd['DC_cre'] = np.zeros(HOURS_IN_YEAR)
        elif energy_source == "NONE":
            tsd['E_cre'] = np.zeros(HOURS_IN_YEAR)
            tsd['DC_cre'] = np.zeros(HOURS_IN_YEAR)
        else:
            raise Exception('check potential error in input database of LCA infrastructure / COOLING')

    elif scale_technology == "DISTRICT":
        tsd['DC_cre'] = tsd['Qcs_sys'] / efficiency_average_year
        tsd['E_cre'] = np.zeros(HOURS_IN_YEAR)
    elif scale_technology == "NONE":
        tsd['DC_cre'] = np.zeros(HOURS_IN_YEAR)
        tsd['E_cre'] = np.zeros(HOURS_IN_YEAR)
    else:
        raise Exception('check potential error in input database of LCA infrastructure / COOLING')
    return tsd

