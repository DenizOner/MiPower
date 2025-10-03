# MiPower — Brugerdefineret integration til Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** er en Home Assistant-integration, der giver dig mulighed for at styre strømtilstanden for medieafspillere, som ikke understøtter traditionel Wake-on-LAN (WOL), men som kan "vækkes" via en Bluetooth-parringsanmodning. Den blev specifikt designet til enheder som Xiaomi Mi Box, men kan fungere med andre lignende Android TV-bokse.

Denne integration opretter en `switch` (kontakt) entitet i Home Assistant. 
- **Tænding** af kontakten sender en række Bluetooth-kommandoer via `bluetoothctl` for at vække enheden.
- **Slukning** af kontakten kalder `media_player.turn_off` tjenesten for den forbundne enhed.
- Kontaktens tilstand synkroniseres automatisk med tilstanden af den forbundne medieafspillerentitet.

## 🤝 Støt Projektet

MiPower-projektet udvikles med en vision om at tilføje værdi til open source-fællesskabet. Din støtte er afgørende for at bevare projektets kontinuitet og udviklingshastighed.

Hvis du sætter pris på mit arbejde, kan du støtte mig via GitHub Sponsors eller følgende platforme. På forhånd tak!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternativt kan du se alle finansieringsmuligheder ved at klikke på **Sponsor-knappen (❤️)** i øverste højre hjørne af repositoryet.

## Forudsætninger

- **Home Assistant OS / Supervised / Container:** Denne integration kræver en Linux-baseret Home Assistant-installation, hvor kommandolinjeværktøjet `bluetoothctl` er tilgængeligt og tilgængeligt. Den vil **ikke** fungere på en Home Assistant Core-installation på Windows.

## Installation via HACS (Anbefales)

Denne integration er tilgængelig som et brugerdefineret lager i HACS.

1.  Naviger til dit HACS dashboard.
2.  Klik på **Integrations** (Integrationer).
3.  Klik på menuen med de tre prikker i øverste højre hjørne og vælg **"Custom repositories"** ("Brugerdefinerede lagre").
4.  I dialogboksen skal du indtaste følgende oplysninger:
    - **Repository (Lager):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategori):** `Integration` (Integration)
5.  Klik på **"Add"** ("Tilføj").
6.  "MiPower"-integrationen vises nu på din HACS-liste. Klik på den.
7.  Klik på knappen **"Download"** ("Download") og derefter igen på **"Download"** ("Download") i det næste vindue.
8.  Når downloadet er fuldført, **skal du genstarte Home Assistant**, for at integrationen kan indlæses.

## Manuel installation

Selvom HACS er den anbefalede metode, kan du også installere integrationen manuelt.

1.  Gå til lagerets [Udgivelser side](https://github.com/DenizOner/MiPower/releases) og download `mipower.zip`-filen fra den nyeste udgivelse.
2.  Udpak den downloadede fil.
3.  Inde i den udpakkede mappe finder du en `custom_components`-mappe. Kopier `mipower`-mappen derfra.
4.  Indsæt den kopierede `mipower`-mappe i `custom_components`-mappen i din Home Assistant-konfigurationsmappe. Hvis `custom_components`-mappen ikke eksisterer, skal du oprette den.
    - Den endelige sti skal se sådan ud: `.../config/custom_components/mipower/`
5.  Genstart Home Assistant.

## Konfiguration

Efter genstart kan du tilføje og konfigurere MiPower-kontakten.

1.  Gå til **Settings > Devices & Services** (Indstillinger > Enheder og Tjenester).
2.  Klik på knappen **"+ Add Integration"** ("+ Tilføj integration") i nederste højre hjørne.
3.  Søg efter **"MiPower"** og klik på den.

### Nem opsætning (Anbefales)

Dette er den enkleste måde at konfigurere integrationen på.

1.  Når du bliver bedt om det, skal du vælge **"Easy Setup"** ("Nem opsætning").
2.  Integrationen vil automatisk opdage Bluetooth-aktiverede medieafspillere på dit system.
3.  Vælg din målenhed (f.eks. "Xiaomi Mi Box 4") fra rullemenuen.
4.  Klik på **"Submit"** ("Indsend").

Det er det! Integrationen opretter en kontakt, der er forbundet til din medieafspiller.

### Avanceret opsætning

Brug denne metode, hvis Nem opsætning ikke finder din enhed, eller hvis du skal konfigurere avancerede timingindstillinger fra starten.

1.  **Trin 1: Valg af enhed**
    - Vælg **"Advanced Setup"** ("Avanceret opsætning").
    - Vælg din målmedieafspiller fra listen over *alle* medieafspillere i din Home Assistant.
2.  **Trin 2: MAC-adresse**
    - Integrationen vil forsøge at finde Bluetooth MAC-adressen for den valgte enhed. 
    - Hvis den findes, udfyldes den på forhånd. Kontroller, at den er korrekt.
    - Hvis den ikke findes, skal du indtaste Bluetooth MAC-adressen på din enhed manuelt.
3.  **Trin 3: Timingindstillinger**
    - Du kan konfigurere forskellige timeouts og forsinkelser for Bluetooth-kommandoerne. For de fleste brugere er standardværdierne tilstrækkelige.
4.  Klik på **"Submit"** ("Indsend") for at fuldføre opsætningen.

## Indstillinger

Når du har konfigureret din MiPower-kontakt, kan du justere timingindstillingerne når som helst.

1.  Gå til **Settings > Devices & Services** (Indstillinger > Enheder og Tjenester).
2.  Find MiPower-integrationen, og klik på **"Configure"** ("Konfigurer").
3.  Juster skyderne for "debounce", timeouts og forsinkelser efter behov.

## Forklaring af timingindstillinger

I konfigurations- eller indstillingsmenuen kan du finjustere timingen af Bluetooth-kommandoerne. For de fleste brugere fungerer standardværdierne godt.

- **Turn-On Debounce (Tændingsforsinkelse):** Den mindste tid (i sekunder), der skal gå, før 'tænd'-kommandoen kan udføres igen. Dette forhindrer spam af enheden med vækningssignaler, hvis kontakten hurtigt slås til og fra.

- **Turn-Off Debounce (Slukningsforsinkelse):** Den mindste tid (i sekunder), der skal gå, før 'sluk'-kommandoen kan udføres igen. 

- **Delay Between Commands (Forsinkelse mellem kommandoer):** En meget kort forsinkelse (i sekunder) mellem afsendelse af på hinanden følgende kommandoer til `bluetoothctl`-værktøjet. På nogle systemer kan tilføjelse af en lille pause forbedre pålideligheden.

- **Process Spawn Timeout (Processtart-timeout):** Den maksimale tid (i sekunder) der skal ventes på, at `bluetoothctl`-processen starter. Hvis den ikke starter inden for denne tid, mislykkes tændingsforsøget.

- **Pairing Timeout (Parrings-timeout):** I den forenklede tændingslogik er dette den tid, der skal ventes efter afsendelse af `pair`-kommandoen, før succes antages. Det giver enheden tid til at behandle vækningssignalet.

- **Bluetooth Scan Duration (Bluetooth-scanningsvarighed):** Varigheden (i sekunder), som integrationen scanner efter Bluetooth-enheder, før den forsøger at sende parringskommandoen. En længere scanning kan hjælpe med at finde enheder, der er langsomme til at annoncere deres tilstedeværelse.

## Læs på dit eget sprog

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