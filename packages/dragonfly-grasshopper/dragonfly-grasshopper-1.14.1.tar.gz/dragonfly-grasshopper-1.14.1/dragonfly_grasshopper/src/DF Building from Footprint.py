# Dragonfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Dragonfly.
#
# Copyright (c) 2019, Ladybug Tools.
# You should have received a copy of the GNU General Public License
# along with Dragonfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Create Dragonfly Buildings from footprint geometry (horizontal Rhino surfaces).
-

    Args:
        _footprint_geo: A list of horizontal Rhino surfaces to be converted
            into Buildings.
        _floor_to_floor: A list of float values with a length equal to the number of
            stories in each Building. Each value in the list represents the
            floor_to_floor height of the Story starting from the first floor and
            then moving to the top floor.
        perim_offset_: An optional positive number that will be used to offset
            the perimeter of the footprint to create core/perimeter Rooms.
            If this value is None or 0, no offset will occur and each floor
            plate will be represented with a single Room2D.
        _name_: Text to set the base name for the Building, which will also be
            incorporated into unique Building identifier. This will be combined
            with the index of each input _footprint_geo to yield a unique name
            for each output Building. If the name is not provided, a random one
            will be assigned.
        _program_: Text for the program of the Buildings (to be looked up in the
            ProgramType library) such as that output from the "HB List Programs"
            component. This can also be a custom ProgramType object. If no program
            is input here, the Buildings will have a generic office program.
        _constr_set_: Text for the construction set of the Buildings, which is used
            to assign all default energy constructions needed to create an energy
            model. Text should refer to a ConstructionSet within the library such
            as that output from the "HB List Construction Sets" component. This
            can also be a custom ConstructionSet object. If nothing is input here,
            the Buildings will have a generic construction set that is not sensitive
            to the Buildings's climate or building energy code.
        conditioned_: Boolean to note whether the Buildings have heating and cooling
            systems.
        _run: Set to True to run the component and create Dragonfly Buildings.
    
    Returns:
        report: Reports, errors, warnings, etc.
        buildings: Dragonfly buildings.
"""

ghenv.Component.Name = "DF Building from Footprint"
ghenv.Component.NickName = 'BuildingFootprint'
ghenv.Component.Message = '0.2.0'
ghenv.Component.Category = "Dragonfly"
ghenv.Component.SubCategory = '0 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = "2"

# document-wide counter to generate new unique Building identifiers
import scriptcontext
try:
    scriptcontext.sticky["bldg_count"]
except KeyError:  # first time that the component is running
    scriptcontext.sticky["bldg_count"] = 1

try:  # import the core honeybee dependencies
    from honeybee.typing import clean_and_id_string
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

try:  # import the core dragonfly dependencies
    from dragonfly.building import Building
except ImportError as e:
    raise ImportError('\nFailed to import dragonfly:\n\t{}'.format(e))

try:
    from ladybug_rhino.config import tolerance
    from ladybug_rhino.togeometry import to_face3d
    from ladybug_rhino.grasshopper import all_required_inputs
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))

try:  # import the dragonfly-energy extension
    import dragonfly_energy
    from honeybee_energy.lib.programtypes import program_type_by_identifier, \
        office_program
    from honeybee_energy.lib.constructionsets import construction_set_by_identifier
except ImportError as e:
    if _program_ is not None:
        raise ValueError('_program_ has been specified but dragonfly-energy '
                         'has failed to import.\n{}'.format(e))
    elif _constr_set_ is not None:
        raise ValueError('_constr_set_ has been specified but dragonfly-energy '
                         'has failed to import.\n{}'.format(e))
    elif conditioned_ is not None:
        raise ValueError('conditioned_ has been specified but dragonfly-energy '
                         'has failed to import.\n{}'.format(e))

import uuid


if all_required_inputs(ghenv.Component) and _run:
    perim_offset_ = 0 if perim_offset_ is None else perim_offset_
    buildings = []  # list of buildings that will be returned

    for i, geo in enumerate(_footprint_geo):
        # get the name for the Building
        if _name_ is None:  # make a default Building name
            name = "Building_{}_{}".format(scriptcontext.sticky["bldg_count"],
                                           str(uuid.uuid4())[:8])
            scriptcontext.sticky["bldg_count"] += 1
        else:
            display_name = '{}_{}'.format(_name_, i + 1)
            name = clean_and_id_string(display_name)

        # create the Building
        building = Building.from_footprint(
            name, footprint=to_face3d(geo), floor_to_floor_heights=_floor_to_floor,
            perimeter_offset=perim_offset_, tolerance=tolerance)
        if _name_ is not None:
            building.display_name = display_name

        # assign the program
        if _program_ is not None:
            if isinstance(_program_, str):
                _program_ = program_type_by_identifier(_program_)
            building.properties.energy.set_all_room_2d_program_type(_program_)
        else:  # generic office program by default
            try:
                building.properties.energy.set_all_room_2d_program_type(office_program)
            except (NameError, AttributeError):
                pass  # honeybee-energy is not installed

        # assign the construction set
        if _constr_set_ is not None:
            if isinstance(_constr_set_, str):
                _constr_set_ = construction_set_by_identifier(_constr_set_)
            building.properties.energy.construction_set = _constr_set_

        # assign an ideal air system
        if conditioned_ or conditioned_ is None:  # conditioned by default
            try:
                building.properties.energy.add_default_ideal_air()
            except (NameError, AttributeError):
                pass  # honeybee-energy is not installed

        buildings.append(building)
