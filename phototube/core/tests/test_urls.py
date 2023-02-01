from django.test import Client, TestCase


class UrlTest(TestCase):
    def setUp(self):
        self.guest = Client()

    def test_404_template(self):
        """404 отдает кастомный шаблон"""
        self.assertTemplateUsed(
            self.guest.get("/unexcisting_page/"), "core/404.html"
        )
