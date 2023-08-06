"""
Lists the plots by category. See ``cea/plots/__init__.py`` for documentation on how plots are organized and
the conventions for adding new plots.
"""




import pkgutil
import importlib
import inspect
import cea.plots
import cea.config
import cea.inputlocator
import cea.plots.cache
import cea.plots.base
from typing import Type

__author__ = "Daren Thomas"
__copyright__ = "Copyright 2018, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Daren Thomas"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def list_categories(plugins):
    """List all the categories implemented in the CEA"""
    import cea.plots
    for importer, modname, ispkg in pkgutil.iter_modules(cea.plots.__path__, cea.plots.__name__ + '.'):
        if not ispkg:
            # only consider subfolders of cea/plots to be categories
            continue
        module = importlib.import_module(modname)
        if not hasattr(module, 'label'):
            # doesn't implement the interface for categories (__init__.py must have a "label" attribute)
            continue
        try:
            yield PlotCategory(module)
        except GeneratorExit:
            return
        except:
            # this module does not follow the conventions outlined in ``cea.plots.__init__.py`` and will be
            # ignored
            continue
    for plugin in plugins:
        for plot_category in plugin.plot_categories:
            yield plot_category


def load_category(category_name, plugins):
    """Returns a PlotsCategory object if is_valid_category(category), else None"""
    for c in list_categories(plugins=plugins):
        if c.name == category_name:
            return c
    return None


def load_plot_by_id(category_name, plot_id, plugins):
    """
    plot_id is a web-friendly way of expressing the plot's name (which is more english friendly)
    """
    category = load_category(category_name, plugins)
    if category:
        for plot in category.plots:
            if plot.id() == plot_id or plot.id() == plot_id.replace("-", "_"):
                return plot
        else:
            print("ERROR: Could not find plot {plot}".format(plot=plot_id))
            return None
    print('ERROR: Could not find plot category {category}'.format(category=category_name))
    return None


def list_plots(plugins):
    for plot_category in list_categories(plugins):
        for plot_class in plot_category.plots:
            yield plot_category, plot_class


class PlotCategory(object):
    """Contains the data of a plot category."""
    def __init__(self, module):
        self._module = module
        self.name = module.__name__.split('.')[-1].replace('_', '-')
        self.label = module.label

    @property
    def plots(self):
        """

        :return: Generator[PlotBase]
        """
        for importer, modname, ispkg in pkgutil.iter_modules(self._module.__path__, self._module.__name__ + '.'):
            if ispkg:
                # only consider modules - not packages
                continue
            module = importlib.import_module(modname)
            for cls_name, cls_object in inspect.getmembers(module, inspect.isclass):
                if cea.plots.PlotBase in inspect.getmro(cls_object):
                    yield cls_object


if __name__ == '__main__':
    from pprint import pprint
    config = cea.config.Configuration()
    cache = cea.plots.cache.NullPlotCache()
    errors = []

    for category in list_categories(plugins=config.plugins):
        print('category:', category.name, ':', category.label)
        for plot_class in category.plots:
            try:
                print('plot_class:', plot_class)
                parameters = {
                    k: config.get(v) for k, v in plot_class.expected_parameters.items()
                }
                plot = plot_class(config.project, parameters=parameters, cache=cache)
                assert plot.name, 'plot missing name: %s' % plot
                assert plot.category_name == category.name
                print('plot:', plot.name, '/', plot.id(), '/', plot.title)

                # plot the plot!
                plot.plot()

                # write plot data
                plot.plot_data_to_file()

            except Exception as e:
                errors.append({'plot': plot_class, 'error': e})

    pprint(errors)
