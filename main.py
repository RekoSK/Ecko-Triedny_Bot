import discord
from discord import Interaction, app_commands, Client
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio
import secret as s
import EightBall as EB
import Melony as M
import random as rd
from time import sleep
import json
import os

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

base_path = os.path.dirname(os.path.abspath(__file__))

json_file_path = os.path.join(base_path, "data", "ulohy.json")
peopleData_Json = os.path.join(base_path, "data", "peopleData.json")

MODRA = 0x00FFFF
CERVENA = 0xFF0000
ZELENA = 0x11FF00

VERZIA = "0.0.3"

BOTCONTROL_CHANNEL = "1280853089674465291"

@client.event
async def on_ready():
    print("Bot online")
    print(".............")
    await tree.sync(guild=discord.Object(id=s.SERVER_ID))

@tree.command(name="8ball", description="Odpovie ti na otázku :o", guild=discord.Object(id=s.SERVER_ID))
async def EightBall(interaction: discord.Interaction, otázka: str):
    veta = EB.Random_Answer()
    embeds = [
        discord.Embed(title="Tvoja veta:", description=otázka, color=MODRA),
        discord.Embed(title="Odpoveď:", description=veta, color=CERVENA)
    ]
    await interaction.response.send_message(embeds=embeds)
    pass

@tree.command(name="melony", description="Pome točiť melóny", guild=discord.Object(id=s.SERVER_ID))
async def Melony(interaction: discord.Interaction):
    delay = 0.05
    embed = discord.Embed(title="...", description="...")
    await interaction.response.send_message(embed=embed)
    message:discord.InteractionMessage = await interaction.original_response()
    
    for i in range(rd.randint(5, 12)):
        vytocene = M.Tocenie()
        embed = discord.Embed(title=vytocene, description="Točím...")
        await message.edit(embed=embed)
        sleep(delay)
    output: M.Output = M.Vytocenie()
    if output.Vyhodnotenie == True:
        embed = discord.Embed(title=output.OutputText, description="Dobre točíš melóny... Vyhral si!", color=ZELENA)
    else:
        embed = discord.Embed(title=output.OutputText, description="Bad gambler detected at the north east!\nPrehral si (lko).", color=CERVENA)
    
    await message.edit(embed=embed)
    pass

@tree.command(name="pridatulohu", description="Pridaj d.ú. pre spolužiakov.", guild=discord.Object(id=s.SERVER_ID))
async def VytvorenieUlohy(interaction: discord.Interaction, predmet: str, úloha: str, dátum_deň: int, dátum_mesiac: int):
    if dátum_deň > 31 or dátum_deň < 1:
        embed = discord.Embed(title="Chyba!", description="Nesprávny dátum (chyba v dni).", color=CERVENA)
        await interaction.response.send_message(ephemeral=True, embed=embed)
        return
    
    if dátum_mesiac > 12 or dátum_mesiac < 1:
        embed = discord.Embed(title="Chyba!", description="Nesprávny dátum (chyba v mesiaci).", color=CERVENA)
        await interaction.response.send_message(ephemeral=True, embed=embed)
        return
    
    global base_path, json_file_path
    predmet = predmet.upper()

    with open(peopleData_Json, "r") as f:
        userData = json.load(f)

    precitalPravidla:bool = False
    for userID in userData["PrecitanyTut"]:
        if userID == interaction.user.id:
            precitalPravidla = True
            break
    
    if not precitalPravidla:
        embed = discord.Embed(title="Chyba!", description="Neprečítal si si pravidlá! Napíš /navodulohy a skús znova...", color=CERVENA)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    with open(json_file_path, "r") as f:
        ulohy: dict = json.load(f)
    
    full_datum: str = "d" + str(dátum_deň) + "_" + str(dátum_mesiac)

    if full_datum not in ulohy:
        ulohy[full_datum] = {}

    if predmet not in ulohy[full_datum]:
        ulohy[full_datum][predmet] = []

    ulohy[full_datum][predmet].append(úloha)

    with open(json_file_path, "w") as f:
        json.dump(ulohy, f, ensure_ascii=False, indent=4)

    embeds: list[discord.Embed] = [discord.Embed(title="Úspešne som pridal d.ú. do databázy.", description="Prosím, vždy sa ujisti že pred tebou už niekto tú istú úlohu nepridal - mohol by nastať chaos...", color=ZELENA), discord.Embed(title=predmet + " (" + str(dátum_deň) + "." + str(dátum_mesiac) + ".)", description=úloha, color=MODRA)]
    await interaction.response.send_message(embeds=embeds)

    pass

