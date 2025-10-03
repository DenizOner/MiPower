# MiPower — Integracija po meri za Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** je integracija za Home Assistant, ki omogoča nadzor stanja napajanja medijskih predvajalnikov, ki ne podpirajo tradicionalnega Wake-on-LAN (WOL), vendar jih je mogoče "prebuditi" z zahtevo za seznanjanje Bluetooth. Zasnovan je bil posebej za naprave, kot je Xiaomi Mi Box, vendar lahko deluje tudi z drugimi podobnimi napravami Android TV Box.

Ta integracija ustvari entiteto `switch` (stikalo) v Home Assistant. 
- **Vklop** stikala pošlje niz ukazov Bluetooth prek `bluetoothctl` za prebujanje naprave.
- **Izklop** stikala pokliče storitev `media_player.turn_off` za povezano napravo.
- Stanje stikala se samodejno sinhronizira s stanjem entitete povezanega medijskega predvajalnika.
## 🤝 Podprite Nas

Projekt MiPower se razvija z vizijo dodajanja vrednosti skupnosti odprte kode. Vaša podpora je ključnega pomena za ohranjanje kontinuitete in hitrosti razvoja tega projekta.

Če cenite moje delo, me lahko podprete preko GitHub Sponzorjev ali naslednjih platform. Hvala vnaprej!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Druga možnost je, da si ogledate vse možnosti financiranja s klikom na **gumb Sponzor (❤️)** v zgornjem desnem kotu repozitorija.

## Predpogoji

- **Home Assistant OS / Supervised / Container:** Ta integracija zahteva namestitev Home Assistant na osnovi Linuxa, kjer je orodje ukazne vrstice `bluetoothctl` na voljo in dostopno. **Ne** bo delovalo na namestitvi Home Assistant Core v sistemu Windows.

## Namestitev prek HACS (Priporočeno)

Ta integracija je na voljo kot repozitorij po meri v HACS.

1.  Pojdite na svojo nadzorno ploščo HACS.
2.  Kliknite **Integrations** (Integracije).
3.  Kliknite meni s tremi pikami v zgornjem desnem kotu in izberite **"Custom repositories"** ("Repozitoriji po meri").
4.  V pogovorno okno vnesite naslednje informacije:
    - **Repository (Repozitorij):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategorija):** `Integration` (Integracija)
5.  Kliknite **"Add"** ("Dodaj").
6.  Integracija "MiPower" se bo zdaj prikazala na vašem seznamu HACS. Kliknite nanjo.
7.  Kliknite gumb **"Download"** ("Prenesi") in nato ponovno **"Download"** ("Prenesi") v naslednjem oknu.
8.  Po končanem prenosu **MORATE ponovno zagnati Home Assistant**, da se integracija naloži.

## Ročna namestitev

Čeprav je HACS priporočena metoda, lahko integracijo namestite tudi ročno.

