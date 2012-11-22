#!/usr/bin/python

import helpers
import csv

if __name__ == "__main__":
    conn = helpers.sqlite_connect()
    cur  = conn.cursor()
    ids = set()
    details = []

    for row in cur.execute("SELECT * FROM registrations WHERE processed='0'"):
        details.append(row)
        ids.add(row[0])

    with open("users.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        for row in details:
            row = list(row)
            for i in range(1,7):
                row[i] = row[i].encode("utf-8")
            writer.writerow(row)

    for id in ids:
        cur.execute("UPDATE registrations SET processed='1' WHERE id=?", (id,))
        conn.commit()
