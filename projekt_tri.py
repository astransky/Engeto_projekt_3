author =(
'''
projekt_tri.py: treti projekt do Engeto Online Python Akademie
author: Ales Stransky
email: ales.stransky@seznam.cz
discord: Ales S#5138
''')


from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys

global handle_csv_soubor

hlavicka = 'code,location,registered,envelopes,valid,Občanská demokratická strana,Řád národa - Vlastenecká unie,\
CESTA ODPOVĚDNÉ SPOLEČNOSTI,Česká str.sociálně demokrat.,Volte Pr.Blok www.cibulka.net,Radostné Česko,\
STAROSTOVÉ A NEZÁVISLÍ,Komunistická str.Čech a Moravy,Strana zelených,"ROZUMNÍ-stop migraci,diktát.EU",\
Společ.proti výst.v Prok.údolí,Strana svobodných občanů,Blok proti islam.-Obran.domova,Občanská demokratická aliance,\
Česká pirátská strana,OBČANÉ 2011-SPRAVEDL. PRO LIDI,Unie H.A.V.E.L.,Česká národní fronta,Referendum o Evropské unii,\
TOP 09,ANO 2011,Dobrá volba 2016,SPR-Republ.str.Čsl. M.Sládka,Křesť.demokr.unie-Čs.str.lid.,\
Česká strana národně sociální,REALISTÉ,SPORTOVCI,Dělnic.str.sociální spravedl.,Svob.a př.dem.-T.Okamura (SPD),\
Strana Práv Občanů,Národ Sobě'


def dej_udaj_z_bunky(bunka):
    udaj=""
    start_pozice=bunka.index('">')+2
    end_pozice=bunka.index('</td>')
    udaj=str(bunka)[start_pozice:end_pozice] 
    
    udaj = udaj.replace("&nbsp;" , " ")
    return udaj


def jake_odkazy_je_mozne_zadat(adresa):
    absolutni_odkazy=[]
    base_url = adresa
    odpoved = get(adresa)
  
    rozdelene_html = BeautifulSoup(odpoved.text, features="html.parser")

    for a in rozdelene_html.find_all('a', href=True):
      # prevod relativniho odkazu na absolutni
        odkazy_absolute_url = urljoin(base_url, a['href'])
        absolutni_odkazy.append(odkazy_absolute_url)
  
    kontrolni_odkazy=[]
    for odkaz in absolutni_odkazy:
        if (odkaz[33:35] == "32"):
            kontrolni_odkazy.append(odkaz)
          
    return(kontrolni_odkazy)




def Vygeneruj_odkazy_na_obce(odkaz_z_parametru):
 
  odpoved = get(odkaz_z_parametru)
  soup = BeautifulSoup(odpoved.text, features="html.parser")
  base_url = odkaz_z_parametru

  vsechny_odkazy=[]
  for a in soup.find_all('a', href=True):
    # prevod relativniho odkazu na absolutni
    absolute_url = urljoin(base_url, a['href'])
    vsechny_odkazy.append(absolute_url)
  
  
  odkazy=list(soup.find_all("a"))
  odkazy_na_obce=[]
  for i in range(len(odkazy)):
      veta=str(odkazy[i])
      if (veta.count(">X</a>")):
          odkazy_na_obce.append(vsechny_odkazy[i-1])  

  return(odkazy_na_obce)


 


