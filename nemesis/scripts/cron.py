#!/usr/bin/env python

import os
import sys

nemesis_root = os.path.dirname(os.path.abspath(__file__)) + "/../"
sys.path.insert(0, nemesis_root)

import helpers

if __name__ == "__main__":
    helpers.clear_old_emails()
    helpers.clear_old_registrations()
