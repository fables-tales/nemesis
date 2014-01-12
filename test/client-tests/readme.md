#Nemesis selenium tests

These tests test the Javascript client portion of Nemesis, and run against
a real web browser. This can be Firefox (the default when using a dev srobo server)
or any other browser Selenium can control.

While some of the selenium drivers can run directly, it's better (and tends
to run faster) if you route then through a standalone selenium server.
At the time of writing the latest is [version 2.39.0](http://selenium.googlecode.com/files/selenium-server-standalone-2.39.0.jar).

The general process for running the tests then becomes:
1. Download the Selenium standalone server jar.
2. Start a selenium server (probably in its own terminal) by running
   `java -jar $the_selenium_jar`.
3. Create a suitable `local.py` in the same directory as this readme
   (see each browser's section for details on what this should be).
5. Run the tests via `python test_userman.py`.

## Firefox on a dev srobo server

Runs firefox in a virtual display in order to cope with the server being
headless.

1. Install the dependencies with the `get-dependencies.sh` script.
2. Copy or link the `badger_firefox.py` file to `local.py`.

## HTMLUnit

Uses HTMLUnit to run tests. This is generally the fastest, but isn't able
to cope with some of the jQuery handling -- YMMV.

2. Copy or link the `htmlunitwithjs_browser.py` file to `local.py`.

## Chrome

Runs Chrome either directly or via the server (the default as it's much
faster).

1. Download the Chrome Driver, from https://sites.google.com/a/chromium.org/chromedriver/downloads,
   2.8 is current at the time of writing.
   * If going via the server, the driver should be put next to the jar.
   * If using it directly, the driver should be put next to `local.py`.
2. Copy/edit/link the `chrome_browser.py` file to `local.py`.

## Other

Other configurations are supported by creating custom `local.py`
files, which must contain two functions `get_browser` and `end_browser` plus a
property '. These are extended by `test_helpers.py`, see there for more
about what's expected.
