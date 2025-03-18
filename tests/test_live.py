import asyncio
import os
import sys

# Add the root directory of the project to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smsru_api.smsru import SmsRu, AsyncSmsRu

API_ID = os.environ.get('SMSRU_API_ID')
TEST_PHONE = os.environ.get('SMSRU_TEST_PHONE')  # 79999999999


def sync_main():
    smsru = SmsRu(API_ID)
    print(smsru.balance())
    print(smsru.limit())
    print(smsru.free())
    print(smsru.senders())
    print(smsru.stop_list())
    print(smsru.callbacks())
    print(smsru.add_stop_list(TEST_PHONE, 'comment'))
    print(smsru.del_stop_list(TEST_PHONE))
    print(smsru.add_callback('https://example.com/callback'))
    print(smsru.del_callback('https://example.com/callback'))
    print(smsru.cost(TEST_PHONE, message='Hello, World!'))

    send_response = smsru.send(TEST_PHONE, message='Hello, World!', debug=True)
    print(send_response)
    phone_id = TEST_PHONE[1:]
    print(smsru.status(send_response['sms'][phone_id]['sms_id']))

    callcheck_response = smsru.callcheck_add(TEST_PHONE)
    print(callcheck_response)
    print(smsru.callcheck_status(callcheck_response['check_id']))
    input(f'Call to {callcheck_response['call_phone_pretty']} and press Enter after call ...')
    print(smsru.callcheck_status(callcheck_response['check_id']))


async def async_main():
    smsru = AsyncSmsRu(API_ID)
    print(await smsru.balance())
    print(await smsru.limit())
    print(await smsru.free())
    print(await smsru.senders())
    print(await smsru.stop_list())
    print(await smsru.callbacks())
    print(await smsru.add_stop_list(TEST_PHONE, 'comment'))
    print(await smsru.del_stop_list(TEST_PHONE))
    print(await smsru.add_callback('https://example.com/callback'))
    print(await smsru.del_callback('https://example.com/callback'))
    print(await smsru.cost(TEST_PHONE, message='Hello, World!'))

    send_response = await smsru.send(TEST_PHONE, message='Hello, World!', debug=True)
    print(send_response)
    phone_id = TEST_PHONE[1:]
    print(await smsru.status(send_response['sms'][phone_id]['sms_id']))

    callcheck_response = await smsru.callcheck_add(TEST_PHONE)
    print(callcheck_response)
    print(await smsru.callcheck_status(callcheck_response['check_id']))
    input(f'Call to {callcheck_response['call_phone_pretty']} and press Enter after call ...')
    print(await smsru.callcheck_status(callcheck_response['check_id']))


if __name__ == '__main__':
    sync_main()
    asyncio.run(async_main())

