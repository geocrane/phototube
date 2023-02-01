from django.test import TestCase
from django.urls import reverse

from ..urls import app_name as posts_namespace


USERNAME = "username"
SLUG = "slug"
POST_ID = 1
CASES = [
    ["index", None, "/"],
    ["group_list", (SLUG,), f"/group/{SLUG}/"],
    ["profile", (USERNAME,), f"/profile/{USERNAME}/"],
    ["post_detail", (POST_ID,), f"/posts/{POST_ID}/"],
    ["post_edit", (POST_ID,), f"/posts/{POST_ID}/edit/"],
    ["post_create", None, "/create/"],
    ["add_comment", (POST_ID,), f"/posts/{POST_ID}/comment/"],
    ["follow_index", None, "/follow/"],
    ["profile_follow", (USERNAME,), f"/profile/{USERNAME}/follow/"],
    ["profile_unfollow", (USERNAME,), f"/profile/{USERNAME}/unfollow/"],
]


class RoutesTests(TestCase):
    def test_URLs_uses_correct_routes(self):
        """URL-адреса используют правильные маршруты."""
        for route, args, url in CASES:
            with self.subTest(route=route):
                self.assertEqual(
                    url, reverse(f"{posts_namespace}:{route}", args=args)
                )
