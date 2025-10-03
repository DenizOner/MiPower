# MiPower — Prilagođena integracija za Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** je integracija za Home Assistant koja vam omogućuje kontrolu stanja napajanja medijskih playera koji ne podržavaju tradicionalni Wake-on-LAN (WOL), ali se mogu "probuditi" putem Bluetooth zahtjeva za uparivanje. Posebno je dizajnirana za uređaje poput Xiaomi Mi Boxa, ali može raditi i s drugim sličnim Android TV kutijama.

Ova integracija stvara `switch` (prekidač) entitet u Home Assistantu. 
- **Uključivanjem** prekidača šalje se niz Bluetooth naredbi putem `bluetoothctl` kako bi se uređaj probudio.
- **Isključivanjem** prekidača poziva se usluga `media_player.turn_off` za povezani uređaj.
- Stanje prekidača automatski se sinkronizira sa stanjem entiteta povezanog medijskog playera.

## 🤝 Podržite nas

Projekt MiPower razvija se s vizijom dodavanja vrijednosti zajednici otvorenog koda. Vaša podrška je ključna za održavanje kontinuiteta i brzine razvoja ovog projekta.

Ako cijenite moj rad, možete me podržati putem GitHub Sponzora ili sljedećih platformi. Unaprijed hvala!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternativno, možete vidjeti sve opcije financiranja klikom na **gumb Sponzor (❤️)** u gornjem desnom kutu spremišta.

## Preduvjeti

- **Home Assistant OS / Supervised / Container:** Ova integracija zahtijeva instalaciju Home Assistanta temeljenu na Linuxu gdje je `bluetoothctl` alat naredbenog retka dostupan i pristupačan. **Neće** raditi na instalaciji Home Assistant Core na Windowsu.

## Instalacija putem HACS-a (Preporučeno)

Ova integracija dostupna je kao prilagođeno spremište u HACS-u.

1.  Dođite do svoje HACS nadzorne ploče.
2.  Kliknite na **Integrations** (Integracije).
3.  Kliknite na izbornik s tri točke u gornjem desnom kutu i odaberite **"Custom repositories"** ("Prilagođena spremišta").
4.  U dijaloškom okviru unesite sljedeće informacije:
    - **Repository (Spremište):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategorija):** `Integration` (Integracija)
5.  Kliknite **"Add"** ("Dodaj").
6.  Integracija "MiPower" sada će se pojaviti na vašem HACS popisu. Kliknite na nju.
7.  Kliknite gumb **"Download"** ("Preuzmi") i zatim ponovno kliknite **"Download"** ("Preuzmi") u sljedećem prozoru.
8.  Nakon dovršetka preuzimanja, **morate ponovo pokrenuti Home Assistant** da bi se integracija učitala.

## Ručna instalacija

Iako je HACS preporučena metoda, integraciju možete instalirati i ručno.

