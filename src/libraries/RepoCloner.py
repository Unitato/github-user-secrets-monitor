#!/usr/bin/env python
# -*- coding: utf-8 -*- #
"""Script that clones repos locally."""

## TODO: multitheading.
import csv
from github import Github
import git
import os
#import shutil
from github import Github
from libraries.utilities import *
from progress.bar import Bar


class GitCloner():
    repos_home = None
    whitelist = None
    github_token = None
    github_userfile = None
    g = None
    whitelist_content = None

    def __init__(self):
        lg("Starting repository cloning process")
        self.repos_home = v("REPOS_DIR")
        self.whitelist = v("WHITELIST")
        self.github_token = v("GITHUB_API")
        self.github_userfile = v("TARGETS")
        self.g = Github(self.github_token)
        self.whitelist_content = list(filter(None, (line.rstrip() for line in open(self.whitelist))))

    def get_userlist(self):
        user_list = []
        with open(self.github_userfile, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if row[0] not in user_list:
                    user_list.append(row[0])

        return user_list

    def get_github_url(self, _repo):
        return "https://github.com/%s.git" % (_repo)

    def get_user_repo_urls(self, _user):
        repo_urls = []
        try:
            for repo in self.g.get_user(_user).get_repos():
                print(repo)
                repo_url = self.get_github_url(repo.full_name)

                if repo_url not in repo_urls:
                    repo_urls.append(repo_url)
                    lg(repo_url)
        except Exception as ex:
            lg("Couldn't get repos urls for %s" % (_user))
            lg("{}".format(ex))
            pass

        return repo_urls

    def get_user_repos(self, _user):
        repos = []
        try:
            for repo in self.g.get_user(_user).get_repos():
                result = repo.full_name

                # check whitelist
                if result in self.whitelist_content:
                    lg("[whitelisted] Skipping %s" % result)
                    continue

                if result not in repos:
                    repos.append(result)

        except Exception as ex:
            lg("Couldn't get repos for %s" % (_user))
            lg("{}".format(ex))
            pass

        return repos

    def get_all_repos(self, _users):
        lg("Collecting all user repos")
        repos_all = []
        bar = Bar('Fetching repo list', max=len(_users))
        for user in _users:
            bar.next()
            # print("Repo fetch progress: %s%%" % (round((status/len(_users))*100)), end='\r' )
            #progressbar(status, "Fetching: ", len(_users))
            repos_all += self.get_user_repos(user)
        bar.finish()
        print("")
        lg("Repo fetch complete")
        return repos_all

    def clone_repo(self, _repo):
        # create userdir
        user_dir = "%s/%s" % (self.repos_home, _repo.split('/', 1)[0])
        create_dir(user_dir)
        # clone user repos
        # if not check_whitelist(_repo):
        try:
            git.Git(user_dir).clone(self.get_github_url(_repo))

        except Exception as ex:
            lg("Unable to clone %s." % (_repo))
            lg(ex)
            return

    def run(self):
        users = self.get_userlist()
        repos = self.get_all_repos(users)
        create_dir(self.repos_home)

        bar = Bar('Cloning repos', max=len(repos))
        for repo in repos:
            bar.next()
            self.clone_repo(repo)
        bar.finish()

        print("")
        lg("Repo clone complete")
        lg("Cloned %s" % (get_folder_size(self.repos_home)))
        lg("The following repos were cloned")
        lg(repos)
