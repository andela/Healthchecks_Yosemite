from datetime import timedelta

from django.utils import timezone
from hc.api.management.commands.sendreports import Command
from hc.api.models import Check, Channel
from hc.test import BaseTestCase


class SendReportsTestCase(BaseTestCase):

    def test_sends_daily_report(self):
        """ Tests one run sends daily reports """
        joined_date= timezone.now() - timedelta(days=1)
        self.alice.date_joined = joined_date
        self.profile.daily_reports_allowed = 1
        self.alice.save()
        self.profile.save()
        check = Check(user=self.alice, status="up", last_ping=timezone.now())
        check.save()

        result = Command().handle_one_run()
        self.assertEqual(result, 1)

    def test_sends_weekly_report(self):
        """ Tests one run sends weekly reports """
        joined_date = timezone.now() - timedelta(days=7)
        self.alice.date_joined = joined_date
        self.profile.weekly_reports_allowed = 7
        self.alice.save()
        self.profile.save()
        check = Check(user=self.alice, status="up", last_ping=timezone.now())
        check.save()

        result = Command().handle_one_run()
        self.assertEqual(result, 1)

    def test_sends_monthly_report(self):
        """ Tests one run sends monthly reports """
        joined_date= timezone.now() - timedelta(days=30)
        self.alice.date_joined = joined_date
        self.profile.reports_allowed = 30
        self.alice.save()
        self.profile.save()
        check = Check(user=self.alice, status="up", last_ping=timezone.now())
        check.save()

        result = Command().handle_one_run()
        self.assertEqual(result, 1)
