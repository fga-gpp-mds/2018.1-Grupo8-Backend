from django.test import Client
from .models import SocialInformation, Person as User
from django.urls import include, path, reverse
from rest_framework.test import APIRequestFactory, APITestCase
from .views import SocialInformationViewset, UserViewset
from  rest_framework import serializers, status
from django.utils.translation import ugettext_lazy as _
# Create your tests here.


class UserTests(APITestCase):

    def setUp(self):
        """
        This method will run before any test.
        """
        self.superuser = User.objects.create_superuser(
            username='flyer user',
            email='flye@user.com',
            password='idontneedthisshit'
        )
        self.user = User.objects.create(
            username='teste',
            first_name='teste',
            last_name='teste',
            email='teste@teste.com',
            password='teste'
        )
        self.url = '/api/users/'
        # self.client.force_login(self.user)
        self.client.force_authenticate(self.superuser)

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.user.delete()

    def test_create_user(self):
        """
        Ensure we can create a user object.
        """
        response = self.client.get(self.url + str(self.user.pk) + '/')
        # new_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)

    def test_invalid_create_user(self):
        """
        Ensure we can't create a invalid user object.
        """
        data = {
        'username':'updated',
        'first_name':'teste',
        'last_name':'teste',
        'email':'erro',
        'password':'teste'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        """
        Ensure we can create a new user object.
        """
        self.assertEqual(self.user.username, 'teste')
        data = {
            'username':'updated',
            'first_name':'teste',
            'last_name':'teste',
            'email':'teste@teste.com',
            'password':'teste'
        }
        response = self.client.put(self.url + str(self.user.pk) + '/', data)

        new_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.assertEqual(new_user.username, 'updated')

    def test_invalid_update_user(self):
        """
        Ensure we can't update a user object with invalid fields.
        """
        self.assertEqual(self.user.username, 'teste')
        data = {
            'username':'updated',
            'first_name':'teste',
            'last_name':'teste',
            'email':'erro',
            'password':'teste'
        }
        response = self.client.put(self.url + str(self.user.pk) + '/', data)


        new_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data,
            {'email': [_('Enter a valid email address.')]}
        )

    def test_partial_update_user(self):
        """
        Ensure we can partially update a user object.
        """
        self.assertEqual(self.user.email, 'teste@teste.com')
        data = {
            'email':'silverson@teste.com',
        }
        response = self.client.patch(self.url + str(self.user.pk) + '/', data)
        new_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.assertEqual(new_user.email, 'silverson@teste.com')

    def test_invalid_partial_update_user(self):
        """
        Ensure we can't partially update invalid information on a valid user
        object.
        """
        self.assertEqual(self.user.email, 'teste@teste.com')
        data = {
            'email':'silverson',
        }
        response = self.client.patch(self.url + str(self.user.pk) + '/', data)
        new_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data,
            {'email': [_('Enter a valid email address.')]}
        )

# class SocialInformationTests(APITestCase):
#
#     def setUp(self):
#         """
#         This method will run before any test.
#         """
#
#         self.user = User.objects.create(
#             username='teste',
#             first_name='teste',
#             last_name='teste',
#             email='teste@teste.com',
#             password='teste'
#         )
#         self.social = SocialInformation.objects.create(
#             owner=self.user,
#             state='AC',
#             city='Rio Branco',
#             income='10.00',
#             education='EFC',
#             job='Dono de Casa',
#             birth_date='2018-04-07'
#         )
#         self.url = '/api/socialInformation/'
#
#     def tearDown(self):
#         """
#         This method will run after any test.
#         """
#         self.user.delete()
#         self.social.delete()
#
#     def test_create_social(self):
#         """
#         Ensure we can create a social information object.
#         """
#         response = self.client.get(self.url + str(self.social.pk) + '/')
#         new_social = SocialInformation.objects.get(pk=self.social.pk)
#         self.assertEqual(response.status_code,  status.HTTP_200_OK)
#
#     def test_invalid_create_social(self):
#         """
#         Ensure we can't create a invalid social information object.
#         """
#         data = {
#             "owner": self.user,
#             "state": "AC",
#             "city": "Rio Branco",
#             "income": "10.00",
#             "education": "EFC",
#             "job": "Dono de Casa",
#             "birth_date": "20180-32-13"
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_update_social(self):
#         """
#         Ensure we can update a new social information object.
#         """
#         self.assertEqual(self.social.job, 'Dono de Casa')
#         data = {
#             "owner": self.user.pk,
#             "state": "AC",
#             "city": "Rio Branco",
#             "income": "10.00",
#             "education": "EFC",
#             "job": "Dono de Prédio",
#             "birth_date": "2018-04-07"
#         }
#         response = self.client.put(self.url + str(self.social.pk) + '/', data)
#
#
#         new_social = SocialInformation.objects.get(pk=self.social.pk)
#         self.assertEqual(response.status_code,  status.HTTP_200_OK)
#         self.assertEqual(new_social.job, 'Dono de Prédio')
#
#     def test_invalid_update_social(self):
#         """
#         Ensure we can't update a social object with invalid fields.
#         """
#         self.assertEqual(self.social.birth_date, '2018-04-07')
#         data = {
#             "owner": self.user.pk,
#             "state": "AC",
#             "city": "Rio Branco",
#             "income": "10.00",
#             "education": "EFC",
#             "job": "Dono de Casa",
#             "birth_date": "20180-43-213"
#         }
#         response = self.client.put(self.url + str(self.social.pk) + '/', data)
#
#
#         new_social = SocialInformation.objects.get(pk=self.social.pk)
#         self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)
#         self.assertEquals(
#             response.data,
#             {"birth_date": [
#                 "Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]]."
#             ]}
#         )
#
#     def test_partial_update_social(self):
#         """
#         Ensure we can partially update a social object.
#         """
#         self.assertEqual(self.social.job, 'Dono de Casa')
#         data = {
#             'job':'Dono de Condomínio',
#         }
#         response = self.client.patch(self.url + str(self.social.pk) + '/', data)
#         new_social = SocialInformation.objects.get(pk=self.social.pk)
#         self.assertEqual(response.status_code,  status.HTTP_200_OK)
#         self.assertEqual(new_social.job, 'Dono de Condomínio')
#
#     def test_invalid_partial_update_social(self):
#         """
#         Ensure we can't partially update invalid information on a valid social
#         object.
#         """
#         self.assertEqual(self.social.job, 'Dono de Casa')
#         data = {
#             'birth_date': '20180-56-89',
#         }
#         response = self.client.patch(self.url + str(self.social.pk) + '/', data)
#         new_social = SocialInformation.objects.get(pk=self.social.pk)
#         self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)
#         self.assertEquals(
#             response.data,
#             {"birth_date": [
#                 "Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]]."
#             ]}
#         )
