# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Leland Stanford Junior University
# Copyright (c) 2018 The Regents of the University of California
#
# This file is part of pelicun.
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, 
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors 
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
# 
# You should have received a copy of the BSD 3-Clause License along with 
# pelicun. If not, see <http://www.opensource.org/licenses/>.
#
# Contributors:
# Adam Zsarnóczay

"""
This subpackage performs unit tests on the file_io module of pelicun.

"""

import pytest

import os, sys, inspect
current_dir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0,os.path.dirname(parent_dir))

from pelicun.file_io import *

# -------------------------------------------------------------------------------
# read_SimCenter_DL_input
# ------------------------------------------------------------------------------

def test_read_SimCenter_DL_input_minimum_input():
    """
    Test if the minimum input is read without producing any errors and also 
    check if some warnings are shown that draw attention to the lack of
    potentially important information in the input file.
    """
    
    # load the reference results
    with open('resources/test_DL_reference_min.json') as f:
        ref_DL = json.load(f)
    
    # read the input file and check for at least one warning
    with pytest.warns(UserWarning) as e_info:
        test_DL = read_SimCenter_DL_input('resources/test_DL_input_min.json', 
                                        verbose=False)
        
    # check if the returned dictionary is appropriate
    assert ref_DL == test_DL


def test_read_SimCenter_DL_input_full_input():
    """
    Test if the full input (i.e. all possible fields populated and all supported 
    decision variables turned on) is read without producing any errors or 
    warnings.
    """

    # load the reference results
    with open('resources/test_DL_reference_full.json') as f:
        ref_DL = json.load(f)

    # read the input file
    test_DL = read_SimCenter_DL_input('resources/test_DL_input_full.json',
                                      verbose=False)

    # check if the returned dictionary is appropriate
    assert ref_DL == test_DL
    
def test_read_SimCenter_DL_input_non_standard_units():
    """
    Test if the inputs are properly converted when non-standard units are used.
    """

    # load the reference results
    with open('resources/test_DL_reference_ns_units.json') as f:
        ref_DL = json.load(f)

    # read the input file and check for at least one warning
    with pytest.warns(UserWarning) as e_info:
        test_DL = read_SimCenter_DL_input(
            'resources/test_DL_input_ns_units.json', verbose=False)

    # check if the returned dictionary is appropriate
    assert ref_DL == test_DL
    
def test_read_SimCenter_DL_input_unknown_unit():
    """
    Test if a warning is shown if the input file contains an unknown unit type.
    """
    
    with pytest.warns(UserWarning) as e_info:
        test_DL = read_SimCenter_DL_input(
            'resources/test_DL_input_unknown_unit.json', verbose=False)
        
def test_read_SimCenter_DL_input_injuries_only():
    """
    Test if the inputs are read properly if the user is only interested in 
    calculating injuries.
    """

    # load the reference results
    with open('resources/test_DL_reference_injuries_only.json') as f:
        ref_DL = json.load(f)

    # read the input file and check for at least one warning because the plan
    # area is not specified in the file 
    with pytest.warns(UserWarning) as e_info:
        test_DL = read_SimCenter_DL_input(
            'resources/test_DL_input_injuries_only.json', verbose=False)

    # check if the returned dictionary is appropriate
    assert ref_DL == test_DL
    
    # now test if warnings are shown if the plan area is in the file, but 
    # other pieces of data are missing
    
    # load the reference results
    with open('resources/test_DL_reference_injuries_missing_data.json') as f:
        ref_DL = json.load(f)
    
    with pytest.warns(UserWarning) as e_info:
        test_DL = read_SimCenter_DL_input(
            'resources/test_DL_input_injuries_missing_data.json', 
            verbose=False)

    # check if the returned dictionary is appropriate
    assert ref_DL == test_DL


def test_read_SimCenter_DL_input_unknown_component_unit():
    """
    Test if an error is shown if the input file contains an unknown unit type
    for one of the components.
    """

    with pytest.raises(ValueError) as e_info:
        test_DL = read_SimCenter_DL_input(
            'resources/test_DL_input_unknown_comp_unit.json',
            verbose=False)
        
def test_read_SimCenter_DL_input_no_realizations():
    """
    Test if an error is shown if the input file contains no information about 
    the number of realizations to run.
    """

    with pytest.raises(ValueError) as e_info:
        test_DL = read_SimCenter_DL_input(
            'resources/test_DL_input_no_realizations.json', verbose=False)