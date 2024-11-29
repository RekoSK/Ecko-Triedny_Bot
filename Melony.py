import random as rd

class Output:
    OutputText:str
    Vyhodnotenie:bool

IMG: str = [
    "🥝","🥥","🍇","🍈","🍉","🍊","🍋","🍋‍🟩","🍌","🍍","🥭","🍎","🍏","🍐","🍑","🍒","🍓","🫐","🆒"
]

def Tocenie():
    vytocene: str = ["", "", ""]
    for i in range(3):
        randomNumb = rd.randint(0, len(IMG) - 1)
        vytocene[i] = IMG[randomNumb]

    vytocene_Fullstring:str = ""
    for i in vytocene:
        vytocene_Fullstring += i
    
    return vytocene_Fullstring
    

def Vytocenie():
    vytocene: str = ["", "", ""]
    for i in range(3):
        randomNumb = rd.randint(0, len(IMG) - 1)
        vytocene[i] = IMG[randomNumb]
    
    coolbool:bool = False
    for h in vytocene:
        if h == vytocene[0]:
            coolbool = True
        else:
            coolbool = False
            break
    
    output: Output = Output()
    vytocene_Fullstring:str = ""
    for i in vytocene:
        vytocene_Fullstring += i
    
    output.OutputText = vytocene_Fullstring
    output.Vyhodnotenie = coolbool

    return output
