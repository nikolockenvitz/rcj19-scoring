import win32_color_console as wcc

default_colors = wcc.get_text_attr()
default_bg = default_colors & 0x0070
default_fg = default_colors & 0x0007

def printSuccess (successMessage):
    wcc.set_text_attr(wcc.FOREGROUND_GREEN | default_bg |
                      wcc.FOREGROUND_INTENSITY)
    print(successMessage)
    wcc.set_text_attr(default_colors)

def printWarning (warningMessage):
    wcc.set_text_attr(wcc.FOREGROUND_YELLOW | default_bg |
                      wcc.FOREGROUND_INTENSITY)
    print("*** Warning:", warningMessage)
    wcc.set_text_attr(default_colors)

def printError (errorMessage):
    wcc.set_text_attr(wcc.FOREGROUND_RED | default_bg |
                      wcc.FOREGROUND_INTENSITY)
    print("*** Error:", errorMessage)
    wcc.set_text_attr(default_colors)
