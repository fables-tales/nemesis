#!/bin/bash
cd test/client-tests && python test_userman.py
cd ../api-tests && ./apache_tests.sh
