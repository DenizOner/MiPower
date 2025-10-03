# MiPower — Home Assistant tilpasset integrasjon

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** er en Home Assistant-integrasjon som lar deg kontrollere strømtilstanden til mediespillere som ikke støtter tradisjonell Wake-on-LAN (WOL), men som kan "vekkes" av en Bluetooth-sammenkoblingsforespørsel. Den ble spesielt designet for enheter som Xiaomi Mi Box, men kan fungere med andre lignende Android TV-bokser.

Denne integrasjonen oppretter en `switch` (bryter)-entitet i Home Assistant. 
- **Å slå PÅ** bryteren sender en serie Bluetooth-kommandoer via `bluetoothctl` for å vekke enheten.
- **Å slå AV** bryteren kaller opp `media_player.turn_off`-tjenesten for den tilknyttede enheten.
- Bryterens tilstand synkroniseres automatisk med tilstanden til den tilknyttede mediespiller-entiteten.

## 🤝 Støtt Prosjektet

MiPower-prosjektet utvikles med en visjon om å tilføre verdi til åpen kildekode-samfunnet. Din støtte er avgjørende for å opprettholde kontinuiteten og utviklingshastigheten i dette prosjektet.

Hvis du verdsetter arbeidet mitt, kan du støtte meg via GitHub Sponsors eller følgende plattformer. Takk på forhånd!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternativt kan du se alle finansieringsalternativene ved å klikke på **Sponsor-knappen (❤️)** i øvre høyre hjørne av depotet.

## Forutsetninger

- **Home Assistant OS / Supervised / Container:** Denne integrasjonen krever en Linux-basert Home Assistant-installasjon der kommandolinjeverktøyet `bluetoothctl` er tilgjengelig og kan nås. Den vil **IKKE** fungere på en Home Assistant Core-installasjon på Windows.

## Installasjon via HACS (Anbefalt)

Denne integrasjonen er tilgjengelig som et tilpasset repositorium i HACS.

1.  Naviger til HACS-oversikten din.
2.  Klikk på **Integrations** (Integrasjoner).
3.  Klikk på tremenyen øverst til høyre og velg **"Custom repositories"** ("Tilpassede repositorier").
4.  I dialogboksen, skriv inn følgende informasjon:
    - **Repository (Repositorium):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategori):** `Integration` (Integrasjon)
5.  Klikk **"Add"** ("Legg til").
6.  "MiPower"-integrasjonen vil nå vises i HACS-listen din. Klikk på den.
7.  Klikk på **"Download"** ("Last ned")-knappen og deretter på **"Download"** ("Last ned") igjen i neste vindu.
8.  Etter at nedlastingen er fullført, **MÅ du starte Home Assistant på nytt** for at integrasjonen skal lastes inn.

## Manuell installasjon

Selv om HACS er den anbefalte metoden, kan du også installere integrasjonen manuelt.

