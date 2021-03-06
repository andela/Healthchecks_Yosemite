from django.test.utils import override_settings

from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):
    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Integration Settings", status_code=200)

            ### Test that the team access works
            # team consists (alice, bob)
            # saving user alice in the system

    def test_team_access_works(self):
        self.channel = Channel(user=self.alice, kind="email")
        self.channel.value = "alice@example.org"
        self.channel.save()

        # We login as bob since bob has access
        # navigate to below url
        url = "/integrations/{}/checks/".format(self.channel.code)

        self.client.login(username="bob@example.org", password="password")
        res = self.client.get(url)
        self.assertContains(res, "Assign Checks to Channel", status_code=200)

    ### Test that bad kinds don't work (kinds that were not included in the channel_kinds)

    def test_bad_kinds(self):
        self.client.login(username="bob@example.org", password="password")
        kinds = ("twitter", "instagram", "linkedin", "medium")
        for kind in kinds:
            url = "/integrations/add_{}/".format(kind)
            response = self.client.get(url)
            assert response.status_code == 404

