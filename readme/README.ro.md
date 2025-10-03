# MiPower — Integrare personalizată Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** este o integrare Home Assistant care vă permite să controlați starea de alimentare a playere-lor media care nu acceptă Wake-on-LAN (WOL) tradițional, dar care pot fi „trezite” printr-o solicitare de împerechere Bluetooth. A fost concepută special pentru dispozitive precum Xiaomi Mi Box, dar poate funcționa și cu alte dispozitive Android TV Box similare.

Această integrare creează o entitate de tip `switch` (întrerupător) în Home Assistant. 
- **Pornirea** întrerupătorului trimite o serie de comenzi Bluetooth prin `bluetoothctl` pentru a trezi dispozitivul.
- **Oprirea** întrerupătorului apelează serviciul `media_player.turn_off` pentru dispozitivul conectat.
- Starea întrerupătorului este sincronizată automat automat cu starea entității player-ului media conectat.

## 🤝 Susțineți-ne

Proiectul MiPower este dezvoltat cu viziunea de a adăuga valoare comunității open source. Sprijinul dumneavoastră este vital pentru menținerea continuității și a vitezei de dezvoltare a acestui proiect.

Dacă apreciați munca mea, mă puteți susține prin GitHub Sponsors sau următoarele platforme. Vă mulțumesc anticipat!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternativ, puteți vedea toate opțiunile de finanțare făcând clic pe **butonul Sponsor (❤️)** din colțul din dreapta sus al depozitului.

## Pre-condiții

- **Home Assistant OS / Supervised / Container:** Această integrare necesită o instalare Home Assistant bazată pe Linux, unde instrumentul de linie de comandă `bluetoothctl` este disponibil și accesibil. **NU** va funcționa pe o instalare Home Assistant Core pe Windows.

## Instalare prin HACS (Recomandat)

Această integrare este disponibilă ca un depozit personalizat în HACS.

1.  Navigați la tabloul de bord HACS.
2.  Faceți clic pe **Integrations** (Integrări).
3.  Faceți clic pe meniul cu trei puncte din colțul din dreapta sus și selectați **"Custom repositories"** ("Depozite personalizate").
4.  În caseta de dialog, introduceți următoarele informații:
    - **Repository (Depozit):** `https://github.com/DenizOner/MiPower`
    - **Category (Categorie):** `Integration` (Integrare)
5.  Faceți clic pe **"Add"** ("Adaugă").
6.  Integrarea „MiPower” va apărea acum în lista HACS. Faceți clic pe ea.
7.  Faceți clic pe butonul **"Download"** ("Descărcare") și apoi faceți clic din nou pe **"Download"** ("Descărcare") în fereastra următoare.
8.  După finalizarea descărcării, **trebuie să reporniți Home Assistant** pentru ca integrarea să fie încărcată.

## Instalare Manuală

Deși HACS este metoda recomandată, puteți instala integrarea și manual.

