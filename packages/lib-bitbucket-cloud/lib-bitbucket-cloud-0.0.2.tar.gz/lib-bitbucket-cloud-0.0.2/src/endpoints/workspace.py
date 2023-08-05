# endpoints/workspace.py
import requests
from .vars import Variables
import os


class Repository(object):
    url = Variables()
    repository_url = url.bitbucket_url() + "repositories"

    def __init__(self, workspace, repo_slug, password, username):
        self.workspace = workspace
        self.repo_slug = repo_slug
        self.username = username
        self.password = password

    def get_all_repos_by_request(self):
        """
        :return: List of repositories inside a workspace.
        ex. [pjicode/repo-backup, ...]
        """
        repo_values = []
        continue_page = True
        page = 1
        print("{siteurl}/{workspace}?page={page}".format(
            siteurl=self.repository_url, workspace=self.workspace, page=page))
        while continue_page:
            repo = "{siteurl}/{workspace}?page={page}".format(
                siteurl=self.repository_url, workspace=self.workspace, page=page)
            repo = requests.get(repo, auth=(self.username, self.password))
            all_repos = repo.json()
            x = 0
            while x <= len(all_repos['values']) - 1:
                repo_values.append(all_repos['values'][x]['full_name'])
                x += 1
            if not all_repos['values']:
                break
            page += 1
        print("There are {pages} pages of repositories and a total of {total} in the {workspace} workspace.".format(
            pages=page, total=len(repo_values), workspace=self.workspace
        ))
        return repo_values

    def get_repo_by_name(self):
        """
        All data associated with a repository.
        """
        repo_url = "{siteurl}/{workspace}/{repo}".format(
            siteurl=self.repository_url, workspace=self.workspace, repo=self.repo_slug)
        repo = requests.get(repo_url, auth=(self.username, self.password))
        return repo


class FileContent(Repository):
    """
    Used to gather file contents of a repository and returns it as text
    """

    def __init__(self, node, path, workspace, repo_slug, password, username):
        super().__init__(workspace, repo_slug, password, username)
        self.node = node
        self.path = path

    def get_src_of_repo(self, meta: bool = False):
        """
        :param meta=true adds the query parameter format=meta to the request
        :return: text of the file requested.
        """
        if meta:
            repo_url = "{siteurl}/{workspace}/{repo}/src?format=meta".format(siteurl=self.repository_url,
                                                                             workspace=self.workspace, repo=self.repo_slug)
        else:
            repo_url = "{siteurl}/{workspace}/{repo}/src".format(siteurl=self.repository_url,
                                                                 workspace=self.workspace, repo=self.repo_slug)

        file_metadata = requests.get(repo_url, auth=(self.username, self.password))
        metafile = file_metadata.json()
        valid = 'yes' if 'pagelen' in metafile else 'no'
        src_contents = []
        if valid == 'yes':
            i = 0
            while i < len(metafile['values']):
                meta_link = metafile['values'][i]['links']['self']['href']
                meta_list = meta_link.split('/')
                src_contents += meta_list[-1]
                i += 1
        return src_contents

    def post_src_in_repo(self, payload: dict):
        """
        :param payload:
        :return:
        """

    def get_repo_file_contents(self, node: str, path: str):
        """
        This endpoints is used to retrieve the contents of a single file, or the contents of a
         directory at a specified revision.
        :return:
        """
        repo_url = "{siteurl}/{workspace}/{repo}/src/{node}/{path}".format(
            siteurl=self.repository_url, workspace=self.workspace, repo=self.repo_slug, node=node, path=path)
        file = requests.get(repo_url, auth=(self.username, self.password))
        return file


class Members(Repository):
    """/members/{member}"""


