#!/usr/bin/env python
import os
import json
import pprint
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from libraries.utilities import *

class Notify:
    api_key = None
    template = None
    to_emails = None
    from_email = None
    subject = None

    def __init__(self, _API):
        self.api_key = _API

    def add_mailto(self, _recipients):
        recipients = []
        if is_json(_recipients):
            _recipients = json.loads(_recipients)
            for item in _recipients:
                email, sep, name = item.partition(',')
                to = (email, name)
                recipients.append(to)
        else:
            recipients.append(_recipients)

        if recipients:
            self.to_emails = recipients

    def add_content_html(self, _template):
        if isinstance(_template, list):
            self.template = ''.join(_template)

        if isinstance(_template, str):
            self.template = _template

    def update_content_html(self, _old, _new):
        lg("Updating email content")
        if isinstance(_new, list):
            str = ""
            for item in _new:
                #look for urls
                final_str = item
                str = "{}<br>{}".format(str,final_str)
            self.template = self.template.replace(_old, str)
            return

        # default is str
        self.template = self.template.replace(_old, _new)


    def add_from(self, _from):
        email, sep, name = _from.partition(',')
        self.from_email = (email,name)

    def add_subject(self, _subject):
        self.subject = _subject

    def validate(self):
        if not self.api_key:
            print("[Error] Please specify SendGrid API key")
            return False
        if not self.subject:
            print("[Error] Please specify email subject")
            return False
        if not self.to_emails:
            print("[Error] Please specify email recipients")
            return False
        if not self.from_email:
            print("[Error] Please specify from email address")
            return False
        if not self.template:
            print("[Error] Please specify email body")
            return False
        # Passed error checking, yay
        return True

    def printme(self):
        print("")
        print("FROM:    {}".format(self.from_email))
        print("TO:      {}".format(self.to_emails))
        print("SUBJECT: {}".format(self.subject))
        pprint.pprint(self.template)
        #print("{}".format(self.template))
        print("")


    def send_mail(self):
        # validate parameters
        if not self.validate():
            print("Validation Error found... exiting...")
            return False

        self.printme()
        # send email
        # exit()
        message = Mail(
            from_email=self.from_email,
            to_emails=self.to_emails,
            subject=self.subject,
            html_content=self.template)
        try:
            sendgrid_client = SendGridAPIClient(self.api_key)
            response = sendgrid_client.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
