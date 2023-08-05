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

from geojson_modelica_translator.geojson_modelica_translator import (
    GeoJsonModelicaTranslator
)
from geojson_modelica_translator.model_connectors.spawn import SpawnConnector
from geojson_modelica_translator.system_parameters.system_parameters import (
    SystemParameters
)

from ..base_test_case import TestCaseBase


class SpawnModelConnectorSingleBuildingTest(TestCaseBase):
    def setUp(self):
        project_name = "spawn_single"
        self.data_dir, self.output_dir = self.set_up(os.path.dirname(__file__), project_name)

        # load in the example geojson with a single offie building
        filename = os.path.join(self.data_dir, "spawn_geojson_ex1.json")
        self.gj = GeoJsonModelicaTranslator.from_geojson(filename)
        # use the GeoJson translator to scaffold out the directory
        self.gj.scaffold_directory(self.output_dir, project_name)

        # load system parameter data
        filename = os.path.join(self.data_dir, "spawn_system_params_ex1.json")
        sys_params = SystemParameters(filename)

        # now test the spawn connector (independent of the larger geojson translator
        self.spawn = SpawnConnector(sys_params)

        for b in self.gj.json_loads:
            self.spawn.add_building(b)

    def test_spawn_init(self):
        self.assertIsNotNone(self.spawn)
        self.assertEqual(self.spawn.system_parameters.get_param("buildings.custom")[0]["load_model"], "spawn", )

    def test_spawn_to_modelica(self):
        self.spawn.to_modelica(self.gj.scaffold)

    def test_spawn_to_modelica_and_run(self):
        self.spawn.to_modelica(self.gj.scaffold)

        file_to_run = os.path.abspath(
            os.path.join(self.gj.scaffold.loads_path.files_dir, 'B5a6b99ec37f4de7f94020090', 'coupling.mo'),
        )
        self.run_and_assert_in_docker(
            file_to_run, project_path=self.gj.scaffold.project_path, project_name=self.gj.scaffold.project_name
        )
