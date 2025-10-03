# MiPower — Home Assistantin mukautettu integraatio

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** on Home Assistant -integraatio, jonka avulla voit ohjata niiden mediasoittimien virran tilaa, jotka eivät tue perinteistä Wake-on-LANia (WOL), mutta jotka voidaan "herättää" Bluetooth-pariliitospyynnöllä. Se on suunniteltu erityisesti laitteille, kuten Xiaomi Mi Box, mutta saattaa toimia muiden vastaavien Android TV-boksien kanssa.

Tämä integraatio luo `switch`-entiteetin (kytkimen) Home Assistantiin. 
- Kytkimen **kytkeminen PÄÄLLE** lähettää sarjan Bluetooth-komentoja `bluetoothctl`-työkalun kautta laitteen herättämiseksi.
- Kytkimen **kytkeminen POIS PÄÄLTÄ** kutsuu linkitetyn laitteen `media_player.turn_off`-palvelua.
- Kytkimen tila synkronoidaan automaattisesti linkitetyn mediasoittimen entiteetin tilan kanssa.

## 🤝 Tue meitä

MiPower-projekti kehitetään visiolla lisätä arvoa avoimen lähdekoodin yhteisöön. Tukesi on elintärkeää tämän projektin jatkuvuuden ja kehitysnopeuden ylläpitämiseksi.

Jos arvostat työtäni, voit tukea minua GitHub Sponsorsin tai seuraavien alustojen kautta. Kiitos jo etukäteen!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Vaihtoehtoisesti voit nähdä kaikki rahoitusvaihtoehdot napsauttamalla **Sponsori-painiketta (❤️)** arkiston oikeassa yläkulmassa.

## Esivaatimukset

- **Home Assistant OS / Supervised / Container:** Tämä integraatio vaatii Linux-pohjaisen Home Assistant -asennuksen, jossa `bluetoothctl`-komentorivityökalu on käytettävissä ja saatavilla. Se **ei** toimi Windows-käyttöjärjestelmän Home Assistant Core -asennuksessa.

## Asennus HACS:n kautta (Suositeltu)

Tämä integraatio on saatavilla mukautettuna arkistona HACS:ssä.

1.  Siirry HACS-hallintapaneeliin.
2.  Napsauta **Integrations** (Integraatiot).
3.  Napsauta oikeassa yläkulmassa olevaa kolmen pisteen valikkoa ja valitse **"Custom repositories"** ("Mukautetut arkistot").
4.  Syötä valintaikkunaan seuraavat tiedot:
    - **Repository (Arkisto):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategoria):** `Integration` (Integraatio)
5.  Napsauta **"Add"** ("Lisää").
6.  "MiPower"-integraatio näkyy nyt HACS-listassasi. Napsauta sitä.
7.  Napsauta **"Download"** ("Lataa") -painiketta ja sitten uudelleen **"Download"** ("Lataa") seuraavassa ikkunassa.
8.  Kun lataus on valmis, sinun **on käynnistettävä Home Assistant uudelleen**, jotta integraatio latautuu.

## Manuaalinen asennus

Vaikka HACS on suositeltava menetelmä, voit asentaa integraation myös manuaalisesti.

