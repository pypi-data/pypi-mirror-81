


import plotly.graph_objs as go
from plotly.offline import plot
import cea.plots.demand
from cea.plots.variable_naming import NAMING, COLOR, LOGO
from cea.constants import HOURS_IN_YEAR
import pandas as pd

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2018, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "2.8"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


class LoadDurationCurvePlot(cea.plots.demand.DemandPlotBase):
    name = "Load Duration Curve"

    def __init__(self, project, parameters, cache):
        super(LoadDurationCurvePlot, self).__init__(project, parameters, cache)
        self.analysis_fields = ["E_sys_kWh",
                                "Qhs_sys_kWh", "Qww_sys_kWh",
                                "Qcs_sys_kWh", 'Qcdata_sys_kWh', 'Qcre_sys_kWh']

    @property
    def data(self):
        return self.hourly_loads[self.hourly_loads['Name'].isin(self.buildings)]

    @property
    def layout(self):
        return go.Layout(xaxis=dict(title='Duration Normalized [%]'),
                         yaxis=dict(title='Load [kW]'), showlegend=True)

    def calc_graph(self):
        graph = []
        duration = range(HOURS_IN_YEAR)
        x = [(a - min(duration)) / (max(duration) - min(duration)) * 100 for a in duration]
        self.analysis_fields = self.remove_unused_fields(self.data, self.analysis_fields)
        for field in self.analysis_fields:
            name = NAMING[field]
            y = self.data.sort_values(by=field, ascending=False)[field].values
            trace = go.Scattergl(x=x, y=y, name=name, fill='tozeroy', opacity=0.8,
                               marker=dict(color=COLOR[field]))
            graph.append(trace)
        return graph

    def calc_table(self):
        # calculate variables for the analysis
        self.analysis_fields = self.remove_unused_fields(self.data, self.analysis_fields)
        load_peak = self.data[self.analysis_fields].max().round(2).tolist()
        load_total = (self.data[self.analysis_fields].sum() / 1000).round(2).tolist()

        # calculate graph
        load_utilization = []
        load_names = []
        # data = ''
        duration = range(HOURS_IN_YEAR)
        x = [(a - min(duration)) / (max(duration) - min(duration)) * 100 for a in duration]
        for field in self.analysis_fields:
            data_frame_new = self.data.sort_values(by=field, ascending=False)
            y = data_frame_new[field].values
            load_utilization.append(evaluate_utilization(x, y))
            load_names.append(NAMING[field] + ' (' + field.split('_', 1)[0] + ')')
        column_names = ['Load Name', 'Peak Load [kW]', 'Yearly Demand [MWh]', 'Utilization [-]']
        column_data = [load_names, load_peak, load_total, load_utilization]
        table_df = pd.DataFrame({cn: cd for cn, cd in zip(column_names, column_data)}, columns=column_names)
        return table_df


def load_duration_curve(data_frame, analysis_fields, title, output_path):
    # CALCULATE GRAPH
    traces_graph = calc_graph(analysis_fields, data_frame)

    # CALCULATE TABLE
    traces_table = calc_table(analysis_fields, data_frame)

    # PLOT GRAPH

    traces_graph.append(traces_table)
    layout = go.Layout(images=LOGO, title=title, xaxis=dict(title='Duration Normalized [%]', domain=[0, 1]),
                       yaxis=dict(title='Load [kW]', domain=[0.0, 0.7]), showlegend=True)
    fig = go.Figure(data=traces_graph, layout=layout)
    plot(fig, auto_open=False, filename=output_path)

    return {'data': traces_graph, 'layout': layout}


def calc_table(analysis_fields, data_frame):
    # calculate variables for the analysis
    load_peak = data_frame[analysis_fields].max().round(2).tolist()
    load_total = (data_frame[analysis_fields].sum() / 1000).round(2).tolist()

    # calculate graph
    load_utilization = []
    load_names = []
    # data = ''
    duration = range(HOURS_IN_YEAR)
    x = [(a - min(duration)) / (max(duration) - min(duration)) * 100 for a in duration]
    for field in analysis_fields:
        data_frame_new = data_frame.sort_values(by=field, ascending=False)
        y = data_frame_new[field].values
        load_utilization.append(evaluate_utilization(x, y))
        load_names.append(NAMING[field] + ' (' + field.split('_', 1)[0] + ')')
    table = go.Table(domain=dict(x=[0, 1], y=[0.7, 1.0]),
                     header=dict(
                         values=['Load Name', 'Peak Load [kW]', 'Yearly Demand [MWh]', 'Utilization [-]']),
                     cells=dict(values=[load_names, load_peak, load_total, load_utilization]))
    return table


def calc_graph(analysis_fields, data_frame):
    graph = []
    duration = range(HOURS_IN_YEAR)
    x = [(a - min(duration)) / (max(duration) - min(duration)) * 100 for a in duration]
    for field in analysis_fields:
        name = NAMING[field]
        data_frame_new = data_frame.sort_values(by=field, ascending=False)
        y = data_frame_new[field].values
        trace = go.Scattergl(x=x, y=y, name=name, fill='tozeroy', opacity=0.8,
                           marker=dict(color=COLOR[field]))
        graph.append(trace)

    return graph


def evaluate_utilization(x, y):
    dataframe_util = pd.DataFrame({'x': x, 'y': y})
    if 0 in dataframe_util['y'].values:
        index_occurrence = dataframe_util['y'].idxmin(axis=0, skipna=True)
        utilization_perc = round(dataframe_util.loc[index_occurrence, 'x'], 1)
        utilization_days = int(utilization_perc * HOURS_IN_YEAR / (24 * 100))
        return str(utilization_perc) + '% or ' + str(utilization_days) + ' days a year'
    else:
        return 'all year'


if __name__ == '__main__':
    import cea.config
    import cea.inputlocator

    config = cea.config.Configuration()
    locator = cea.inputlocator.InputLocator(config.scenario)
    cache = cea.plots.cache.PlotCache(config.project)
    # cache = cea.plots.cache.NullPlotCache()

    LoadDurationCurvePlot(config.project, {'buildings': None,
                                           'scenario-name': config.scenario_name,
                                           'timeframe': config.plots.timeframe},
                          cache).plot(auto_open=True)
    LoadDurationCurvePlot(config.project, {'buildings': locator.get_zone_building_names()[0:2],
                                           'scenario-name': config.scenario_name,
                                           'timeframe': config.plots.timeframe},
                          cache).plot(auto_open=True)
    LoadDurationCurvePlot(config.project, {'buildings': [locator.get_zone_building_names()[0]],
                                           'scenario-name': config.scenario_name,
                                           'timeframe': config.plots.timeframe},
                          cache).plot(auto_open=True)
