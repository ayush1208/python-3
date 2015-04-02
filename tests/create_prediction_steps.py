# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2015 BigML
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

import json
import time
from datetime import datetime, timedelta
from world import world
from bigml.api import HTTP_CREATED
from bigml.api import FINISHED, FAULTY
from bigml.api import get_status


def i_create_a_prediction(step, data=None):
    if data is None:
        data = "{}"
    model = world.model['resource']
    data = json.loads(data)
    resource = world.api.create_prediction(model, data)
    world.status = resource['code']
    assert world.status == HTTP_CREATED, "Wrong status: %s" % world.status
    world.location = resource['location']
    world.prediction = resource['object']
    world.predictions.append(resource['resource'])


def i_create_a_centroid(step, data=None):
    if data is None:
        data = "{}"
    cluster = world.cluster['resource']
    data = json.loads(data)
    resource = world.api.create_centroid(cluster, data)
    world.status = resource['code']
    assert world.status == HTTP_CREATED
    world.location = resource['location']
    world.centroid = resource['object']
    world.centroids.append(resource['resource'])


def i_create_a_proportional_prediction(step, data=None):
    if data is None:
        data = "{}"
    model = world.model['resource']
    data = json.loads(data)
    resource = world.api.create_prediction(model, data,
                                           args={'missing_strategy': 1})
    world.status = resource['code']
    assert world.status == HTTP_CREATED
    world.location = resource['location']
    world.prediction = resource['object']
    world.predictions.append(resource['resource'])


def the_prediction_is(step, objective, prediction):
    if str(world.prediction['prediction'][objective]) == prediction:
        assert True
    else:
        assert False, "Found: %s, expected %s" % (
            str(world.prediction['prediction'][objective]), prediction)


def the_median_prediction_is(step, objective, prediction):
    median = str(world.prediction['prediction_path']
                 ['objective_summary']['median'])
    if median == prediction:
        assert True
    else:
        assert False, "Found: %s, expected %s" % (
            median, prediction)


def the_centroid_is_with_distance(step, centroid, distance):
    if str(world.centroid['centroid_name']) == centroid:
        assert True
    else:
        assert False, "Found: %s, expected: %s" % (str(world.centroid['centroid_name']), centroid)
    if str(world.centroid['distance']) == distance:
        assert True
    else:
        assert False, "Found: %s, expected: %s" % (str(world.centroid['distance']), distance)


def the_centroid_is(step, centroid):
    if str(world.centroid['centroid_name']) == centroid:
        assert True
    else:
        assert False, "Found: %s, expected: %s" % (str(world.centroid['centroid_name']), centroid)


def the_centroid_is_ok(step):
    assert world.api.ok(world.centroid)


def the_confidence_is(step, confidence):
    local_confidence = round(float(world.prediction['confidence']), 4)
    confidence = round(float(confidence), 4)
    assert local_confidence == confidence


def i_create_an_ensemble_prediction(step, data=None):
    if data is None:
        data = "{}"
    ensemble = world.ensemble['resource']
    data = json.loads(data)
    resource = world.api.create_prediction(ensemble, data)
    world.status = resource['code']
    assert world.status == HTTP_CREATED
    world.location = resource['location']
    world.prediction = resource['object']
    world.predictions.append(resource['resource'])


def wait_until_prediction_status_code_is(step, code1, code2, secs):
    start = datetime.utcnow()
    step.given('I get the prediction "{id}"'.format(id=world.prediction['resource']))
    status = get_status(world.prediction)
    while (status['code'] != int(code1) and
           status['code'] != int(code2)):
        time.sleep(3)
        assert datetime.utcnow() - start < timedelta(seconds=int(secs))
        step.given('I get the prediction "{id}"'.format(id=world.prediction['resource']))
        status = get_status(world.prediction)
    assert status['code'] == int(code1)


def the_prediction_is_finished_in_less_than(step, secs):
    wait_until_prediction_status_code_is(step, FINISHED, FAULTY, secs)


def create_local_ensemble_prediction(step, input_data):
    world.local_prediction = world.local_ensemble.predict(
        json.loads(input_data), add_confidence=True)


def create_local_ensemble_prediction(step, input_data):
    world.local_prediction = world.local_ensemble.predict(json.loads(input_data))
    

def create_local_ensemble_prediction(step, input_data):
    world.local_prediction = world.local_ensemble.predict(
        json.loads(input_data), with_confidence=True)


def i_create_an_anomaly_score(step, data=None):
    if data is None:
        data = "{}"
    anomaly = world.anomaly['resource']
    data = json.loads(data)
    resource = world.api.create_anomaly_score(anomaly, data)
    world.status = resource['code']
    assert world.status == HTTP_CREATED
    world.location = resource['location']
    world.anomaly_score = resource['object']
    world.anomaly_scores.append(resource['resource'])


def the_anomaly_score_is(step, score):
    if str(world.anomaly_score['score']) == score:
        assert True
    else:
        assert False, "Found: %s, expected %s" % (
            str(world.anomaly_score['score']), score)