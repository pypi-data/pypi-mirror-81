#!/usr/bin/env python
# -*- coding: utf-8 -*-

# AROSICS - Automated and Robust Open-Source Image Co-Registration Software
#
# Copyright (C) 2017-2020  Daniel Scheffler (GFZ Potsdam, daniel.scheffler@gfz-potsdam.de)
#
# This software was developed within the context of the GeoMultiSens project funded
# by the German Federal Ministry of Education and Research
# (project grant code: 01 IS 14 010 A-C).
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for the local co-registration module of AROSICS."""

import unittest
import shutil
import os
from pkgutil import find_loader

# custom
from .cases import test_cases
from arosics import COREG_LOCAL
from geoarray import GeoArray


class COREG_LOCAL_init(unittest.TestCase):
    """Test case on object initialization of COREG_LOCAL."""

    def setUp(self):
        self.ref_path = test_cases['INTER1']['ref_path']
        self.tgt_path = test_cases['INTER1']['tgt_path']
        self.coreg_kwargs = test_cases['INTER1']['kwargs_local']

    def test_coreg_init_from_disk(self):
        self.CRL = COREG_LOCAL(self.ref_path, self.tgt_path, **self.coreg_kwargs)

    def test_coreg_init_from_inMem_GeoArray(self):
        # get GeoArray instances
        self.ref_gA = GeoArray(self.ref_path)
        self.tgt_gA = GeoArray(self.tgt_path)

        # assure the raster data are in-memory
        self.ref_gA.to_mem()
        self.tgt_gA.to_mem()

        # get instance of COREG_LOCAL object
        self.CRL = COREG_LOCAL(self.ref_gA, self.tgt_gA, **self.coreg_kwargs)


class CompleteWorkflow_INTER1_S2A_S2A(unittest.TestCase):
    """Test case for the complete workflow of local co-registration based on two Sentinel-2 datasets, one with
    ~25% cloud cover, the other one without any clouds. The subsets cover the S2A tiles only partly (nodata areas
    are present).
    """

    def setUp(self):
        self.ref_path = test_cases['INTER1']['ref_path']
        self.tgt_path = test_cases['INTER1']['tgt_path']
        self.coreg_kwargs = test_cases['INTER1']['kwargs_local']

    def tearDown(self):
        """Delete output."""
        dir_out = os.path.dirname(self.coreg_kwargs['path_out'])
        if os.path.isdir(dir_out):
            shutil.rmtree(dir_out)

    def test_calculation_of_tie_point_grid(self):
        # get instance of COREG_LOCAL object
        CRL = COREG_LOCAL(self.ref_path, self.tgt_path, **self.coreg_kwargs)

        # use the getter of the CoRegPoints_table to calculate tie point grid
        # noinspection PyStatementEffect
        CRL.CoRegPoints_table

        # test tie point grid visualization
        if find_loader('mpl_toolkits.basemap'):  # only works if basemap is installed
            CRL.view_CoRegPoints(hide_filtered=True)
            CRL.view_CoRegPoints(hide_filtered=False)
            CRL.view_CoRegPoints(shapes2plot='vectors')

        if find_loader('folium') and find_loader('geojson'):
            CRL.view_CoRegPoints_folium()

        # test shift correction and output writer
        CRL.correct_shifts()

        self.assertTrue(os.path.exists(self.coreg_kwargs['path_out']),
                        'Output of local co-registration has not been written.')

    def test_calculation_of_tie_point_grid_float_coords(self):
        # NOTE: This does not test against unequaly sized output of get_image_windows_to_match().

        # overwrite gt and prj
        ref = GeoArray(self.ref_path)
        ref.to_mem()
        ref.filePath = None
        tgt = GeoArray(self.tgt_path)
        tgt.to_mem()
        tgt.filePath = None

        ref.gt = [330000.19999996503, 10.00000001, 0.0, 5862000.7999997628, 0.0, -10.00000001]
        # ref.gt = [330000.1, 10.1, 0.0, 5862000.1, 0.0, -10.1]
        tgt.gt = [335440.19999996503, 10.00000001, 0.0, 5866490.7999997628, 0.0, -10.00000001]
        # tgt.gt = [330000.1, 10.1, 0.0, 5862000.1, 0.0, -10.1]

        # get instance of COREG_LOCAL object
        CRL = COREG_LOCAL(ref, tgt, **dict(CPUs=32,
                                           **self.coreg_kwargs))

        # use the getter of the CoRegPoints_table to calculate tie point grid
        # noinspection PyStatementEffect
        CRL.CoRegPoints_table


# if __name__ == '__main__':
#     unittest.main(argv=['first-arg-is-ignored'],exit=False, verbosity=2)
#
#      suite = unittest.TestLoader().loadTestsFromTestCase(eval("CompleteWorkflow_INTER1_S2A_S2A"))
#     alltests = unittest.TestSuite(suite)
#
#      # Part 2: Saving the results of each testsuite and the query for the job.status in individual variables.
#      testResult = unittest.TextTestRunner(verbosity=2).run(alltests)
