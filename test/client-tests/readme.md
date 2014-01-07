#Nemesis selenium tests

These tests test the Javascript client portion of Nemesis, and run against
a real web browser. This can be Firefox (the default when using a dev srobo server)
or any other browser Selenium can control.

Instructions are provided for Firefox & Chrome.

# Firefox on a dev srobo server

1. Install the dependencies with the `get-dependencies.sh` script.
2. Copy or link the `badger_firefox.py` file to `local_browser.py` in this folder.
3. Open two terminals.
4. In the first start a selenium server by running  `java -jar $the_selenium_jar`
5. Run the tests in the second (`python test_userman.py`).

# Chrome

1. Download the Chrome Driver, from https://sites.google.com/a/chromium.org/chromedriver/downloads,
   2.8 is current at the time of writing. If you put this next to the
   `chrome_browser.py` file, it should all just work.
2. Copy and edit the `chrome.tpl` file to `local.py` in this folder.

## Other

Other configurations are supported by creating custom `local_browser.py`
files, which must contain two functions `get_browser` and `end_browser` plus a
property '. These are extended by `test_helpers.py`, see there for more
about what's expected.
