# endpoints/user.py
import requests
from .vars import Variables
import os
import requests


class User(object):

    url = Variables()
    user_url = url.bitbucket_url() + 'user'

    def __init__(self, email, password, username):
        self.email = email
        self.username = username
        self.password = password

    def get_user(self, email: str):
        user_email = self.user_url + '/emails/{email}'.format(email=email)
        requests.get(user_email)
