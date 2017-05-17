from django.test import Client, TestCase

from hc.api.models import Check, Ping


class PingTestCase(TestCase):

    def setUp(self):
        super(PingTestCase, self).setUp()
        self.check = Check.objects.create()

    def test_it_works(self):
        """
        Tests that it works
        """
        response = self.client.get("/ping/%s/" % self.check.code)
        assert response.status_code == 200

        self.check.refresh_from_db()
        assert self.check.status == "up"

        ping = Ping.objects.latest("id")
        assert ping.scheme == "http"

    def test_it_handles_bad_uuid(self):
        response = self.client.get("/ping/not-uuid/")
        assert response.status_code == 400

    def test_it_handles_120_char_user_agent(self):
        """
        Tests that it handles 120 characters
        """
        user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/44.0.2403.89 Safari/537.36")

        response = self.client.get("/ping/%s/" % self.check.code, HTTP_USER_AGENT=user_agent)
        assert response.status_code == 200

        ping = Ping.objects.latest("id")
        assert ping.user_agent == user_agent

    def test_it_truncates_long_user_agent(self):
        """
        Tests that it truncates long user_agent
        """
        user_agent = "01234567890" * 30

        response = self.client.get("/ping/%s/" % self.check.code, HTTP_USER_AGENT=user_agent)
        assert response.status_code == 200

        ping = Ping.objects.latest("id")
        assert len(ping.user_agent) == 200
        assert user_agent.startswith(ping.user_agent)

    def test_it_reads_forwarded_ip(self):
        """
        Tests that it reads the forwarded IP
        """
        ip = "1.1.1.1"
        response = self.client.get("/ping/%s/" % self.check.code,
                                   HTTP_X_FORWARDED_FOR=ip)
        ping = Ping.objects.latest("id")
        ### Assert the expected response status code and ping's remote address
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ping.remote_addr, "1.1.1.1")

        ip = "1.1.1.1, 2.2.2.2"
        response = self.client.get("/ping/%s/" % self.check.code,
                                   HTTP_X_FORWARDED_FOR=ip, REMOTE_ADDR="3.3.3.3")
        ping = Ping.objects.latest("id")
        assert response.status_code == 200
        assert ping.remote_addr == "1.1.1.1"

    def test_it_reads_forwarded_protocol(self):
        """
        Tests that it reads the forwarded protocol
        """
        response = self.client.get("/ping/%s/" % self.check.code,
                                   HTTP_X_FORWARDED_PROTO="https")
        ping = Ping.objects.latest("id")
        ### Assert the expected response status code and ping's scheme
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ping.scheme, 'https')

    def test_it_never_caches(self):
        response = self.client.get("/ping/%s/" % self.check.code)
        assert "no-cache" in response.get("Cache-Control")

    ### Test that when a ping is made a check with a paused status changes status
    def test_check_status_changes_when_ping_is_made_on_paused_check(self):
        """
        For a Check with paused status, when a ping is made, the status should change.
        """
        self.check.status = "paused"
        self.client.get("/ping/{}/".format(self.check.code))
        self.check.refresh_from_db()
        self.assertNotEqual(self.check.status, "paused")

    ### Test that a post to a ping works

    def test_post_request_to_ping_works(self):
        """
        A POST request to ping view should work
        """
        response = self.client.post("/ping/{}/".format(self.check.code))
        self.assertEqual(response.status_code, 200)

    ### Test that the csrf_client head works(Cross Site Request Forgery middleware)
    def test_csrf_client_head_works(self):
        """
        Tests that the HEAD request using the csrf_client works
        """
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.get("/ping/{}/".format(self.check.code))
        self.assertEqual(response.status_code, 200)