1.  Siirry arkiston [Releases-sivulle](https://github.com/DenizOner/MiPower/releases) ja lataa `mipower.zip`-tiedosto uusimmasta versiosta.
2.  Pura ladattu tiedosto.
3.  Pakatun kansion sisältä löydät `custom_components`-hakemiston. Kopioi `mipower`-kansio sen sisältä.
4.  Liitä kopioitu `mipower`-kansio `custom_components`-kansioon Home Assistantin konfigurointihakemistossa. Jos `custom_components`-kansiota ei ole olemassa, sinun on luotava se.
    - Lopullisen polun tulisi näyttää tältä: `.../config/custom_components/mipower/`
5.  Käynnistä Home Assistant uudelleen.

## Konfigurointi

Uudelleenkäynnistyksen jälkeen voit lisätä ja konfiguroida MiPower-kytkimen.

1.  Siirry kohtaan **Settings > Devices & Services** (Asetukset > Laitteet ja Palvelut).
2.  Napsauta **"+ Add Integration"** ("+ Lisää integraatio") -painiketta oikeassa alakulmassa.
3.  Hae **"MiPower"** ja napsauta sitä.

### Helppo asennus (Suositeltu)

Tämä on yksinkertaisin tapa konfiguroida integraatio.

1.  Kun sinua pyydetään, valitse **"Easy Setup"** ("Helppo asennus").
2.  Integraatio löytää automaattisesti Bluetooth-yhteensopivat mediasoittimet järjestelmästäsi.
3.  Valitse kohdelaite (esim. "Xiaomi Mi Box 4") pudotusvalikosta.
4.  Napsauta **"Submit"** ("Lähetä").

Siinä kaikki! Integraatio luo mediasoittimeesi linkitetyn kytkimen.

### Edistynyt asennus

Käytä tätä menetelmää, jos Helppo asennus ei löydä laitettasi tai jos sinun on määritettävä edistyneet ajoitusasetukset alusta alkaen.

1.  **Vaihe 1: Laitteen Valinta**
    - Valitse **"Advanced Setup"** ("Edistynyt asennus").
    - Valitse kohdemediasoittimesi luettelosta, jossa on *kaikki* Home Assistant -mediasoittimet.
2.  **Vaihe 2: MAC-osoite**
    - Integraatio yrittää löytää valitun laitteen Bluetooth MAC-osoitteen. 
    - Jos se löytyy, se esitäytetään. Varmista, että se on oikein.
    - Jos sitä ei löydy, sinun on syötettävä laitteesi Bluetooth MAC-osoite manuaalisesti.
3.  **Vaihe 3: Ajoitusasetukset**
    - Voit määrittää erilaisia aikakatkaisuja ja viiveitä Bluetooth-komennoille. Useimmille käyttäjille oletusarvot ovat riittävät.
4.  Napsauta **"Submit"** ("Lähetä") viimeistelläksesi asennuksen.

## Asetukset

Kun olet määrittänyt MiPower-kytkimesi, voit säätää ajoitusasetuksia milloin tahansa.

1.  Siirry kohtaan **Settings > Devices & Services** (Asetukset > Laitteet ja Palvelut).
2.  Etsi MiPower-integraatio ja napsauta **"Configure"** ("Määritä").
3.  Säädä *debounce*, aikakatkaisuja ja viiveitä tarpeen mukaan liukusäätimillä.

## Ajoitusasetusten selitys

Konfigurointi- tai asetusvalikossa voit hienosäätää Bluetooth-komentojen ajoitusta. Useimmille käyttäjille oletusarvot toimivat hyvin.

- **Turn-On Debounce (Käynnistyksen viive):** Vähimmäisaika (sekunneissa), jonka on kuluttava ennen kuin 'käynnistä'-komento voidaan suorittaa uudelleen. Tämä estää laitetta ylikuormittamasta herätyssignaaleilla, jos kytkintä kytketään nopeasti.

- **Turn-Off Debounce (Sammutuksen viive):** Vähimmäisaika (sekunneissa), jonka on kuluttava ennen kuin 'sammuta'-komento voidaan suorittaa uudelleen. 

- **Delay Between Commands (Viive komentojen välillä):** Erittäin lyhyt viive (sekunneissa) peräkkäisten komentojen lähettämisen välillä `bluetoothctl`-apuohjelmalle. Joissakin järjestelmissä lyhyen tauon lisääminen voi parantaa luotettavuutta.

- **Process Spawn Timeout (Prosessi käynnistymisen aikakatkaisu):** Enimmäisaika (sekunneissa), jonka odotetaan `bluetoothctl`-prosessin käynnistymistä. Jos se ei käynnisty tässä ajassa, käynnistysyritys epäonnistuu.

- **Pairing Timeout (Pariliitoksen aikakatkaisu):** Yksinkertaistetussa käynnistyslogiikassa tämä on aika, jonka odotetaan `pair`-komennon lähettämisen jälkeen ennen kuin oletetaan onnistumista. Se antaa laitteelle aikaa käsitellä herätyssignaalin.

- **Bluetooth Scan Duration (Bluetooth-skannauksen kesto):** Kesto (sekunneissa), jonka integraatio etsii Bluetooth-laitteita ennen kuin yrittää lähettää pariliitoskomennon. Pidempi skannaus voi auttaa löytämään laitteita, jotka mainostavat läsnäoloaan hitaasti.

## Lue omalla kielelläsi

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