from pytest import fixture
import os
from ..endpoints import Repository, FileContent


@fixture()
def setup_repos():
    os.environ['SITE'] = 'https://api.bitbucket.org/2.0/'
    os.environ['WORKSPACE'] = 'pjicode'
    os.environ['USERNAME'] = 'zachary_sanders'
    os.environ['PASSWORD'] = 'jv2srWPupTHVnveJW7gp'
    return 1


@fixture()
def setup_file_contents():
    os.environ['SITE'] = 'https://api.bitbucket.org/2.0/'
    os.environ['WORKSPACE'] = 'pjicode'
    os.environ['USERNAME'] = 'zachary_sanders'
    os.environ['PASSWORD'] = 'jv2srWPupTHVnveJW7gp'
    os.environ['PATH'] = '/tests/test_endpoint_specification'
    os.environ['REPO'] = 'lib-bitbucket-cloud'
    os.environ['NODE'] = 'master'
    return 1
