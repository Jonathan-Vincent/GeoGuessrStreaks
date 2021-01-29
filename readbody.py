#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import csv

#Setup names of files
gamelist=[]
month = 'D'
for i in range(1,10):
    for j in range(1,6):
        gamelist.append(month+'S'+str(i)+'-'+str(j)+'.txt')
month = 'J'
for i in range(1,5):
    for j in range(1,6):
        gamelist.append(month+'S'+str(i)+'-'+str(j)+'.txt')


attemptdict = defaultdict(lambda:0)
successdict = defaultdict(lambda:0)
locationsdict = defaultdict(lambda:0)
playerdict = defaultdict(lambda:0)
playersucc = defaultdict(lambda:[0,0])
orderdict = defaultdict(lambda:[])
#Iterate through html files and extract guesses
for gamefile in gamelist:
    with open(gamefile,'r') as f:
        body = f.read()
    
    body = body[body.find('grid grid--gutter'):body.find('<aside class=')]
    streaklist = body.split('</div><div class=\"results-highscore__guess')[:-1]
    
    playerlist = body.split('class="results-highscore__player-nick">')[1:]
    
    plist = []
    for p in playerlist:
        player = p[:p.find('<')]
        playerdict[player] += 1
        plist.append(player)
    

    streaks = []
    for i in streaklist:
        num=i[i.rfind('>')+1:i.rfind(' ')]
        streaks.append(int(num))

    countries = []
    countrylist = body.split('></div></div><div class="country-list__name-column">')[1:]
    for j,i in enumerate(countrylist):
        country = i[:i.find('<')]
        countries.append(country)
        locationsdict[country] += 1
        orderdict[country] = orderdict[country] + [j]
    
    
    for j,streaklength in enumerate(streaks):
        player = plist[j]
        playersucc[player] = [sum(x) for x in zip(playersucc[player], [streaklength,streaklength+1])]
        if streaklength == 0:
            country = countries[0]
            attemptdict[country] += 1
        else:
            for i in range(streaklength):
                country = countries[i]
                successdict[country] += 1
                attemptdict[country] += 1
                
            i+=1
            country = countries[i]
            attemptdict[country] += 1
        
        
data =[]

playeraccs = []

for player in playersucc.keys():
    succs,atts = playersucc[player]
    acc = succs/atts
    playeraccs += [[player,acc,succs,atts]]
    
playeraccs = sorted(playeraccs, key=lambda x: x[1])

tophalf = [i[0] for i in playeraccs[int(len(playeraccs)/2):]]
topdecile = [i[0] for i in playeraccs[int(9*len(playeraccs)/10):]]


tophalfattempt = defaultdict(lambda:0)
tophalfsuccess = defaultdict(lambda:0)
topdecileattempt = defaultdict(lambda:0)
topdecilesuccess = defaultdict(lambda:0)


#Work out overall accuracies for the top half and the top decile
for gamefile in gamelist:
    with open(gamefile,'r') as f:
        body = f.read()
    
    body = body[body.find('grid grid--gutter'):body.find('<aside class=')]
    streaklist = body.split('</div><div class=\"results-highscore__guess')[:-1]
    playerlist = body.split('class="results-highscore__player-nick">')[1:]
    
    plist = []
    for p in playerlist:
        player = p[:p.find('<')]
        plist.append(player)
    

    streaks = []
    for i in streaklist:
        num=i[i.rfind('>')+1:i.rfind(' ')]
        streaks.append(int(num))

    countries = []
    countrylist = body.split('></div></div><div class="country-list__name-column">')[1:]
    for j,i in enumerate(countrylist):
        country = i[:i.find('<')]
        countries.append(country)
        
    if 'Montenegro' in countries:
        print(gamefile)
     
    for i,streaklength in enumerate(streaks):
        player = plist[i]
        if player in tophalf:
            if streaklength == 0:
                country = countries[0]
                tophalfattempt[country] += 1
            else:
                for i in range(streaklength):
                    country = countries[i]
                    tophalfsuccess[country] += 1
                    tophalfattempt[country] += 1
                
                i+=1
                country = countries[i]
                tophalfattempt[country] += 1
                
        if player in topdecile:
            if streaklength == 0:
                country = countries[0]
                topdecileattempt[country] += 1
            else:
                for i in range(streaklength):
                    country = countries[i]
                    topdecilesuccess[country] += 1
                    topdecileattempt[country] += 1
                
                i+=1
                country = countries[i]
                topdecileattempt[country] += 1

#assemble data in order to output to CSV

for country in attemptdict.keys():
    attempts = attemptdict[country]
    successes = successdict[country]
    
    
    thattempts = tophalfattempt[country]
    thsuccesses = tophalfsuccess[country]
    
    
    tdattempts = topdecileattempt[country]
    tdsuccesses = topdecilesuccess[country]
    
    thrate = thsuccesses/thattempts
    tdrate = tdsuccesses/tdattempts

    locations = locationsdict[country]
    order = orderdict[country]
    
    srate = successes/attempts

    data.append([country, attempts, successes, srate, locations])


data = sorted(data, key=lambda x: x[3])

#uncomment to save data to CSV file
'''
data = [['country', 'attempts', 'successes', 'srate', 'locations']] + data
for row in data:
    print(row)
with open("GeoData.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)'''