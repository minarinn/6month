from django.test import TestCase
from users.tasks import manual_task, cleanup_task, smtp_task


class CeleryTasksTest(TestCase):
    def test_manual_task(self):
        result = manual_task('TestUser')
        self.assertEqual(result, 'Hello TestUser')

    def test_cleanup_task(self):
        result = cleanup_task()
        self.assertEqual(result, 'cleanup done')

    def test_smtp_task(self):
        result = smtp_task('test@example.com')
        self.assertEqual(result, 'email sent')