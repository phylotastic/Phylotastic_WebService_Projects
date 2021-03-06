import mysql.connector
from mysql.connector import errorcode

import credentials #for database credentials


class DatabaseAPI(object):
	"""
	Class to connect, insert, update and query the database
	"""
	def __init__(self, db_name):
		"""
		Initiates a database connection
		"""
		db_user = credentials.mysql['user']
		db_pass = credentials.mysql['password']

		self.mysql_conn = None
        # Create the database connection
		try:
			cnx = mysql.connector.connect(user=db_user, password=db_pass, database=db_name)
			self.mysql_conn = cnx
			#print "Database connected"
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with the user name or password")
				cnx.close()
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
				cnx.close()
			else:
				print(err)
				cnx.close()
		

	#-----------------------------------------------
	def prepare_insert_statement(self, table_name, table_fields):
		"""
		Prepares insertion statement
		"""
		stmt_1 = "INSERT INTO " + table_name + " ("
		stmt_2 = ""
		stmt_3 = " VALUES ("

		for indx, field in enumerate(table_fields):
			stmt_2 = stmt_2 + field
			stmt_3 = stmt_3 + "%s"			
			if indx != len(table_fields)-1:
				stmt_2 = stmt_2 + ","
				stmt_3 = stmt_3 + ","				
		stmt_2 = stmt_2+ ")"
		stmt_3 = stmt_3+ ")"

		insert_stmt = stmt_1 + stmt_2 + stmt_3
		#print insert_stmt
		return insert_stmt

	#---------------------------------------------
	def insert_db_multiple(self, table_name, table_fields, table_rows):
		"""
		Inserts multile rows into the database
		"""
		cursor = self.mysql_conn.cursor()
		insert_stmt = ( self.prepare_insert_statement(table_name, table_fields) )
        
		for row in table_rows:
			# Insert new row
			cursor.execute(insert_stmt, row)
	
		# Make sure data is committed to the database
		self.mysql_conn.commit()
		cursor.close()
		self.mysql_conn.close()

	#--------------------------------------------
	def insert_db_single(self, table_name, table_fields, table_row):
		"""
		Inserts a single row into the database and returns the last inserted id
		"""
		cursor = self.mysql_conn.cursor()
		insert_stmt = ( self.prepare_insert_statement(table_name, table_fields) )
        
		# Insert new row
		cursor.execute(insert_stmt, table_row)
		last_id = cursor.lastrowid

	
		# Make sure data is committed to the database
		self.mysql_conn.commit()
		cursor.close()
		self.mysql_conn.close()

		return last_id
	
	#---------------------------------------------------
	def prepare_query_statement(self, table_name, table_fields, condition=None, extra_stmt=None):
		"""
		Prepares query statement
		"""
		stmt_1 = "SELECT " 
		stmt_2 = " FROM " + table_name
		if condition is not None:
			stmt_3 = " WHERE " + condition
		else:
			stmt_3 = ""

		for indx, field in enumerate(table_fields):
			stmt_1 = stmt_1 + field
			if indx != len(table_fields)-1:
				stmt_1 = stmt_1 + ","
				
		query_stmt = stmt_1 + stmt_2 + stmt_3

		if extra_stmt is not None:
			query_stmt = query_stmt + " " + extra_stmt
		
		#print query_stmt
		return query_stmt

	#----------------------------------------------
	def query_db(self, table_name, table_fields, condition=None, condition_values=None, extra=None):
		"""
		Makes query into the database
		:param condition_values: values related to the condition 
    	:type condition_values: tuple.

		"""
		cursor = self.mysql_conn.cursor(buffered=True)
		query_stmt = ( self.prepare_query_statement(table_name, table_fields, condition, extra) )
		
		if condition_values is None:
			cursor.execute(query_stmt)
		else:
			cursor.execute(query_stmt, condition_values)

		query_result = []
		
		#for field1, field2, ... in cursor 
		for row in cursor:
			query_result.append(row)
		#return a list of lists(rows)
		
		
		cursor.close()
		self.mysql_conn.close()

		return query_result

	#-----------------------------------------------
	def prepare_update_statement(self, table_name, table_fields, condition):
		"""
		Prepares update statement
		"""
		stmt_1 = "UPDATE " + table_name + " SET "
		stmt_2 = ""
		stmt_3 = " WHERE " + condition

		for indx, field in enumerate(table_fields):
			stmt_2 = stmt_2 + field + " = %s"
						
			if indx != len(table_fields)-1:
				stmt_2 = stmt_2 + ","
								
		update_stmt = stmt_1 + stmt_2 + stmt_3
		#print update_stmt
		return update_stmt

	#---------------------------------------------
	def update_db_single(self, table_name, table_fields, field_values, condition):
		"""
		Update multile rows into the database
		"""
		cursor = self.mysql_conn.cursor()
		update_stmt = ( self.prepare_update_statement(table_name, table_fields, condition) )
        
		cursor.execute(update_stmt, field_values)
	
		# Make sure data is committed to the database
		self.mysql_conn.commit()
		cursor.close()
		self.mysql_conn.close()