1.  Gå til repositoriets [Utgivelsesside](https://github.com/DenizOner/MiPower/releases) og last ned `mipower.zip`-filen fra den nyeste utgivelsen.
2.  Pakk ut den nedlastede filen.
3.  Inne i den utpakkede mappen finner du en `custom_components`-mappe. Kopier `mipower`-mappen derfra.
4.  Lim inn den kopierte `mipower`-mappen i `custom_components`-mappen i Home Assistant-konfigurasjonskatalogen. Hvis `custom_components`-mappen ikke eksisterer, må du opprette den.
    - Den endelige stien skal se slik ut: `.../config/custom_components/mipower/`
5.  Start Home Assistant på nytt.

## Konfigurasjon

Etter omstarten kan du legge til og konfigurere MiPower-bryteren.

1.  Gå til **Settings > Devices & Services** (Innstillinger > Enheter og Tjenester).
2.  Klikk på **"+ Add Integration"** ("+ Legg til Integrasjon")-knappen nederst til høyre.
3.  Søk etter **"MiPower"** og klikk på den.

### Enkelt oppsett (Anbefalt)

Dette er den enkleste måten å konfigurere integrasjonen på.

1.  Når du blir bedt om det, velg **"Easy Setup"** ("Enkelt oppsett").
2.  Integrasjonen vil automatisk oppdage Bluetooth-aktiverte mediespillere på systemet ditt.
3.  Velg målenheten din (f.eks. "Xiaomi Mi Box 4") fra rullegardinlisten.
4.  Klikk **"Submit"** ("Send inn").

Det er det! Integrasjonen vil opprette en bryter som er koblet til mediespilleren din.

### Avansert oppsett

Bruk denne metoden hvis Enkelt oppsett ikke finner enheten din, eller hvis du trenger å konfigurere avanserte tidsinnstillinger fra starten.

1.  **Trinn 1: Enhetsvalg**
    - Velg **"Advanced Setup"** ("Avansert oppsett").
    - Velg målenhet for mediespilleren fra listen over *alle* mediespillere i Home Assistant.
2.  **Trinn 2: MAC-adresse**
    - Integrasjonen vil prøve å finne Bluetooth MAC-adressen til den valgte enheten. 
    - Hvis den blir funnet, vil den forhåndsutfylles. Bekreft at den er riktig.
    - Hvis den ikke blir funnet, må du manuelt angi Bluetooth MAC-adressen til enheten din.
3.  **Trinn 3: Tidsinnstillinger**
    - Du kan konfigurere ulike tidsavbrudd og forsinkelser for Bluetooth-kommandoene. For de fleste brukere er standardverdiene tilstrekkelige.
4.  Klikk **"Submit"** ("Send inn") for å fullføre oppsettet.

## Alternativer

Når du har konfigurert MiPower-bryteren din, kan du når som helst justere tidsinnstillingene.

1.  Gå til **Settings > Devices & Services** (Innstillinger > Enheter og Tjenester).
2.  Finn MiPower-integrasjonen og klikk **"Configure"** ("Konfigurer").
3.  Juster glidebryterne for *debounce*, tidsavbrudd og forsinkelser etter behov.

## Forklaring av Tidsinnstillinger

I konfigurasjons- eller alternativer-menyen kan du finjustere timingen av Bluetooth-kommandoene. For de fleste brukere fungerer standardverdiene bra.

- **Turn-On Debounce (Påslagsforsinkelse):** Minimum tid (i sekunder) som må gå før 'slå på'-kommandoen kan utføres igjen. Dette forhindrer spamming av enheten med vekkesignaler hvis bryteren veksles raskt.

- **Turn-Off Debounce (Avslagsforsinkelse):** Minimum tid (i sekunder) som må gå før 'slå av'-kommandoen kan utføres igjen. 

- **Delay Between Commands (Forsinkelse mellom kommandoer):** En veldig kort forsinkelse (i sekunder) mellom sending av påfølgende kommandoer til `bluetoothctl`-verktøyet. På enkelte systemer kan det å legge til en liten pause forbedre påliteligheten.

- **Process Spawn Timeout (Prosessstart Tidsavbrudd):** Maksimal tid (i sekunder) å vente på at `bluetoothctl`-prosessen skal starte. Hvis den ikke klarer å starte innen denne tiden, vil påslagsforsøket mislykkes.

- **Pairing Timeout (Sammenkobling Tidsavbrudd):** I den forenklede påslagslogikken er dette tiden du skal vente etter at du har sendt `pair`-kommandoen før du antar suksess. Det gir enheten tid til å behandle vekkesignalet.

- **Bluetooth Scan Duration (Bluetooth Skannelengde):** Varigheten (i sekunder) som integrasjonen vil skanne etter Bluetooth-enheter før den prøver å sende sammenkoblingskommandoen. En lengre skanning kan hjelpe til med å finne enheter som er trege med å annonsere sin tilstedeværelse.

## Les på ditt eget språk

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