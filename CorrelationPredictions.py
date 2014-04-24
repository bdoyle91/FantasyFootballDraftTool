from __future__ import division
import StatCorrelations
import sqlite3 as lite

passingList = ["COMP", "ATT", "PCT", "YDS", "YDS_PER_A", "LONG", "TD", "INT", "SACK", "RATE", "YDS_PER_G"]
rushingList = ["ATT", "YDS", "YDS_PER_A", "LONG", "TWENTY_PLUS", "TD", "YDS_PER_G", "FUM", "FIRST_DOWNS"]
receivingList = ["REC", "TAR", "YDS", "AVG", "TD", "LONG", "TWENTY_PLUS", "YDS_PER_G", "FUM", "YAC", "FIRST_DOWNS"]
kickingList = ["FGM", "FGA", "FGPCT", "LNG", "XPM", "XPA", "PCT"]
LAST_SEASON = "2013"

listOfAllTables = ["Passing", "Rushing", "Receiving", "Defense", "Kicking"]

cDict = StatCorrelations.findAllAverages(StatCorrelations.ALL_LOTS)


def correlateStat(playerName, position):
	print "\n"
	conn = lite.connect('ESPN.db')
	conn.text_factory = str # set sqlite3 connection to use unicode instead of 8-bit byte strings. 
	with conn:
		c = conn.cursor()	# Defines cursor
		tableName1 = ""
		tableName2 = ""

		if position.strip() == "QB":
			tableName1 = "Passing"
			tableName2 = "Rushing"
			statList1 = passingList
			statList2 = rushingList
		elif position.strip() == "RB":
			tableName1 = "Rushing"
			tableName2 = "Receiving"
		elif position.strip() == "WR" or position.strip() == "TE":	
			tableName1 = "Receiving"
		else:
			tableName1 = "Kicking"


		commandString1 = "SELECT * FROM " + tableName1 + "_" + str(LAST_SEASON) + " WHERE PLAYER=\"" + playerName + "\";"
		commandString2 = "SELECT * FROM " + tableName2 + "_" + str(LAST_SEASON) + " WHERE PLAYER=\"" + playerName + "\";"
		stats1 = c.execute(commandString1)
		s1 = stats1.fetchone()
		# print "Stats1: " + str(s1) + "\n"
		stats2 = c.execute(commandString2)
		s2 = stats2.fetchone()
		# print "Stats2: " + str(s2)
		firstLen = len(s1)
		secondLen = len(s2)
		firstVal = firstLen - len(passingList)
		secondVal = secondLen - len(rushingList)

		list1 = list(s1)
		list2 = list(s2)
		applyMultiplier(firstVal, firstLen, position, tableName1, list1, statList1)
		# print "\n"
		applyMultiplier(secondVal, secondLen, position, tableName2, list2, statList2)
		# conn.commit() # MAY NOT NEED THIS
	conn.close()

def applyMultiplier(firstVal, length, position, tableName, inputList, statList):
	i = firstVal
	j = 0
	while i < length:
		# print "i: " + str(i)
		multiplier = cDict[str(position.strip()) + "-" + str(tableName) + "-" + str(statList[j])]
		# print "multiplier " + str(multiplier)
		# print "list1[i]: " + str(type(s1[i]))
		inputList[i] = float(inputList[i]) * multiplier
		# print "list1[i]: " + str(s1[i])
		i = i + 1
		j = j + 1
	# print inputList
	return inputList

