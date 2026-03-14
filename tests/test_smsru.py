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

    @patch('smsru_api.client.httpx.Client')
    def test_context_manager_reuses_single_httpx_client(self, mock_client_cls):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'OK'}
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        with self.smsru as smsru:
            first = smsru.balance()
            second = smsru.limit()

        self.assertEqual(first['status'], 'OK')
        self.assertEqual(second['status'], 'OK')
        mock_client_cls.assert_called_once_with()
        self.assertEqual(mock_client.post.call_count, 2)
        mock_client.close.assert_called_once_with()

    @patch('smsru_api.client.httpx.Client')
    def test_regular_calls_remain_one_shot_after_context_exit(self, mock_client_cls):
        managed_client = MagicMock()
        managed_response = MagicMock()
        managed_response.json.return_value = {'status': 'OK'}
        managed_client.post.return_value = managed_response

        temporary_context_client = MagicMock()
        temporary_response = MagicMock()
        temporary_response.json.return_value = {'status': 'OK'}
        temporary_context_client.__enter__.return_value = temporary_context_client
        temporary_context_client.post.return_value = temporary_response

        mock_client_cls.side_effect = [managed_client, temporary_context_client]

        with self.smsru as smsru:
            smsru.balance()

        response = self.smsru.balance()

        self.assertEqual(response['status'], 'OK')
        managed_client.close.assert_called_once_with()
        temporary_context_client.post.assert_called_once()
        temporary_context_client.__exit__.assert_called_once()

    def test_close_is_idempotent(self):
        self.smsru.close()
        self.smsru.close()

    @patch('smsru_api.client.httpx.Client')
    def test_alias_supports_context_manager(self, mock_client_cls):
        from smsru_api import SmsRu

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'OK'}
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        with SmsRu(self.api_id) as smsru:
            response = smsru.balance()

        self.assertEqual(response['status'], 'OK')
        mock_client.close.assert_called_once_with()


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

    @patch('smsru_api.aioclient.httpx.AsyncClient')
    async def test_async_context_manager_reuses_single_httpx_client(self, mock_client_cls):
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'OK'}
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        async with self.smsru as smsru:
            first = await smsru.balance()
            second = await smsru.limit()

        self.assertEqual(first['status'], 'OK')
        self.assertEqual(second['status'], 'OK')
        mock_client_cls.assert_called_once_with()
        self.assertEqual(mock_client.post.await_count, 2)
        mock_client.aclose.assert_awaited_once_with()

    @patch('smsru_api.aioclient.httpx.AsyncClient')
    async def test_regular_async_calls_remain_one_shot_after_context_exit(self, mock_client_cls):
        managed_client = AsyncMock()
        managed_response = MagicMock()
        managed_response.json.return_value = {'status': 'OK'}
        managed_client.post.return_value = managed_response

        temporary_context_client = AsyncMock()
        temporary_response = MagicMock()
        temporary_response.json.return_value = {'status': 'OK'}
        temporary_context_client.__aenter__.return_value = temporary_context_client
        temporary_context_client.post.return_value = temporary_response

        mock_client_cls.side_effect = [managed_client, temporary_context_client]

        async with self.smsru as smsru:
            await smsru.balance()

        response = await self.smsru.balance()

        self.assertEqual(response['status'], 'OK')
        managed_client.aclose.assert_awaited_once_with()
        temporary_context_client.post.assert_awaited_once()
        temporary_context_client.__aexit__.assert_awaited_once()

    async def test_aclose_is_idempotent(self):
        await self.smsru.aclose()
        await self.smsru.aclose()

    @patch('smsru_api.aioclient.httpx.AsyncClient')
    async def test_async_alias_supports_context_manager(self, mock_client_cls):
        from smsru_api import AsyncSmsRu

        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'OK'}
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        async with AsyncSmsRu(self.api_id) as smsru:
            response = await smsru.balance()

        self.assertEqual(response['status'], 'OK')
        mock_client.aclose.assert_awaited_once_with()


if __name__ == '__main__':
    unittest.main()
