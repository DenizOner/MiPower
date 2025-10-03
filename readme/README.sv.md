# MiPower — Anpassad Home Assistant-integration

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** är en Home Assistant-integration som låter dig styra strömstatusen för mediaspelare som inte stöder traditionell Wake-on-LAN (WOL) men som kan "väckas" av en Bluetooth-parningsförfrågan. Den är specifikt utformad för enheter som Xiaomi Mi Box, men kan fungera med andra liknande Android TV-boxar.

Denna integration skapar en `switch`-entitet (strömbrytare) i Home Assistant. 
- **Att slå PÅ** strömbrytaren skickar en serie Bluetooth-kommandon via `bluetoothctl` för att väcka enheten.
- **Att slå AV** strömbrytaren anropar tjänsten `media_player.turn_off` för den länkade enheten.
- Strömbrytarens tillstånd synkroniseras automatiskt med tillståndet för den länkade mediaspelarentiteten.

## 🤝 Stöd Projektet

MiPower-projektet utvecklas med visionen att tillföra värde till open source-communityn. Ditt stöd är avgörande för att upprätthålla kontinuiteten och utvecklingshastigheten i detta projekt.

Om du uppskattar mitt arbete kan du stödja mig via GitHub Sponsors eller följande plattformar. Tack på förhand!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternativt kan du se alla finansieringsalternativ genom att klicka på **Sponsor-knappen (❤️)** i repositoryts övre högra hörn.

## Förutsättningar

- **Home Assistant OS / Supervised / Container:** Denna integration kräver en Linux-baserad Home Assistant-installation där kommandoradsverktyget `bluetoothctl` är tillgängligt och åtkomligt. Den kommer **INTE** att fungera på en Home Assistant Core-installation på Windows.

## Installation via HACS (Rekommenderas)

Denna integration är tillgänglig som ett anpassat arkiv (custom repository) i HACS.

1.  Navigera till din HACS-översikt.
2.  Klicka på **Integrations** (Integrationer).
3.  Klicka på menyn med tre punkter i det övre högra hörnet och välj **"Custom repositories"** ("Anpassade arkiv").
4.  I dialogrutan anger du följande information:
    - **Repository (Arkiv):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategori):** `Integration` (Integration)
5.  Klicka på **"Add"** ("Lägg till").
6.  "MiPower"-integrationen kommer nu att visas i din HACS-lista. Klicka på den.
7.  Klicka på knappen **"Download"** ("Ladda ner") och sedan på **"Download"** ("Ladda ner") igen i nästa fönster.
8.  När nedladdningen är klar **MÅSTE du starta om Home Assistant** för att integrationen ska laddas.

## Manuell installation

Även om HACS är den rekommenderade metoden, kan du också installera integrationen manuellt.

1.  Gå till arkivets [Sida för utgåvor (Releases)](https://github.com/DenizOner/MiPower/releases) och ladda ner filen `mipower.zip` från den senaste utgåvan.
2.  Packa upp den nedladdade filen.
3.  Inuti den uppackade mappen hittar du en katalog `custom_components`. Kopiera mappen `mipower` inifrån den.
4.  Klistra in den kopierade mappen `mipower` i mappen `custom_components` i din Home Assistant-konfigurationskatalog. Om mappen `custom_components` inte finns, måste du skapa den.
    - Den slutliga sökvägen ska se ut så här: `.../config/custom_components/mipower/`
5.  Starta om Home Assistant.

## Konfiguration

Efter omstarten kan du lägga till och konfigurera MiPower-strömbrytaren.

1.  Gå till **Settings > Devices & Services** (Inställningar > Enheter & Tjänster).
2.  Klicka på knappen **"+ Add Integration"** ("+ Lägg till Integration") i det nedre högra hörnet.
3.  Sök efter **"MiPower"** och klicka på den.

### Enkel installation (Rekommenderas)

Detta är det enklaste sättet att konfigurera integrationen.

1.  När du blir tillfrågad väljer du **"Easy Setup"** ("Enkel Installation").
2.  Integrationen kommer automatiskt att upptäcka Bluetooth-aktiverade mediaspelare på ditt system.
3.  Välj din målenhet (t.ex. "Xiaomi Mi Box 4") från rullgardinsmenyn.
4.  Klicka på **"Submit"** ("Skicka").

Det är allt! Integrationen skapar en strömbrytare kopplad till din mediaspelare.

### Avancerad installation

Använd denna metod om Enkel installation inte hittar din enhet eller om du behöver konfigurera avancerade tidsinställningar från början.

1.  **Steg 1: Enhetsval**
    - Välj **"Advanced Setup"** ("Avancerad Installation").
    - Välj din målmediaspelare från listan över *alla* mediaspelare i din Home Assistant.
2.  **Steg 2: MAC-adress**
    - Integrationen kommer att försöka hitta Bluetooth MAC-adressen för den valda enheten. 
    - Om den hittas, kommer den att fyllas i i förväg. Kontrollera att den är korrekt.
    - Om den inte hittas, måste du ange enhetens Bluetooth MAC-adress manuellt.
3.  **Steg 3: Tidsinställningar**
    - Du kan konfigurera olika tidsgränser (timeouts) och fördröjningar för Bluetooth-kommandona. För de flesta användare är standardvärdena tillräckliga.
4.  Klicka på **"Submit"** ("Skicka") för att slutföra installationen.

## Alternativ

När du har konfigurerat din MiPower-strömbrytare kan du när som helst justera tidsinställningarna.

1.  Gå till **Settings > Devices & Services** (Inställningar > Enheter & Tjänster).
2.  Hitta MiPower-integrationen och klicka på **"Configure"** ("Konfigurera").
3.  Justera reglagen för *debounce*, tidsgränser och fördröjningar efter behov.

## Förklaring av Tidsinställningar

I konfigurations- eller alternativmenyn kan du finjustera tidpunkten för Bluetooth-kommandona. För de flesta användare fungerar standardvärdena bra.

- **Turn-On Debounce (Fördröjning vid påslagning):** Den minsta tid (i sekunder) som måste passera innan 'slå på'-kommandot kan utföras igen. Detta förhindrar att enheten spammas med väckningssignaler om strömbrytaren växlas snabbt.

- **Turn-Off Debounce (Fördröjning vid avstängning):** Den minsta tid (i sekunder) som måste passera innan 'slå av'-kommandot kan utföras igen. 

- **Delay Between Commands (Fördröjning mellan kommandon):** En mycket kort fördröjning (i sekunder) mellan att skicka på varandra följande kommandon till `bluetoothctl`-verktyget. På vissa system kan en liten paus förbättra tillförlitligheten.

- **Process Spawn Timeout (Tidsgräns för processstart):** Den maximala tid (i sekunder) att vänta på att `bluetoothctl`-processen ska starta. Om den inte startar inom denna tid, misslyckas uppvakningsförsöket.

- **Pairing Timeout (Tidsgräns för parning):** I den förenklade uppvakningslogiken är detta den tid som ska väntas efter att `pair`-kommandot har skickats innan man antar framgång. Det ger enheten tid att bearbeta väckningssignalen.

- **Bluetooth Scan Duration (Varaktighet för Bluetooth-skanning):** Den tid (i sekunder) som integrationen kommer att skanna efter Bluetooth-enheter innan den försöker skicka parningskommandot. En längre skanning kan hjälpa till att hitta enheter som är långsamma med att annonsera sin närvaro.

## Läs på ditt eget språk

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