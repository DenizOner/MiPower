# MiPower — Aangepaste Home Assistant-integratie

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** is een Home Assistant-integratie waarmee u de stroomstatus kunt regelen van mediaspelers die geen traditionele Wake-on-LAN (WOL) ondersteunen, maar wel kunnen worden "gewekt" door een Bluetooth-koppelingsverzoek. Het is specifiek ontworpen voor apparaten zoals de Xiaomi Mi Box, maar kan ook werken met andere vergelijkbare Android TV-boxen.

Deze integratie creëert een `switch` (schakelaar)-entiteit in Home Assistant. 
- **Het AANZETTEN** van de schakelaar stuurt een reeks Bluetooth-commando's via `bluetoothctl` om het apparaat wakker te maken.
- **Het UITZETTEN** van de schakelaar roept de `media_player.turn_off`-service aan voor het gekoppelde apparaat.
- De status van de schakelaar wordt automatisch gesynchroniseerd met de status van de gekoppelde mediaspeler-entiteit.

## 🤝 Steun Ons

Het MiPower-project wordt ontwikkeld met de visie om waarde toe te voegen aan de open source-gemeenschap. Uw steun is van vitaal belang om de continuïteit en ontwikkelingssnelheid van dit project te behouden.

Als u mijn inspanningen waardeert, kunt u mij steunen via GitHub Sponsors of de volgende platforms. Alvast bedankt!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Als alternatief kunt u alle financieringsopties bekijken door te klikken op de **Sponsor-knop (❤️)** in de rechterbovenhoek van de repository.

## Vereisten

- **Home Assistant OS / Supervised / Container:** Voor deze integratie is een Linux-gebaseerde Home Assistant-installatie vereist, waarbij de `bluetoothctl` commandoregeltool beschikbaar en toegankelijk is. Het zal **niet** werken op een Home Assistant Core-installatie op Windows.

## Installatie via HACS (Aanbevolen)

Deze integratie is beschikbaar als een aangepaste repository in HACS.

1.  Navigeer naar uw HACS-dashboard.
2.  Klik op **Integrations** (Integraties).
3.  Klik op het drie-puntjesmenu in de rechterbovenhoek en selecteer **"Custom repositories"** ("Aangepaste repositories").
4.  Voer in het dialoogvenster de volgende informatie in:
    - **Repository:** `https://github.com/DenizOner/MiPower`
    - **Category (Categorie):** `Integration` (Integratie)
5.  Klik op **"Add"** ("Toevoegen").
6.  De "MiPower"-integratie verschijnt nu in uw HACS-lijst. Klik erop.
7.  Klik op de **"Download"** ("Downloaden") knop en vervolgens nogmaals op **"Download"** ("Downloaden") in het volgende venster.
8.  Nadat de download is voltooid, **moet u Home Assistant herstarten** om de integratie te laden.

## Handmatige installatie

Hoewel HACS de aanbevolen methode is, kunt u de integratie ook handmatig installeren.

