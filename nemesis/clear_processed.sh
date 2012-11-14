#!/bin/bash
sqlite3 db/nemesis.sqlite "delete from registrations where processed='1';"
