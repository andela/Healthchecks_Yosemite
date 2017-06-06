from hc.api.models import Check
from hc.test import BaseTestCase


class UpdatePriorityTestCase(BaseTestCase):

    def setUp(self):
        super(UpdatePriorityTestCase, self).setUp()
        self.check = Check(user=self.alice)
        self.check.save()

 
    def test_it_works(self):
        url = "/checks/%s/priority/" % self.check.code
        payload = {"priority": 1}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        self.assertRedirects(r, "/checks/")

        check = Check.objects.get(code=self.check.code)
        assert check.priority == 1


    def test_team_access_works(self):
        url = "/checks/%s/priority/" % self.check.code
        payload = {"priority": -2}

        # Logging in as bob, not alice. Bob has team access so this
        # should work.
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url, data=payload)

        check = Check.objects.get(code=self.check.code)
        assert check.priority == -2

   