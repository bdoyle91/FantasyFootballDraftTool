import teamClass
import sqlite3 as lite

# Maximum Number of players from each position allowed on a roster
MAX_QBS_PER_TEAM = 4
MAX_RBS_PER_TEAM = 8
MAX_WRS_PER_TEAM = 8
MAX_TES_PER_TEAM = 3
MAX_DSTS_PER_TEAM = 3
MAX_KS_PER_TEAM = 3

TEAM_SIZE = 16

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
# Returns:		Select Command info
#
##########################################################################################
	def CALL_SQL_UPDATE(self, database, columns, value, table, clauses=""):
		command = "UPDATE " + table + " SET "  + columns + " = \'" + value + "\' " + clauses
		self.EXECUTE_SQL_COMMAND(database, command)
		self.conn.close()



