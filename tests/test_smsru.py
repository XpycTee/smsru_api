import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import httpx

from smsru_api import AsyncClient, Client
from smsru_api.template import OutOfPhoneNumbers, OutOfTimestamp


class BaseClientPayloadTests(unittest.TestCase):
    def setUp(self):
        self.api_id = 'TEST_API_ID'
        self.client = Client(self.api_id)

    def test_collect_data_rejects_timestamp_too_far_in_future(self):
        with patch('smsru_api.template.time.time', return_value=1_000):
            with self.assertRaises(OutOfTimestamp):
                self.client._collect_data(('79999999999',), message='Test message', timestamp=5_184_001 + 1_000)

    def test_collect_data_accepts_timestamp_on_upper_boundary(self):
        timestamp = 5_184_000 + 1_000

        with patch('smsru_api.template.time.time', return_value=1_000):
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

    def test_collect_data_multi_ignores_numbers_and_message(self):
        data = self.client._collect_data(
            ('79999999999',),
            message='Ignored',
            multi={'8 (999) 000-00-01': 'Actual message'},
        )

        self.assertEqual(data, {'to[9990000001]': 'Actual message'})

    def test_collect_data_rejects_more_than_hundred_numbers(self):
        numbers = tuple(f'79990000{i:03d}' for i in range(101))

        with self.assertRaises(OutOfPhoneNumbers):
            self.client._collect_data(numbers, message='Test message')

    def test_collect_data_rejects_more_than_hundred_multi_numbers(self):
        multi = {f'79990000{i:03d}': f'message-{i}' for i in range(101)}

        with self.assertRaises(OutOfPhoneNumbers):
            self.client._collect_data((), multi=multi)

    def test_collect_data_rejects_ttl_out_of_range(self):
        with self.assertRaises(OutOfTimestamp):
            self.client._collect_data(('79999999999',), message='Test message', ttl=0)

        with self.assertRaises(OutOfTimestamp):
            self.client._collect_data(('79999999999',), message='Test message', ttl=1441)

    def test_collect_data_accepts_ttl_boundaries(self):
        min_data = self.client._collect_data(('79999999999',), message='Test message', ttl=1)
        max_data = self.client._collect_data(('79999999999',), message='Test message', ttl=1440)

        self.assertEqual(min_data['ttl'], 1)
        self.assertEqual(max_data['ttl'], 1440)

    def test_collect_data_requires_message_without_multi(self):
        with self.assertRaisesRegex(ValueError, 'Не указан текст сообщения'):
            self.client._collect_data(('79999999999',))

    def test_collect_data_requires_number_without_multi(self):
        with self.assertRaisesRegex(ValueError, 'Не указан номер'):
            self.client._collect_data((), message='Test message')

    def test_collect_data_accepts_valid_ip_address(self):
        data = self.client._collect_data(('79999999999',), message='Test message', ip_address='127.0.0.1')

        self.assertEqual(data['ip'], '127.0.0.1')

    def test_collect_data_rejects_invalid_ip_address(self):
        with self.assertRaises(ValueError):
            self.client._collect_data(('79999999999',), message='Test message', ip_address='not-an-ip')

    def test_collect_data_serializes_optional_fields(self):
        with patch('smsru_api.template.time.time', return_value=1_000):
            data = self.client._collect_data(
                ('8 (999) 000-00-00',),
                message='Test message',
                from_name='Sender',
                ip_address='2001:db8::1',
                timestamp=1_600,
                ttl=15,
                day_time=True,
                translit=True,
                debug=True,
                partner_id=12345,
            )

        self.assertEqual(
            data,
            {
                'to': '9990000000',
                'text': 'Test message',
                'test': 1,
                'from': 'Sender',
                'time': 1_600,
                'ttl': 15,
                'daytime': 1,
                'ip': '2001:db8::1',
                'translit': 1,
                'partner_id': 12345,
            },
        )

    def test_collect_data_debug_does_not_override_explicit_test_false(self):
        data = self.client._collect_data(('79999999999',), message='Test message', debug=True, test=False)

        self.assertNotIn('test', data)

    def test_collect_data_explicit_test_true_sets_test_flag(self):
        data = self.client._collect_data(('79999999999',), message='Test message', test=True)

        self.assertEqual(data['test'], 1)

    def test_normalize_phone_removes_country_code_and_formatting(self):
        self.assertEqual(self.client._normalize_phone('+7 (999) 123-45-67'), '9991234567')
        self.assertEqual(self.client._normalize_phone('8 (999) 123-45-67'), '9991234567')

    def test_normalize_and_validate_phone_accepts_valid_number(self):
        self.assertEqual(self.client._normalize_and_validate_phone('+7 (999) 123-45-67'), '9991234567')

    def test_normalize_and_validate_phone_rejects_invalid_number(self):
        with self.assertRaisesRegex(ValueError, 'Неверно указан номер телефона'):
            self.client._normalize_and_validate_phone('abc')

        with self.assertRaisesRegex(ValueError, 'Неверно указан номер телефона'):
            self.client._normalize_and_validate_phone('8 999')

    def test_collect_data_rejects_invalid_number(self):
        with self.assertRaisesRegex(ValueError, 'Неверно указан номер телефона'):
            self.client._collect_data(('abc',), message='Test message')

    def test_collect_data_rejects_invalid_multi_number(self):
        with self.assertRaisesRegex(ValueError, 'Неверно указан номер телефона'):
            self.client._collect_data((), multi={'abc': 'Test message'})

    def test_sync_and_async_clients_build_same_payload(self):
        sync_client = Client(self.api_id)
        async_client = AsyncClient(self.api_id)
        kwargs = {
            'message': 'Test message',
            'from_name': 'Sender',
            'ip_address': '127.0.0.1',
            'timestamp': 1_300,
            'ttl': 15,
            'day_time': True,
            'translit': True,
            'debug': True,
            'partner_id': 12345,
        }

        with patch('smsru_api.template.time.time', return_value=1_000):
            sync_data = sync_client._collect_data(('8 (999) 000-00-00',), **kwargs)
            async_data = async_client._collect_data(('8 (999) 000-00-00',), **kwargs)

        self.assertEqual(sync_data, async_data)


