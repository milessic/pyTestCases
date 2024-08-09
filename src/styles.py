class Colors:
    black = "black"
    red = "#ffb3ba"
    green = "#baffc9"
    yellow = "#ffdfba"
    gray = "#ababab"


class LightGrayTheme:
    bg = "#f0f0f0"
    highlight = "#d9d9d9"
    fg = "#333333"
    txt_bg = "#ffffff"
    txt_fg = "#4f4f4f"
    btn_highlight = "#cccccc"
    status_bg = "#e6e6e6"

class BlackTheme:
    bg = "#000000"
    highlight = "#1a1a1a"
    fg = "#ffffff"
    txt_bg = "#2b2b2b"
    txt_fg = "#eaeaea"
    btn_highlight = "#4d4d4d"
    status_bg = "#151515"

class WhiteTheme:
    bg = "#ffffff"
    highlight = "#f2f2f2"
    fg = "#000000"
    txt_bg = "#e6e6e6"
    txt_fg = "#333333"
    btn_highlight = "#cccccc"
    status_bg = "#f7f7f7"

class BlueTheme:
    bg = "#007acc"
    highlight = "#005999"
    fg = "#ffffff"
    txt_bg = "#cce7ff"
    txt_fg = "#003366"
    btn_highlight = "#66b2ff"
    status_bg = "#004080"

class RedTheme:
    bg = "#b30000"
    highlight = "#800000"
    fg = "#ffffff"
    txt_bg = "#ffcccc"
    txt_fg = "#330000"
    btn_highlight = "#ff6666"
    status_bg = "#660000"

class DarkBlueTheme:
    bg = "#22303c"
    highlight = "#9DB2BF"
    fg = "#ffffff"
    txt_bg ="#FFFDFA" 
    txt_fg ="#15202b" 
    btn_highlight="#ffffff"
    status_bg = "#6b6967"

class PastelTheme:
    bg = "#ffd1dc"
    highlight = "#ffb3c1"
    fg = "#4b0082"
    txt_bg = "#fff0f5"
    txt_fg = "#800080"
    btn_highlight = "#ff69b4"
    status_bg = "#ff80bf"


class Styles:
    def __init__(self, theme_name:str):

        default_theme = BlackTheme
        match theme_name.lower():
            case "darkblue":
                stylesheet = DarkBlueTheme
            case "lightgray":
                stylesheet = LightGrayTheme 
            case "black":
                stylesheet = BlackTheme
            case "white":
                stylesheet = WhiteTheme
            case "blue":
                stylesheet = BlueTheme
            case "red":
                stylesheet = RedTheme
            case "pastel":
                stylesheet = PastelTheme
            case "none":
                stylesheet = default_theme
            case _:
                print(f"Theme not supported - '{theme_name}'!")
                stylesheet = default_theme
        for k,v in stylesheet.__dict__.items():
            if k.startswith("__"):
                continue
            setattr(self, k,v)

