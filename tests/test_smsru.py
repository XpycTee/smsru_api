import json
import os
import sys
import unittest
from unittest.mock import AsyncMock, patch, MagicMock

# Add the root directory of the project to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smsru_api import Client, AsyncClient


class TestSmsRu(unittest.TestCase):
    def setUp(self):
        self.api_id = 'TEST_API_ID'
        self.smsru = Client(self.api_id)

    @patch('smsru_api.client.request.urlopen')
    def test_send(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.send('79999999999', message='Test message', debug=True)
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_send_multi(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.send(multi={'79999999999': 'Test message', '79999999998': 'Test message 2'}, debug=True)
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_callcheck_add(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.callcheck_add('79999999999')
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_callcheck_status(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.callcheck_status('test_check_id')
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_status(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.status('sms_id')
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_cost(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.cost('79999999999', message='Test message')
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_balance(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.balance()
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_limit(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.limit()
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_free(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.free()
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_senders(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.senders()
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_stop_list(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.stop_list()
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_add_stop_list(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.add_stop_list('79999999999', comment='Test comment')
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_del_stop_list(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.del_stop_list('79999999999')
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_callbacks(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.callbacks()
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_add_callback(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.add_callback('http://example.com')
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.client.request.urlopen')
    def test_del_callback(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({'status': 'OK'}).encode()
        mock_urlopen.return_value = mock_response

        response = self.smsru.del_callback('http://example.com')
        self.assertEqual(response['status'], 'OK')


class TestAsyncSmsRu(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.api_id = 'TEST_API_ID'
        self.smsru = AsyncClient(self.api_id)

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_send(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.send('79999999999', message='Test message', debug=True)
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_send_multi(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.send(multi={'79999999999': 'Test message', '79999999998': 'Test message 2'}, debug=True)
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_callcheck_add(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.callcheck_add('79999999999')
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_callcheck_status(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.callcheck_status('test_check_id')
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_status(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.status('sms_id')
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_cost(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.cost('79999999999', message='Test message')
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_balance(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.balance()
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_limit(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.limit()
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_free(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.free()
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_senders(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.senders()
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_stop_list(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.stop_list()
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_add_stop_list(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.add_stop_list('79999999999', comment='Test comment')
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_del_stop_list(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.del_stop_list('79999999999')
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_callbacks(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.callbacks()
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_add_callback(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.add_callback('http://example.com')
        self.assertEqual(response['status'], 'OK')

    @patch('smsru_api.aioclient.aiohttp.ClientSession.post')
    async def test_del_callback(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={'status': 'OK'})
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.smsru.del_callback('http://example.com')
        self.assertEqual(response['status'], 'OK')

if __name__ == '__main__':
    unittest.main()
