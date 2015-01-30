import socket
import sys
import MySQLdb
import json
import config

def log( msg ):
   print msg
   return

log("Connecting to MySQL...")
db = MySQLdb.connect(host=config.c['host'], user=config.c['user'], passwd=config.c['password'], db=config.c['db']) 
db.autocommit(True)
cur = db.cursor() 

# checks if given column exists, if not, it is created 
def check_and_create_column(column):
	query = "SHOW COLUMNS FROM " + config.c['table'] + " LIKE '" + column + "'"
	cur.execute(query)
	if cur.rowcount == 0:
		log("Column '" + column + "' doesnt exist, creating...")
		cur.execute("ALTER TABLE " + config.c['table'] + " ADD " + column + " text")

	return


def process_data(packet_data):

	try:
		data_json = json.loads(packet_data)
	except ValueError:
		print "Invalid json object!!"
		return

	query = "INSERT INTO " + config.c['table'] + "("

	for key in data_json:
		check_and_create_column(key)
		query = query + MySQLdb.escape_string(key) + ", "

	query = query[:-2]
	query = query + ") VALUES ("

	for key in data_json:
		query = query + "\"" + MySQLdb.escape_string(data_json[key]) + "\", "

	query = query[:-2]
	query = query + ");"

	log(query)
	cur.execute(query)


# INSERT INTO table_name (column1, column2, column3,...)
# VALUES (value1, value2, value3,...)



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (config.c['server_addr'], config.c['server_port'])
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            log('data recieved, processing...')
            process_data(data)
            if data:
                connection.send("ok")
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()