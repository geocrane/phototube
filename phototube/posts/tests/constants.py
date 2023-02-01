from django.urls import reverse

from ..urls import app_name as posts_namespace


TEST_USER = "TEST_USER"
TEST_SLUG = "TEST_SLUG"
ANOTHER_USER = "ANOTHER_USER"
ANOTHER_SLUG = "ANOTHER_SLUG"

INDEX_URL = reverse(f"{posts_namespace}:index")
INDEX_URL_PAGE2 = INDEX_URL + "?page=2"
GROUP_URL = reverse(f"{posts_namespace}:group_list", args=[TEST_SLUG])
GROUP_URL_PAGE2 = GROUP_URL + "?page=2"
ANOTHER_GROUP_URL = reverse(
    f"{posts_namespace}:group_list", args=[ANOTHER_SLUG]
)
PROFILE_URL = reverse(f"{posts_namespace}:profile", args=[TEST_USER])
PROFILE_URL_PAGE2 = PROFILE_URL + "?page=2"
ANOTHER_PROFILE_URL = reverse(
    f"{posts_namespace}:profile", args=[ANOTHER_USER]
)
POST_CREATE_URL = reverse(f"{posts_namespace}:post_create")
LOGIN_URL = reverse("users:login")
CREATE_REDIRECT = f"{LOGIN_URL}?next={POST_CREATE_URL}"
FOLLOW_INDEX_URL = reverse(f"{posts_namespace}:follow_index")
FOLLOW_INDEX_URL_PAGE2 = FOLLOW_INDEX_URL + "?page=2"
FOLLOW_URL = reverse(f"{posts_namespace}:profile_follow", args=[TEST_USER])
ANOTHER_FOLLOW_URL = reverse(
    f"{posts_namespace}:profile_follow", args=[ANOTHER_USER]
)
UNFOLLOW_URL = reverse(f"{posts_namespace}:profile_unfollow", args=[TEST_USER])
FOLLOW_REDIRECT = f"{LOGIN_URL}?next={FOLLOW_URL}"
UNFOLLOW_REDIRECT = f"{LOGIN_URL}?next={UNFOLLOW_URL}"

SMALL_GIF = (
    b"\x47\x49\x46\x38\x39\x61\x02\x00"
    b"\x01\x00\x80\x00\x00\x00\x00\x00"
    b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
    b"\x00\x00\x00\x2C\x00\x00\x00\x00"
    b"\x02\x00\x01\x00\x00\x02\x02\x0C"
    b"\x0A\x00\x3B"
)

NEW_SMALL_GIF = (
    b"\x47\x49\x46\x38\x39\x61\x02\x00"
    b"\x01\x00\x80\x00\x00\x00\x00\x00"
    b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
    b"\x00\x00\x00\x2C\x00\x00\x00\x00"
    b"\x02\x00\x01\x00\x00\x02\x02\x0C"
    b"\x0A\x00\x3B\x3B"
)
