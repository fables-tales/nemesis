#Nemesis

This is Nemesis, a new system for allowing team leaders running teams for the
[Student Robotics](http://studentrobotics.org) competition to change their passwords.


##Contributing

Please file issues on GitHub. Not on the student robotics trac. Also please
send me a GitHub pull request if you want to merge changes in. This allows
for easy management in my brain

##Phippen, you ass, just let me hack on it


1. Get an srobo dev server [here](http://studentrobotics.org)
2. You've got nemesis in `/srv/nemesis`
3. Run the rest-api tests by changing into `test/api-tests` and running
   `./apache_tests.sh`
4. Run the javascript client tests by changing into `test/client-tests`
   installing the dependencies with `./get-dependencies.sh` and then run the
   tests (details in the readme in that directory)

Once you've greenlit all the tests, make some changes, go wild, send me patches
either via GitHub or via gerrit and I'll review them for you!