1.  Idite na [stranicu izdanja](https://github.com/DenizOner/MiPower/releases) spremišta i preuzmite `mipower.zip` datoteku najnovijeg izdanja.
2.  Raspakirajte preuzetu datoteku.
3.  Unutar raspakirane mape pronaći ćete direktorij `custom_components`. Kopirajte mapu `mipower` iz njega.
4.  Zalijepite kopiranu mapu `mipower` u mapu `custom_components` u vašem konfiguracijskom direktoriju Home Assistanta. Ako mapa `custom_components` ne postoji, morate je stvoriti.
    - Konačna putanja trebala bi izgledati ovako: `.../config/custom_components/mipower/`
5.  Ponovo pokrenite Home Assistant.

## Konfiguracija

Nakon ponovnog pokretanja, možete dodati i konfigurirati MiPower prekidač.

1.  Idite na **Settings > Devices & Services** (Postavke > Uređaji i usluge).
2.  Kliknite gumb **"+ Add Integration"** ("+ Dodaj integraciju") u donjem desnom kutu.
3.  Pretražite **"MiPower"** i kliknite na njega.

### Jednostavno postavljanje (Preporučeno)

Ovo je najjednostavniji način konfiguriranja integracije.

1.  Kada se to od vas zatraži, odaberite **"Easy Setup"** ("Jednostavno postavljanje").
2.  Integracija će automatski otkriti medijske playere s omogućenim Bluetoothom na vašem sustavu.
3.  Odaberite svoj ciljni uređaj (npr. "Xiaomi Mi Box 4") s padajućeg popisa.
4.  Kliknite **"Submit"** ("Pošalji").

To je to! Integracija će stvoriti prekidač povezan s vašim medijskim playerom.

### Napredno postavljanje

Koristite ovu metodu ako jednostavno postavljanje ne pronađe vaš uređaj ili ako trebate konfigurirati napredne postavke vremena od početka.

1.  **Korak 1: Odabir uređaja**
    - Odaberite **"Advanced Setup"** ("Napredno postavljanje").
    - Odaberite svoj ciljni medijski player s popisa *svih* medijskih playera u vašem Home Assistantu.
2.  **Korak 2: MAC adresa**
    - Integracija će pokušati pronaći Bluetooth MAC adresu odabranog uređaja. 
    - Ako se pronađe, bit će unaprijed popunjena. Potvrdite da je ispravna.
    - Ako se ne pronađe, morate ručno unijeti Bluetooth MAC adresu vašeg uređaja.
3.  **Korak 3: Postavke vremena**
    - Možete konfigurirati različita vremenska ograničenja (*timeouts*) i kašnjenja za Bluetooth naredbe. Za većinu korisnika, zadane vrijednosti su dovoljne.
4.  Kliknite **"Submit"** ("Pošalji") za dovršetak postavljanja.

## Opcije

Nakon što ste konfigurirali svoj MiPower prekidač, postavke vremena možete prilagoditi u bilo kojem trenutku.

1.  Idite na **Settings > Devices & Services** (Postavke > Uređaji i usluge).
2.  Pronađite MiPower integraciju i kliknite **"Configure"** ("Konfiguriraj").
3.  Podesite klizače za *debounce*, vremenska ograničenja i kašnjenja prema potrebi.

## Objašnjenje postavki vremena

U izborniku konfiguracije ili opcija možete fino podesiti vrijeme Bluetooth naredbi. Za većinu korisnika, zadane vrijednosti dobro funkcioniraju.

- **Turn-On Debounce (Debounce uključivanja):** Minimalno vrijeme (u sekundama) koje mora proći prije nego što se naredba 'uključi' može ponovno izvršiti. Time se sprječava preopterećenje uređaja signalima buđenja ako se prekidač brzo prebacuje.

- **Turn-Off Debounce (Debounce isključivanja):** Minimalno vrijeme (u sekundama) koje mora proći prije nego što se naredba 'isključi' može ponovno izvršiti. 

- **Delay Between Commands (Kašnjenje između naredbi):** Vrlo kratko kašnjenje (u sekundama) između slanja uzastopnih naredbi uslužnom programu `bluetoothctl`. Na nekim sustavima, dodavanje male pauze može poboljšati pouzdanost.

- **Process Spawn Timeout (Vremensko ograničenje pokretanja procesa):** Maksimalno vrijeme (u sekundama) za čekanje da se `bluetoothctl` proces pokrene. Ako se ne uspije pokrenuti unutar tog vremena, pokušaj uključivanja neće uspjeti.

- **Pairing Timeout (Vremensko ograničenje uparivanja):** U pojednostavljenoj logici uključivanja, ovo je vrijeme koje treba čekati nakon slanja naredbe `pair` prije pretpostavke uspjeha. Daje uređaju vremena da obradi signal buđenja.

- **Bluetooth Scan Duration (Trajanje Bluetooth skeniranja):** Trajanje (u sekundama) tijekom kojeg će integracija skenirati Bluetooth uređaje prije nego što pokuša poslati naredbu za uparivanje. Dulje skeniranje može pomoći u pronalaženju uređaja koji sporo oglašavaju svoju prisutnost.

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