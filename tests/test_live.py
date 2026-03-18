import os
import unittest

import pytest

from smsru_api import AsyncClient, Client

pytestmark = pytest.mark.live


def _load_dotenv_if_available():
    if os.environ.get("SMSRU_LOAD_DOTENV", "false").lower() != "true":
        return

    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    load_dotenv()


def _get_live_settings():
    _load_dotenv_if_available()

    api_id = os.environ.get("SMSRU_API_ID")
    test_phone = os.environ.get("SMSRU_TEST_PHONE")
    auto_test = os.environ.get("AUTO_TEST", "false").lower() == "true"

    if not api_id or not test_phone:
        raise unittest.SkipTest(
            "Live tests require SMSRU_API_ID and SMSRU_TEST_PHONE. "
            "Run them explicitly with: pytest tests/test_live.py -m live"
        )

    return api_id, test_phone, auto_test


class TestSmsRu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_id, cls.test_phone, cls.auto_test = _get_live_settings()

    def setUp(self):
        self.smsru = Client(self.__class__.api_id)

    def test_send(self):
        response = self.smsru.send(self.__class__.test_phone, message="Test message", debug=True)
        self.assertEqual(response["status"], "OK")

    def test_send_multi(self):
        response = self.smsru.send(
            multi={"79999999999": "Test message", "79999999998": "Test message 2"},
            debug=True,
        )
        self.assertEqual(response["status"], "OK")

    @unittest.skipIf(os.environ.get("AUTO_TEST", "false").lower() == "true", "Skipping callcheck flow test in auto test mode")
    def test_callcheck_flow(self):
        add_response = self.smsru.callcheck_add(self.__class__.test_phone)
        self.assertEqual(add_response["status"], "OK")
        self.assertIn("check_id", add_response)
        self.assertTrue(add_response["check_id"])

        status_response = self.smsru.callcheck_status(add_response["check_id"])
        self.assertEqual(status_response["status"], "OK")

    def test_status(self):
        response = self.smsru.status("sms_id")
        self.assertEqual(response["status"], "OK")

    def test_cost(self):
        response = self.smsru.cost(self.__class__.test_phone, message="Test message")
        self.assertEqual(response["status"], "OK")

    def test_balance(self):
        response = self.smsru.balance()
        self.assertEqual(response["status"], "OK")

    def test_limit(self):
        response = self.smsru.limit()
        self.assertEqual(response["status"], "OK")

    def test_free(self):
        response = self.smsru.free()
        self.assertEqual(response["status"], "OK")

    def test_senders(self):
        response = self.smsru.senders()
        self.assertEqual(response["status"], "OK")

    def test_stop_list(self):
        response = self.smsru.stop_list()
        self.assertEqual(response["status"], "OK")

    def test_add_stop_list(self):
        response = self.smsru.add_stop_list(self.__class__.test_phone, comment="Test comment")
        self.assertEqual(response["status"], "OK")

    def test_del_stop_list(self):
        response = self.smsru.del_stop_list(self.__class__.test_phone)
        self.assertEqual(response["status"], "OK")

    def test_callbacks(self):
        response = self.smsru.callbacks()
        self.assertEqual(response["status"], "OK")

    def test_add_callback(self):
        response = self.smsru.add_callback("http://example.com")
        self.assertEqual(response["status"], "OK")

    def test_del_callback(self):
        response = self.smsru.del_callback("http://example.com")
        self.assertEqual(response["status"], "OK")


class TestAsyncSmsRu(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_id, cls.test_phone, cls.auto_test = _get_live_settings()

    async def asyncSetUp(self):
        self.smsru = AsyncClient(self.__class__.api_id)

    async def test_send(self):
        response = await self.smsru.send(self.__class__.test_phone, message="Test message", debug=True)
        self.assertEqual(response["status"], "OK")

    async def test_send_multi(self):
        response = await self.smsru.send(
            multi={"79999999999": "Test message", "79999999998": "Test message 2"},
            debug=True,
        )
        self.assertEqual(response["status"], "OK")

    @unittest.skipIf(os.environ.get("AUTO_TEST", "false").lower() == "true", "Skipping callcheck flow test in auto test mode")
    async def test_callcheck_flow(self):
        add_response = await self.smsru.callcheck_add(self.__class__.test_phone)
        self.assertEqual(add_response["status"], "OK")
        self.assertIn("check_id", add_response)
        self.assertTrue(add_response["check_id"])

        status_response = await self.smsru.callcheck_status(add_response["check_id"])
        self.assertEqual(status_response["status"], "OK")

    async def test_status(self):
        response = await self.smsru.status("sms_id")
        self.assertEqual(response["status"], "OK")

    async def test_cost(self):
        response = await self.smsru.cost(self.__class__.test_phone, message="Test message")
        self.assertEqual(response["status"], "OK")

    async def test_balance(self):
        response = await self.smsru.balance()
        self.assertEqual(response["status"], "OK")

    async def test_limit(self):
        response = await self.smsru.limit()
        self.assertEqual(response["status"], "OK")

    async def test_free(self):
        response = await self.smsru.free()
        self.assertEqual(response["status"], "OK")

    async def test_senders(self):
        response = await self.smsru.senders()
        self.assertEqual(response["status"], "OK")

    async def test_stop_list(self):
        response = await self.smsru.stop_list()
        self.assertEqual(response["status"], "OK")

    async def test_add_stop_list(self):
        response = await self.smsru.add_stop_list(self.__class__.test_phone, comment="Test comment")
        self.assertEqual(response["status"], "OK")

    async def test_del_stop_list(self):
        response = await self.smsru.del_stop_list(self.__class__.test_phone)
        self.assertEqual(response["status"], "OK")

    async def test_callbacks(self):
        response = await self.smsru.callbacks()
        self.assertEqual(response["status"], "OK")

    async def test_add_callback(self):
        response = await self.smsru.add_callback("http://example.com")
        self.assertEqual(response["status"], "OK")

    async def test_del_callback(self):
        response = await self.smsru.del_callback("http://example.com")
        self.assertEqual(response["status"], "OK")


if __name__ == "__main__":
    unittest.main()
