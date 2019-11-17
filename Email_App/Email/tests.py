from django.test import TestCase
from django.urls import reverse, resolve

# # Create your tests here.


class TestUrls(TestCase):

    # Send Email
    def test_email(self):
        url = reverse('Send Email')
        # print(url)
        assert resolve(url).view_name == 'Send Email'
