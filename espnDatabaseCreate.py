import scrapingFunctions

#Gather Passing Information
Passing_Page = "http://espn.go.com/nfl/statistics/player/_/stat/passing/sort/passingYards/seasontype/2/qualified/false/count/"
Passers = scrapingFunctions.getAllPages(Passing_Page)
print('-------------- PASSERS --------------------')
print(Passers)

Rushing_Page = "http://espn.go.com/nfl/statistics/player/_/stat/rushing/seasontype/2/qualified/false/count/"
Rushers = scrapingFunctions.getAllPages(Rushing_Page)
print('\n\n\n\n-------------- RUSHERS --------------------')
print(Rushers)


Receiving_Page = "http://espn.go.com/nfl/statistics/player/_/stat/receiving/seasontype/2/qualified/false/count/"
Receivers = scrapingFunctions.getAllPages(Receiving_Page)
print('\n\n\n\n-------------- RECEIVERS --------------------')
print(Receivers)

# MiscScoring_Page = "http://espn.go.com/nfl/statistics/player/_/stat/scoring/seasontype/2/qualified/false/count/"
# MiscScorers = scrapingFunctions.getAllPages(MiscScoring_Page,"MiscScorers")
# print('\n\n\n\n-------------- MISC SCORING --------------------')
# print(MiscScorers)
