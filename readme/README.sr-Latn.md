# MiPower — Prilagođena integracija za Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** je integracija za Home Assistant koja vam omogućava da kontrolišete stanje napajanja medija plejera koji ne podržavaju tradicionalni Wake-on-LAN (WOL), ali se mogu „probuditi“ zahtevom za uparivanje preko Bluetooth-a. Specijalno je dizajnirana za uređaje kao što je Xiaomi Mi Box, ali može raditi i sa drugim sličnim Android TV boksovima.

Ova integracija kreira `switch` (prekidač) entitet u Home Assistant-u. 
- **Uključivanje** prekidača šalje niz Bluetooth komandi preko `bluetoothctl` da probudi uređaj.
- **Isključivanje** prekidača poziva uslugu `media_player.turn_off` za povezani uređaj.
- Stanje prekidača se automatski sinhronizuje sa stanjem entiteta povezanog medija plejera.

## 🤝 Podržite nas

Projekat MiPower se razvija sa vizijom dodavanja vrednosti zajednici otvorenog koda. Vaša podrška je od vitalnog značaja za održavanje kontinuiteta i brzine razvoja ovog projekta.

Ako cenite moj rad, možete me podržati preko GitHub Sponzora ili sledećih platformi. Hvala unapred!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternativno, sve opcije finansiranja možete videti klikom na **dugme Sponzor (❤️)** u gornjem desnom uglu spremišta.

## Preduslovi

- **Home Assistant OS / Supervised / Container:** Ova integracija zahteva instalaciju Home Assistant-a baziranu na Linux-u, gde je alat komandne linije `bluetoothctl` dostupan i pristupačan. **NEĆE** raditi na instalaciji Home Assistant Core-a na Windows-u.

## Instalacija preko HACS-a (Preporučeno)

Ova integracija je dostupna kao prilagođeni repozitorijum u HACS-u.

1.  Idite na svoju HACS kontrolnu tablu.
2.  Kliknite na **Integrations** (Integracije).
3.  Kliknite na meni sa tri tačke u gornjem desnom uglu i izaberite **"Custom repositories"** ("Prilagođeni repozitorijumi").
4.  U dijalog boksu unesite sledeće informacije:
    - **Repository (Repozitorijum):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategorija):** `Integration` (Integracija)
5.  Kliknite na **"Add"** ("Dodaj").
6.  Integracija "MiPower" će se sada pojaviti na vašoj HACS listi. Kliknite na nju.
7.  Kliknite na dugme **"Download"** ("Preuzmi"), a zatim ponovo **"Download"** ("Preuzmi") u sledećem prozoru.
8.  Nakon što se preuzimanje završi, **MORATE ponovo pokrenuti Home Assistant** da bi se integracija učitala.

## Ručna instalacija

Iako je HACS preporučeni metod, integraciju možete instalirati i ručno.

