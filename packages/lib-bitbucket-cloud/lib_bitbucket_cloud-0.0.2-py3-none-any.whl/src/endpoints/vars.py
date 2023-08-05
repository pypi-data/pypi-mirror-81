import os
from datetime import date


class Variables(object):

    def bitbucket_url(self):
        version = {'1': '1.0', '2': '2.0', '3': '3.0'}
        bitbucket = 'https://api.bitbucket.org/{version}/'.format(version=version['2'])
        return bitbucket
