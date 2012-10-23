all:
	cd nemesis/ && ./make_db.sh
	cd test/ && ./all_tests.sh
