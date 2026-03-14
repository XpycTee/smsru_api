import os
import sys
import time
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

# Add the root directory of the project to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smsru_api import AsyncClient, Client
from smsru_api.template import OutOfPhoneNumbers, OutOfTimestamp


class BaseClientPayloadTests(unittest.TestCase):
    def setUp(self):
        self.api_id = 'TEST_API_ID'
        self.client = Client(self.api_id)

    def test_collect_data_rejects_timestamp_too_far_in_future(self):
        timestamp = int(time.time()) + 5184001

        with self.assertRaises(OutOfTimestamp):
            self.client._collect_data(('79999999999',), message='Test message', timestamp=timestamp)

    def test_collect_data_accepts_valid_future_timestamp(self):
        timestamp = int(time.time()) + 3600

        data = self.client._collect_data(('79999999999',), message='Test message', timestamp=timestamp)

        self.assertEqual(data['time'], timestamp)

    def test_collect_data_normalizes_multi_numbers(self):
        data = self.client._collect_data(
            (),
            multi={
                '+7 (999) 000-00-00': 'First',
                '8 (999) 000-00-01': 'Second',
            },
            debug=True,
        )

        self.assertEqual(
            data,
            {
                'to[9990000000]': 'First',
                'to[9990000001]': 'Second',
                'test': 1,
            },
        )

    def test_collect_data_rejects_more_than_hundred_numbers(self):
        numbers = tuple(f'79990000{i:03d}' for i in range(101))

        with self.assertRaises(OutOfPhoneNumbers):
            self.client._collect_data(numbers, message='Test message')

    def test_collect_data_rejects_ttl_out_of_range(self):
        with self.assertRaises(OutOfTimestamp):
            self.client._collect_data(('79999999999',), message='Test message', ttl=0)

        with self.assertRaises(OutOfTimestamp):
            self.client._collect_data(('79999999999',), message='Test message', ttl=1441)

    def test_sync_and_async_clients_build_same_payload(self):
        sync_client = Client(self.api_id)
        async_client = AsyncClient(self.api_id)
        kwargs = {
            'message': 'Test message',
            'from_name': 'Sender',
            'ip_address': '127.0.0.1',
            'timestamp': int(time.time()) + 300,
            'ttl': 15,
            'day_time': True,
            'translit': True,
            'debug': True,
            'partner_id': 12345,
        }

        sync_data = sync_client._collect_data(('8 (999) 000-00-00',), **kwargs)
        async_data = async_client._collect_data(('8 (999) 000-00-00',), **kwargs)

        self.assertEqual(sync_data, async_data)


class TestSmsRu(unittest.TestCase):
    def setUp(self):
        self.api_id = 'TEST_API_ID'
        self.smsru = Client(self.api_id)

    @patch('smsru_api.client.httpx.Client.post')
    def test_send_posts_expected_payload(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'OK'}
        mock_post.return_value = mock_response

        response = self.smsru.send('8 (999) 999-99-99', message='Test message', debug=True)

        self.assertEqual(response['status'], 'OK')
        mock_post.assert_called_once_with(
            'https://sms.ru/sms/send',
            data={
                'api_id': self.api_id,
                'json': 1,
                'partner_id': 358434,
                'to': '9999999999',
                'text': 'Test message',
                'test': 1,
            },
        )
        mock_response.raise_for_status.assert_called_once_with()

    @patch('smsru_api.client.httpx.Client.post')
    def test_send_multi_posts_normalized_payload(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'OK'}
        mock_post.return_value = mock_response

        response = self.smsru.send(
            multi={
                '+7 (999) 999-99-99': 'First',
                '8 (999) 999-99-98': 'Second',
            },
            debug=True,
        )

        self.assertEqual(response['status'], 'OK')
        mock_post.assert_called_once_with(
            'https://sms.ru/sms/send',
            data={
                'api_id': self.api_id,
                'json': 1,
                'partner_id': 358434,
                'to[9999999999]': 'First',
                'to[9999999998]': 'Second',
                'test': 1,
            },
        )
        mock_response.raise_for_status.assert_called_once_with()

    @patch('smsru_api.client.httpx.Client.post')
    def test_balance_posts_default_payload(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'OK'}
        mock_post.return_value = mock_response

        response = self.smsru.balance()

        self.assertEqual(response['status'], 'OK')
        mock_post.assert_called_once_with(
            'https://sms.ru/my/balance',
            data={
                'api_id': self.api_id,
                'json': 1,
                'partner_id': 358434,
            },
        )
        mock_response.raise_for_status.assert_called_once_with()


class TestAsyncSmsRu(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.api_id = 'TEST_API_ID'
        self.smsru = AsyncClient(self.api_id)

    @patch('smsru_api.aioclient.httpx.AsyncClient.post')
    async def test_send_posts_expected_payload(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'OK'}
        mock_post.return_value = mock_response

        response = await self.smsru.send('8 (999) 999-99-99', message='Test message', debug=True)

        self.assertEqual(response['status'], 'OK')
        mock_post.assert_awaited_once_with(
            'https://sms.ru/sms/send',
            data={
                'api_id': self.api_id,
                'json': 1,
                'partner_id': 358434,
                'to': '9999999999',
                'text': 'Test message',
                'test': 1,
            },
        )
        mock_response.raise_for_status.assert_called_once_with()

    @patch('smsru_api.aioclient.httpx.AsyncClient.post')
    async def test_send_multi_posts_normalized_payload(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'OK'}
        mock_post.return_value = mock_response

        response = await self.smsru.send(
            multi={
                '+7 (999) 999-99-99': 'First',
                '8 (999) 999-99-98': 'Second',
            },
            debug=True,
        )

        self.assertEqual(response['status'], 'OK')
        mock_post.assert_awaited_once_with(
            'https://sms.ru/sms/send',
            data={
                'api_id': self.api_id,
                'json': 1,
                'partner_id': 358434,
                'to[9999999999]': 'First',
                'to[9999999998]': 'Second',
                'test': 1,
            },
        )
        mock_response.raise_for_status.assert_called_once_with()

    @patch('smsru_api.aioclient.httpx.AsyncClient.post')
    async def test_balance_posts_default_payload(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'OK'}
        mock_post.return_value = mock_response

        response = await self.smsru.balance()

        self.assertEqual(response['status'], 'OK')
        mock_post.assert_awaited_once_with(
            'https://sms.ru/my/balance',
            data={
                'api_id': self.api_id,
                'json': 1,
                'partner_id': 358434,
            },
        )
        mock_response.raise_for_status.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
