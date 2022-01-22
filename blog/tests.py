from django.urls import reverse, resolve
from django.test import TestCase
from django.test import Client
from .views import home


class TestViews(TestCase):
  def setUp(self) -> None:
      self.client = Client()
  def test_home(self):
    response = self.client.get('home')
    url = reverse('home')
    self.assertEquals(resolve(url).func, home)
    self.assertEquals(response.status_code, 404)
    
  