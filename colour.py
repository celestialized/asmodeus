from colorama import Fore, Style

def colour(what, how):
    return "{}{}{}".format(how, what, Style.RESET_ALL)

def ok(what):
    return colour(what, Fore.GREEN)
    
def num(what):
    return colour(what, Fore.CYAN)
    
def err(what):
    return colour(what, Fore.RED)
    
def path(what):
    return colour(what, Fore.YELLOW)

def name(what):
    return colour(what, Fore.YELLOW)

def over(what):
    return colour(what, Fore.LIGHTGREEN_EX)

def script(what):
    return colour(what, Fore.LIGHTRED_EX)

def param(what):
    return colour(what, Fore.LIGHTBLUE_EX)