1.  Ga naar de [Releases-pagina](https://github.com/DenizOner/MiPower/releases) van de repository en download het `mipower.zip`-bestand van de nieuwste release.
2.  Pak het gedownloade bestand uit.
3.  Binnen de uitgepakte map vindt u een `custom_components`-map. Kopieer de `mipower`-map hieruit.
4.  Plak de gekopieerde `mipower`-map in de `custom_components`-map in uw Home Assistant-configuratiedirectory. Als de `custom_components`-map niet bestaat, moet u deze aanmaken.
    - Het uiteindelijke pad moet er als volgt uitzien: `.../config/custom_components/mipower/`
5.  Herstart Home Assistant.

## Configuratie

Na het herstarten kunt u de MiPower-schakelaar toevoegen en configureren.

1.  Ga naar **Settings > Devices & Services** (Instellingen > Apparaten & Services).
2.  Klik op de **"+ Add Integration"** ("+ Integratie Toevoegen") knop in de rechterbenedenhoek.
3.  Zoek naar **"MiPower"** en klik erop.

### Eenvoudige installatie (Aanbevolen)

Dit is de eenvoudigste manier om de integratie te configureren.

1.  Kies, wanneer daarom gevraagd wordt, **"Easy Setup"** ("Eenvoudige Installatie").
2.  De integratie zal automatisch Bluetooth-apparaten met mediaspeler-functionaliteit op uw systeem detecteren.
3.  Selecteer uw doelapparaat (bijv. "Xiaomi Mi Box 4") uit de vervolgkeuzelijst.
4.  Klik op **"Submit"** ("Verzenden").

Dat is alles! De integratie maakt een schakelaar die aan uw mediaspeler is gekoppeld.

### Geavanceerde installatie

Gebruik deze methode als de Eenvoudige installatie uw apparaat niet vindt of als u vanaf het begin geavanceerde timing-instellingen moet configureren.

1.  **Stap 1: Apparaatselectie**
    - Kies **"Advanced Setup"** ("Geavanceerde Installatie").
    - Selecteer uw doelmediaspeler uit de lijst met *alle* mediaspelers in uw Home Assistant.
2.  **Stap 2: MAC-adres**
    - De integratie zal proberen het Bluetooth MAC-adres van het geselecteerde apparaat te vinden. 
    - Indien gevonden, wordt dit vooraf ingevuld. Controleer of het correct is.
    - Indien niet gevonden, moet u handmatig het Bluetooth MAC-adres van uw apparaat invoeren.
3.  **Stap 3: Timing-instellingen**
    - U kunt verschillende time-outs en vertragingen configureren voor de Bluetooth-commando's. Voor de meeste gebruikers zijn de standaardwaarden voldoende.
4.  Klik op **"Submit"** ("Verzenden") om de installatie te voltooien.

## Opties

Nadat u uw MiPower-schakelaar heeft geconfigureerd, kunt u de timing-instellingen op elk gewenst moment aanpassen.

1.  Ga naar **Settings > Devices & Services** (Instellingen > Apparaten & Services).
2.  Zoek de MiPower-integratie en klik op **"Configure"** ("Configureren").
3.  Pas de schuifregelaars voor *debounce*, time-outs en vertragingen indien nodig aan.

## Uitleg van de Timing-instellingen

In het configuratie- of optiemenu kunt u de timing van de Bluetooth-commando's verfijnen. Voor de meeste gebruikers werken de standaardwaarden goed.

- **Turn-On Debounce (Aanzetten Debounce):** De minimale tijd (in seconden) die moet verstrijken voordat het 'aanzetten'-commando opnieuw kan worden uitgevoerd. Dit voorkomt dat het apparaat wordt gespamd met weksignalen als de schakelaar snel wordt omgeschakeld.

- **Turn-Off Debounce (Uitzetten Debounce):** De minimale tijd (in seconden) die moet verstrijken voordat het 'uitzetten'-commando opnieuw kan worden uitgevoerd. 

- **Delay Between Commands (Vertraging Tussen Commando's):** Een zeer korte vertraging (in seconden) tussen het verzenden van opeenvolgende commando's naar het `bluetoothctl`-hulpprogramma. Op sommige systemen kan het toevoegen van een kleine pauze de betrouwbaarheid verbeteren.

- **Process Spawn Timeout (Proces Start Time-out):** De maximale tijd (in seconden) om te wachten tot het `bluetoothctl`-proces start. Als het niet binnen deze tijd start, mislukt de poging om aan te zetten.

- **Pairing Timeout (Koppel Time-out):** In de vereenvoudigde aanzet-logica is dit de hoeveelheid tijd om te wachten na het verzenden van het `pair`-commando voordat succes wordt aangenomen. Het geeft het apparaat tijd om het weksignaal te verwerken.

- **Bluetooth Scan Duration (Bluetooth Scan Duur):** De duur (in seconden) dat de integratie naar Bluetooth-apparaten zal scannen voordat wordt geprobeerd het koppelcommando te verzenden. Een langere scan kan helpen bij het vinden van apparaten die traag zijn in het adverteren van hun aanwezigheid.

## Lees in uw eigen taal

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