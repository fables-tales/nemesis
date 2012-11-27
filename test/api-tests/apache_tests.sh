service httpd restart
touch .apachetest
python -m unittest discover
rm .apachetest
