import os
import random

import pytest

from smsru_api.smsru import SmsRu


@pytest.fixture(scope='module')
def init_smsru():
    return SmsRu(os.environ['API_KEY'])


@pytest.fixture
def get_number(init_smsru):
    rnd_num = random.randint(9990000000, 9999999999)
    result = init_smsru.send(str(rnd_num), message='Test message', debug=True)
    return result['sms'][str(rnd_num)]['sms_id']


@pytest.mark.parametrize(
    'number,expected', [
        ([str(random.randint(9990000000, 9999999999))], 'OK'),
        ([str(random.randint(9990000000, 9999999999)) for _ in range(1, 5)], 'OK'),
        ('322', 'ERROR')
    ]
)
def test_send(number, expected, init_smsru):
    result = init_smsru.send(*number, message='Test message', debug=True)
    assert type(result) == dict
    assert result['status'] == "OK", result["status_text"]
    for num in result['sms']:
        assert result['sms'][num]['status'] == expected, result['sms'][num]["status_text"] if result['sms'][num]['status'] == 'ERROR' else None


def test_status(init_smsru, get_number):
    result = init_smsru.status(get_number)
    assert type(result) == dict
    assert result['status'] == "OK", result["status_text"] if result['status'] == 'ERROR' else None


@pytest.mark.parametrize(
    'number,expected', [
        ([str(random.randint(9990000000, 9999999999))], 'OK'),
        ([str(random.randint(9990000000, 9999999999)) for _ in range(1, 5)], 'OK'),
        ('322', 'ERROR')
    ]
)
def test_cost(number, expected, init_smsru):
    result = init_smsru.cost(*number, message='Test message')
    assert type(result) == dict
    assert result['status'] == "OK", result["status_text"]
    for num in result['sms']:
        assert result['sms'][num]['status'] == expected, result['sms'][num]["status_text"] if result['sms'][num]['status'] == 'ERROR' else None


def test_balance(init_smsru):
    result = init_smsru.balance()
    assert type(result) == dict
    assert result['status'] == "OK", result["status_text"] if result['status'] == 'ERROR' else None


def test_limit(init_smsru):
    result = init_smsru.limit()
    assert type(result) == dict
    assert result['status'] == "OK", result["status_text"] if result['status'] == 'ERROR' else None


def test_free_limit(init_smsru):
    result = init_smsru.free()
    assert result['status'] == "OK", result["status_text"] if result['status'] == 'ERROR' else None


def test_senders(init_smsru):
    result = init_smsru.senders()
    assert type(result) == dict
    assert result['status'] == "OK", result["status_text"] if result['status'] == 'ERROR' else None


def test_stop_list_before_adding(init_smsru):
    result = init_smsru.stop_list()
    assert type(result) == dict
    assert result['status'] == "OK", result["status_text"] if result['status'] == 'ERROR' else None


@pytest.mark.parametrize(
    'number,expected', [
        ('9000000000', 'OK'),
        ('9000000001', 'OK'),
        ('322', 'ERROR')
    ]
)
def test_add_stop_list(number, expected, init_smsru):
    result = init_smsru.add_stop_list(number, 'Test')
    assert type(result) == dict
    assert result['status'] == expected, result["status_text"] if result['status'] == 'ERROR' else None


def test_stop_list_after_adding(init_smsru):
    result = init_smsru.stop_list()
    assert type(result) == dict
    assert result['status'] == "OK", result["status_text"] if result['status'] == 'ERROR' else None


@pytest.mark.parametrize(
    'number,expected', [
        ('9000000000', 'OK'),
        ('9000000001', 'OK'),
        ('322', 'ERROR'),
        ('9000000002', 'OK')
    ]
)
def test_del_stop_list(number, expected, init_smsru):
    result = init_smsru.del_stop_list(number)
    assert type(result) == dict
    assert result['status'] == expected, result["status_text"] if result['status'] == 'ERROR' else None


def test_stop_list_after_deleting(init_smsru):
    result = init_smsru.stop_list()
    assert type(result) == dict
    assert result['status'] == "OK", result["status_text"] if result['status'] == 'ERROR' else None


def test_callbacks_before_adding(init_smsru):
    result = init_smsru.callbacks()
    assert type(result) == dict
    assert result['status'] == "OK", result["status_text"] if result['status'] == 'ERROR' else None


@pytest.mark.parametrize(
    'callback,expected', [
        ('http://test.net', 'OK'),
        ('https://test.get', 'OK'),
        ('test.bad', 'ERROR'),
        ('ftp://test.bad', 'ERROR')
    ]
)
def test_add_callback(callback, expected, init_smsru):
    result = init_smsru.add_callback(callback)
    assert type(result) == dict
    assert result['status'] == expected, result["status_text"] if result['status'] == 'ERROR' else None


def test_callbacks_after_adding(init_smsru):
    result = init_smsru.callbacks()
    assert type(result) == dict
    assert result['status'] == "OK", result["status_text"] if result['status'] == 'ERROR' else None


@pytest.mark.parametrize(
    'callback,expected', [
        ('http://test.net', 'OK'),
        ('https://test.get', 'OK'),
        ('test.bad', 'ERROR'),
        ('rtp://test.bad', 'ERROR'),
        ('http://localhost', 'ERROR')
    ]
)
def test_del_callback(callback, expected, init_smsru):
    result = init_smsru.del_callback(callback)
    assert type(result) == dict
    assert result['status'] == expected, result["status_text"] if result['status'] == 'ERROR' else None


def test_callbacks_after_deleting(init_smsru):
    result = init_smsru.callbacks()
    assert type(result) == dict
    assert result['status'] == "OK", result["status_text"] if result['status'] == 'ERROR' else None