1.  Idite na [stranicu izdanja](https://github.com/DenizOner/MiPower/releases) repozitorijuma i preuzmite datoteku `mipower.zip` iz najnovijeg izdanja.
2.  Raspakujte preuzetu datoteku.
3.  Unutar raspakovane fascikle, naći ćete direktorijum `custom_components`. Kopirajte fasciklu `mipower` iz njega.
4.  Nalepite kopiranu fasciklu `mipower` u fasciklu `custom_components` u vašem konfiguracionom direktorijumu Home Assistant-a. Ako fascikla `custom_components` ne postoji, morate je kreirati.
    - Konačna putanja bi trebalo da izgleda ovako: `.../config/custom_components/mipower/`
5.  Ponovo pokrenite Home Assistant.

## Konfiguracija

Nakon ponovnog pokretanja, možete dodati i konfigurisati MiPower prekidač.

1.  Idite na **Settings > Devices & Services** (Podešavanja > Uređaji i Usluge).
2.  Kliknite na dugme **"+ Add Integration"** ("+ Dodaj Integraciju") u donjem desnom uglu.
3.  Pretražite **"MiPower"** i kliknite na njega.

### Jednostavna konfiguracija (Preporučeno)

Ovo je najjednostavniji način za konfigurisanje integracije.

1.  Kada se zatraži, izaberite **"Easy Setup"** ("Jednostavna Konfiguracija").
2.  Integracija će automatski otkriti medija plejer sa omogućenim Bluetooth-om na vašem sistemu.
3.  Izaberite svoj ciljni uređaj (npr. "Xiaomi Mi Box 4") sa padajuće liste.
4.  Kliknite na **"Submit"** ("Pošalji").

To je to! Integracija će kreirati prekidač povezan sa vašim medija plejerom.

### Napredna konfiguracija

Koristite ovu metodu ako Jednostavna konfiguracija ne pronađe vaš uređaj ili ako morate da konfigurišete napredna podešavanja vremena od početka.

1.  **Korak 1: Izbor uređaja**
    - Izaberite **"Advanced Setup"** ("Napredna Konfiguracija").
    - Izaberite svoj ciljni medija plejer sa liste *svih* medija plejera u vašem Home Assistant-u.
2.  **Korak 2: MAC adresa**
    - Integracija će pokušati da pronađe Bluetooth MAC adresu odabranog uređaja. 
    - Ako se pronađe, biće unapred popunjena. Proverite da li je tačna.
    - Ako se ne pronađe, morate ručno uneti Bluetooth MAC adresu svog uređaja.
3.  **Korak 3: Podešavanja vremena**
    - Možete konfigurisati različite vremenske periode i kašnjenja za Bluetooth komande. Za većinu korisnika, podrazumevane vrednosti su dovoljne.
4.  Kliknite na **"Submit"** ("Pošalji") da biste dovršili podešavanje.

## Opcije

Nakon što konfigurišete svoj MiPower prekidač, možete u bilo kom trenutku prilagoditi podešavanja vremena.

1.  Idite na **Settings > Devices & Services** (Podešavanja > Uređaji i Usluge).
2.  Pronađite MiPower integraciju i kliknite **"Configure"** ("Konfiguriši").
3.  Podesite klizače za *debounce*, vremenske periode i kašnjenja po potrebi.

## Objašnjenje podešavanja vremena

U meniju za konfiguraciju ili opcije, možete fino podesiti vreme Bluetooth komandi. Za većinu korisnika, podrazumevane vrednosti dobro funkcionišu.

- **Turn-On Debounce (Poništavanje greške pri uključivanju):** Minimalno vreme (u sekundama) koje mora da prođe pre nego što se komanda „uključi“ može ponovo izvršiti. Ovo sprečava slanje neželjenih signala za buđenje uređaju ako se prekidač brzo prebacuje.

- **Turn-Off Debounce (Poništavanje greške pri isključivanju):** Minimalno vreme (u sekundama) koje mora da prođe pre nego što se komanda „isključi“ može ponovo izvršiti. 

- **Delay Between Commands (Kašnjenje između komandi):** Vrlo kratko kašnjenje (u sekundama) između slanja uzastopnih komandi alatu `bluetoothctl`. Na nekim sistemima, dodavanje male pauze može poboljšati pouzdanost.

- **Process Spawn Timeout (Vremenski period pokretanja procesa):** Maksimalno vreme (u sekundama) čekanja da se pokrene proces `bluetoothctl`. Ako se ne pokrene u ovom roku, pokušaj uključivanja neće uspeti.

- **Pairing Timeout (Vremenski period uparivanja):** U pojednostavljenoj logici uključivanja, ovo je vreme čekanja nakon slanja komande `pair` pre nego što se pretpostavi uspeh. Daje uređaju vremena da obradi signal za buđenje.

- **Bluetooth Scan Duration (Trajanje Bluetooth skeniranja):** Trajanje (u sekundama) tokom kojeg će integracija skenirati Bluetooth uređaje pre nego što pokuša da pošalje komandu za uparivanje. Duže skeniranje može pomoći u pronalaženju uređaja koji sporo oglašavaju svoje prisustvo.

## Čitajte na svom jeziku

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