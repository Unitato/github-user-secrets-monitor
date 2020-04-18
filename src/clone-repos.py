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


repos_home = "{}/repos".format(v("SCRIPT_DIR"))
whitelist = v("WHITELIST")
github_token = v("GITHUB_API")
github_userfile = v("TARGETS")

g = Github(github_token)
whitelist_content = list(filter(None, (line.rstrip() for line in open(whitelist))))

print("asdasdasdsad")

def create_dir(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)


def get_userlist():
    user_list = []
    with open(github_userfile, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            if row[0] not in user_list:
                user_list.append(row[0])

    return user_list


def get_github_url(_repo):
    return "https://github.com/%s.git" % (_repo)


def get_user_repo_urls(_user):
    repo_urls = []
    try:
        for repo in g.get_user(_user).get_repos():
            repo_url = get_github_url(repo.full_name)

            if repo_url not in repo_urls:
                repo_urls.append(repo_url)
                lg(repo_url)
    except:
        lg("Couldn't get repos for %s" % (_user))
        pass

    return repo_urls


def get_user_repos(_user):
    repos = []
    try:
        for repo in g.get_user(_user).get_repos():
            result = repo.full_name

            # check whitelist
            if result in whitelist_content:
                lg("[whitelisted] Skipping %s" % result)
                continue

            if result not in repos:
                repos.append(result)
                # print(result)
    except:
        lg("Couldn't get repos for %s" % (_user))
        pass

    return repos


def get_all_repos(_users):
    print("a")
    lg("Collecting all user repos")
    repos_all = []
    status = 0
    for user in _users:
        status += 1
        # print("Repo fetch progress: %s%%" % (round((status/len(_users))*100)), end='\r' )
        progressbar(status, "Fetching: ", len(_users))
        repos_all += get_user_repos(user)
    lg("Repo fetch complete")
    return repos_all


def clone_repo(_repo):
    # create userdir
    user_dir = "%s/%s" % (repos_home, _repo.split('/', 1)[0])
    create_dir(user_dir)
    # clone user repos
    # if not check_whitelist(_repo):
    try:
        git.Git(user_dir).clone(get_github_url(_repo))

    except Exception as ex:
        lg("Unable to clone %s." % (_repo))
        lg(ex)
        return


users = get_userlist()
repos = get_all_repos(users)

create_dir(repos_home)

status = 0
for repo in repos:
    status += 1
    percent = round((status/len(repos))*100)
    size = get_folder_size(repos_home)
    #print("Repo clone progress [%s - %s so far]: %s%%    " % (repo,size,percent), end='\r' )
    progressbar(percent, "Repo clone progress [{}]: ".format(size))
    print("STATUS: {}".format(status))
    clone_repo(repo)
lg("Repo clone complete")
lg("Cloned %s" % (get_folder_size(repos_home)))
lg(repos)
