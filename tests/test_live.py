import os
import sys
import unittest

# Add the root directory of the project to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv

from smsru_api import Client, AsyncClient


# Load environment variables from .env file
load_dotenv()

API_ID = os.environ.get('SMSRU_API_ID')
TEST_PHONE = os.environ.get('SMSRU_TEST_PHONE')  # 79999999999

# Get auto_test from environment variable
auto_test = os.environ.get('AUTO_TEST', 'false').lower() == 'true'

class TestSmsRu(unittest.TestCase):
    def setUp(self):
        self.api_id = API_ID
        self.smsru = Client(self.api_id)
        self.check_id = None

    def test_send(self):
        response = self.smsru.send(TEST_PHONE, message='Test message', debug=True)
        self.assertEqual(response['status'], 'OK')

    def test_send_multi(self):
        response = self.smsru.send(multi={'79999999999': 'Test message', '79999999998': 'Test message 2'}, debug=True)
        self.assertEqual(response['status'], 'OK')

    @unittest.skipIf(auto_test, "Skipping callcheck_add test in auto test mode")
    def test_callcheck_add(self):
        response = self.smsru.callcheck_add(TEST_PHONE)
        self.assertEqual(response['status'], 'OK')
        self.check_id = response['check_id']

    @unittest.skipIf(auto_test, "Skipping callcheck_status test in auto test mode")
    def test_callcheck_status(self):
        if not self.check_id:
            self.skipTest("Skipping callcheck_status test because check_id is not set")
        response = self.smsru.callcheck_status(self.check_id)
        self.assertEqual(response['status'], 'OK')

    def test_status(self):
        response = self.smsru.status('sms_id')
        self.assertEqual(response['status'], 'OK')

    def test_cost(self):
        response = self.smsru.cost(TEST_PHONE, message='Test message')
        self.assertEqual(response['status'], 'OK')

    def test_balance(self):
        response = self.smsru.balance()
        self.assertEqual(response['status'], 'OK')

    def test_limit(self):
        response = self.smsru.limit()
        self.assertEqual(response['status'], 'OK')

    def test_free(self):
        response = self.smsru.free()
        self.assertEqual(response['status'], 'OK')

    def test_senders(self):
        response = self.smsru.senders()
        self.assertEqual(response['status'], 'OK')

    def test_stop_list(self):
        response = self.smsru.stop_list()
        self.assertEqual(response['status'], 'OK')

    def test_add_stop_list(self):
        response = self.smsru.add_stop_list(TEST_PHONE, comment='Test comment')
        self.assertEqual(response['status'], 'OK')

    def test_del_stop_list(self):
        response = self.smsru.del_stop_list(TEST_PHONE)
        self.assertEqual(response['status'], 'OK')

    def test_callbacks(self):
        response = self.smsru.callbacks()
        self.assertEqual(response['status'], 'OK')

    def test_add_callback(self):
        response = self.smsru.add_callback('http://example.com')
        self.assertEqual(response['status'], 'OK')

    def test_del_callback(self):
        response = self.smsru.del_callback('http://example.com')
        self.assertEqual(response['status'], 'OK')


class TestAsyncSmsRu(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.api_id = API_ID
        self.smsru = AsyncClient(self.api_id)
        self.check_id = None

    async def test_send(self):
        response = await self.smsru.send(TEST_PHONE, message='Test message', debug=True)
        self.assertEqual(response['status'], 'OK')

    async def test_send_multi(self):
        response = await self.smsru.send(multi={'79999999999': 'Test message', '79999999998': 'Test message 2'}, debug=True)
        self.assertEqual(response['status'], 'OK')

    @unittest.skipIf(auto_test, "Skipping callcheck_add test in auto test mode")
    async def test_callcheck_add(self):
        response = await self.smsru.callcheck_add(TEST_PHONE)
        self.assertEqual(response['status'], 'OK')
        self.check_id = response['check_id']

    @unittest.skipIf(auto_test, "Skipping callcheck_status test in auto test mode")
    async def test_callcheck_status(self):
        if not self.check_id:
            self.skipTest("Skipping callcheck_status test because check_id is not set")
        response = await self.smsru.callcheck_status(self.check_id)
        self.assertEqual(response['status'], 'OK')
    
    async def test_status(self):
        response = await self.smsru.status('sms_id')
        self.assertEqual(response['status'], 'OK')

    async def test_cost(self):
        response = await self.smsru.cost(TEST_PHONE, message='Test message')
        self.assertEqual(response['status'], 'OK')

    async def test_balance(self):
        response = await self.smsru.balance()
        self.assertEqual(response['status'], 'OK')  

    async def test_limit(self):
        response = await self.smsru.limit()
        self.assertEqual(response['status'], 'OK')

    async def test_free(self):
        response = await self.smsru.free()
        self.assertEqual(response['status'], 'OK')

    async def test_senders(self):
        response = await self.smsru.senders()
        self.assertEqual(response['status'], 'OK')

    async def test_stop_list(self):
        response = await self.smsru.stop_list()
        self.assertEqual(response['status'], 'OK')

    async def test_add_stop_list(self):
        response = await self.smsru.add_stop_list(TEST_PHONE, comment='Test comment')
        self.assertEqual(response['status'], 'OK')

    async def test_del_stop_list(self):
        response = await self.smsru.del_stop_list(TEST_PHONE)
        self.assertEqual(response['status'], 'OK')

    async def test_callbacks(self):
        response = await self.smsru.callbacks()
        self.assertEqual(response['status'], 'OK')

    async def test_add_callback(self):
        response = await self.smsru.add_callback('http://example.com')
        self.assertEqual(response['status'], 'OK')

    async def test_del_callback(self):
        response = await self.smsru.del_callback('http://example.com')
        self.assertEqual(response['status'], 'OK')


if __name__ == '__main__':
    unittest.main()
