#!/bin/bash
cd test/api-tests && ./apache_tests.sh
cd ../client-tests && python test_userman.py
