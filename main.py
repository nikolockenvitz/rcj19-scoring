"""
This script calculates points for RCJ Line and will output
standings afterward.

Input are two semicolon-separated CSV files (so they can be
edited in Excel as well) which contain all runs (one file
for Line and one for Line Entry).

After calculating points for each run, total score for each
team will be calculated (e.g. best 2 of 3 runs). Teams will
be ordered by points and time.

Standings are written to semicolon-separated CSV files, one
file for Line and one for Line Entry. Additionally the
result is written into one HTML document.

Format of files:
Input (Column-Id, description):
 0 Run#
 1 Teamname
 2 Time (mm:ss)
 3 not started? (empty cell means started, everything else not started)
 4 Gaps
 5 Obstacles
 6 Bumper
 7 Ramps
 8 Intersections
 9 Victims alive
10 Victims dead after all alive victims are rescued
11 Victims dead before all alive victime are rescued
12 Evacuation tile (high/low)
13 LOPs in evacuation zone
14 Line found and followed till third tile after evacuation zone (empty means no)
15 Tiles Section 1
16 Tiles Section 2
17 Tiles Section 3
18 Tiles Section 4
19 Tiles Section 5
20 Tiles Section 6
21 Tiles Section 7
22 Tiles Section 8
23 Attempts Section 1
24 Attempts Section 2
25 Attempts Section 3
26 Attempts Section 4
27 Attempts Section 5
28 Attempts Section 6
29 Attempts Section 7
30 Attempts Section 8

Output (Column-Id, description):
 0 Position
 1 Teamname
 2 Total Score
 3 Total Time
 4 -
 5 Score Run 1
 6 Time Run 1
 7 Score Run 2
 8 Time Run 2
 9 Score Run 3
10 Time Run 3

"""

import sys
from runParser import Run, convSec2Time
from html import HTMLOutput

FILENAMES = [["iRuns.csv",      "oResult.csv"],
             ["iRunsEntry.csv", "oResultEntry.csv"]]

oHTMLOutput = HTMLOutput()

for file in FILENAMES:
    # read runs from file
    try:
        f = open(file[0], "r")
        aLines = f.readlines()
        f.close()
    except FileNotFoundError:
        print("*** Couldn't find '{}'. Make sure file exists.".format(file[0]))
        continue

    # dictionary to store runs for each team
    # key: teamname, value: [run1, run2, run3]
    dTeams = {}

    # parse values and calculate points for each run
    for sLine in aLines[1:]: # skip headline
        if(sLine.strip() == "" or
           sLine.strip() == ";"*(len(sLine.strip()))):
            continue
        oRun = Run().parse(sLine).calculate()
        if(oRun.sTeamname in dTeams):
            # add run to already existing runs of this team
            dTeams[oRun.sTeamname].append(oRun)
        else:
            # insert new entry to dictionary
            dTeams[oRun.sTeamname] = [oRun]

    # calculate total score and total time for each team (e.g. best 2 of 3)
    # insert into sorted list aStandings (ordered by score desc, time asc)
    # element in aStandings: [teamname, score, time, run1, run2, run3]
    aStandings = []
    for sTeamname, aRuns in dTeams.items():
        # init entry which will be inserted into aStandings
        aTeam = [sTeamname, 0, 0] + aRuns

        # sort aRuns
        # TODO: improve to O(n*log_n)
        aConsideredRuns = []
        for oRun in aRuns:
            bInserted = False
            for i in range(len(aConsideredRuns)):
                if(oRun.iScore > aConsideredRuns[i].iScore or
                   (oRun.iScore == aConsideredRuns[i].iScore and
                    oRun.iTime  <  aConsideredRuns[i].iTime)):
                    aConsideredRuns = aConsideredRuns[:i] + [oRun] + aConsideredRuns[i:]
                    bInserted = True
                    break
            if(not bInserted):
                aConsideredRuns.append(oRun)

        # consider only best 2 runs
        aConsideredRuns = aConsideredRuns[:2]

        # total score and time
        for oRun in aConsideredRuns:
            aTeam[1] += oRun.iScore
            aTeam[2] += oRun.iTime

        # insert into aStandings
        # TODO: currently O(n^2), improve to O(n*log_n), tree-like
        bInserted = False
        for i in range(len(aStandings)):
            if(aTeam[1] > aStandings[i][1] or
               (aTeam[1] == aStandings[i][1] and
                aTeam[2] <  aStandings[i][2])):
                # insert before
                aStandings = aStandings[:i] + [aTeam] + aStandings[i:]
                bInserted = True
                break
        if(not bInserted):
            aStandings.append(aTeam)

    # prepare output
    aOutput = []

    iPosition  = 0
    iDiff      = 1
    iLastScore = None
    iLastTime  = None
    for aTeam in aStandings:
        if(aTeam[1] != iLastScore or aTeam[2] != iLastTime):
            iLastScore = aTeam[1]
            iLastTime  = aTeam[2]
            iPosition += iDiff
            iDiff      = 1
        else:
            iDiff += 1

        aScoresAndTimes = ["-","-","-","-","-","-"]
        for oRun in aTeam[3:6]:
            if(oRun.iRun < 1 or oRun.iRun > 3 or
                aScoresAndTimes[(oRun.iRun-1)*2] != "-"):
                print("*** Error: Invalid run-id {} for team '{}'".format(oRun.iRun, oRun.sTeamname))
                continue
            aScoresAndTimes[(oRun.iRun-1)*2]   = oRun.iScore
            aScoresAndTimes[(oRun.iRun-1)*2+1] = convSec2Time(oRun.iTime)

        aOutput.append([iPosition, aTeam[0], aTeam[1], convSec2Time(aTeam[2]),
                        aScoresAndTimes[0], aScoresAndTimes[1],
                        aScoresAndTimes[2], aScoresAndTimes[3],
                        aScoresAndTimes[4], aScoresAndTimes[5]])

    # prepare HTML output
    oHTMLOutput.addStanding("Rescue Line" + (" Entry" if "entry" in file[0].lower() else ""),
                            aOutput)

    # write standings to CSV-file
    try:
        f = open(file[1], "w")

        sLineTemplate = "{};\"{}\";{};{};;{};{};{};{};{};{}\n"
        f.write(sLineTemplate.format("#","Team","Punktzahl","Zeit","Lauf 1","","Lauf 2","","Lauf 3",""))
        for aLine in aOutput:
            f.write(sLineTemplate.format(*aLine))
        f.close()
        print("Successfully wrote to '{}'.".format(file[1]))
    except PermissionError:
        print("*** Couldn't write to '{}'. Is it opened in another program?".format(file[1]))

    print("")

# write standings to HTML-document
oHTMLOutput.output()

# if program is executed in cmd, prevent closing
if("idlelib" not in sys.modules): input("")