def zpracuj_dilci_obci(odkaz_na_obci) : 
  global handle_csv_soubor    

  vysledky_stran=[]
  for i in range(32):
      vysledky_stran.append("-")
  
  veta=str(odkaz_na_obci)
  cislo_obce=veta[veta.index("xobec=")+6 : veta.index("xobec=")+12 ]  
  
  
  
  celkovy_html_kod_obce = get(odkaz_na_obci)
  html_kod_obce = BeautifulSoup(celkovy_html_kod_obce.text, features="html.parser")

  list_jmeno_obce=list(html_kod_obce.find_all("h3", limit=3))
  
  veta=str(list_jmeno_obce[1])   #pro Prahu
  if (veta.count("Obec:")):
      jmeno_obce=veta[veta.index("Obec:")+6:veta.index("<h3>")-6]
  else:
     veta=str(list_jmeno_obce[2])
     jmeno_obce=veta[veta.index("Obec:")+6:veta.index("<h3>")-6]



  #volici v seznamu
  bunka=str( html_kod_obce.select_one(
        ".table > tr:nth-child(3) > td:nth-child(4)")
        )
  volici=dej_udaj_z_bunky(bunka)

  #vydane obalky
  bunka=str( html_kod_obce.select_one(
        ".table > tr:nth-child(3) > td:nth-child(5)")
        )
  obalky=dej_udaj_z_bunky(bunka)

  #platne hlasy
  bunka=str( html_kod_obce.select_one(
        ".table > tr:nth-child(3) > td:nth-child(8)")
        )
  hlasy=dej_udaj_z_bunky(bunka)



  list_html_kod_obce = (celkovy_html_kod_obce.text).split("\n")
  
  # LEVA TABULKA
  zacatek_tabulky = list_html_kod_obce.index('Popis tabulky') + 4
  
  konec_tabulky=zacatek_tabulky
  #na kterem radku tabulka konci:
  while list_html_kod_obce[konec_tabulky]  != "</table>":
      konec_tabulky+=1
      
  i=0
  while (zacatek_tabulky+13)+i*7 < konec_tabulky:

      bunka=list_html_kod_obce[(zacatek_tabulky+13)+i*7] #cislo strany
      cislo_strany=dej_udaj_z_bunky(bunka)
      bunka=list_html_kod_obce[(zacatek_tabulky+13)+i*7 +2]  #platne hlasy
      hlasu=dej_udaj_z_bunky(bunka)

      if (cislo_strany != "-"):
          vysledky_stran[int(cislo_strany)]=hlasu
      i+=1


  # PRAVA TABULKA
  zacatek_tabulky= konec_tabulky +12   # konec predchozi tabulky + 12

  #na kterem radku tabulka konci:
  konec_tabulky=zacatek_tabulky
  while list_html_kod_obce[konec_tabulky]  != "</table>":
      konec_tabulky+=1
      
  
  i=0
  while (zacatek_tabulky+13)+i*7 < konec_tabulky:
    
      bunka=list_html_kod_obce[(zacatek_tabulky+13)+i*7] #cislo strany
      cislo_strany=dej_udaj_z_bunky(bunka)
      bunka=list_html_kod_obce[(zacatek_tabulky+13)+i*7 +2]  #platne hlasy
      hlasu=dej_udaj_z_bunky(bunka)

      if (cislo_strany != "-"):
          vysledky_stran[int(cislo_strany)]=hlasu
      i+=1
  
  
  handle_csv_soubor.write(f"\n{cislo_obce},{jmeno_obce},{volici},{obalky},{hlasy}")
  
  for i in range(1,32):
      handle_csv_soubor.write(","+ vysledky_stran[i])
  
  



##############################################         Zacatek programu          ###################################################

url_hlavni_stranky="https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
kontrolni_odkazy=jake_odkazy_je_mozne_zadat(url_hlavni_stranky)
#print (kontrolni_odkazy)

odkaz_z_parametru=str(sys.argv[1])  # prvni argument
jmeno_souboru=str(sys.argv[2])      # druhy argument


#print(odkaz_z_parametru)
#print(jmeno_souboru)
#odkaz_z_parametru="https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
#jmeno_souboru="vysledky_prostejov1.csv"

if not(odkaz_z_parametru in kontrolni_odkazy):
    print ("Jako prvni parametr byl zadan nespravny webovy odkaz, beh programu je ukoncen")
    quit()

handle_csv_soubor = open(jmeno_souboru, mode="w")
handle_csv_soubor.write(hlavicka)

odkazy_na_obce=Vygeneruj_odkazy_na_obce(odkaz_z_parametru)

for odkaz in odkazy_na_obce:
    zpracuj_dilci_obci(odkaz)

#odkaz_na_dilci_obci= "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=506761&xvyber=7103"
#zpracuj_dilci_obci(odkaz_na_dilci_obci) 

handle_csv_soubor.close()