def correlateAllPlayers():
	conn = lite.connect('ESPN.db')
	conn.text_factory = str # set sqlite3 connection to use unicode instead of 8-bit byte strings. 
	with conn:
		conn.row_factory = lite.Row
		c = conn.cursor()	# Defines cursor
		for table in listOfAllTables: #ALTER TABLE {tableName} ADD COLUMN COLNew {type};
			nameOfTable = str(table) + "_" + str(LAST_SEASON)
			commandString = "SELECT * FROM " + nameOfTable + ";"
			# print commandString
			c.execute(commandString)
			row = c.fetchone()
			# print "rowtype" + str(type(row))
			if "CORRELATION_FACTOR" not in row.keys():
				# print "IN CORRELATION_FACTOR IF STATEMENT"
				commandString = "ALTER TABLE " + nameOfTable + " ADD COLUMN CORRELATION_FACTOR INTEGER;"
				# print commandString
				c.execute(commandString)
			if table == "Passing":
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'QB';"
				# print commandString
				c.execute(commandString)
				# print c.fetchall()
				# r = c.fetchmany()
				# print type(r)
				# print r
				for r in c.fetchall():
					# r = c.fetchone()
					# print "r " + str(r)
					corrFactor = (float(r[7]) * cDict["QB-Passing-YDS"] + float(r[10]) * cDict["QB-Passing-TD"] + float(r[14]) * cDict["QB-Passing-YDS_PER_G"]) / 3
					# print str(corrFactor)
					commandString = "UPDATE " + nameOfTable + " SET CORRELATION_FACTOR = " + str(int(corrFactor)) + " WHERE PLAYER = '" + r[1] + "';"
					# print commandString
					c.execute(commandString)
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'QB';"
				# print commandString
				c.execute(commandString)
				totalCorr = 0.0
				# print c.fetchmany(15)
				for r in c.fetchmany(15):
					totalCorr = totalCorr + float(r[15])
				# print "totalCorr " + str(totalCorr)
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'QB';"
				# print commandString
				c.execute(commandString)
				avgCorr = totalCorr / 15
				# print "avgCorr: " + str(avgCorr)
				# print c.fetchall()
				for r in c.fetchall():
					# print "r15: " + str(r[15])
					# print "division: " + str(r[15]/avgCorr)
					commandString = "UPDATE " + nameOfTable + " SET CORRELATION_FACTOR = " + str(r[15]/avgCorr) + " WHERE PLAYER = '" + r[1] + "';"
					c.execute(commandString)

			elif table == "Rushing":
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'QB';"
				# print commandString
				c.execute(commandString)
				# print c.fetchall()
				# r = c.fetchmany()
				# print type(r)
				# print r
				for r in c.fetchall():
					# r = c.fetchone()
					# print "r " + str(r)
					corrFactor = (float(r[5]) * cDict["QB-Rushing-YDS"] + float(r[9]) * cDict["QB-Rushing-TD"]) / 2
					# print str(corrFactor)
					commandString = "UPDATE " + nameOfTable + " SET CORRELATION_FACTOR = " + str(int(corrFactor)) + " WHERE PLAYER = '" + r[1] + "';"
					# print commandString
					c.execute(commandString)
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'QB';"
				# print commandString
				c.execute(commandString)
				totalCorr = 0.0
				# print c.fetchmany(15)
				for r in c.fetchmany(15):
					totalCorr = totalCorr + float(r[13])
				# print "totalCorr " + str(totalCorr)
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'QB';"
				# print commandString
				c.execute(commandString)
				avgCorr = totalCorr / 15
				# print "avgCorr: " + str(avgCorr)
				# print c.fetchall()
				for r in c.fetchall():
					# print "r13: " + str(r[13])
					# print "division: " + str(r[13]/avgCorr)
					commandString = "UPDATE " + nameOfTable + " SET CORRELATION_FACTOR = " + str(r[13]/avgCorr) + " WHERE PLAYER = '" + r[1] + "';"
					c.execute(commandString)

				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'RB';"
				# print commandString
				c.execute(commandString)
				# print c.fetchall()
				# r = c.fetchmany()
				# print type(r)
				# print r
				for r in c.fetchall():
					# r = c.fetchone()
					# print "r " + str(r)
					# ('RB-Rushing-ATT', 0.4092034359509148)
					corrFactor = (float(r[5]) * cDict["RB-Rushing-YDS"] + float(r[9]) * cDict["RB-Rushing-TD"] + float(r[12]) * cDict["RB-Rushing-FIRST_DOWNS"] + float(r[10]) * cDict["RB-Rushing-YDS_PER_G"] + float(r[8]) * cDict["RB-Rushing-TWENTY_PLUS"] + float(r[4]) * cDict["RB-Rushing-ATT"]) / 6
					# print str(corrFactor)
					commandString = "UPDATE " + nameOfTable + " SET CORRELATION_FACTOR = " + str(int(corrFactor)) + " WHERE PLAYER = '" + r[1] + "';"
					# print commandString
					c.execute(commandString)
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'RB';"
				# print commandString
				c.execute(commandString)
				totalCorr = 0.0
				# print c.fetchmany(15)
				for r in c.fetchmany(50):
					totalCorr = totalCorr + float(r[13])
				# print "totalCorr " + str(totalCorr)
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'RB';"
				# print commandString
				c.execute(commandString)
				avgCorr = totalCorr / 50
				# print "avgCorr: " + str(avgCorr)
				# print c.fetchall()
				for r in c.fetchall():
					# print "r13: " + str(r[13])
					# print "division: " + str(r[13]/avgCorr)
					commandString = "UPDATE " + nameOfTable + " SET CORRELATION_FACTOR = " + str(r[13]/avgCorr) + " WHERE PLAYER = '" + r[1] + "';"
					c.execute(commandString)

			elif table == "Receiving":
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'WR';"
				# print commandString
				c.execute(commandString)
				# print c.fetchall()
				# r = c.fetchmany()
				# print type(r)
				# print r
				for r in c.fetchall():
					# r = c.fetchone()
					# print "r " + str(r)
					corrFactor = (float(r[6]) * cDict["WR-Receiving-YDS"] + float(r[14]) * cDict["WR-Receiving-FIRST_DOWNS"] + float(r[11]) * cDict["WR-Receiving-YDS_PER_G"] + float(r[4]) * cDict["WR-Receiving-REC"] + float(r[10]) * cDict["WR-Receiving-TWENTY_PLUS"] + float(r[8]) * cDict["WR-Receiving-TD"] + float(r[5]) * cDict["WR-Receiving-TAR"]) / 7
					# print str(corrFactor)
					commandString = "UPDATE " + nameOfTable + " SET CORRELATION_FACTOR = " + str(int(corrFactor)) + " WHERE PLAYER = '" + r[1] + "';"
					# print commandString
					c.execute(commandString)
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'WR';"
				# print commandString
				c.execute(commandString)
				totalCorr = 0.0
				# print c.fetchmany(15)
				for r in c.fetchmany(50):
					totalCorr = totalCorr + float(r[15])
				# print "totalCorr " + str(totalCorr)
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'WR';"
				# print commandString
				c.execute(commandString)
				avgCorr = totalCorr / 50
				# print "avgCorr: " + str(avgCorr)
				# print c.fetchall()
				for r in c.fetchall():
					# print "r15: " + str(r[15])
					# print "division: " + str(r[15]/avgCorr)
					commandString = "UPDATE " + nameOfTable + " SET CORRELATION_FACTOR = " + str(r[15]/avgCorr) + " WHERE PLAYER = '" + r[1] + "';"
					c.execute(commandString)

				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'RB';"
				# print commandString
				c.execute(commandString)
				# print c.fetchall()
				# r = c.fetchmany()
				# print type(r)
				# print r
				for r in c.fetchall():
					# r = c.fetchone()
					# print "r " + str(r)
					# ('RB-Receiving-YDS_PER_G', 0.2892476791408025)
					corrFactor = (float(r[4]) * cDict["RB-Receiving-REC"] + float(r[14]) * cDict["RB-Receiving-FIRST_DOWNS"] + float(r[6]) * cDict["RB-Receiving-YDS"] + float(r[5]) * cDict["RB-Receiving-TAR"] + float(r[11]) * cDict["RB-Receiving-YDS_PER_G"]) / 5
					# print str(corrFactor)
					commandString = "UPDATE " + nameOfTable + " SET CORRELATION_FACTOR = " + str(int(corrFactor)) + " WHERE PLAYER = '" + r[1] + "';"
					# print commandString
					c.execute(commandString)
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'RB';"
				# print commandString
				c.execute(commandString)
				totalCorr = 0.0
				# print c.fetchmany(15)
				for r in c.fetchmany(50):
					totalCorr = totalCorr + float(r[15])
				# print "totalCorr " + str(totalCorr)
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'RB';"
				# print commandString
				c.execute(commandString)
				avgCorr = totalCorr / 50
				# print "avgCorr: " + str(avgCorr)
				# print c.fetchall()
				for r in c.fetchall():
					# print "r15: " + str(r[15])
					# print "division: " + str(r[15]/avgCorr)
					commandString = "UPDATE " + nameOfTable + " SET CORRELATION_FACTOR = " + str(r[15]/avgCorr) + " WHERE PLAYER = '" + r[1] + "';"
					c.execute(commandString)

				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'TE';"
				# print commandString
				c.execute(commandString)
				# print c.fetchall()
				# r = c.fetchmany()
				# print type(r)
				# print r
				for r in c.fetchall():
					# r = c.fetchone()
					# print "r " + str(r)
					# ('TE-Receiving-TD', 0.4086663336663337)
					corrFactor = (float(r[6]) * cDict["TE-Receiving-YDS"] + float(r[14]) * cDict["TE-Receiving-FIRST_DOWNS"] + float(r[11]) * cDict["TE-Receiving-YDS_PER_G"] + float(r[10]) * cDict["TE-Receiving-TWENTY_PLUS"] + float(r[4]) * cDict["TE-Receiving-REC"] + float(r[8]) * cDict["TE-Receiving-TD"]) / 6
					# print str(corrFactor)
					commandString = "UPDATE " + nameOfTable + " SET CORRELATION_FACTOR = " + str(int(corrFactor)) + " WHERE PLAYER = '" + r[1] + "';"
					# print commandString
					c.execute(commandString)
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'TE';"
				# print commandString
				c.execute(commandString)
				totalCorr = 0.0
				# print c.fetchmany(15)
				for r in c.fetchmany(15):
					totalCorr = totalCorr + float(r[15])
				# print "totalCorr " + str(totalCorr)
				commandString = "SELECT * FROM " + nameOfTable + " WHERE POS = 'TE';"
				# print commandString
				c.execute(commandString)
				avgCorr = totalCorr / 15
				# print "avgCorr: " + str(avgCorr)
				# print c.fetchall()
				for r in c.fetchall():
					# print "r15: " + str(r[15])
					# print "division: " + str(r[15]/avgCorr)
					commandString = "UPDATE " + nameOfTable + " SET CORRELATION_FACTOR = " + str(r[15]/avgCorr) + " WHERE PLAYER = '" + r[1] + "';"
					c.execute(commandString)
		conn.commit()			
	conn.close()		


correlateAllPlayers()
# correlateStat("Peyton Manning", " QB")
