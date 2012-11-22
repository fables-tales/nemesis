source ../../venv/bin/activate
python ../../nemesis/app.py 1>/dev/null 2>/dev/null &
sleep 0.4
python -m unittest discover
killall python

