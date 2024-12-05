import tkinter.font as tkfont

def configure():
    """Configure default, text, and fixed fonts to use Helvetica family and set sizes."""
    family = "Helvetica"
    
    # Configure the default font
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=15, family=family)
    
    # Configure the text font
    text_font = tkfont.nametofont("TkTextFont")
    text_font.configure(size=12, family=family)
    
    # Configure the fixed font
    fixed_font = tkfont.nametofont("TkFixedFont")
    fixed_font.configure(size=12, family=family)