1.  Pojdite na [stran z izdajami](https://github.com/DenizOner/MiPower/releases) repozitorija in prenesite datoteko `mipower.zip` iz najnovejše izdaje.
2.  Razpakirajte preneseno datoteko.
3.  Znotraj razpakirane mape boste našli imenik `custom_components`. Kopirajte mapo `mipower` iz nje.
4.  Prilepite skopirano mapo `mipower` v mapo `custom_components` v vašem konfiguracijskem imeniku Home Assistant. Če mapa `custom_components` ne obstaja, jo morate ustvariti.
    - Končna pot bi morala izgledati takole: `.../config/custom_components/mipower/`
5.  Ponovno zaženite Home Assistant.

## Konfiguracija

Po ponovnem zagonu lahko dodate in konfigurirate stikalo MiPower.

1.  Pojdite na **Settings > Devices & Services** (Nastavitve > Naprave in Storitve).
2.  Kliknite gumb **"+ Add Integration"** ("+ Dodaj Integracijo") v spodnjem desnem kotu.
3.  Poiščite **"MiPower"** in kliknite nanj.

### Enostavna nastavitev (Priporočeno)

To je najpreprostejši način za konfiguriranje integracije.

1.  Ko ste pozvani, izberite **"Easy Setup"** ("Enostavna Nastavitev").
2.  Integracija bo samodejno odkrila medijske predvajalnike, ki podpirajo Bluetooth v vašem sistemu.
3.  Izberite ciljno napravo (npr. "Xiaomi Mi Box 4") s spustnega seznama.
4.  Kliknite **"Submit"** ("Pošlji").

To je to! Integracija bo ustvarila stikalo, povezano z vašim medijskim predvajalnikom.

### Napredna nastavitev

To metodo uporabite, če Enostavna nastavitev ne najde vaše naprave ali če morate od začetka konfigurirati napredne nastavitve časov.

1.  **1. korak: Izbira naprave**
    - Izberite **"Advanced Setup"** ("Napredna Nastavitev").
    - Izberite ciljni medijski predvajalnik s seznama *vseh* medijskih predvajalnikov v vašem Home Assistant.
2.  **2. korak: MAC naslov**
    - Integracija bo poskušala najti MAC naslov Bluetooth izbrane naprave. 
    - Če ga najde, bo predhodno izpolnjen. Preverite, ali je pravilen.
    - Če ga ne najde, morate ročno vnesti MAC naslov Bluetooth vaše naprave.
3.  **3. korak: Nastavitve časov**
    - Za ukaze Bluetooth lahko konfigurirate različne časovne omejitve in zamude. Za večino uporabnikov so privzete vrednosti zadostne.
4.  Kliknite **"Submit"** ("Pošlji") za dokončanje nastavitve.

## Možnosti

Ko konfigurirate stikalo MiPower, lahko kadar koli prilagodite nastavitve časov.

1.  Pojdite na **Settings > Devices & Services** (Nastavitve > Naprave in Storitve).
2.  Poiščite integracijo MiPower in kliknite **"Configure"** ("Konfiguriraj").
3.  Po potrebi prilagodite drsnike za *debounce*, časovne omejitve in zamude.

## Razlaga nastavitev časov

V meniju za konfiguracijo ali možnosti lahko natančno nastavite čas ukazov Bluetooth. Za večino uporabnikov privzete vrednosti delujejo dobro.

- **Turn-On Debounce (Dušenje Vklopa):** Minimalni čas (v sekundah), ki mora preteči, preden se lahko ukaz 'vklopi' ponovno izvede. To preprečuje, da bi se naprava preplavila s signali za prebujanje, če se stikalo hitro preklopi.

- **Turn-Off Debounce (Dušenje Izklopa):** Minimalni čas (v sekundah), ki mora preteči, preden se lahko ukaz 'izklopi' ponovno izvede. 

- **Delay Between Commands (Zamik med ukazi):** Zelo kratek zamik (v sekundah) med pošiljanjem zaporednih ukazov pripomočku `bluetoothctl`. V nekaterih sistemih lahko dodajanje majhnega premora izboljša zanesljivost.

- **Process Spawn Timeout (Časovna omejitev zagona procesa):** Najdaljši čas (v sekundah) čakanja na zagon procesa `bluetoothctl`. Če se v tem času ne zažene, poskus vklopa ne bo uspel.

- **Pairing Timeout (Časovna omejitev seznanjanja):** Pri poenostavljeni logiki vklopa je to čas čakanja po pošiljanju ukaza `pair`, preden se domneva uspeh. Napravi daje čas za obdelavo signala za prebujanje.

- **Bluetooth Scan Duration (Trajanje skeniranja Bluetooth):** Trajanje (v sekundah), ki ga bo integracija skenirala za naprave Bluetooth, preden poskusi poslati ukaz za seznanjanje. Daljše skeniranje lahko pomaga najti naprave, ki počasi oglašujejo svojo prisotnost.

## Berite v svojem jeziku

*   [Afrikaans](README.af.md)
*   [العربية (Arabic)](README.ar.md)
*   [български (Bulgarian)](README.bg.md)
*   [বাংলা (Bengali)](README.bn.md)
*   [Català (Catalan)](README.ca.md)
*   [Čeština (Czech)](README.cs.md)
*   [Dansk (Danish)](README.da.md)
*   [Deutsch (German)](README.de.md)
*   [Deutsch (Schweiz) (German, Switzerland)](README.de-CH.md)
*   [Ελληνικά (Greek)](README.el.md)
*   [English](../README.md)
*   [Español (Spanish)](README.es.md)
*   [Eesti (Estonian)](README.et.md)
*   [Euskara (Basque)](README.eu.md)
*   [فارسی (Persian)](README.fa.md)
*   [Suomi (Finnish)](README.fi.md)
*   [Français (French)](README.fr.md)
*   [Gaeilge (Irish)](README.ga.md)
*   [Galego (Galician)](README.gl.md)
*   [ગુજરાતી (Gujarati)](README.gu.md)
*   [עברית (Hebrew)](README.he.md)
*   [हिन्दी (Hindi)](README.hi.md)
*   [Hrvatski (Croatian)](README.hr.md)
*   [Magyar (Hungarian)](README.hu.md)
*   [Bahasa Indonesia (Indonesian)](README.id.md)
*   [Íslenska (Icelandic)](README.is.md)
*   [Italiano (Italian)](README.it.md)
*   [日本語 (Japanese)](README.ja.md)
*   [ქართული (Georgian)](README.ka.md)
*   [ಕನ್ನಡ (Kannada)](README.kn.md)
*   [한국어 (Korean)](README.ko.md)
*   [Kernewek (Cornish)](README.kw.md)
*   [Lëtzebuergesch (Luxembourgish)](README.lb.md)
*   [Lietuvių (Lithuanian)](README.lt.md)
*   [Latviešu (Latvian)](README.lv.md)
*   [മലയാളം (Malayalam)](README.ml.md)
*   [Монгол (Mongolian)](README.mn.md)
*   [मराठी (Marathi)](README.mr.md)
*   [Bahasa Melayu (Malay)](README.ms.md)
*   [Norsk bokmål (Norwegian Bokmål)](README.nb.md)
*   [नेपाली (Nepali)](README.ne.md)
*   [Nederlands (Dutch)](README.nl.md)
*   [Polski (Polish)](README.pl.md)
*   [Português (Portuguese)](README.pt.md)
*   [Português (Brasil) (Portuguese, Brazil)](README.pt-BR.md)
*   [Română (Romanian)](README.ro.md)
*   [Русский (Russian)](README.ru.md)
*   [Slovenčina (Slovak)](README.sk.md)
*   [Slovenščina (Slovenian)](README.sl.md)
*   [Српски (Serbian)](README.sr.md)
*   [Srpski (latinica) (Serbian, Latin)](README.sr-Latn.md)
*   [Svenska (Swedish)](README.sv.md)
*   [Kiswahili (Swahili)](README.sw.md)
*   [తెలుగు (Telugu)](README.te.md)
*   [ไทย (Thai)](README.th.md)
*   [Türkçe (Turkish)](README.tr.md)
*   [Українська (Ukrainian)](README.uk.md)
*   [اردو (Urdu)](README.ur.md)
*   [Tiếng Việt (Vietnamese)](README.vi.md)
*   [简体中文 (Simplified Chinese)](README.zh-CN.md)
*   [繁體中文 (香港) (Traditional Chinese, Hong Kong)](README.zh-HK.md)

---