"""
The weather-helper script sets the weather data used (``inputs/weather.epw``) for simulations.
"""




import os
import cea.config
import cea.inputlocator

__author__ = "Daren Thomas"
__copyright__ = "Copyright 2019, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Daren Thomas"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def copy_weather_file(source_weather_file, locator):
    """
    Copy a weather file to the scenario's inputs.

    :param string source_weather_file: path to a weather file (``*.epw``)
    :param cea.inputlocator.InputLocator locator: use the InputLocator to find output path
    :return: (this script doesn't return anything)
    """
    from shutil import copyfile
    assert os.path.exists(source_weather_file), "Could not find weather file: {source_weather_file}".format(
        source_weather_file=source_weather_file
    )
    copyfile(source_weather_file, locator.get_weather_file())
    print("Set weather for scenario <{scenario}> to {source_weather_file}".format(
        scenario=os.path.basename(locator.scenario),
        source_weather_file=source_weather_file
    ))


def main(config):
    """
    Assign the weather file to the input folder.

    :param cea.config.Configuration config: Configuration object for this script
    :return:
    """
    assert os.path.exists(config.scenario), 'Scenario not found: %s' % config.scenario
    locator = cea.inputlocator.InputLocator(config.scenario)

    copy_weather_file(config.weather_helper.weather, locator)


if __name__ == '__main__':
    main(cea.config.Configuration())
