"""
This script calculates points for RCJ Line and will output
standings afterward.

Input are two semicolon-separated CSV files (so they can be
edited in Excel as well) which contain all runs (one file
for Line and one for Line Enty).

After calculating points for each run, total score for each
team will be calculated (e.g. best 2 of 3 runs). Teams will
be ordered by points and time.

Standings are written to semicolon-separated CSV files, one
file for Line and one for Line Entry

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

"""

import sys
from runParser import Run

FILENAMES = [["iRuns.csv",      "oResult.csv"]]#,
             #["iRunsEntry.csv", "oResultEntry.csv"]]

for file in FILENAMES:
    # read runs from file
    try:
        f = open(file[0], "r")
        aLines = f.readlines()
        f.close()
    except FileNotFoundError:
        print("*** Couldn't find '{}'. Make sure file exists.".format(file[0]))
        continue

    # parse values and calculate points for each run
    aRuns = []
    for sLine in aLines[1:]: # skip headline
        aRuns.append(Run().parse(sLine).calculate())

    # group runs by team and additional rule (e.g. best 2 of 3)

    # sort standings (score descending, time ascending)

    # write standings to file
    try:
        f = open(file[1], "w")
        f.write("#;Team;Punktzahl;Zeit\n")
        for oRun in aRuns:
            f.write("{};\"{}\";{};{}\n".format(oRun.iRun,
                                               oRun.sTeamname,
                                               oRun.score,
                                               oRun.iTime))
        f.close()
        print("Successfully wrote to '{}'.".format(file[1]))
    except PermissionError:
        print("*** Couldn't write to '{}'. Is it opened in another program?".format(file[1]))
        continue

# if program is executed in cmd, prevent closing
if("idlelib" not in sys.modules): input("")
