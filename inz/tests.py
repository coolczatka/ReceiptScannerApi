from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .views import *
from rest_framework.authtoken import views


class TestApi(TestCase):

    def test_register(self):
        view = UserViewSet.as_view({'post':'create'})
        factory = APIRequestFactory()
        email = "unikalny123@qwe.pl"
        password = "p0lsK4G01a"
        data = {'email': email, 'password': password}
        request = factory.post("/inz/users/",data,format='json')
        user = User(password=password,email=email)
        response = view(request)
        assert response.status_code == 201
        self.assertEqual(response.data['email'],user.email)

    def test_login(self):
        view = UserViewSet.as_view({'post': 'create'})
        factory = APIRequestFactory()
        username = "unikalny123@qwe.pl"
        password = "p0lsK4G01a"
        data = {'email': username, 'password': password}
        request = factory.post("/inz/users/", data, format='json')
        view(request)
        data = {'username': username, 'password': password}
        request = factory.post("/inz/login", data, format='json')
        login_view = views.obtain_auth_token
        response = login_view(request)

        assert response.status_code == 200
        self.assertTrue('token' in response.data)
