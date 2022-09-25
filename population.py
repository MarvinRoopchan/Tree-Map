from __future__ import annotations
import json
from typing import Optional, List, Dict

from tree_data import AbstractTree

# Constants for the World Bank population files
WORLD_BANK_POPULATIONS = 'populations.json'
WORLD_BANK_REGIONS = 'regions.json'


class PopulationTree(AbstractTree):
    """A tree representation of country population data.

    This tree always has three levels:
      - The root represents the entire world.
      - Each node in the second level is a region (defined by the World Bank).
      - Each node in the third level is a country.

    The data_size attribute corresponds to the 2019 population of the country,
    as reported by the World Bank.

    """

    def __init__(self: PopulationTree, world: bool,
                 root: Optional[object] = None,
                 subtrees: Optional[List[PopulationTree]] = None,
                 data_size: int = 0) -> None:
        """Initialize a new PopulationTree.

        If <world> is True, then this tree is the root of the population tree,
        and it should load data from the World Bank files.
        In this case, none of the other parameters are used.

        If <world> is False, pass the other arguments directly to the superclass
        constructor. Do NOT load new data from the World Bank files.
        """
        if world:
            region_trees = _load_data()
            AbstractTree.__init__(self, 'World', region_trees)
        else:
            if subtrees is None:
                subtrees = []
            AbstractTree.__init__(self, root, subtrees, data_size)

    def get_separator(self: AbstractTree) -> str:
        """ Return a Population Tree specific separator string."""

        return '->'


def _load_data() -> List[PopulationTree]:
    """Create a list of trees corresponding to different world regions.

    Each tree consists of a root node -- the region -- attached to one or
    more leaves -- the countries in that region.
    """
    # Get data from World Bank files.
    country_populations = _get_population_data()
    regions = _get_region_data()

    population_trees = []
    for region in regions:
        subtrees = []
        for country in regions[region]:
            if country in country_populations:
                population = country_populations[country]
                tree = PopulationTree(False, country, [], population)
                subtrees.append(tree)
        internal_node = PopulationTree(False, region, subtrees)
        population_trees.append(internal_node)

    return population_trees

    # Be sure to read the docstring of the PopulationTree constructor to see
    # how to call it.
    # You'll want to complete the two helpers called above first (otherwise
    # this function won't run).
    # You can complete this function *without* using recursion.
    # Remember that each region tree has only two levels:
    #   - a root storing the name of the region
    #   - zero or more leaves, each representing a country in the region


def _get_population_data() -> Dict[str, int]:
    """Return country population data from the World Bank.

    The return value is a dictionary, where the keys are country names,
    and the values are the corresponding populations of those countries.

    Ignore all countries that do not have any population data,
    or population data that cannot be read as an int.
    """
    # We are doing some pre-processing of the data for you.
    # The first element returned is ignored because it's just metadata.
    # The second element's first 47 elements are ignored because they aren't
    # countries.
    _, population_data = _get_json_data(WORLD_BANK_POPULATIONS)
    population_data = population_data[47:]

    # The following line is a good place to put a breakpoint, so that you can
    # pause the program and use the debugger to inspect the contents of
    # population_data.
    countries = {}

    for x in population_data:
        if isinstance(x['value'], int):
            countries[x['country']['value']] = \
                x['value']

    return countries


def _get_region_data() -> Dict[str, List[str]]:
    """Return country region data from the World Bank.

    The return value is a dictionary, where the keys are region names,
    and the values a list of country names contained in that region.

    Ignore all regions that do not contain any countries.
    """
    # We ignore the first component of the returned JSON, which is metadata.
    _, country_data = _get_json_data(WORLD_BANK_REGIONS)

    # The following line is a good place to put a breakpoint to help inspect
    # the contents of country_data.
    regions = {}

    for country in country_data:
        if country['region']['id'] != 'NA':
            if country['region']['value'] not in regions:
                regions[country['region']['value']] = [country['name']]

            else:
                regions[country['region']['value']].append(country['name'])

    return regions


def _get_json_data(fname: str) -> dict:
    """Return a dictionary representing the JSON data from file fname.

    You should not modify this function.
    """
    f = open(fname)
    return json.loads(f.read())


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(
        config={
            'allowed-io': ['_get_json_data'],
            'extra-imports': ['json', 'tree_data']})