@tasks.loop(minutes=1)  # Check every minute
async def check_time():
    global base_path, json_file_path
    now = datetime.now()
    if now.weekday() < 5 and now.hour == 15 and now.minute == 0:
        channel = client.get_channel("1311383210466480128")
        #1280792838765809707
        if channel:
            nextDay = now + timedelta(days=1)
            time_string = "d" + str(nextDay.day) + "_" + str(nextDay.month)
            
            with open(json_file_path, "r") as f:
                ulohy = json.load(f)
            
            if time_string not in ulohy:
                embed = discord.Embed(title="Hurááá!", description="Na zajtra nie sú zaznačené žiadne nové úlohy! :)", color=ZELENA)
                await channel.send(embed=embed)
                return
            else:
                embeds: list[discord.Embed] = {}
                embed = discord.Embed(title="Úlohy na zajtra:", color=CERVENA)
                embeds.append(embed)
                for predmet in ulohy[time_string]:
                    embed = discord.Embed(title="**" +predmet + "**", color=MODRA)
                    for uloha in predmet:
                        embed.add_field(value=uloha)
                    embeds.append(embed)
                

            await channel.send(embeds=embeds)

        else:
            print("FATAL ERROR: ERROR FINDING CHANNEL!")

    if (now.weekday() < 5) and now.hour == 6 and now.minute == 0:
        channel = client.get_channel("1311383210466480128")
        if channel:
            nextDay = now + timedelta(days=1)
            time_string = "d" + str(nextDay.day) + "_" + str(nextDay.month)
            with open(json_file_path, "r") as f:
                ulohy = json.load(f)
            
            if time_string not in ulohy:
                print("Žiadne úlohy na dnes.")
                return
            else:
                embeds: list[discord.Embed] = {}
                embed = discord.Embed(title="Nezabudni na dnešné úlohy:", color=CERVENA)
                embeds.append(embed)
                for predmet in ulohy[time_string]:
                    embed = discord.Embed(title="**" +predmet + "**", color=MODRA)
                    for uloha in predmet:
                        embed.add_field(value=uloha)
                    embeds.append(embed)
                

            await channel.send(embeds=embeds)

        else:
            print("FATAL ERROR: ERROR FINDING CHANNEL!")


@tree.command(name="zobrazitulohy", description="Zobrazí úlohy na vybratý dátum", guild=discord.Object(id=s.SERVER_ID))
async def ZobrazUlohy(interaction:discord.Interaction, dátum_deň: int, dátum_mesiac: int):
    global json_file_path
    time_string = "d" + str(dátum_deň) + "_" + str(dátum_mesiac)
    print(time_string)
    with open(json_file_path, "r") as f:
        ulohy = json.load(f)
    
    if time_string not in ulohy:
        embed = discord.Embed(title="Hurááá!", description="Nenašiel som žiadne úlohy na tento deň :)", color=ZELENA)
        await interaction.response.send_message(embed=embed)
        return
    else:
        embeds: list[discord.Embed] = []
        now = datetime.now()
        embed = discord.Embed(title=str(now.day + 1) + "." + str(now.month), color=CERVENA)
        for predmet in ulohy[time_string]:
            embed = discord.Embed(title="**" +predmet + "**", color=MODRA)
            for i in range(len(ulohy[time_string][predmet])):
                embed.add_field(value=ulohy[time_string][predmet][i], name="Úloha č." + str(i + 1))
            embeds.append(embed)
        

    await interaction.response.send_message("**Úlohy z dňa " + str(dátum_deň) + "." + str(dátum_mesiac) + ".**",embeds=embeds)

@tree.command(name="navodulohy", description="Zobrazí ako správne posielať úlohy", guild=discord.Object(id=s.SERVER_ID))
async def NavodUlohy(interaction: discord.Interaction):
    global peopleData_Json
    with open(peopleData_Json, "r") as f:
        userData = json.load(f)
    
    userData["PrecitanyTut"].append(interaction.user.id)

    with open(peopleData_Json, "w") as f:
        json.dump(userData, f, indent=4)
    
    embed = discord.Embed(title="Návod na vytváranie d.ú.", description="**1.**\nDo úloh prosím píš iba skratky predmetov (napr. MAT), keďže je tento program stále vo vývoji, inak sa d.ú. bude zobrazovať 2-krát...\n**2.**\nDátum úlohy je termín, dokedy musí byť úloha odovzdaná, nie dnešný dátum!\n**3.**\nPred pridaním úlohy sa vždy ujisti, či už nie je pridaná - zbytočne tam bude dva-krát.\n**4.**\nProsím, zadávaj sem iba úlohy. Viem že je to common sense, ale nájdu sa individuá ktorým príde vtipné sem dávať iné veci...\n\n*Teraz už môžeš použiť /pridatulohu. V prípade otázok, kontaktuj Andreja.*")
    await interaction.response.send_message(embed=embed, ephemeral=True)
    pass

@tree.command(name="info", description="Zobrazí info o botovi.", guild=discord.Object(id=s.SERVER_ID))
async def InfoBot(interaction: discord.Interaction):
    embed: discord.Embed = discord.Embed(title="**Éčko, verzia " + VERZIA + "**", description="Bot triedy 1.E, naprogramovaný Andrejom Revákom (rekosk).\n\n*V prípade záujmu o bota ho kontaktuj*")
    await interaction.response.send_message(embed=embed, ephemeral=True)


client.run(s.DISCORD_TOKEN)