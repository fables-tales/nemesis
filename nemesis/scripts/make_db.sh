sqlite3 db/nemesis.sqlite "CREATE table IF NOT EXISTS auth (token VARCHAR(256), username VARCHAR(256))"
sqlite3 db/nemesis.sqlite "CREATE table IF NOT EXISTS registrations (username         VARCHAR(256) UNIQUE PRIMARY KEY,\
                                                                     teacher_username VARCHAR(256),\
                                                                     college          VARCHAR(256),\
                                                                     team             VARCHAR(256),\
                                                                     email            VARCHAR(256),\
                                                                     request_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
                                                                     verify_code      VARCHAR(256));"
sqlite3 db/nemesis.sqlite "CREATE table IF NOT EXISTS email_changes (username         VARCHAR(256) UNIQUE PRIMARY KEY,\
                                                                     new_email        VARCHAR(256),\
                                                                     request_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
                                                                     verify_code      VARCHAR(256));"
sqlite3 db/nemesis.sqlite "CREATE table IF NOT EXISTS outbox (id INTEGER PRIMARY KEY ASC AUTOINCREMENT,\
                                                              toaddr                VARCHAR(256),\
                                                              template_name         VARCHAR(256),\
                                                              template_vars_json    VARCHAR(512),\
                                                              request_time          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                              last_error            VARCHAR(256),\
                                                              retry_count           INTEGER DEFAULT 0,\
                                                              sent_time             TIMESTAMP);"
