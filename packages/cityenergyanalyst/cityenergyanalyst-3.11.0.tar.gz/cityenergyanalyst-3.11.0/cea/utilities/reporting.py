"""
Functions for Report generation
"""



import numpy as np
import pandas as pd
import os
from plotly.offline import plot
import plotly.graph_objs as go
from cea.constants import HOURS_IN_YEAR



__author__ = "Gabriel Happle"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Gabriel Happle", "Daren Thomas"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def full_report_to_xls(tsd, output_folder, basename):
    """ this function is to write a full report to an ``*.xls`` file containing all intermediate and final results of a
    single building thermal loads calculation"""

    df = pd.DataFrame(tsd)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    #timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    #output_path = os.path.join(output_folder,"%(basename)s-%(timestamp)s.xls" % locals())
    output_path = os.path.join(output_folder, "%(basename)s.xls" % locals())
    writer = pd.ExcelWriter(output_path, engine='xlwt')

    df.to_excel(writer, na_rep='NaN')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    writer.close()


def quick_visualization_tsd(tsd, output_folder, basename):

    # import keys
    from cea.demand.thermal_loads import TSD_KEYS_HEATING_LOADS, TSD_KEYS_HEATING_TEMP, TSD_KEYS_RC_TEMP, \
        TSD_KEYS_COOLING_LOADS, TSD_KEYS_MOISTURE, TSD_KEYS_VENTILATION_FLOWS, TSD_KEYS_COOLING_SUPPLY_TEMP, \
        TSD_KEYS_COOLING_SUPPLY_FLOWS

    # set to True to produce plotly graphs of selected variables
    plot_heat_load = True
    plot_heat_temp = True
    plot_cool_load = True
    plot_cool_moisture = True
    plot_cool_air = True
    plot_cool_sup = True
    auto_open = False 

    if plot_heat_load:
        filename = os.path.join(output_folder, "heat-load-{}.html").format(basename)
        traces = []
        for key in TSD_KEYS_HEATING_LOADS:
            y = tsd[key][50:150]
            trace = go.Scattergl(x=np.linspace(1, 100, 100), y=y, name=key, mode='lines+markers')
            traces.append(trace)
        fig = go.Figure(data=traces)
        plot(fig, filename=filename, auto_open=auto_open)

    if plot_heat_temp:
        filename = os.path.join(output_folder, "heat-temp-{}.html").format(basename)
        traces = []
        keys = []
        keys.extend(TSD_KEYS_HEATING_TEMP)
        keys.extend(TSD_KEYS_RC_TEMP)
        for key in keys:
            y = tsd[key][50:150]
            trace = go.Scattergl(x=np.linspace(1, 100, 100), y=y, name=key, mode='lines+markers')
            traces.append(trace)
        fig = go.Figure(data=traces)
        plot(fig, filename=filename, auto_open=auto_open)

    if plot_cool_load:
        filename = os.path.join(output_folder, "cool-load-{}.html").format(basename)
        traces = []
        for key in TSD_KEYS_COOLING_LOADS:
            y = tsd[key]
            trace = go.Scattergl(x=np.linspace(1, HOURS_IN_YEAR, HOURS_IN_YEAR), y=y, name=key, mode='lines+markers')
            traces.append(trace)
        fig = go.Figure(data=traces)
        plot(fig, filename=filename, auto_open=auto_open)

    if plot_cool_moisture:
        filename = os.path.join(output_folder, "cool-moisture-{}.html").format(basename)
        traces = []
        for key in TSD_KEYS_MOISTURE:
            y = tsd[key]
            trace = go.Scattergl(x=np.linspace(1, HOURS_IN_YEAR, HOURS_IN_YEAR), y=y, name=key, mode='lines+markers')
            traces.append(trace)
        fig = go.Figure(data=traces)
        plot(fig, filename=filename, auto_open=auto_open)

    if plot_cool_air:
        filename = os.path.join(output_folder, "cool-air-{}.html").format(basename)
        traces = []
        for key in TSD_KEYS_VENTILATION_FLOWS:
            y = tsd[key]
            trace = go.Scattergl(x=np.linspace(1, HOURS_IN_YEAR, HOURS_IN_YEAR), y=y, name=key, mode='lines+markers')
            traces.append(trace)
        fig = go.Figure(data=traces)
        plot(fig, filename=filename, auto_open=auto_open)

    if plot_cool_sup:
        filename = os.path.join(output_folder, "cool-sup-{}.html").format(basename)
        traces = []
        keys = []
        keys.extend(TSD_KEYS_COOLING_SUPPLY_TEMP)
        keys.extend(TSD_KEYS_COOLING_SUPPLY_FLOWS)
        for key in keys:
            y = tsd[key]
            trace = go.Scattergl(x=np.linspace(1, HOURS_IN_YEAR, HOURS_IN_YEAR), y=y, name=key, mode='lines+markers')
            traces.append(trace)
        fig = go.Figure(data=traces)
        plot(fig, filename=filename, auto_open=auto_open)