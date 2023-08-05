#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from setuptools import find_packages, setup

from management.format_modelica_files import FormatModelicaFiles
from management.update_licenses import UpdateLicenses
from management.update_schemas import UpdateSchemas

# Dependencies to checkout MBL
# import os
# import shutil
# from io import BytesIO
# from sys import platform  # #AA added
# from zipfile import ZipFile
#
# from requests import get

with open("README.rst") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="GeoJSON Modelica Translator",
    version="0.2.0",
    description="Package for converting GeoJSON to Modelica models for Urban Scale Analyses.",
    long_description="Package for converting GeoJSON to Modelica models for Urban Scale Analyses.",
    author="Nicholas Long",
    author_email="nicholas.long@nrel.gov",
    url="https://github.com/urbanopt/geojson_modelica_translator",
    license=license,
    packages=find_packages(exclude=("tests", "docs")),
    cmdclass={
        "update_schemas": UpdateSchemas,
        "update_licenses": UpdateLicenses,
        "format_modelica_files": FormatModelicaFiles,
    },
    install_requires=[
        "geojson==2.5.0",
        "jsonschema==3.2.0",
        "jsonpath-ng==1.5.2",
        "requests==2.24.0",
        'teaser @ git+https://github.com/urbanopt/TEASER.git@rc-argument-names#egg=teaser',
        "modelica-builder==0.1.0",
        # 'modelica_builder @ git+https://github.com/urbanopt/modelica-builder.git@develop#egg=modelica_builder',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)


# Do not checkout MBL for now. This will need to be reeneabled once non-developers start using it.
#
# # install portions of the Modelica Buildings Library for grabbing files as needed (e.g. MOS files, examples, etc)
# libs_to_extract = ["Buildings/Applications/DHC"]
# save_path = "geojson_modelica_translator/modelica/buildingslibrary"
# tmp_save_path = "geojson_modelica_translator/modelica/tmp_buildingslibrary"
# repo_name = "lbl-srg/modelica-buildings"
# if os.path.exists(save_path):
#     shutil.rmtree(save_path)
# if os.path.exists(tmp_save_path):
#     shutil.rmtree(tmp_save_path)
# # mbl_archive_name = "issue1437_district_heating_cooling"
# mbl_archive_name = "2eb417f9ca2a9dce188988f1937bf79253daa9ff"  # AA needed to use this in order to avoid an error about a package.order file # noqa
# r = get(f"https://github.com/{repo_name}/archive/{mbl_archive_name}.zip")
# with ZipFile(BytesIO(r.content)) as zip:
#     files = zip.namelist()
#     for file in files:
#         # check if this needs to be extracted by looking into the libs_to_extract list
#         for lib_to_extract in libs_to_extract:
#             # make the path system independent when searching
#             if platform == "win64" or platform == "win32":  # AA added this to resolve an error due to a too-long file path # noqa
#                 # if os.path.join(lib_to_extract.replace("/", os.path.sep)) in file:
#                 if os.path.join(lib_to_extract) in file:
#                     print(f"extracting ... {file}")
#                     # zip.extract(file, path=tmp_save_path)
#                     zip.extract(file)  # AA replaced this due to file path length
#             else:  # AA added, for non-Windows case
#                 if os.path.join(lib_to_extract.replace("/", os.path.sep)) in file:
#                     print(f"extracting ... {file}")
#                     zip.extract(file, path=tmp_save_path)
#
#
# # Move the whole directory
# if platform == "win64" or platform == "win32":
#     shutil.move(f"{repo_name}-{mbl_archive_name}", save_path)  # AA modified this due to problem with file path length
# else:
#     shutil.move(os.path.join(tmp_save_path, f"{repo_name}-{mbl_archive_name}"), save_path)
#
# # clean up/remove the tmp directory
# if os.path.exists(tmp_save_path):
#     shutil.rmtree(tmp_save_path)
