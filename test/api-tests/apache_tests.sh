service httpd restart
sleep 1
touch .apachetest
python -m unittest discover
rm .apachetest
