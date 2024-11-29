import random as rd

ODPOVEDE: str = [
    "Áno, jasné",
    "Nie, čo si si ako myslel že poviem?",
    "Určite nie. Koniec tejto konverzácie.",
    "100% Áno!",
    "Súhlasím!",
    "Vieš čo, iba kvôli tomu že si gay poviem nie.",
    "Skôr nie...",
    "Skôr áno...",
    "To vie iba boh a tvoja prababka.",
    "Možno...",
    "Tak na toto NEBUDEM odpovedať!",
    "Veď toto ani akinátor nevie :D",
    "Myslím si že hej.",
    "Pravdepodobne áno.",
    "Je to tak 50/50",
    "True af",
    "Based",
    "Nie + ratio + L + bad + noob",
    "Akožeeee... Povedal by som hej, ale keď tak o tom rozmýšlam, tak skôr asi nie.",
    "Nemyslím si no...",
    "Nn.",
    "Nie, ďalšia otázka.",
    "Jj",
    "100% Nie, a už sa nikdy neopýtaj na takúto blbosť!"
]

NADAVKY:str = "dont care + didnt ask + cry about it + stay mad + get real + L + mald seethe cope harder + h0es mad + basic + skill issue + ratio + you fell off + the audacity + triggered + any askers + redpilled + get a life + ok and? + cringe + touch grass + donowalled + not based + your’re probably white + not funny didn’t laugh + you’re* + grammar issue + go outside + get good + reported + ad hominem + GG! + ur momdon’t care + didn’t ask + cry about it + stay mad + get real + L + mald seethe cope harder + hoes mad + basic + skill issue + ratio + you fell off + the audacity + triggered + any askers + redpilled + get a life + ok and? + cringe + touch grass + donowalled + not based + your’re a full time discordian + not funny didn’t laugh + you’re* + grammar issue + go outside + get good + your gay + reported + ad hominem + GG! + ur mom + unknown + random + biased + racially motivated + kys + ur unfunny +ratio don’t care + didn’t ask + cry about it + stay mad + get real + L + mald seethe copedon’t care + didn’t ask + cry about it + stay mad + get real + L + mald seethe cope harder + h0es mad + basic + skill issue + ratio + you fell off + the audacity + triggered + any askers + redpilled + get a life + ok and? + cringe + touch grass + donowalled + not based + your’re probably white + not funny didn’t laugh + you’re* + grammar issue + go outside + get good + reported + ad hominem + GG! + ur momdon’t care + didn’t ask + cry about it + stay mad + get real + L + mald seethe cope harder + hoes mad + basic + skill issue + ratio + you fell off + the audacity + triggered + any askers + redpilled + get a life + ok and? + cringe + touch grass + donowalled + not based + your’re a full time discordian + not funny didn’t laugh + you’re* + grammar issue + go outside + get good + your gay + reported + ad hominem + ur mom + ur unfunny +ratio don’t care + didn’t ask + cry about it + stay mad + get real + so bad + so ass"

def Random_Answer():
    randomNumb = rd.randint(0, len(ODPOVEDE))
    return ODPOVEDE[randomNumb]

def Random_Nadavka(mention):
    return "{} vieš čo si myslím? **VIEŠ ČO SI MYSLÍM???:**\n".format(mention) + NADAVKY