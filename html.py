FILENAME_HTML_TEMPLATE = "template.html"
FILENAME_HTML_OUTPUT   = "results.html"

class HTMLOutput:
    def __init__(self):
        self.loadHTMLTemplate()
        self.sStanding1Title   = ""
        self.sStanding1Content = ""
        self.sStanding2Title   = ""
        self.sStanding2Content = ""

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
        sRowTemplate = "<tr>" + "<td>{}</td>"*10 + "</tr>"

        for aRow in aContent:
            sHTMLRows += sRowTemplate.format(*aRow)
            sHTMLRows += "\n"

        if(self.sStanding1Title == "" and
           self.sStanding1Content == ""):
            self.sStanding1Title   = sTitle
            self.sStanding1Content = sHTMLRows
        else:
            self.sStanding2Title   = sTitle
            self.sStanding2Content = sHTMLRows

    def output(self):
        if(self.sHTMLTemplate != ""):
            sHTML = self.sHTMLTemplate.format(title1 = self.sStanding1Title,
                                              content1 = self.sStanding1Content,
                                              title2 = self.sStanding2Title,
                                              content2 = self.sStanding2Content)

            try:
                f = open(FILENAME_HTML_OUTPUT, "w")
                f.write(sHTML)
                f.close()
                print("Successfully wrote to '{}'.".format(FILENAME_HTML_OUTPUT))
            except PermissionError:
                print("*** Couldn't write to '{}'. Is it opened in another program?".format(file[1]))
        else:
            print("*** Couldn't write to '{}' since loading of template failed.".format(FILENAME_HTML_OUTPUT))

