#!/usr/bin/env python
# -*- coding: utf-8 -*- #
"""Scanner Script."""
import re
from libraries.utilities import *
from libraries.notify import Notify

bash_script = "/tmp/audit.sh"

create_dir(v("RESULTS_DIR"))

result_temp1 = "/tmp/result_temp1.txt"
result_temp2 = "/tmp/result_temp2.txt"
result_temp3 = "/tmp/result_temp3.txt"

result_final = v("RESULTS_FINAL")

file = open(bash_script, "w")
cmd = "git secrets --scan -r {}/ 2>&1 | tee {}".format(v("REPOS_DIR"), result_temp1)
file.write(cmd)
cmd = "cat /tmp/result_temp.txt | grep '^/app' > {}".format(result_temp2)
file.write(cmd)
file.close()

lg("Executing {}".format(bash_script))
run_bash(bash_script)

# Fix the findings to show URL
results = []
result_temp2_list = load_file_contents(result_temp2)
for line in result_temp2_list:
    regex_expression = r"^(\/app\/repos)\/([A-Za-z0-9_.-]*)\/([A-Za-z0-9_.-]*)\/(.+?):(\d+):(.*$)"
    regex = re.compile(regex_expression)
    rez = regex.split(line)

    try:
        url = "{}/{}/{}/blob/master/{}#L{}".format("https://github.com", rez[2], rez[3], rez[4], rez[5])
        # , rez[6]
        ahref = "<a href='{}'>{}</a>".format(url, url)
        output = ahref
    except IndexError:
        output = line

    results.append(output)

if results:
    lg("THINGS WERE FOUND!!! SENDING NOTIFICATION EMAIL!!!")
    notify = Notify(v("SENDGRID_API"))
    notify.add_from(v("EMAIL_FROM"))
    notify.add_mailto(v("EMAIL_NOTIFY"))
    notify.add_subject(v("EMAIL_SUBJECT"))
    notify.add_content_html(load_template(v("EMAIL_TEMPLATE")))
    notify.update_content_html("<!--RESULTS-->", results)
    notify.send_mail()
else:
    lg("Nothing found, going to sleep")
