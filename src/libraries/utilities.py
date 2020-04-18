#!/usr/bin/env python
# -*- coding: utf-8 -*- #
"""Utilities Library."""
import os
import time
import sys
import yaml
import json
from subprocess import Popen, PIPE

SCRIPT_TIMESTAMP = os.environ["SCRIPT_TIMESTAMP"]


# Shorthand to get environment viriables
def v(_setting):
    return os.environ[_setting]


def lg(_STR, _TYPE="NOTICE"):
    logger(_STR, _TYPE)


def logger(_STR, _TYPE="NOTICE"):
    NOW = time.strftime("%Y-%m-%d %H:%M:%S")
    LOG_FILE = os.path.join("/app", os.environ["LOG_DIR"], "{}_audit.log".format(SCRIPT_TIMESTAMP))
    # print("Writing to {}".format(log_file))
    OUTPUT = "{} - [{}] {}\r\n".format(NOW, _TYPE, _STR)
    print(OUTPUT)
    f = open(LOG_FILE, "a+")
    f.write(OUTPUT)
    f.close()


# Load the configuration file into OS Environment variables.
# I am sure there is a better way to deal with configuration files.
def load_config(_CONFIG_FILE):
    # LOAD THROUGH CONFIG FILE
    if os.path.exists(_CONFIG_FILE):
        print("######  Starting audit script ######")
        os.environ["SCRIPT_DIR"] = os.getcwd()
        # print("[NOTICE] Config found. Loading '{}'...".format(_CONFIG_FILE))
        with open(_CONFIG_FILE, 'r') as stream:
            CONFIG = yaml.safe_load(stream)
            for k, v in CONFIG.items():
                if isinstance(CONFIG[k], list):
                    os.environ[k.upper()] = json.dumps(CONFIG[k])
                if isinstance(CONFIG[k], str):
                    os.environ[k.upper()] = CONFIG[k]
        lg("Configuration file '{}' loaded successfully...".format(_CONFIG_FILE))
        #exit()
    else:
        # print("[ERROR] Configuration file not found...")
        lg("Configuration file not found...", "ERROR")
        sys.exit()

# helper to mask secret strings, leaving the 4 characters in clear text.
def maskme(_STR, show_len=-4):
    ## TODO: Need to check for total lenth, to make sure the string is 12+ char
    return len(str(_STR)[:show_len]) * "#" + str(_STR)[show_len:]


# helper to run a pyton file and print to screen
def run_python(_python_file):
    cmd = ['python', _python_file]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if stdout.decode():
        lg(stdout.decode())
    if stderr.decode():
        lg(stderr.decode())


def is_json(_myjson):
    try:
        json_object = json.loads(_myjson)
    except ValueError as e:
        return False
    return True


# helper to run a bash file and print to screen
def run_bash(_python_file):
    cmd = ['bash', _python_file]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if stdout.decode():
        lg(stdout.decode())
    if stderr.decode():
        lg(stderr.decode())


def create_dir(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)


def load_file_contents(_filepath):
    return filter(None, (line.rstrip() for line in open(_filepath)))


def load_template(_file):
    try:
        with open(_file) as f:
            # print(f.readlines())
            return f.readlines()
    except IOError:
        print("Template file not accessible")


def get_folder_size(filepath, unit="MB"):
    bit_shift = {"B": 0, "kb": 7, "KB": 10, "mb": 17, "MB": 20, "gb": 27, "GB": 30, "TB": 40}

    def folder_size(_path):
        total = 0
        for entry in os.scandir(_path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += folder_size(entry.path)
        return total

    total_stize = folder_size(filepath)
    return '{:,.0f}'.format(total_stize / float(1 << bit_shift[unit])) + " " + unit
