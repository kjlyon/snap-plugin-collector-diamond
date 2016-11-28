# -*- coding: utf-8 -*-
# http://www.apache.org/licenses/LICENSE-2.0.txt
#
# Copyright 2016 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import snap_plugin.v1 as snap
import sys
import os
import time
from snap_diamond import DiamondCollector


def test_get_config_policy():
    dia = DiamondCollector("diamond", 1)
    policy = dia.get_config_policy()
    assert isinstance(policy, snap.ConfigPolicy)
    assert len(policy) == 1
    assert len(policy["diamond"].rules) == 2
    assert policy["diamond"].rules["config"].required is True
    assert policy["diamond"].rules["collectors_path"].required is True


def test_update_catalog():
    dia = DiamondCollector("diamond", 1)
    # When the diamond pypi package is installed the collectors are placed
    # in the share dir.
    cfg = snap.ConfigMap(config='''{"collectors":{"CPUCollector": {}}}''',
                         collectors_path=os.path.dirname(
                             os.path.dirname(
                                 sys.executable))+"/share/diamond/collectors")
    metrics = dia.update_catalog(cfg)
    assert len(metrics) > 5


def test_collect():
    dia = DiamondCollector("diamond", 1)
    cfg = snap.ConfigMap(config='''{"collectors":{"CPUCollector": {}}}''',
                         collectors_path=os.path.dirname(
                             os.path.dirname(
                                 sys.executable))+"/share/diamond/collectors")
    metrics_to_collect = dia.update_catalog(cfg)
    metrics_collected = dia.collect(metrics_to_collect)
    assert len(metrics_collected) == len(metrics_to_collect)
    assert metrics_collected[0].data is not None
    # time collected is less than now
    assert metrics_collected[0].timestamp < time.time()
    # it took less than a second to collect the metrics
    assert metrics_collected[0].timestamp > time.time()-1


