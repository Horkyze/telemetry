INSTALL STEPS

1) install python 2.7 from https://www.python.org/downloads/release/python-279/
2) install MySQLdb (MySQL connector for python) from http://sourceforge.net/projects/mysql-python/
3) create desired database & run create_table.sql eighter from phpmyadmin or console 
4) edit config.py file to match db and server settings 
5) inside cmd run: python /path/to/server.py
6) server is now ready and waiting for connections :)

To test, if server is working properly, run client.py, which sends data every k seconds.
Watch database for changes.

FEATURES 

Recieved data (from tcp) is parsed as JSON object, pairs of "key": "value"
Database is checked is given columns (key) exists, if not they are created.
Data is inserted into table as "text" type.
Server replys "ok" to the client.

Client can close and re-establish connection without the need of server restart.



BUGS

When sever is restarted during transmition - client should re-establish connection, 
when using UDP there is not such problem. 
TCP MySQL timeout



