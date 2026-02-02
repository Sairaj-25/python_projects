from builtins import list

import matchStats
while True:
    print('===Statistics===')
    print('1. Toss Winning Stats')
    print('2. Yearwise matches played/won')
    print('3. Citywise Matches played/won')
    print('4. Exit')
    choice = int(input('Enter a choice: '))

    if choice == 1:
        team = matchStats.showTeams()
        listToss = matchStats.tossWin(team)
        print(team)
        print("Total Matches played:",listToss[0])
        print("No of times toss won:",listToss[1])
        print("Toss winning percentage is", round(float(listToss[1] / listToss[0]*100), 2))

    if choice == 2:
        team = matchStats.showTeams()
        dictYearWise = matchStats.yearWise_WonPlayed(team)
        print('*' * 60)
        print(team)
        print(' ' * 3, "YEAR", ' ' * 7, "MATCHES PLAYED", ' ' * 7, "MATCHES WON")
        for keys in dictYearWise:
            print(' '*3,keys,' '*12,dictYearWise[keys]["Total"],' '*18,dictYearWise[keys]["Won"])
        print("*"*60)

    if choice == 3:
        team = matchStats.showTeams()
        dictLocation = matchStats.locationWise(team)
        print('*' * 60)
        print(team)
        print(' ' * 10, "CITY", ' ' * 7, "MATCHES PLAYED", ' ' * 7, "MATCHES WON")
        for keys in dictLocation:
            print("{:>16}  {:>12}{:02d}  {:>17}{:02d} ".format(keys,'',dictLocation[keys]["total"],'',dictLocation[keys]["won"]))
        print("*" * 60)

    if choice == 4:
        break