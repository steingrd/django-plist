
CC=gcc
CFLAGS=-Wall -framework Foundation -ObjC

test_dict: test_dict.m
	$(CC) $(CFLAGS) -o $@ $?
	
test: test_dict
	python make_test_fixtures.py
	./test_dict 
	
clean:
	rm -fr test_dict *.plist
