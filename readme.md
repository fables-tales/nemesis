#Nemesis

This is Nemesis, a system for allowing team leaders running teams for the
[Student Robotics](http://studentrobotics.org) (SR) competition to administrate
the user accounts of the team (including their own).

##Contributing

Please file issues on Student Robotics [trac](http://trac.srobo.org) if you can.
If you can't, please raise issues on GitHub instead, but be aware they'll
be moved to trac for handling.

Patches should be submitted to SR's [gerrit](http://gerrit.srobo.org) if
possible, but GitHub pull requests (to @PeterJCLaw) are OK if you can't do this.
These are likely to be moved to gerrit for handling.

##Development on a clone of the deployment server

1. Get an srobo dev server [here](http://github.com/samphippen/badger-vagrant)
2. You've got nemesis in `/srv/nemesis`
3. Run the current set of valid tests using the `./run-tests` script.
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
