#Nemesis

This is Nemesis, a new system for allowing team leaders running teams for the
[Student Robotics](http://studentrobotics.org) competition to change their passwords.


##Contributing

Please file issues on GitHub. Not on the student robotics trac. Also please
send me a GitHub pull request if you want to merge changes in. This allows
for easy management in my brain

##Phippen, you ass, just let me hack on it

1. Get an srobo dev server [here](http://github.com/samphippen/badger-vagrant)
2. You've got nemesis in `/srv/nemesis`
3. Run the rest-api tests by changing into `test/api-tests` and running
   `./apache_tests.sh`
4. There are some obsolete javascript client tests in `test/client-tests`.
   In theory, the dependencies could be installed with `./get-dependencies.sh`,
   see the readme in the same directory to run the tests.

Once you've greenlit all the tests, make some changes, go wild, send me patches
either via GitHub or via gerrit and I'll review them for you!

##Development server, avoiding WSGI

It's also possible to develop using the srobo dev server just as the LDAP host.
For this, you'll need to install python, nose, pyldap & flask onto your dev machine,
and the configure nemesis to use a remote LDAP host.
This configuration is done in the config.ini within the `srusers` submodule of the
`libnemesis` submodule.

There's then a development mode server which you can run:

    python nemesis/app.py

which shows stack traces when things go wrong, and will auto-reload when you make code changes.

You'll also need to create the sqlite DB manually, which can be done using:

    ./nemesis/scripts/make_db.sh

Note that this will only create the DB if it's missing, and not update it or remove it.
As a result, if the schema changes the DB must be manually removed & re-created.
