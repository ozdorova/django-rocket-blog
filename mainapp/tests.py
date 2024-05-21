from http import HTTPStatus
from urllib import response
from django.core.cache import cache
from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class TestPages(TestCase):
    fixtures = ['mainapp_articlemodel.json', 'mainapp_category.json', 'mainapp_comments.json', 'users_user.json', 'auth_group.json']
    
    def setUp(self) -> None:
        cache.clear()
    
    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        self.assertTemplateUsed(response, 'mainapp/index.html')
        
        self.assertEqual(response.context_data['title'], 'Главная')
    
    def test_redirect_addpost(self):
        path = reverse('addpost')
        
        redirect_uri = reverse('users:login') + '?next=' + path
        
        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)
    
    