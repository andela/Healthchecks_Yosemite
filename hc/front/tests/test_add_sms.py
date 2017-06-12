import json

from django.test.utils import override_settings
from hc.api.models import Channel
from hc.test import BaseTestCase
from mock import patch
from twilio.rest import Client


@override_settings(TWILIO_AUTH_TOKEN="ACe838992263098fe0a6cd12278cb7fbac",         TWILIO_ACCOUNT_SID ="5973a845138a8cbb2f8e5f6df3d8fb8c")


class AddSmsTestCase(BaseTestCase):

     def test_it_sends_sms_notification(self):
        TWILIO_AUTH_TOKEN = "ACe838992263098fe0a6cd12278cb7fbac"
        TWILIO_ACCOUNT_SID = "5973a845138a8cbb2f8e5f6df3d8fb8c"
        client = Client(TWILIO_AUTH_TOKEN, TWILIO_ACCOUNT_SID)
        number = client.api.account.incoming_phone_numbers.create(
                  voice_url="http://demo.twilio.com/docs/voice.xml",
                  phone_number= "+15005550006")
