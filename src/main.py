#!/usr/bin/env python
# -*- coding: utf-8 -*- #
"""Main controller scipt."""

import os
import time

os.environ["SCRIPT_TIMESTAMP"] = time.strftime("%Y%m%d-%H%M%S")
from libraries.utilities import *
from libraries.RepoCloner import GitCloner

CONFIG_FILE = "config/secrets.yaml"
load_config(CONFIG_FILE)
# fix file paths
os.environ["BLACKLIST"] = os.path.join(v("SCRIPT_DIR"), v("BLACKLIST"))
os.environ["WHITELIST"] = os.path.join(v("SCRIPT_DIR"), v("WHITELIST"))
os.environ["TARGETS"] = os.path.join(v("SCRIPT_DIR"), v("TARGETS"))
os.environ["REPOS_DIR"] = os.path.join(v("SCRIPT_DIR"), "repos")
os.environ["RESULTS_DIR"] = os.path.join(v("SCRIPT_DIR"), "results")
os.environ["RESULTS_FINAL"] = os.path.join(v("RESULTS_DIR"), "audit-results.txt")

# print(os.environ)
lg("======= RUNNING GIT AUDIT SCRIPT =======")

run_python("set-patterns.py")
c = GitCloner()
c.run()
run_python("git-scanner.py")
