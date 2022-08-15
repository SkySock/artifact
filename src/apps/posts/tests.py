import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase
from django.core.files import File
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest import mock

from apps.artifact_auth.services.base_auth import create_token
from apps.posts.models.post import Post
from apps.subscription.models import UserSubscriptionType, SponsorshipSubscription
from apps.users.models import ArtifactUser


class PostTests(APITestCase):
    def setUp(self):
        self.file_mock = mock.MagicMock(spec=File)
        self.file_mock.name = 'photo.jpg'

        self.user_test1 = ArtifactUser.objects.create(username='TestUser_1')
        self.user_test2 = ArtifactUser.objects.create(username='TestUser_2')

        self.sub1 = UserSubscriptionType.objects.create(
            owner=self.user_test1,
            name='111',
            description='111',
            image=self.file_mock,
            price=111
        )
        self.sub2 = UserSubscriptionType.objects.create(
            owner=self.user_test1,
            name='222',
            description='222',
            image=self.file_mock,
            price=222
        )
        self.sub3 = UserSubscriptionType.objects.create(
            owner=self.user_test1,
            name='333',
            description='333',
            image=self.file_mock,
            price=333
        )

        self.sub21 = UserSubscriptionType.objects.create(
            owner=self.user_test2,
            name='2121',
            description='2121',
            image=self.file_mock,
            price=2121
        )

        SponsorshipSubscription.objects.create(user=self.user_test2, subscription=self.sub2)

        image = io.BytesIO()
        Image.new('RGB', (512, 512)).save(image, 'JPEG')
        image.seek(0)

        post_image = SimpleUploadedFile('image.jpg', image.getvalue())

        self.post_data1 = {
        }

        self.user_test1_token = create_token(self.user_test1.id)['access_token']
        self.user_test2_token = create_token(self.user_test2.id)['access_token']

    def test_create_invalid_post(self):
        response = self.client.post(reverse('create_post'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_valid_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token)

        self.assertFalse(Post.objects.all().exists())

        response = self.client.post(reverse('create_post'))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Post.objects.all().exists())
        self.assertEqual(response.data['author'].get('id'), self.user_test1.id)

    def test_update_description_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token)
        response = self.client.post(reverse('create_post'))
        post_id = response.data['id']
        self.assertEqual(Post.objects.get(pk=post_id).description, '')

        update_desc_response = self.client.patch(
            reverse('update_post', kwargs={'pk': post_id}),
            data={'description': 'test_desc'}
        )
        self.assertEqual(update_desc_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_desc_response.data['description'], 'test_desc')
        self.assertEqual(Post.objects.get(pk=post_id).description, 'test_desc')

    def test_invalid_update_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token)
        response = self.client.post(reverse('create_post'))
        post_id = response.data['id']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test2_token)

        update_desc_response = self.client.patch(
            reverse('update_post', kwargs={'pk': post_id}),
            data={'description': 'test_desc'}
        )

        self.assertEqual(update_desc_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_subscription_type_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token)
        response = self.client.post(reverse('create_post'))
        post_id = response.data['id']
        self.assertEqual(Post.objects.get(pk=post_id).description, '')

        update_desc_response = self.client.patch(
            reverse('update_post', kwargs={'pk': post_id}),
            data={'level_subscription': self.sub2.id}
        )

        self.assertEqual(update_desc_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_desc_response.data['level_subscription'], self.sub2.id)
        self.assertEqual(Post.objects.get(pk=post_id).level_subscription, self.sub2)
