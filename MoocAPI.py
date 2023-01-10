import json
import os.path
import time
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains


class URLS:
    MOOC = "https://ohjelmointi-22.mooc.fi"
    LOGIN = "sign-in"
    LOGOUT = "sign-out"
    ASSIGNMENT = "osa-"
    TMC_MOOC_LOGIN = "https://tmc.mooc.fi/login"


class MoocAPI:
    ANSWERS = {
        "answers": {
            "0": {
                "0": [
                    [
                        "print(\":-)\")",
                        " "
                    ],
                    [
                        "print(\"Aapo\")",
                        "print(\"Eero\")",
                        "print(\"Juhani\")",
                        "print(\"Lauri\")",
                        "print(\"Simeoni\")",
                        "print(\"Timo\")",
                        "print(\"Tuomas\")",
                        " "
                    ],
                    [
                        "print(\"Ukko Nooa, Ukko Nooa oli kunnon mies.\")",
                        "print(\"Kun h\u00e4n meni saunaan, laittoi laukun naulaan.\")",
                        "print(\"Ukko Nooa, Ukko Nooa oli kunnon mies.\")",
                        " "
                    ],
                    [
                        "print(365 * 24 * 60)",
                        " "
                    ],
                    [
                        "print('print(\"Moi kaikki!\")')",
                        " "
                    ]
                ],
                "1": [
                    [
                        "nimi = input(\"Anna nimesi: \")",
                        "print(nimi)",
                        "print(nimi)",
                        " "
                    ],
                    [
                        "nimi = input(\"Anna nimesi: \")",
                        "print(\"!\" + nimi + \"!\"+ nimi + \"!\")",
                        " "
                    ],
                    [
                        "etunimi = input(\"Etunimi: \")",
                        "sukunimi = input(\"Sukunimi: \")",
                        "katuosoite = input(\"Katuosoite: \")",
                        "pnro_ja_kaupunki = input(\"Postinumero ja kaupunki\")",
                        " ",
                        "print(etunimi + \" \" + sukunimi) # tulostetaan v\u00e4lily\u00f6nti nimien v\u00e4liin",
                        "print(katuosoite)",
                        "print(pnro_ja_kaupunki)",
                        " "
                    ],
                    [
                        "# esimerkkivastaus",
                        "osa1 = input(\"Anna 1. osa: \")",
                        "osa2 = input(\"Anna 2. osa: \")",
                        "osa3 = input(\"Anna 3. osa: \")",
                        "print(osa1 + \"-\" + osa2 + \"-\" + osa3 + \"!\")",
                        " "
                    ],
                    [
                        "nimi = input(\"Anna nimi: \")",
                        "vuosi = input(\"Anna vuosi: \")",
                        " ",
                        "print(nimi + \" on urhea ritari, syntynyt vuonna \" + vuosi + \". Er\u00e4\u00e4n\u00e4 aamuna \" + nimi)",
                        "print(\"her\u00e4si kovaan meluun: lohik\u00e4\u00e4rme l\u00e4hestyi kyl\u00e4\u00e4. Vain \" + nimi + \" voisi pelastaa kyl\u00e4n asukkaat.\")",
                        " "
                    ]
                ],
                "2": [
                    [
                        "nimi = \"Teppo Testaaja\"",
                        "ika = 20",
                        "taito1 = \"python\"",
                        "taso1 = \"aloittelija\"",
                        "taito2 = \"java\"",
                        "taso2 = \"veteraani\"",
                        "taito3 = \"ohjelmointi\"",
                        "taso3 = \"puoliammattilainen\"",
                        "ala = 2000",
                        "yla = 3000",
                        " ",
                        "print(f\"nimeni on {nimi}, olen {ika}-vuotias\")",
                        "print(\"\")",
                        "print(\"taitoihini kuuluvat\")",
                        "print(\" -\", taito1, \"(\"+taso1+\")\")",
                        "print(\" -\", taito2, \"(\"+taso2+\")\")",
                        "print(\" -\", taito3, \"(\"+taso3+\")\")",
                        "print(\"\")",
                        "print(f\"haen ty\u00f6t\u00e4, josta maksetaan palkkaa {ala}-{yla} euroa kuussa\")",
                        " ",
                        " "
                    ],
                    [
                        "x = 27",
                        "y = 15",
                        " ",
                        "print(f\"{x} + {y} = {x+y}\")",
                        "print(f\"{x} - {y} = {x-y}\")",
                        "print(f\"{x} * {y} = {x*y}\")",
                        "# tulostus voitaisiin hoitaa my\u00f6s seuraavasti",
                        "print(x, \"/\", y, \"=\", (x / y))",
                        " "
                    ],
                    [
                        "print(5, end= \"\")",
                        "print(\" + \", end= \"\")",
                        "print(8, end= \"\")",
                        "print(\" - \", end= \"\")",
                        "print(4, end= \"\")",
                        "print(\" = \", end= \"\")",
                        "print(5 + 8 - 4)",
                        " "
                    ]
                ],
                "3": [
                    [
                        "syote = input(\"anna luku: \")",
                        "tulo = int(syote) * 5",
                        "print(f\"Kun kerrotaan {syote} luvulla 5, saadaan {tulo}\")",
                        " "
                    ],
                    [
                        "nimi = input(\"Anna nimi: \")",
                        "syntynyt = int(input(\"Anna syntym\u00e4vuosi: \"))",
                        "ika = 2020 - syntynyt",
                        "print(f\"Moi {nimi}, olet {ika} vuotta vanha vuoden 2020 lopussa\")",
                        " "
                    ],
                    [
                        "syote = input(\"Kuinka monen vuorokauden sekunnit tulostetaan? \")",
                        "vuorokaudet = int(syote)",
                        "sekunnit = vuorokaudet * 24 * 60 * 60",
                        "print(sekunnit)",
                        " "
                    ],
                    [
                        "luku1 = int(input(\"Anna luku 1: \"))",
                        "luku2 = int(input(\"Anna luku 2: \"))",
                        "luku3 = int(input(\"Anna luku 3: \"))",
                        " ",
                        "tulo = luku1 * luku2 * luku3",
                        " ",
                        "print(\"Tulo on\", tulo)",
                        " ",
                        " ",
                        " "
                    ],
                    [
                        "luku1 = int(input('Luku 1: '))",
                        "luku2 = int(input('Luku 2: '))",
                        "print(\"Lukujen summa\", luku1 + luku2)",
                        "print(\"Lukujen tulo\", luku1 * luku2)",
                        " "
                    ],
                    [
                        "luku1 = int(input('Luku 1: '))",
                        "luku2 = int(input('Luku 2: '))",
                        "luku3 = int(input('Luku 3: '))",
                        "luku4 = int(input('Luku 4: '))",
                        "summa = luku1 + luku2 + luku3 + luku4",
                        "print(f\"Lukujen summa on {summa} ja keskiarvo {summa/4}\")",
                        " "
                    ],
                    [
                        "kertaa_unicafessa = int(input(\"Montako kertaa viikossa sy\u00f6t Unicafessa? \"))",
                        "unicafe_hinta = float(input(\"Unicafe-lounaan hinta? \"))",
                        "ostokset = float(input(\"Paljonko k\u00e4yt\u00e4t viikossa ruokaostoksiin? \"))",
                        " ",
                        "viikossa = ostokset + kertaa_unicafessa * unicafe_hinta",
                        " ",
                        "print(\"Kustannukset keskim\u00e4\u00e4rin:\")",
                        "print(f\"P\u00e4iv\u00e4ss\u00e4 {viikossa / 7} euroa\")",
                        "print(f\"Viikossa {viikossa} euroa\")",
                        " ",
                        " "
                    ],
                    [
                        "opiskelijoita = int(input(\"Montako opiskelijaa? \"))",
                        "ryhmakoko = int(input(\"Ryhm\u00e4n koko: \"))",
                        " ",
                        "ryhmia = (opiskelijoita + ryhmakoko - 1) // ryhmakoko",
                        "print(\"Ryhmien m\u00e4\u00e4r\u00e4:\", ryhmia)",
                        " "
                    ]
                ],
                "4": [
                    [
                        "luku = int(input(\"Anna luku: \"))",
                        "if luku == 1984:",
                        "    print('Orwell')",
                        " ",
                        " "
                    ],
                    [
                        "syote = int(input(\"sy\u00f6t\u00e4 luku? \"))",
                        "itseisarvo = syote",
                        "if syote < 0:",
                        "    itseisarvo = syote * -1",
                        "print(\"Luvun itseisarvo on\", itseisarvo)",
                        " "
                    ],
                    [
                        "nimi = input(\"Mik\u00e4 on nimesi:  \")",
                        "if nimi != \"Jerry\":",
                        "    keittoja = int(input(\"Kuinka monta annosta keittoa: \"))",
                        "    hinta = 5.9 * keittoja",
                        "    print(\"Kokonaishinta on\", hinta)",
                        "print(\"Seuraava!\")",
                        " ",
                        " ",
                        " "
                    ],
                    [
                        "luku = int(input(\"Anna luku: \"))",
                        " ",
                        "if luku < 1000:",
                        "    print(\"Luku on pienempi kuin 1000\")",
                        " ",
                        "if luku < 100:",
                        "    print(\"Luku on pienempi kuin 100\")",
                        " ",
                        "if luku < 10:",
                        "    print(\"Luku on pienempi kuin 10\")",
                        " ",
                        "print(\"Kiitos!\")",
                        " ",
                        " "
                    ],
                    [
                        "luku1 = int(input(\"Luku 1 \"))",
                        "luku2 = int(input(\"Luku 2 \"))",
                        "komento = input(\"Komento: \")",
                        " ",
                        "if komento == \"summa\":",
                        "    print(f\"{luku1} + {luku2} = {luku1 + luku2}\")",
                        "if komento == \"erotus\":",
                        "    print(f\"{luku1} - {luku2} = {luku1 - luku2}\")",
                        "if komento == \"tulo\":",
                        "    print(f\"{luku1} * {luku2} = {luku1 * luku2}\")",
                        " "
                    ],
                    [
                        "lampo_f = int(input(\"Anna l\u00e4mp\u00f6tila (F): \"))",
                        " ",
                        "lampo_c = (lampo_f - 32) * 5/9",
                        " ",
                        "print(f\"{lampo_f} fahrenheit-astetta on {lampo_c} celsius-astetta\") ",
                        " ",
                        "if lampo_c < 0:",
                        "    print(\"Paleltaa!\")",
                        " ",
                        " "
                    ],
                    [
                        "tuntipalkka = float(input(\"Tuntipalkka: \"))",
                        "tunnit = int(input(\"Ty\u00f6tunnit: \"))",
                        "viikonpaiva = input(\"Viikonp\u00e4iv\u00e4: \")",
                        " ",
                        "if viikonpaiva == \"sunnuntai\":",
                        "    # Sunnuntailta saa tuplapalkan",
                        "    tuntipalkka *= 2",
                        " ",
                        "palkka_yhteensa = tuntipalkka * tunnit",
                        "print(f\"Palkka {palkka_yhteensa} euroa\")",
                        " "
                    ],
                    [
                        "pisteet = int(input(\"Kuinka paljon pisteit\u00e4? \"))",
                        "if pisteet < 100:",
                        "    kerroin = 1.1",
                        "    print(\"Sait 10 % bonusta\")",
                        "    ",
                        "if pisteet >= 100:",
                        "    kerroin = 1.15",
                        "    print(\"Sait 15 % bonusta\")",
                        " ",
                        "# a *= b on sama kuin a = a * b",
                        "pisteet *= kerroin",
                        "print(\"Pisteit\u00e4 on nyt\", pisteet)",
                        " "
                    ],
                    [
                        "lampotila = int(input(\"L\u00e4mp\u00f6tila: \"))",
                        "sade = input(\"Sataako (kyll\u00e4/ei): \")",
                        "print(\"Pue housut ja t-paita\")",
                        "if lampotila < 21:",
                        "    print(\"Ota my\u00f6s pitk\u00e4hihainen paita\")",
                        "if lampotila < 11:",
                        "    print(\"Pue p\u00e4\u00e4lle takki\")",
                        "if lampotila < 6:",
                        "    print(\"Suosittelen l\u00e4mmint\u00e4 takkia\")",
                        "    print(\"Kannattaa ottaa my\u00f6s hanskat\")",
                        "if sade == \"kyll\u00e4\":",
                        "    print(\"Muista sateenvarjo!\")",
                        " "
                    ],
                    [
                        "# Otetaan k\u00e4ytt\u00f6\u00f6n neli\u00f6juuri math-moduulista",
                        "from math import sqrt",
                        " ",
                        "a = int(input(\"Anna a: \"))",
                        "b = int(input(\"Anna b: \"))",
                        "c = int(input(\"Anna c: \"))",
                        " ",
                        "diskriminantti = b**2 - (4 * a * c)",
                        " ",
                        "juuri1 = (-b + sqrt(diskriminantti)) / (2 * a)",
                        "juuri2 = (-b - sqrt(diskriminantti)) / (2 * a)",
                        " ",
                        "print(f\"Juuret ovat {juuri1} ja {juuri2}\")",
                        " ",
                        "# Otetaan k\u00e4ytt\u00f6\u00f6n neli\u00f6juuri math-moduulista",
                        " ",
                        "# Huomaa, ett\u00e4 neli\u00f6juuren voi laskea my\u00f6s potenssin avulla:",
                        "# sqrt(9) on sama asia kuin 9 ** 0.5"
                    ]
                ]
            },
            "1": {
                "0": [
                    [
                        "luku = int(input(\"Anna luku: \"))",
                        "if luku > 100:",
                        "    print(\"Luku oli suurempi kuin sata\")",
                        "    luku = luku - 100",
                        "    print(\"Nyt luvun arvo on pienentynyt sadalla\") ",
                        "    print(\"Arvo on nyt\"+ str(luku))",
                        "print(str(luku) + \" taitaa olla onnenlukuni!\")",
                        "print(\"Hyv\u00e4\u00e4 p\u00e4iv\u00e4njatkoa!\")",
                        " "
                    ],
                    [
                        "sana = input(\"Anna sana: \")",
                        " ",
                        "pituus = len(sana)",
                        "if pituus > 1:",
                        "    print(\"Sanassa \" + sana + \" on \", pituus, \"kirjainta\")",
                        " ",
                        "print(\"Kiitos!\")",
                        " ",
                        " "
                    ],
                    [
                        "luku = float(input(\"Anna luku: \"))",
                        "kokonaisosa = int(luku)",
                        "desimaaliosa = luku - kokonaisosa",
                        "print(f\"Kokonaisosa: {kokonaisosa}\" )",
                        "print(f\"Desimaaliosa: {desimaaliosa}\")",
                        " ",
                        " "
                    ]
                ],
                "1": [
                    [
                        "ika = int(input(\"Kuinka vanha olet: \"))",
                        " ",
                        "if ika < 18:",
                        "    print(\"Et ole t\u00e4ysi-ik\u00e4inen!\")",
                        "else:",
                        "    print(\"Olet t\u00e4ysi-ik\u00e4inen!\")",
                        " ",
                        " "
                    ],
                    [
                        "luku1 = int(input(\"Anna ensimm\u00e4inen luku: \"))",
                        "luku2 = int(input(\"Anna toinen luku: \"))",
                        " ",
                        "if luku1 > luku2:",
                        "    print(\"Suurempi luku:\", luku1)",
                        "elif luku2 > luku1:",
                        "    print(\"Suurempi luku:\", luku2)",
                        "else:",
                        "    print(\"Luvut ovat yht\u00e4 suuret!\")",
                        " ",
                        " ",
                        " "
                    ],
                    [
                        "print(\"Henkil\u00f6 1:\")",
                        "nimi1 = input(\"Nimi: \")",
                        "ika1 = int(input(\"Ik\u00e4: \"))",
                        " ",
                        "print(\"Henkil\u00f6 2:\")",
                        "nimi2 = input(\"Nimi: \")",
                        "ika2 = int(input(\"Ik\u00e4: \"))",
                        " ",
                        "if ika1 > ika2:",
                        "    print(f\"Vanhempi on {nimi1}\")",
                        "elif ika2 > ika1:",
                        "    print(f\"Vanhempi on {nimi2}\")",
                        "else:",
                        "    print(f\"{nimi1} ja {nimi2} ovat yht\u00e4 vanhoja\")",
                        " "
                    ],
                    [
                        "sana1 = input(\"Anna 1. sana: \")",
                        "sana2 = input(\"Anna 2. sana: \")",
                        " ",
                        "if sana1 > sana2:",
                        "    print(sana1, \"on aakkosj\u00e4rjestyksess\u00e4 viimeinen\")",
                        "elif sana2 > sana1:",
                        "    print(sana2, \"on aakkosj\u00e4rjestyksess\u00e4 viimeinen\")",
                        "else:",
                        "    print(\"Annoit saman sanan kahdesti.\")",
                        " ",
                        " "
                    ]
                ],
                "2": [
                    [
                        "ika = int(input(\"kerro ik\u00e4si: \"))",
                        "if ika < 0:",
                        "    print(\"Taitaa olla virhe\")",
                        "elif ika < 5:",
                        "    print(\"En usko, ett\u00e4 osaat kirjoittaa\")",
                        "else:",
                        "    print(\"Ok, olet siis \" + str(ika) + \"-vuotias\")",
                        " "
                    ],
                    [
                        "nimi = input(\"Anna nimesi: \")",
                        " ",
                        "if nimi == \"Tupu\" or nimi == \"Hupu\" or nimi == \"Lupu\":",
                        "    print(\"Olet luultavasti Aku Ankan veljenpoika.\")",
                        "elif nimi == \"Mortti\" or nimi == \"Vertti\":",
                        "    print(\"Olet luultavasti Mikki Hiiren veljenpoika.\")",
                        "else:",
                        "    print(\"Et ole kenenk\u00e4\u00e4n tuntemani hahmon veljenpoika.\")",
                        " "
                    ],
                    [
                        "pisteet = int(input(\"Anna pisteet [0-100]: \"))",
                        " ",
                        "if pisteet < 0 or pisteet > 100:",
                        "    arvosana = \"mahdotonta!\"",
                        "elif pisteet < 50:",
                        "    arvosana = \"hyl\u00e4tty\"",
                        "elif pisteet < 60:",
                        "    arvosana = \"1\"",
                        "elif pisteet < 70:",
                        "    arvosana = \"2\"",
                        "elif pisteet < 80:",
                        "    arvosana = \"3\"",
                        "elif pisteet < 90:",
                        "    arvosana = \"4\"",
                        "else:",
                        "    arvosana = \"5\"",
                        " ",
                        "print(f\"Arvosana: {arvosana}\")",
                        " "
                    ],
                    [
                        "luku = int(input(\"Luku: \"))",
                        " ",
                        "if luku % 3 == 0 and luku % 5 == 0:",
                        "    # T\u00e4m\u00e4 pit\u00e4\u00e4 testata ensin, koska jos t\u00e4m\u00e4 on tosi,",
                        "    # my\u00f6s molemmat seuraavat vaihtoehdot ovat tosia",
                        "    print(\"FizzBuzz\")",
                        "elif luku % 3 == 0:",
                        "    print(\"Fizz\")",
                        "elif luku % 5 == 0:",
                        "    print(\"Buzz\")",
                        " "
                    ],
                    [
                        "vuosi = int(input(\"Anna vuosi: \"))",
                        " ",
                        "# Oletetaan aluksi, ett\u00e4 ei ole karkausvuosi",
                        "karkausvuosi = False",
                        " ",
                        "if vuosi % 100 == 0:",
                        "    if vuosi % 400 == 0:",
                        "        karkausvuosi = True",
                        "elif vuosi % 4 == 0:",
                        "    karkausvuosi = True",
                        " ",
                        "if karkausvuosi:",
                        "    print(\"Vuosi on karkausvuosi.\")",
                        "else:",
                        "    print(\"Vuosi ei ole karkausvuosi.\")",
                        " "
                    ],
                    [
                        "kirjain1 = input(\"Anna 1. kirjain: \")",
                        "kirjain2 = input(\"Anna 2. kirjain: \")",
                        "kirjain3 = input(\"Anna 3. kirjain: \")",
                        " ",
                        "if kirjain1 > kirjain2 and kirjain1 > kirjain3:",
                        "    if kirjain2 > kirjain3:",
                        "        keski = kirjain2",
                        "    else:",
                        "        keski = kirjain3",
                        "elif kirjain2 > kirjain3:",
                        "    if kirjain3 > kirjain1:",
                        "        keski = kirjain3",
                        "    else:",
                        "        keski = kirjain1",
                        "else:",
                        "    if kirjain2 > kirjain1:",
                        "        keski = kirjain2",
                        "    else:",
                        "        keski = kirjain1",
                        " ",
                        "print(\"Keskimm\u00e4inen kirjain on \" + keski)",
                        " "
                    ],
                    [
                        "suuruus = int(input(\"Lahjan suuruus: \"))",
                        " ",
                        "if suuruus < 5000:",
                        "    vero = 0",
                        "elif suuruus <= 25000:",
                        "    vero = 100 + (suuruus - 5000) * 0.08",
                        "elif suuruus <= 55000:",
                        "    vero = 1700 + (suuruus - 25000) * 0.10",
                        "elif suuruus <= 200000:",
                        "    vero = 4700 + (suuruus - 55000) * 0.12",
                        "elif suuruus <= 1000000:",
                        "    vero = 22100 + (suuruus - 200000) * 0.15",
                        "else:",
                        "    vero = 142100 + (suuruus - 1000000) * 0.17",
                        " ",
                        "if vero == 0:",
                        "    print(\"Ei veroa!\")",
                        "else:",
                        "    print(f\"Vero: {vero} euroa\")",
                        " ",
                        " "
                    ]
                ],
                "3": [
                    [
                        "while True:",
                        "    print(\"moi\")",
                        "    vastaus = input(\"Jatketaanko? \")",
                        "    if vastaus == \"ei\":",
                        "        break",
                        "    ",
                        "print(\"ei sitten\")",
                        " "
                    ],
                    [
                        "from math import sqrt",
                        "while True:",
                        "    luku = int(input(\"luku: \"))",
                        "    if luku == 0:",
                        "        break",
                        "    if luku > 0:",
                        "        print(sqrt(luku))",
                        "    else:",
                        "        print(\"Ep\u00e4kelpo luku\")",
                        "        ",
                        "print(\"Lopetetaan...\")",
                        " "
                    ],
                    [
                        "luku = 5",
                        "print(\"L\u00e4ht\u00f6laskenta!\")",
                        "while True:",
                        "  print(luku)",
                        "  luku = luku - 1",
                        "  if luku == 0:",
                        "    break",
                        " ",
                        "print(\"Nyt!\")",
                        " "
                    ],
                    [
                        "salasana = input(\"Salasana: \")",
                        "while True:",
                        "    salasana_uudelleen = input(\"Toista salasana: \")",
                        "    if salasana == salasana_uudelleen:",
                        "        break",
                        "    print(\"Ei ollut sama!\")",
                        " ",
                        "print(\"K\u00e4ytt\u00e4j\u00e4tunnus luotu!\")",
                        " "
                    ],
                    [
                        "yrityksia = 1",
                        "while True:",
                        "    pin = input(\"PIN-koodi: \")",
                        "    if pin == \"4321\":",
                        "        break",
                        "    print(\"V\u00e4\u00e4rin\")",
                        "    yrityksia += 1",
                        " ",
                        "if yrityksia == 1:  ",
                        "    print(\"Oikein, tarvitsit vain yhden yrityksen!\")",
                        "else:",
                        "    print(f\"Oikein, tarvitsit {yrityksia} yrityst\u00e4\")",
                        " "
                    ],
                    [
                        "aloitusvuosi = int(input(\"Vuosi: \"))",
                        "vuosi = aloitusvuosi + 1",
                        "while True:",
                        "    if vuosi % 100 == 0:",
                        "        if vuosi % 400 == 0:",
                        "            break",
                        "    elif vuosi % 4 == 0:",
                        "        break",
                        " ",
                        "    vuosi += 1",
                        " ",
                        "print(f\"Vuotta {aloitusvuosi} seuraava karkausvuosi on {vuosi}\")",
                        " "
                    ],
                    [
                        "tarina = \"\"",
                        "edellinen = \"\"",
                        "while True:",
                        "    sana = input(\"Anna sana: \")",
                        "    if sana == \"loppu\" or sana == edellinen:",
                        "        break",
                        "    tarina += sana + \" \"",
                        "    edellinen = sana",
                        " ",
                        "print(tarina)",
                        " "
                    ],
                    [
                        "print(\"Sy\u00f6t\u00e4 kokonaislukuja, 0 lopettaa:\")",
                        "lukuja = 0",
                        "summa = 0",
                        "positiivisia = 0",
                        " ",
                        "while True:",
                        "    luku = int(input(\"luku: \"))",
                        "    if luku == 0:",
                        "        break",
                        "    lukuja += 1",
                        "    summa += luku",
                        "    if luku>0:",
                        "        positiivisia += 1",
                        " ",
                        "print(\"Lukuja yhteens\u00e4\", lukuja)",
                        "print(\"Lukujen summa\", summa)",
                        "print(\"Lukujen keskiarvo\", summa/lukuja)",
                        "print(\"Positiivisia\", positiivisia)",
                        "print(\"Negatiivisia\", lukuja-positiivisia)",
                        " "
                    ]
                ]
            },
            "2": {
                "0": [
                    [
                        "luku = 2",
                        "while luku <= 30:",
                        "    print(luku)",
                        "    luku += 2",
                        " ",
                        " "
                    ],
                    [
                        "print(\"Valmiina?\")",
                        "luku = int(input(\"Anna luku: \"))",
                        "while luku > 0:",
                        "  print(luku)",
                        "  luku -= 1",
                        "print(\"Nyt!\")",
                        " "
                    ],
                    [
                        "asti = int(input(\"Mihin asti: \"))",
                        "luku = 1",
                        "while luku < asti:",
                        "    print(luku)",
                        "    luku += 1",
                        " "
                    ],
                    [
                        "asti = int(input(\"Mihin asti: \"))",
                        "luku = 1",
                        "while luku <= asti:",
                        "    print(luku)",
                        "    luku *= 2",
                        " "
                    ],
                    [
                        "asti = int(input(\"Mihin asti: \"))",
                        "kerroin = int(input(\"Mik\u00e4 kerroin: \"))",
                        "luku = 1",
                        "while luku <= asti:",
                        "    print(luku)",
                        "    luku *= kerroin",
                        " "
                    ],
                    [
                        "asti = int(input(\"Mihin asti: \"))",
                        "luku = 1",
                        "summa = 1",
                        "while summa < asti:",
                        "    luku += 1",
                        "    summa += luku",
                        "print(summa)",
                        " "
                    ],
                    [
                        "asti = int(input(\"Mihin asti: \"))",
                        "luku = 1",
                        "summa = 1",
                        "luvut = \"1\"",
                        "while summa < asti:",
                        "    luku += 1",
                        "    summa += luku",
                        "    # huomaa, ett\u00e4 f-stringi\u00e4 voi k\u00e4ytt\u00e4\u00e4 my\u00f6s n\u00e4in",
                        "    luvut += f\" + {luku}\" ",
                        "print(f\"Laskettiin {luvut} = {summa}\")",
                        " "
                    ]
                ],
                "2": [
                    [
                        "luku = int(input(\"Anna luku: \"))",
                        "laskuri1 = 1",
                        "while laskuri1 <= luku:",
                        "    laskuri2 = 1",
                        "    while laskuri2 <= luku:",
                        "        print(f\"{laskuri1} x {laskuri2} = {laskuri1*laskuri2}\")",
                        "        laskuri2 += 1",
                        "    laskuri1 += 1",
                        " ",
                        " ",
                        " "
                    ],
                    [
                        "lause = input(\"Anna lause: \")",
                        " ",
                        "# Lis\u00e4t\u00e4\u00e4n alkuun v\u00e4lily\u00f6nti, jotta k\u00e4sittely helpottuu",
                        "lause = \" \" + lause",
                        " ",
                        "# Etsit\u00e4\u00e4n kohdat, joita ennen on v\u00e4lily\u00f6nti",
                        "kohta = 1",
                        "while kohta < len(lause):",
                        "    if lause[kohta-1] == \" \" and lause[kohta] != \" \":",
                        "        print(lause[kohta])",
                        "    kohta += 1",
                        " ",
                        " "
                    ],
                    [
                        "while True:",
                        "    luku = int(input(\"Anna luku: \"))",
                        "    if luku <= 0:",
                        "        break",
                        " ",
                        "    kertoma = 1",
                        "    uusi = 1",
                        "    while uusi <= luku:",
                        "        kertoma *= uusi",
                        "        uusi += 1",
                        " ",
                        "    print(f\"Luvun {luku} kertoma on {kertoma}\")",
                        " ",
                        "print(\"Kiitos ja moi!\")",
                        " ",
                        " "
                    ],
                    [
                        "luku = int(input(\"Luku: \"))",
                        " ",
                        "kohta = 1",
                        "while kohta+1 <= luku:",
                        "    print(kohta+1)",
                        "    print(kohta)",
                        "    kohta += 2",
                        " ",
                        "if kohta <= luku:",
                        "    print(kohta)",
                        " ",
                        " "
                    ],
                    [
                        "luku = int(input(\"Luku: \"))",
                        " ",
                        "vasen = 1",
                        "oikea = luku",
                        " ",
                        "while vasen < oikea:",
                        "    print(vasen)",
                        "    print(oikea)",
                        "    vasen += 1",
                        "    oikea -= 1",
                        " ",
                        "if vasen == oikea:",
                        "    print(vasen)",
                        " "
                    ]
                ],
                "3": [
                    [
                        "def seitseman_veljesta():",
                        "    print(\"Aapo\")",
                        "    print(\"Eero\")",
                        "    print(\"Juhani\")",
                        "    print(\"Lauri\")",
                        "    print(\"Simeoni\")",
                        "    print(\"Timo\")",
                        "    print(\"Tuomas\")",
                        "if __name__ == \"__main__\":",
                        "    seitseman_veljesta()    ",
                        " "
                    ],
                    [
                        "def ensimmainen(merkkijono):",
                        "    print(merkkijono[0])",
                        "if __name__ == \"__main__\":",
                        "    ensimmainen('nukkumaanmenoaika')    ",
                        " "
                    ],
                    [
                        "def  keskiarvo(luku1, luku2, luku3):",
                        "    vastaus = (luku1 + luku2 + luku3) / 3",
                        "    print(vastaus)",
                        " ",
                        "if __name__ == \"__main__\":",
                        "     keskiarvo(1, 2, 3)",
                        " "
                    ],
                    [
                        "def tulosta_monesti(merkkijono, kertaa):",
                        "    while kertaa > 0:",
                        "        print(merkkijono)",
                        "        kertaa -= 1",
                        "    ",
                        "if __name__ == \"__main__\":",
                        "    tulosta_monesti(\"python\", 5)",
                        "# tee ratkaisu t\u00e4h\u00e4n",
                        " "
                    ],
                    [
                        "def risunelio(koko):",
                        "    rivit = koko",
                        "    while rivit > 0:",
                        "        print(\"#\" * koko)",
                        "        rivit -= 1",
                        "        ",
                        "if __name__ == \"__main__\":",
                        "    risunelio(5)",
                        "# tee ratkaisu t\u00e4nne",
                        " "
                    ],
                    [
                        "def shakkilauta(koko):",
                        "    i = 0",
                        "    while i < koko:",
                        "        if i % 2 == 0:",
                        "            rivi = \"10\"*koko",
                        "        else:",
                        "            rivi = \"01\"*koko",
                        "        # poistetaan rivin lopusta ylim\u00e4\u00e4r\u00e4iset merkit",
                        "        print(rivi[0:koko])",
                        "        i += 1",
                        "# tee ratkaisu t\u00e4nne",
                        " ",
                        " "
                    ],
                    [
                        "def nelio(merkit, koko):",
                        "    i = 0",
                        "    rivi = \"\"",
                        "    while i < koko * koko:",
                        "        if i > 0 and i % koko == 0:",
                        "            print(rivi)",
                        "            rivi = \"\"",
                        "        rivi += merkit[i % len(merkit)]",
                        "        i += 1",
                        "    print(rivi)",
                        "# tee ratkaisu t\u00e4nne",
                        " ",
                        " "
                    ]
                ]
            }
        }
    }

    def __init__(self):
        self._driver: webdriver.Firefox = webdriver.Firefox()
        self._logged_in: bool = False
        self._logged_in_tmc: bool = False

    def _wait_for_url(self, url: str, timeout: int = 10) -> bool:
        """
        Waits until url has changed
        :param url: Desired url
        :param timeout: How long it will wait
        :return: If successful
        """
        try:
            WebDriverWait(self._driver, timeout).until(
                lambda e: self._driver.current_url == url)
            return True
        except TimeoutException:
            return False

    def _wait_for_not_url(self, url: str, timeout: int = 10) -> bool:
        """
        Waits until url has changed
        :param url: Not desired url
        :param timeout: How long it will wait
        :return: If successful
        """
        try:
            WebDriverWait(self._driver, timeout).until(
                lambda e: self._driver.current_url != url)
            return True
        except TimeoutException:
            return False

    def _wait_for_element_present(self, search_term: tuple, timeout: int = 5) -> bool:
        """
        Waits until it finds correct element
        :param search_term: Such as (By.ID, "<id>")
        :param timeout: How long will it search
        :return: If successful
        """
        try:
            element_present = EC.presence_of_element_located(search_term)
            WebDriverWait(self._driver, timeout).until(element_present)
            return True
        except TimeoutException:
            return False

    def is_logged_in(self) -> bool:
        """
        Returns if you are logged into MOOC
        :return: True of False
        """
        return self._logged_in

    def logout(self):
        """
        Logs out of MOOC
        """
        if self._logged_in:
            self._driver.get(f"{URLS.MOOC}/{URLS.LOGOUT}")
            self._logged_in = False

    def login(self, username: str, password: str) -> bool:
        """
        Logs into MOOC
        :param username: MOOC username
        :param password: MOOC password
        :return: if successful
        """
        if not self._logged_in:
            login_url: str = f"{URLS.MOOC}/{URLS.LOGIN}"
            self._driver.get(login_url)

            username_e: WebElement = self._driver.find_element_by_id("outlined-adornment-email")  # Email input
            password_e: WebElement = self._driver.find_element_by_id("outlined-adornment-password")  # Password input

            username_e.send_keys(username)
            password_e.send_keys(password)

            submit_button_e: WebElement = self._driver.find_element_by_xpath("//button[@type='submit']")
            submit_button_e.click()

            if self._wait_for_url(f"{URLS.MOOC}/"):
                self._logged_in = True
        return self._logged_in

    def _login_to_tmc(self, username: str, password: str) -> bool:
        if not self._logged_in_tmc:
            self._driver.get(URLS.TMC_MOOC_LOGIN)
            username_e: WebElement = self._driver.find_element_by_id("username")  # Email input
            password_e: WebElement = self._driver.find_element_by_id("password")  # Password input

            username_e.send_keys(username)
            password_e.send_keys(password)

            submit_button_e: WebElement = self._driver.find_element_by_xpath("//input[@type='submit']")
            submit_button_e.click()

            if self._wait_for_not_url(f"{URLS.TMC_MOOC_LOGIN}/"):
                self._logged_in_tmc = True
        return self._logged_in_tmc

    def _get_assignment_links(self, assignment_num: int) -> List[str]:
        """
        Returns a list of links where all the assignments are (aka. part 1 - 1, part 1 - 2...)
        :param assignment_num: For example: 1,2,3,4...
        :return: List of assignemnt links
        """

        self._driver.get(f"{URLS.MOOC}/{URLS.ASSIGNMENT}{assignment_num}")

        links_e: List[WebElement] = self._driver.find_element_by_xpath("/html/body/div/div[1]/div/div[2]/main/div/div/div/div[1]/div/ol").find_elements_by_tag_name("a")  # Finds all assignment links

        assignment_links: List[int] = []

        # Gets links from link elements
        for i, link_e in enumerate(links_e):
            link = link_e.get_attribute("href")
            assignment_links.append(link)

        return assignment_links

    def _go_to_sub_assignment(self, url: str):
        """
        Opens sub assignment page and waits for it to load
        :param url: Url of the page
        """
        self._driver.get(URLS.MOOC)  # Makes sure website is refreshed so it can detect when the correct url is present
        self._driver.get(url)
        self._wait_for_url(url)
        self._wait_for_element_present((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/main/div/article/a"))

    def _get_answer_for_assignment(self) -> List[str]:
        """
        Returns an answer for current open assignment
        :return: a list of lines of code (corresponding to the correct answer)
        """
        # Waits for page to load
        WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div[2]/div/div/div/div/div/pre/code/table/tbody")))

        divs: List[WebElement] = self._driver.find_elements_by_xpath("//div[@class='hljs-ln-line']")  # Divs containing lines of code
        answers: List[str] = []  # All lines of code converted into a list of strings
        # Adds the code into the list
        for div in divs:
            answers.append(div.text)

        self._driver.close()
        return answers

    def _get_sub_assignment_answers(self) -> List[List[str]]:
        """
        Returns a list of answers for each assignment on the page
        """
        # Wait until the page is ready
        try:
            WebDriverWait(self._driver, 5).until(lambda e: self._driver.find_elements_by_xpath("//div[@class='ProgrammingExerciseCard__Body-t91a2f-0 cTbyrn']"))  # Waits for all assignments to load
            WebDriverWait(self._driver, 5.).until(lambda e: len(self._driver.find_elements_by_xpath("//div[@class='sc-ljsmAU jFDlvU']")) == 0)  # Waits for all assignment contents to load
        except TimeoutException:
            print("Could not load the page...")
            return []

        # Find assignment divs
        assignment_divs: List[WebElement] = self._driver.find_elements_by_xpath("//div[@class='MuiPaper-root InBrowserProgrammingExercise__StyledPaper-n0r9hj-0 fjlUfr MuiPaper-elevation1 MuiPaper-rounded']")

        all_answers: List[List[str]] = []  # Contains all answers for each assignment on the page
        for i, div in enumerate(assignment_divs):  # Loop through each div and check if there is an answer
            buttons: List[WebElement] = div.find_elements_by_tag_name("button")  # List of buttons that the user can press on each assignment
            if len(buttons) == 4:  # Checks if answer button exists
                buttons[3].click()  # Clicks the answer button
                self._driver.switch_to.window(self._driver.window_handles[len(self._driver.window_handles) - 1])  # Selects the answer window
                answer = self._get_answer_for_assignment()  # Gets the answer
                all_answers.append(answer)
                self._driver.switch_to.window(self._driver.window_handles[len(self._driver.window_handles) - 1])

        return all_answers

    def _set_sub_assignment_answers(self, answers: List[List[str]]):
        # Wait until the page is ready
        try:
            WebDriverWait(self._driver, 5).until(lambda e: self._driver.find_elements_by_xpath("//div[@class='ProgrammingExerciseCard__Body-t91a2f-0 cTbyrn']"))  # Waits for all assignments to load
            WebDriverWait(self._driver, 5.).until(lambda e: len(self._driver.find_elements_by_xpath("//div[@class='sc-ljsmAU jFDlvU']")) == 0)  # Waits for all assignment contents to load
        except TimeoutException:
            print("Could not load the page...")
            return []

        # Finds the div containing all answer div
        answer_div: WebElement = self._driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/main/div/article/div[1]")
        answer_boxes: List[WebElement] = answer_div.find_elements_by_xpath("//div[contains(@class, 'MuiPaper-root InBrowserProgrammingExercise__StyledPaper-n0r9hj-0 fjlUfr MuiPaper-elevation1 MuiPaper-rounded')]")

        # Loops through each answer_box element and adds answers to it
        fail_count = 0
        for i, answer_box in enumerate(answer_boxes):
            # self._driver.execute_script("arguments[0].scrollIntoView();", answer_box)  # Scrolls the page so the answers load
            self._wait_for_element_present((By.XPATH, './/div[@class="view-lines monaco-mouse-cursor-text"]'))  # Waits for the answers to load
            view_line_div: WebElement = answer_box.find_element_by_xpath('.//div[@class="view-lines monaco-mouse-cursor-text"]')  # Gets the div containing view-lines

            view_lines: List[WebElement] = view_line_div.find_elements_by_xpath('.//div[@class="view-line"]')  # Gets the view-line elements that contain the answers
            textarea: WebElement = answer_box.find_element_by_xpath(".//textarea[@class='inputarea monaco-mouse-cursor-text']")  # This is where the answers are written

            # Clears the textarea
            textarea.send_keys(Keys.LEFT_CONTROL, "a")
            textarea.send_keys(Keys.BACKSPACE)

            # Sends the answer as keys
            for line in answers[i]:
                textarea.send_keys(line)
                textarea.send_keys(Keys.ENTER, Keys.SPACE)
                textarea.send_keys(Keys.LEFT_SHIFT, Keys.HOME)
                textarea.send_keys(Keys.BACKSPACE)
            # Submits the answer
            submit_button: WebElement = answer_box.find_elements_by_tag_name("button")[1]
            submit_button.click()

            # Wait until website has checked the assignment
            try:
                WebDriverWait(self._driver, 10).until(
                    lambda e: len(self._driver.find_elements_by_xpath("//div[@class='MuiPaper-root sc-jlZJtj QgNfY MuiPaper-elevation1 MuiPaper-rounded']")) - 1 == i - fail_count)  # Waits for all assignments to load
                print(f"Assignment {i + 1}: Done!")
            except TimeoutException:
                fail_count += 1
                print(f"Assignment {i + 1}: Server error!")

    @staticmethod
    def _save_answers(answers):
        with open('answers.json', 'w+') as outfile:
            json.dump(answers, outfile)

    @staticmethod
    def _load_answers() -> dict:
        if os.path.exists("./answers.json"):
            with open('answers.json') as json_file:
                data = json.load(json_file)
                return data
        return {}

    def get_answers(self, user: str, password: str) -> bool:
        success: bool = self.login(user, password)
        if not success:
            print("Could not login...")
            return False

        self._login_to_tmc(user, password)

        black_list: Dict[str, List[int]] = {"3": [2]}
        all_answers: dict = {"answers": {}}
        for i in range(3):
            all_answers["answers"][i] = {}  # Initializes the data
            links = self._get_assignment_links(i + 1)  # Gets the links to the assignment pages
            for x, link in enumerate(links):
                # Skips blacklisted assignment pages
                if str(i + 1) in black_list:
                    if x + 1 in black_list[str(i + 1)]:
                        continue
                self._go_to_sub_assignment(link)  # Opens an assignment page
                answers = self._get_sub_assignment_answers()  # Gets answers from that page
                if answers:
                    all_answers["answers"][i][x] = answers  # Saves those answers into a dictionary

        self._save_answers(all_answers)

        for i, a in enumerate(answers):
            print(f"{i}: {a}")

        return True

    def set_answers(self, user: str, password: str) -> bool:
        success: bool = self.login(user, password)
        if not success:
            print("Could not login...")
            return False

        assignments: Dict[str:List[List]] = self._load_answers()

        if "answers" not in assignments:
            print("Could not find answers.json. Using hard-coded answers.")
            assignments = MoocAPI.ANSWERS

        for i, assignment_key in enumerate(assignments["answers"]):
            print("X------------------------X")
            print(f"Assignment Category {i + 1}")
            links: List[str] = self._get_assignment_links(int(assignment_key) + 1)

            print("I-------------I")
            for x, sub_assignment_key in enumerate(assignments["answers"][assignment_key]):
                print(f"Sub Assignment Category {x + 1}")
                link: str = links[int(sub_assignment_key)]
                sub_assignment_answers: List[List] = assignments["answers"][assignment_key][sub_assignment_key]

                self._go_to_sub_assignment(link)
                self._set_sub_assignment_answers(sub_assignment_answers)
                print("I-------------I")

            print("X------------------------X")

        return True
