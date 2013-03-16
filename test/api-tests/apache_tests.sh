service httpd restart
sleep 1
touch .apachetest
nosetests
rm .apachetest
