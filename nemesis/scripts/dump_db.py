#!/usr/bin/python
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../")

import lib.helpers as helpers
import csv


TARGET_FILENAME = "users.csv"

if __name__ == "__main__":
    if os.path.exists(TARGET_FILENAME):
        print TARGET_FILENAME,"exists, exiting!"
        exit(1)
    else:
        conn = helpers.sqlite_connect()
        cur  = conn.cursor()
        ids = set()
        details = []

        for row in cur.execute("SELECT * FROM registrations WHERE processed='0'"):
            details.append(row)
            ids.add(row[0])

        # Make created files have no 'group' or 'other' access.
        os.umask(0177)

        with open(TARGET_FILENAME, "w") as csvfile:
            writer = csv.writer(csvfile)
            for row in details:
                row = list(row)

                #the format of the row is such that the first and last entries are
                #integers and everything else is a string. Given that the strings
                #come from user input they should be utf-8 encoded to make them
                #work. The other two are id and processed (boolean 1 or 0)
                for i in range(1,7):
                    row[i] = row[i].encode("utf-8")
                writer.writerow(row)

        for id in ids:
            cur.execute("UPDATE registrations SET processed='1' WHERE id=?", (id,))
            conn.commit()
