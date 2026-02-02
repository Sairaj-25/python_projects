import csv

#Toss Winning Stats

def toss_Win(team):
    total =0
    tosswon =0
    listToss=[]
    with open(r'.\matches.csv') as csvfile:
        allDataFile = csv.DictReader(csvfile)
        for data in allDataFile:
              if team in [data['TEAM1'],data['TEAM2']]:
                  total+=1
                  if data['TOSS_WINNER']==team:
                      tosswon+=1
        listToss.append(total)
        listToss.append(tosswon)
    return listToss
    

#Yearwise matches played/won
def yearwise_Wonplayed(team):
    
    listResult=list()
    listYear = getYears()
    for year in listYear:
        with open(r'.\matches.csv') as csvfile:
            allDataFile = csv.DictReader(csvfile)
            total =0
            won=0
            
            for data in allDataFile:
                if (team in [data['TEAM1'],data['TEAM2']]) and  data['SEASON'] == year:
                    total+=1
                    if data['WINNER'] == team:
                        won+=1
            
            listResult.append([year,total,won])
    return listResult
    
#Citywise Matches played/won
def locationwise_Wonplayed(team):
    listResult=list()
    listCity = getCities()
    for city in listCity:
        with open(r'.\matches.csv') as csvfile:
            allDataFile = csv.DictReader(csvfile)
            total =0
            won=0
            
            for data in allDataFile:
                if (team in [data['TEAM1'],data['TEAM2']]) and  data['CITY'] == city:
                    total+=1
                    if data['WINNER'] == team:
                        won+=1
            
            listResult.append([city,total,won])
    return listResult

def getYears():
    listSeason = set()
    with open(r'.\matches.csv') as csvfile:
        allDataFile = csv.DictReader(csvfile)
        for data in allDataFile:
            listSeason.add(data['SEASON'])
    return list(listSeason)

def getCities():
    listCity = set()
    with open(r'.\matches.csv') as csvfile:
        allDataFile = csv.DictReader(csvfile)
        for data in allDataFile:
            listCity.add(data['CITY'])
    return list(listCity)

def readCSVFile():
    print 'in readCSV'
    with open(r'.\matches.csv') as csvfile:
        allDataFile = csv.DictReader(csvfile)
    return allDataFile

def showTeams():
    print '====TEAM===='
    listTeam = ['Mumbai Indians','Chennai Super Kings','Kolkata Knight Riders','Delhi Daredevils','Gujarat Lions','Sunrisers Hyderabad','Kings XI Punjab','Royal Challengers Bangalore','Rajasthan Royals','Rising Pune Supergiants']
    dictTeam = dict(enumerate(listTeam,1))
    value = True
    while value:
        printTeam(dictTeam)
        team=input('Enter a Team: ')
        validTeam = isValidTeam(team,dictTeam)
        if validTeam:
            value = False
        else:
            print 'Invalid Team Choice'
    return dictTeam[team]



def printTeam(dictTeam):
    for keys,Teams in dictTeam.items():
        print "%s. %s"%(keys,Teams)

def isValidTeam(team,dictTeam):
    if team in dictTeam.keys():
        return True
    else:
        return False

