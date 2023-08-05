# tests/test_endpoint_specification.py

from ..endpoints import Repository, FileContent
import os
from pytest import fixture
from .set_envs import setup_repos, setup_file_contents


class TestRepository:
    """
    Used to test BB cloud /repositories/ endpoints.
    These cannot be run as-is you must create a file called .set_envs within the /tests/ directory and set
    the following environment variables:
    :var WORKSPACE - the workspace within bitbucket that contains your repositories.
    :var USERNAME -  the username of your own user or service account.
    :var PASSWORD - passwords as normal for the account OR an APP password generated on your user account if that
    account has mutli-factor auth enabled.
    """

    @fixture()
    def repos(self, setup_repos):
        repos = Repository(workspace=os.getenv('WORKSPACE'), username=os.getenv('USERNAME'),
                           password=os.getenv('PASSWORD'), repo_slug='lib-bitbucket-cloud')
        return repos

    def test_get_repos_by_request(self, repos):
        all_repos = repos.get_all_repos_by_request()

        assert isinstance(all_repos, list)
        assert 'pjicode/repo-backup' in all_repos

    def test_get_repo_by_name(self, repos):
        repo = repos.get_repo_by_name()
        assert repo
        repo_data = repo.json()
        assert repo_data['scm'] == 'git'


class TestFileContent:

    @fixture()
    def repo_file_contents(self, setup_file_contents):
        file_contents = FileContent(workspace=os.getenv('WORKSPACE'), username=os.getenv('USERNAME'),
                                    password=os.getenv('PASSWORD'), repo_slug=os.getenv('REPO'), node=os.getenv('NODE'),
                                    path=os.getenv('PATH'))
        return file_contents

    def test_get_src_of_repo(self, repo_file_contents):
        file = repo_file_contents.get_src_of_repo(meta=True)
        assert file.json()

    def test_get_repo_file_contents(self, repo_file_contents):
        file = repo_file_contents.get_repo_file_contents(path=os.getenv('PATH'), node=os.getenv('NODE'))
        assert file.json()
