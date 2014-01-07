wget -c http://selenium.googlecode.com/files/selenium-server-standalone-2.39.0.jar
yum groupinstall -y 'Fonts'
yum install -y 'firefox'
yum install -y xorg-x11-server-Xvfb
sudo easy_install pyvirtualdisplay
sudo easy_install selenium
