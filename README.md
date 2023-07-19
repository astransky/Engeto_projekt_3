# Engeto_projekt_3
Treti python projekt

Hodně úspěchů při použití aplikace Třetí_projekt. Pro její instalaci je vhodné si vytvořit pythonovské virtuální prostředí – v příkazovém řádku zadat "python -m venv prostredi_tretiho_projektu", tak se vytvoří adresář "prostredi_tretiho_projektu", sem si nakopírujeme soubory  projekt_tri.py a requirements.txt a zde provedeme aktivaci virtuálního prostředí – ve windows příkazem Scripts\Activate. Potřebné knihovny se pak z příkazového řádku nainstalují příkazem "python -m pip install -r requirements.txt". 
Vlastní aplikaci spustíme v příkazovém řádku povelem:  projekt_tri .py "parametr1" "parametr2", kde jako parametr1 uvedeme url link na zvolený územní celek vybraný z internetové stránky https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ a parametr2 je název csv souboru, do kterého aplikace uloží volební výsledky ze zvoleného územního celku.  Příklad:
projekt_tri.py "https://volby.cz/pls/ps2017nss/ps32xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_prostejov1.csv"  .
Územní celky, které je možné z výše uvedené internetové stránky vybrat (tj. zadat jejich url jako parametr1) a pro které umí aplikace zpracovat výsledky jsou všechny odkazy X ve sloupci "Výběr obce", mimo odkazu Zahraničí.

