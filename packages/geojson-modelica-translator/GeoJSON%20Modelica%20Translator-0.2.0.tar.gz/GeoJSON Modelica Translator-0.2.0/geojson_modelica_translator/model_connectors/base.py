"""
****************************************************************************************************
:copyright (c) 2019-2020 URBANopt, Alliance for Sustainable Energy, LLC, and other contributors.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted
provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions
and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions
and the following disclaimer in the documentation and/or other materials provided with the
distribution.

Neither the name of the copyright holder nor the names of its contributors may be used to endorse
or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
****************************************************************************************************
"""

import os
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from modelica_builder.model import Model


class Base(object):
    """
    Base class of the model connectors. The connectors can utilize various methods to create a building (or other
    feature) to a detailed Modelica connection. For example, a simple RC model (using TEASER), a ROM, CSV file, etc.
    """

    def __init__(self, system_parameters):
        """
        Base initializer

        :param system_parameters: SystemParameters object
        """
        self.buildings = []
        self.system_parameters = system_parameters

        # initialize the templating framework (Jinja2)
        self.template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        self.template_env = Environment(loader=FileSystemLoader(searchpath=self.template_dir))

        # store a list of the templated files to include when building the package
        self.template_files_to_include = []

        # Note that the order of the required MO files is important as it will be the order that
        # the "package.order" will be in.
        self.required_mo_files = []
        # extract data out of the urbanopt_building object and store into the base object

    def add_building(self, urbanopt_building, mapper=None):
        """
        Add building to the translator.

        :param urbanopt_building: an urbanopt_building
        """
        pass
        # TODO: Need to convert units, these should exist on the urbanopt_building object
        # TODO: Abstract out the GeoJSON functionality
        if mapper is None:
            number_stories = urbanopt_building.feature.properties["number_of_stories"]
            try:
                number_stories_above_ground = urbanopt_building.feature.properties["number_of_stories_above_ground"]
            except KeyError:
                number_stories_above_ground = urbanopt_building.feature.properties["number_of_stories"]

            try:
                urbanopt_building.feature.properties["floor_height"]
            except KeyError:
                urbanopt_building.feature.properties["floor_height"] = 3  # Default height in meters from sdk

            try:
                # UO SDK defaults to current year, however TEASER only supports up to Year 2015
                # https://github.com/urbanopt/TEASER/blob/master/teaser/data/input/inputdata/TypeBuildingElements.json#L818
                if urbanopt_building.feature.properties["year_built"] > 2015:
                    urbanopt_building.feature.properties["year_built"] = 2015
            except KeyError:
                urbanopt_building.feature.properties["year_built"] = 2015

            self.buildings.append(
                {
                    "area": float(urbanopt_building.feature.properties["floor_area"]) * 0.092936,  # ft2 -> m2
                    "building_id": urbanopt_building.feature.properties["id"],
                    "building_type": urbanopt_building.feature.properties["building_type"],
                    "floor_height": urbanopt_building.feature.properties["floor_height"],  # Already converted to metric
                    "num_stories": urbanopt_building.feature.properties["number_of_stories"],
                    "num_stories_below_grade": number_stories - number_stories_above_ground,
                    "year_built": urbanopt_building.feature.properties["year_built"],
                }
            )

    def copy_required_mo_files(self, dest_folder, within=None):
        """Copy any required_mo_files to the destination and update the within clause if defined. The required mo
        files need to be added as full paths to the required_mo_files member variable in the connectors derived
        classes.

        :param dest_folder: String, folder to copy the resulting MO files into.
        :param within: String, within clause to be replaced in the .mo file. Note that the original MO file needs to
        have a within clause defined to be replaced.
        """
        result = []
        for f in self.required_mo_files:
            if not os.path.exists(f):
                raise Exception(f"Required MO file not found: {f}")

            new_filename = os.path.join(dest_folder, os.path.basename(f))
            if within:
                mofile = Model(f)
                mofile.set_within_statement(within)
                mofile.save_as(new_filename)
                result.append(os.path.join(dest_folder, os.path.basename(f)))
            else:
                # simply copy the file over if no need to update within
                result.append(shutil.copy(f, new_filename))

        return result

    def run_template(self, template, save_file_name, do_not_add_to_list=False, **kwargs):
        """
        Helper method to create the file from Jinja2's templating framework.

        :param template: object, Jinja template from the `template_env.get_template()` command.
        :param save_file_name: string, fully qualified path to save the rendered template to.
        :param do_not_add_to_list: boolean, set to true if you do not want the file to be added to the package.order
        :param kwargs: These are the arguments that need to be passed to the template.

        :return: None
        """
        file_data = template.render(**kwargs)

        os.makedirs(os.path.dirname(save_file_name), exist_ok=True)
        with open(save_file_name, "w") as f:
            f.write(file_data)

        # add to the list of files to include in the package
        if not do_not_add_to_list:
            self.template_files_to_include.append(Path(save_file_name).stem)

    def modelica_path(self, filename):
        """Write a modelica path string for a given filename"""
        p = Path(filename)
        if p.suffix == ".idf":
            # TODO: The output path is awfully brittle.
            # FIXME: The string is hideous, but without it Pathlib thinks double slashes are "spurious"
            # https://docs.python.org/3/library/pathlib.html#pathlib.PurePath
            outputname = "modelica://" + str(Path("Buildings") / "Resources" / "Data"
                                             / "ThermalZones" / "EnergyPlus" / "Validation" / "RefBldgSmallOffice"
                                             / p.name)
        elif p.suffix == ".epw" or p.suffix == ".mos":
            outputname = "modelica://" + str(Path("Buildings") / "Resources" / "weatherdata" / p.name)
        return outputname

    # These methods need to be defined in each of the derived model connectors
    # def to_modelica(self):
