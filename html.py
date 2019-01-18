from time import strftime

FILENAME_HTML_TEMPLATE = "template.html"
FILENAME_HTML_OUTPUT   = "results.html"

TEAMS_QUALIFYING_LINE  = 3
TEAMS_QUALIFYING_ENTRY = 4

class HTMLOutput:
    def __init__(self):
        self.loadHTMLTemplate()
        self.sStandingTitleLine    = ""
        self.sStandingContentLine  = ""
        self.sStandingTitleEntry   = ""
        self.sStandingContentEntry = ""

    def loadHTMLTemplate(self):
        self.sHTMLTemplate = ""
        try:
            f = open(FILENAME_HTML_TEMPLATE, "r")
            self.sHTMLTemplate = f.read()
            f.close()
        except FileNotFoundError:
            print("*** Couldn't find '{}'. Make sure file exists.".format(FILENAME_HTML_TEMPLATE))

    def addStanding(self, sTitle, aContent):
        sHTMLRows = ""
        sRowTemplate = "<tr style=\"{}\">" + "<td>{}</td>"*10 + "</tr>"

        for aRow in aContent:
            aRow = [""] + aRow
            if(("entry" in sTitle.lower() and
                TEAMS_QUALIFYING_ENTRY != None and
                aRow[1] <= TEAMS_QUALIFYING_ENTRY) or
               ("entry" not in sTitle.lower() and
                TEAMS_QUALIFYING_LINE != None and
                aRow[1] <= TEAMS_QUALIFYING_LINE)):
                aRow[0] = "background-color: lightgreen;"
            sHTMLRows += sRowTemplate.format(*aRow)
            sHTMLRows += "\n"

        if("entry" in sTitle.lower()):
            self.sStandingTitleEntry   = sTitle
            self.sStandingContentEntry = sHTMLRows
        else:
            self.sStandingTitleLine   = sTitle
            self.sStandingContentLine = sHTMLRows

    def output(self):
        if(self.sHTMLTemplate != ""):
            sHTML = self.sHTMLTemplate.format(title1 = self.sStandingTitleLine,
                                              content1 = self.sStandingContentLine,
                                              title2 = self.sStandingTitleEntry,
                                              content2 = self.sStandingContentEntry,
                                              lastUpdateTime = strftime("%H:%M"),
                                              lastUpdateDate = strftime("%d.%m.%Y"))

            try:
                f = open(FILENAME_HTML_OUTPUT, "w")
                f.write(sHTML)
                f.close()
                print("Successfully wrote to '{}'.".format(FILENAME_HTML_OUTPUT))
            except PermissionError:
                print("*** Couldn't write to '{}'. Is it opened in another program?".format(file[1]))
        else:
            print("*** Couldn't write to '{}' since loading of template failed.".format(FILENAME_HTML_OUTPUT))

