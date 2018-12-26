"""
Semicolon separated values
(if a cell contains a semicolon the cell-value is in quotes)

Column, Description:
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
"""

# Points
POINTS_TILE_FIRST_TRY  = 5
POINTS_TILE_SECOND_TRY = 3
POINTS_TILE_THIRD_TRY  = 1

POINTS_GAP          = 10
POINTS_OBSTACLE     = 10
POINTS_BUMPER       = 5
POINTS_RAMP         = 5
POINTS_INTERSECTION = 15

POINTS_LOW_VICTIM_ALIVE  = 30
POINTS_LOW_VICTIM_DEAD   = 20
POINTS_HIGH_VICTIM_ALIVE = 40
POINTS_HIGH_VICTIM_DEAD  = 30
POINTS_VICTIM_DEAD_BEFORE = 5
POINTS_DEDUCTION_LOP     =  5 # per victim
POINTS_FINDING_LINE      = 20

class Run:
    def __init__(self):
        self.iRun      = 0
        self.sTeamname = ""
        self.iTime     = 0 # time in seconds
        self.bStarted  = False
        self.iGaps          = 0
        self.iObstacles     = 0
        self.iBumper        = 0
        self.iRamps         = 0
        self.iIntersections = 0
        self.iVictimsAlive      = 0
        self.iVictimsDeadAfter  = 0
        self.iVictimsDeadBefore = 0
        self.bLowEvacuationTile = True
        self.iLOPsEvacuation    = 0
        self.bFoundLineAgain    = False
        self.aTiles    = [0, 0, 0, 0, 0, 0, 0, 0]
        self.aAttempts = [0, 0, 0, 0, 0, 0, 0, 0]

        self.iScore = 0

    def parse(self, sLine):
        # since ; can be in cells, .split(";") is not possible
        aLine = []
        
        bQuoted = False
        sCurValue = ""
        for sChar in sLine.strip():
            if(sChar == "\""):
                bQuoted = not bQuoted
            elif(sChar == ";" and not bQuoted):
                aLine.append(sCurValue)
                sCurValue = ""
            else:
                sCurValue += sChar
        aLine.append(sCurValue)

        def i(sNumber): # convert to int
            return int(sNumber) if sNumber.isdigit() else 0

        self.iRun      = i(aLine[0])
        self.sTeamname = aLine[1]
        self.iTime     = i(aLine[2].split(":")[0])*60 # minutes
        self.iTime    += i(aLine[2].split(":")[1])    # seconds
        self.bStarted  = (aLine[3].strip() == "")
        self.iGaps          = i(aLine[4])
        self.iObstacles     = i(aLine[5])
        self.iBumper        = i(aLine[6])
        self.iRamps         = i(aLine[7])
        self.iIntersections = i(aLine[8])
        self.iVictimsAlive      = i(aLine[9])
        self.iVictimsDeadAfter  = i(aLine[10])
        self.iVictimsDeadBefore = i(aLine[11])
        self.bLowEvacuationTile = (aLine[12].lower() in ("","l","low","f","flach"))
        self.iLOPsEvacuation    = i(aLine[13])
        self.bFoundLineAgain    = (aLine[14].lower() in ("y","yes","j","ja","x"))
        for j in range(8): self.aTiles[j]    = i(aLine[15+j])
        for j in range(8): self.aAttempts[j] = i(aLine[23+j])

        return self

    def calculate(self):
        self.iScore = 0
        
        if(not self.bStarted):
            return self

        self.iScore += POINTS_TILE_FIRST_TRY # for starting tile

        # points per section
        for i in range(8):
            if(self.aAttempts[i] == 1):
                self.iScore += self.aTiles[i] * POINTS_TILE_FIRST_TRY
            elif(self.aAttempts[i] == 2):
                self.iScore += self.aTiles[i] * POINTS_TILE_SECOND_TRY
            elif(self.aAttempts[i] == 3):
                self.iScore += self.aTiles[i] * POINTS_TILE_THIRD_TRY

        # extrapoints (gap, obstacle, ...)
        self.iScore += self.iGaps          * POINTS_GAP
        self.iScore += self.iObstacles     * POINTS_OBSTACLE
        self.iScore += self.iBumper        * POINTS_BUMPER
        self.iScore += self.iRamps         * POINTS_RAMP
        self.iScore += self.iIntersections * POINTS_INTERSECTION

        # points for victims
        iPointsVictim = 0

        if(self.bLowEvacuationTile):
            iPointsVictim += self.iVictimsAlive      * POINTS_LOW_VICTIM_ALIVE
            iPointsVictim += self.iVictimsDeadAfter  * POINTS_LOW_VICTIM_DEAD
            iPointsVictim += self.iVictimsDeadBefore * POINTS_VICTIM_DEAD_BEFORE
        else:
            iPointsVictim += self.iVictimsAlive      * POINTS_HIGH_VICTIM_ALIVE
            iPointsVictim += self.iVictimsDeadAfter  * POINTS_HIGH_VICTIM_DEAD
            iPointsVictim += self.iVictimsDeadBefore * POINTS_VICTIM_DEAD_BEFORE

        iPointsVictim -= ((self.iVictimsAlive     +
                           self.iVictimsDeadAfter +
                           self.iVictimsDeadBefore)
                          * self.iLOPsEvacuation
                          * POINTS_DEDUCTION_LOP )

        self.iScore += max(0, iPointsVictim) # no negative points

        if(self.bFoundLineAgain):
            self.iScore += POINTS_FINDING_LINE
        
        return self

    def show(self):
        print(self.__repr__())
        if(not self.bStarted): print("not started")
        print("Time: {} seconds".format(self.iTime))
        print("Score: {}".format(self.iScore))
        print("Tiles per section:", self.aTiles)
        print("Attempts for each section:", self.aAttempts)
        print("{} gaps".format(self.iGaps))
        print("{} obstacles".format(self.iObstacles))
        print("{} speed bumps".format(self.iBumper))
        print("{} ramps".format(self.iRamps))
        print("{} intersections".format(self.iIntersections))
        print("{} evacuation tile".format("Low" if self.bLowEvacuationTile else "High"))
        print("{} alive victims rescued".format(self.iVictimsAlive))
        print("{} dead victims rescued after all live victims were rescued".format(self.iVictimsDeadAfter))
        print("{} dead victims rescued before all live victims were rescued".format(self.iVictimsDeadBefore))
        print("{} LOPs in evacuation zone".format(self.iLOPsEvacuation))
        if(self.bFoundLineAgain): print("found line again")

    def __repr__(self):
        return "Run {} of {}".format(self.iRun, self.sTeamname)

def convSec2Time(iSeconds):
    sTime = ""
    sTime += format(iSeconds // 60, "02d")
    sTime += ":"
    sTime += format(iSeconds  % 60, "02d")
    return sTime

