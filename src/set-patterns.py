#!/usr/bin/env python
# -*- coding: utf-8 -*- #
"""Main controller scipt."""

import sys
from libraries.utilities import *


blacklist = v("BLACKLIST")
whitelist = v("WHITELIST")
bash_script = "/tmp/update-patterns.sh"

blacklist_content = filter(None, (line.rstrip() for line in open(blacklist)))
whitelist_content = filter(None, (line.rstrip() for line in open(whitelist)))

file = open(bash_script, "w")
lg("Checking for the following blacklisted patterns")
p = []
for line in blacklist_content:
    if '##STOP##' in line:
        print("exiting")
        sys.exit()
    if '#' not in line and line:
        pattern = line.replace("\"", "\\\"")
        cmd = "git secrets --add --global \"%s\" \n" % (pattern)
        p.append(pattern)
        file.write(cmd)
lg(p)


lg("Whitelisting the following patterns")
p = []
for line in whitelist_content:
    if '#' not in line and line:
        pattern = line.replace("\"", "\\\"")
        cmd = "git secrets --add --global -a \"%s\" \n" % (pattern)
        p.append(pattern)
        file.write(cmd)
lg(p)

# Add global AWS settings
p = []
lg("Adding global AWS settings")
cmd = "git secrets --register-aws --global"
p.append(cmd)
file.write(cmd)
lg(p)
file.close()

# Run produced bash files
lg("Executing {}".format(bash_script))
run_bash(bash_script)