class TestSmsRu(unittest.TestCase):
    def setUp(self):
        self.api_id = 'TEST_API_ID'
        self.smsru = Client(self.api_id)

    def expected_defaults(self):
        return {
            'api_id': self.api_id,
            'json': 1,
            'partner_id': self.smsru.defaults['partner_id'],
        }

    def assert_request_method(self, method_name, expected_path, expected_data, *args, **kwargs):
        with patch('smsru_api.client.httpx.Client.post') as mock_post:
            mock_response = MagicMock()
            mock_response.json.return_value = {'status': 'OK'}
            mock_post.return_value = mock_response

            response = getattr(self.smsru, method_name)(*args, **kwargs)

        self.assertEqual(response, {'status': 'OK'})
        mock_post.assert_called_once_with(f'https://sms.ru{expected_path}', data=expected_data)
        mock_response.raise_for_status.assert_called_once_with()

    def test_send_posts_expected_payload(self):
        self.assert_request_method(
            'send',
            '/sms/send',
            {
                **self.expected_defaults(),
                'to': '9999999999',
                'text': 'Test message',
                'test': 1,
            },
            '8 (999) 999-99-99',
            message='Test message',
            debug=True,
        )

    def test_send_multi_posts_normalized_payload(self):
        self.assert_request_method(
            'send',
            '/sms/send',
            {
                **self.expected_defaults(),
                'to[9999999999]': 'First',
                'to[9999999998]': 'Second',
                'test': 1,
            },
            multi={
                '+7 (999) 999-99-99': 'First',
                '8 (999) 999-99-98': 'Second',
            },
            debug=True,
        )

    def test_send_rejects_invalid_number_before_request(self):
        with patch('smsru_api.client.httpx.Client.post') as mock_post:
            with self.assertRaisesRegex(ValueError, 'Неверно указан номер телефона'):
                self.smsru.send('abc', message='Test message')

        mock_post.assert_not_called()

    def test_cost_rejects_invalid_number_before_request(self):
        with patch('smsru_api.client.httpx.Client.post') as mock_post:
            with self.assertRaisesRegex(ValueError, 'Неверно указан номер телефона'):
                self.smsru.cost('abc', message='Test message')

        mock_post.assert_not_called()

    def test_balance_posts_default_payload(self):
        self.assert_request_method('balance', '/my/balance', self.expected_defaults())

    def test_callcheck_add_posts_expected_payload(self):
        self.assert_request_method(
            'callcheck_add',
            '/callcheck/add',
            {**self.expected_defaults(), 'phone': '79999999999'},
            '79999999999',
        )

    def test_callcheck_status_posts_expected_payload(self):
        self.assert_request_method(
            'callcheck_status',
            '/callcheck/status',
            {**self.expected_defaults(), 'check_id': 'check-id'},
            'check-id',
        )

    def test_status_posts_expected_payload(self):
        self.assert_request_method(
            'status',
            '/sms/status',
            {**self.expected_defaults(), 'sms_id': 'sms-id'},
            'sms-id',
        )

    def test_cost_posts_expected_payload(self):
        self.assert_request_method(
            'cost',
            '/sms/cost',
            {
                **self.expected_defaults(),
                'to': '9999999999,9999999998',
                'text': 'Test message',
            },
            '8 (999) 999-99-99',
            '+7 (999) 999-99-98',
            message='Test message',
        )

    def test_limit_posts_default_payload(self):
        self.assert_request_method('limit', '/my/limit', self.expected_defaults())

    def test_free_posts_default_payload(self):
        self.assert_request_method('free', '/my/free', self.expected_defaults())

    def test_senders_posts_default_payload(self):
        self.assert_request_method('senders', '/my/senders', self.expected_defaults())

    def test_stop_list_posts_default_payload(self):
        self.assert_request_method('stop_list', '/stoplist/get', self.expected_defaults())

    def test_add_stop_list_posts_normalized_payload(self):
        self.assert_request_method(
            'add_stop_list',
            '/stoplist/add',
            {
                **self.expected_defaults(),
                'stoplist_phone': '9999999999',
                'stoplist_text': 'Test comment',
            },
            '8 (999) 999-99-99',
            comment='Test comment',
        )

    def test_add_stop_list_uses_empty_comment_by_default(self):
        self.assert_request_method(
            'add_stop_list',
            '/stoplist/add',
            {
                **self.expected_defaults(),
                'stoplist_phone': '9999999999',
                'stoplist_text': '',
            },
            '8 (999) 999-99-99',
        )

    def test_add_stop_list_rejects_invalid_number_before_request(self):
        with patch('smsru_api.client.httpx.Client.post') as mock_post:
            with self.assertRaisesRegex(ValueError, 'Неверно указан номер телефона'):
                self.smsru.add_stop_list('abc')

        mock_post.assert_not_called()

    def test_del_stop_list_posts_normalized_payload(self):
        self.assert_request_method(
            'del_stop_list',
            '/stoplist/del',
            {
                **self.expected_defaults(),
                'stoplist_phone': '9999999999',
            },
            '8 (999) 999-99-99',
        )

    def test_del_stop_list_rejects_invalid_number_before_request(self):
        with patch('smsru_api.client.httpx.Client.post') as mock_post:
            with self.assertRaisesRegex(ValueError, 'Неверно указан номер телефона'):
                self.smsru.del_stop_list('abc')

        mock_post.assert_not_called()

    def test_callbacks_posts_default_payload(self):
        self.assert_request_method('callbacks', '/callback/get', self.expected_defaults())

    def test_add_callback_posts_expected_payload(self):
        self.assert_request_method(
            'add_callback',
            '/callback/add',
            {
                **self.expected_defaults(),
                'url': 'https://example.com/callback',
            },
            'https://example.com/callback',
        )

    def test_del_callback_posts_expected_payload(self):
        self.assert_request_method(
            'del_callback',
            '/callback/del',
            {
                **self.expected_defaults(),
                'url': 'https://example.com/callback',
            },
            'https://example.com/callback',
        )

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

    @patch('smsru_api.client.httpx.Client')
    def test_close_allows_reentering_context_with_new_transport(self, mock_client_cls):
        first_client = MagicMock()
        second_client = MagicMock()
        first_response = MagicMock()
        second_response = MagicMock()
        first_response.json.return_value = {'status': 'OK'}
        second_response.json.return_value = {'status': 'OK'}
        first_client.post.return_value = first_response
        second_client.post.return_value = second_response
        mock_client_cls.side_effect = [first_client, second_client]

        with self.smsru as smsru:
            smsru.balance()

        with self.smsru as smsru:
            smsru.balance()

        self.assertEqual(mock_client_cls.call_count, 2)
        first_client.close.assert_called_once_with()
        second_client.close.assert_called_once_with()

    @patch('smsru_api.client.httpx.Client.post')
    def test_request_propagates_raise_for_status_errors(self, mock_post):
        request = httpx.Request('POST', 'https://sms.ru/my/balance')
        response = httpx.Response(500, request=request)
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError('boom', request=request, response=response)
        mock_post.return_value = mock_response

        with self.assertRaises(httpx.HTTPStatusError):
            self.smsru.balance()

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

    def expected_defaults(self):
        return {
            'api_id': self.api_id,
            'json': 1,
            'partner_id': self.smsru.defaults['partner_id'],
        }

    async def assert_request_method(self, method_name, expected_path, expected_data, *args, **kwargs):
        with patch('smsru_api.aioclient.httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
            mock_response = MagicMock()
            mock_response.json.return_value = {'status': 'OK'}
            mock_post.return_value = mock_response

            response = await getattr(self.smsru, method_name)(*args, **kwargs)

        self.assertEqual(response, {'status': 'OK'})
        mock_post.assert_awaited_once_with(f'https://sms.ru{expected_path}', data=expected_data)
        mock_response.raise_for_status.assert_called_once_with()

    async def test_send_posts_expected_payload(self):
        await self.assert_request_method(
            'send',
            '/sms/send',
            {
                **self.expected_defaults(),
                'to': '9999999999',
                'text': 'Test message',
                'test': 1,
            },
            '8 (999) 999-99-99',
            message='Test message',
            debug=True,
        )

    async def test_send_multi_posts_normalized_payload(self):
        await self.assert_request_method(
            'send',
            '/sms/send',
            {
                **self.expected_defaults(),
                'to[9999999999]': 'First',
                'to[9999999998]': 'Second',
                'test': 1,
            },
            multi={
                '+7 (999) 999-99-99': 'First',
                '8 (999) 999-99-98': 'Second',
            },
            debug=True,
        )

    async def test_send_rejects_invalid_number_before_request(self):
        with patch('smsru_api.aioclient.httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
            with self.assertRaisesRegex(ValueError, 'Неверно указан номер телефона'):
                await self.smsru.send('abc', message='Test message')

        mock_post.assert_not_awaited()

    async def test_cost_rejects_invalid_number_before_request(self):
        with patch('smsru_api.aioclient.httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
            with self.assertRaisesRegex(ValueError, 'Неверно указан номер телефона'):
                await self.smsru.cost('abc', message='Test message')

        mock_post.assert_not_awaited()

    async def test_balance_posts_default_payload(self):
        await self.assert_request_method('balance', '/my/balance', self.expected_defaults())

    async def test_callcheck_add_posts_expected_payload(self):
        await self.assert_request_method(
            'callcheck_add',
            '/callcheck/add',
            {**self.expected_defaults(), 'phone': '79999999999'},
            '79999999999',
        )

    async def test_callcheck_status_posts_expected_payload(self):
        await self.assert_request_method(
            'callcheck_status',
            '/callcheck/status',
            {**self.expected_defaults(), 'check_id': 'check-id'},
            'check-id',
        )

    async def test_status_posts_expected_payload(self):
        await self.assert_request_method(
            'status',
            '/sms/status',
            {**self.expected_defaults(), 'sms_id': 'sms-id'},
            'sms-id',
        )

    async def test_cost_posts_expected_payload(self):
        await self.assert_request_method(
            'cost',
            '/sms/cost',
            {
                **self.expected_defaults(),
                'to': '9999999999,9999999998',
                'text': 'Test message',
            },
            '8 (999) 999-99-99',
            '+7 (999) 999-99-98',
            message='Test message',
        )

    async def test_limit_posts_default_payload(self):
        await self.assert_request_method('limit', '/my/limit', self.expected_defaults())

    async def test_free_posts_default_payload(self):
        await self.assert_request_method('free', '/my/free', self.expected_defaults())

    async def test_senders_posts_default_payload(self):
        await self.assert_request_method('senders', '/my/senders', self.expected_defaults())

    async def test_stop_list_posts_default_payload(self):
        await self.assert_request_method('stop_list', '/stoplist/get', self.expected_defaults())

    async def test_add_stop_list_posts_normalized_payload(self):
        await self.assert_request_method(
            'add_stop_list',
            '/stoplist/add',
            {
                **self.expected_defaults(),
                'stoplist_phone': '9999999999',
                'stoplist_text': 'Test comment',
            },
            '8 (999) 999-99-99',
            comment='Test comment',
        )

    async def test_add_stop_list_uses_empty_comment_by_default(self):
        await self.assert_request_method(
            'add_stop_list',
            '/stoplist/add',
            {
                **self.expected_defaults(),
                'stoplist_phone': '9999999999',
                'stoplist_text': '',
            },
            '8 (999) 999-99-99',
        )

    async def test_add_stop_list_rejects_invalid_number_before_request(self):
        with patch('smsru_api.aioclient.httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
            with self.assertRaisesRegex(ValueError, 'Неверно указан номер телефона'):
                await self.smsru.add_stop_list('abc')

        mock_post.assert_not_awaited()

    async def test_del_stop_list_posts_normalized_payload(self):
        await self.assert_request_method(
            'del_stop_list',
            '/stoplist/del',
            {
                **self.expected_defaults(),
                'stoplist_phone': '9999999999',
            },
            '8 (999) 999-99-99',
        )

    async def test_del_stop_list_rejects_invalid_number_before_request(self):
        with patch('smsru_api.aioclient.httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
            with self.assertRaisesRegex(ValueError, 'Неверно указан номер телефона'):
                await self.smsru.del_stop_list('abc')

        mock_post.assert_not_awaited()

    async def test_callbacks_posts_default_payload(self):
        await self.assert_request_method('callbacks', '/callback/get', self.expected_defaults())

    async def test_add_callback_posts_expected_payload(self):
        await self.assert_request_method(
            'add_callback',
            '/callback/add',
            {
                **self.expected_defaults(),
                'url': 'https://example.com/callback',
            },
            'https://example.com/callback',
        )

    async def test_del_callback_posts_expected_payload(self):
        await self.assert_request_method(
            'del_callback',
            '/callback/del',
            {
                **self.expected_defaults(),
                'url': 'https://example.com/callback',
            },
            'https://example.com/callback',
        )

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

    @patch('smsru_api.aioclient.httpx.AsyncClient')
    async def test_aclose_allows_reentering_context_with_new_transport(self, mock_client_cls):
        first_client = AsyncMock()
        second_client = AsyncMock()
        first_response = MagicMock()
        second_response = MagicMock()
        first_response.json.return_value = {'status': 'OK'}
        second_response.json.return_value = {'status': 'OK'}
        first_client.post.return_value = first_response
        second_client.post.return_value = second_response
        mock_client_cls.side_effect = [first_client, second_client]

        async with self.smsru as smsru:
            await smsru.balance()

        async with self.smsru as smsru:
            await smsru.balance()

        self.assertEqual(mock_client_cls.call_count, 2)
        first_client.aclose.assert_awaited_once_with()
        second_client.aclose.assert_awaited_once_with()

    @patch('smsru_api.aioclient.httpx.AsyncClient.post', new_callable=AsyncMock)
    async def test_request_propagates_raise_for_status_errors(self, mock_post):
        request = httpx.Request('POST', 'https://sms.ru/my/balance')
        response = httpx.Response(500, request=request)
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError('boom', request=request, response=response)
        mock_post.return_value = mock_response

        with self.assertRaises(httpx.HTTPStatusError):
            await self.smsru.balance()

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
