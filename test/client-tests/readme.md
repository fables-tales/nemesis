#Nemesis selenium tests

**This will only work on a dev srobo server, get one from [here](http://github.com/samphippen/badger-vagrant)**


1. Install the dependencies with the `get-dependencies.sh` script

Run these tests for javascript testing of nemesis. You'll need two terminals to
do so. The first you start a selenium server by running  `java -jar
$the_selenium_jar`. The other is to run the tests, do this by running `python
test_userman.py` in this directory.
