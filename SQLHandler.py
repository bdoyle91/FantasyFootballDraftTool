import sqlite3 as lite

##########################################################################################
#
# CLASS: SQL_HANDLER
#
# Members: 		conn - connection string
#				cursor - SQL cursor
#
#
##########################################################################################

class SQL_HANDLER:
	def __init__(self):
		self.conn = []
		self.cursor = []

##########################################################################################
#
# CLASS_FUNCTION: EXECUTE_SQL_COMMAND
#		
# ARGS:			Database Name, Command String
# Returns:		None
#
##########################################################################################

	def EXECUTE_SQL_COMMAND(self, database, command):
		self.conn = lite.connect(database)
		self.cursor = self.conn.cursor()
		self.cursor.execute(command)
		self.conn.commit()

##########################################################################################
#
# CLASS_FUNCTION: CALL_SQL_SELECT
#		
# ARGS:			Database Name, Columns in comma separated format, table name, any and all
#				where, orderby, etc clauses 
# Returns:		Select Command info
#
##########################################################################################
	def CALL_SQL_SELECT(self, database, columns, table, clauses=""):
		command = "SELECT " + columns + " FROM "  + table + " " + clauses
		self.EXECUTE_SQL_COMMAND(database, command)
		info = self.cursor.fetchall()		
		self.conn.close()
		return info

##########################################################################################
#
# CLASS_FUNCTION: CALL_SQL_UPDATE
#		
# ARGS:			Database Name, Columns in comma separated format, value to set, 
#				table name, any and all, where, orderby, etc clauses 
# Returns:		Returns SUCCESS or FAIL
#
##########################################################################################
	def CALL_SQL_UPDATE(self, database, columns, value, table, whereColumn=False, whereValue=False):
		if whereColumn==False:
			command = "UPDATE " + table + " SET "  + columns + " = \'" + value + "\' "
		else: 
			command = "UPDATE " + table + " SET "  + columns + " = \'" + value + "\' WHERE " + whereColumn + "= \'" + whereValue + "\'"
		self.EXECUTE_SQL_COMMAND(database, command)
		self.conn.close()
		return 1



