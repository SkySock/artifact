from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from src.apps.users.models import ArtifactUser, UserFollowing


class FollowTest(APITestCase):
    def setUp(self):
        ArtifactUser.objects.create(username='TestUser_1')
        ArtifactUser.objects.create(username='TestUser_2')

    def test_follow(self):
        user_1 = ArtifactUser.objects.get(username='TestUser_1')
        user_2 = ArtifactUser.objects.get(username='TestUser_2')
        self.client.force_authenticate(user=user_1)
        request = self.client.post(f'/api/v1/users/follow/{user_2.pk}/')

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.data, {'is_followed': True})
        self.assertEqual(UserFollowing.objects.count(), 1)
        self.assertEqual(UserFollowing.objects.get().user, user_1)
        self.assertEqual(UserFollowing.objects.get().following_user, user_2)
