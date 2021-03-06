# -*- coding: utf-8 -*-
#
# Copyright 2015-2022 BigML
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import time
import json
import os
from datetime import datetime
from .world import world
from nose.tools import eq_, assert_less

from bigml.api import HTTP_CREATED
from bigml.api import HTTP_ACCEPTED
from bigml.api import FINISHED
from bigml.api import FAULTY
from bigml.api import get_status

from .read_resource_steps import wait_until_status_code_is


#@step(r'the correlation name is "(.*)"')
def i_check_correlation_name(step, name):
    correlation_name = world.correlation['name']
    eq_(name, correlation_name)

#@step(r'I create a correlation from a dataset$')
def i_create_a_correlation_from_dataset(step):
    dataset = world.dataset.get('resource')
    resource = world.api.create_correlation(dataset, {'name': 'new correlation'})
    world.status = resource['code']
    eq_(world.status, HTTP_CREATED)
    world.location = resource['location']
    world.correlation = resource['object']
    world.correlations.append(resource['resource'])


#@step(r'I update the correlation name to "(.*)"$')
def i_update_correlation_name(step, name):
    resource = world.api.update_correlation(world.correlation['resource'],
                                            {'name': name})
    world.status = resource['code']
    eq_(world.status, HTTP_ACCEPTED)
    world.location = resource['location']
    world.correlation = resource['object']


#@step(r'I wait until the correlation status code is either (\d) or (-\d) less than (\d+)')
def wait_until_correlation_status_code_is(step, code1, code2, secs):
    world.correlation = wait_until_status_code_is(
        code1, code2, secs, world.correlation)


#@step(r'I wait until the correlation is ready less than (\d+)')
def the_correlation_is_finished_in_less_than(step, secs):
    wait_until_correlation_status_code_is(step, FINISHED, FAULTY, secs)
