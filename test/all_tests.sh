cd ../nemesis
python app.py 1>/dev/null 2>/dev/null &
sleep 0.3
cd ../test
python -m unittest discover
killall python

