sqlite3 db/nemesis.sqlite "CREATE table IF NOT EXISTS auth (token VARCHAR(256), username VARCHAR(256))"
sqlite3 db/nemesis.sqlite "CREATE table IF NOT EXISTS registrations (id INTEGER PRIMARY KEY ASC AUTOINCREMENT,\
                                                                     teacher_username VARCHAR(256),\
                                                                     college_group    VARCHAR(256),\
                                                                     first_name       VARCHAR(256),\
                                                                     last_name        VARCHAR(256),\
                                                                     email            VARCHAR(256),\
                                                                     team             VARCHAR(256),\
                                                                     processed        INTEGER DEFAULT 0);"