1.  Accesați [pagina de Lansări](https://github.com/DenizOner/MiPower/releases) a depozitului și descărcați fișierul `mipower.zip` din cea mai recentă lansare.
2.  Dezarhivați fișierul descărcat.
3.  În interiorul folderului dezarhivat, veți găsi un director `custom_components`. Copiați folderul `mipower` din interiorul acestuia.
4.  Lipiți folderul `mipower` copiat în folderul `custom_components` din directorul de configurare Home Assistant. Dacă folderul `custom_components` nu există, trebuie să îl creați.
    - Calea finală ar trebui să arate astfel: `.../config/custom_components/mipower/`
5.  Reporniți Home Assistant.

## Configurare

După repornire, puteți adăuga și configura întrerupătorul MiPower.

1.  Accesați **Settings > Devices & Services** (Setări > Dispozitive și Servicii).
2.  Faceți clic pe butonul **"+ Add Integration"** ("+ Adaugă Integrare") din colțul din dreapta jos.
3.  Căutați **"MiPower"** și faceți clic pe el.

### Configurare Ușoară (Recomandat)

Aceasta este cea mai simplă modalitate de a configura integrarea.

1.  Când vi se solicită, alegeți **"Easy Setup"** ("Configurare Ușoară").
2.  Integrarea va descoperi automat playerele media compatibile Bluetooth pe sistemul dvs.
3.  Selectați dispozitivul țintă (de exemplu, „Xiaomi Mi Box 4”) din lista derulantă.
4.  Faceți clic pe **"Submit"** ("Trimite").

Asta este! Integrarea va crea un întrerupător conectat la playerul dvs. media.

### Configurare Avansată

Utilizați această metodă dacă Configurare Ușoară nu găsește dispozitivul dvs. sau dacă trebuie să configurați setări avansate de sincronizare de la început.

1.  **Pasul 1: Selectarea Dispozitivului**
    - Alegeți **"Advanced Setup"** ("Configurare Avansată").
    - Selectați playerul media țintă din lista *tuturor* playerelor media din Home Assistant.
2.  **Pasul 2: Adresa MAC**
    - Integrarea va încerca să găsească adresa MAC Bluetooth a dispozitivului selectat. 
    - Dacă este găsită, va fi pre-completată. Verificați dacă este corectă.
    - Dacă nu este găsită, trebuie să introduceți manual adresa MAC Bluetooth a dispozitivului dvs.
3.  **Pasul 3: Setări de Sincronizare**
    - Puteți configura diverse timpi de expirare (timeouts) și întârzieri pentru comenzile Bluetooth. Pentru majoritatea utilizatorilor, valorile implicite sunt suficiente.
4.  Faceți clic pe **"Submit"** ("Trimite") pentru a finaliza configurarea.

## Opțiuni

După ce ați configurat întrerupătorul MiPower, puteți ajusta oricând setările de sincronizare.

1.  Accesați **Settings > Devices & Services** (Setări > Dispozitive și Servicii).
2.  Găsiți integrarea MiPower și faceți clic pe **"Configure"** ("Configurează").
3.  Ajustați glisoarele pentru *debounce*, timpii de expirare și întârzierile după cum este necesar.

## Explicarea Setărilor de Sincronizare

În meniul de configurare sau opțiuni, puteți regla fin sincronizarea comenzilor Bluetooth. Pentru majoritatea utilizatorilor, valorile implicite funcționează bine.

- **Turn-On Debounce (Debounce la Pornire):** Timpul minim (în secunde) care trebuie să treacă înainte ca comanda „pornește” să poată fi executată din nou. Acest lucru împiedică supraîncărcarea dispozitivului cu semnale de trezire dacă întrerupătorul este acționat rapid.

- **Turn-Off Debounce (Debounce la Oprire):** Timpul minim (în secunde) care trebuie să treacă înainte ca comanda „oprește” să poată fi executată din nou. 

- **Delay Between Commands (Întârziere între Comenzi):** O întârziere foarte scurtă (în secunde) între trimiterea comenzilor consecutive către utilitarul `bluetoothctl`. Pe unele sisteme, adăugarea unei mici pauze poate îmbunătăți fiabilitatea.

- **Process Spawn Timeout (Timp de Expirare al Pornirii Procesului):** Timpul maxim (în secunde) de așteptare pentru ca procesul `bluetoothctl` să înceapă. Dacă nu reușește să pornească în acest timp, încercarea de pornire va eșua.

- **Pairing Timeout (Timp de Expirare al Împerecherii):** În logica simplificată de pornire, aceasta este durata de așteptare după trimiterea comenzii `pair` înainte de a presupune succesul. Îi oferă dispozitivului timp să proceseze semnalul de trezire.

- **Bluetooth Scan Duration (Durata Scanării Bluetooth):** Durata (în secunde) pe care integrarea o va folosi pentru a scana dispozitivele Bluetooth înainte de a încerca să trimită comanda de împerechere. O scanare mai lungă poate ajuta la găsirea dispozitivelor care își anunță lent prezența.

## Citiți în propria limbă

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