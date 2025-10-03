# MiPower — Vlastná integrácia Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** je integrácia Home Assistant, ktorá vám umožňuje ovládať stav napájania mediálnych prehrávačov, ktoré nepodporujú tradičné Wake-on-LAN (WOL), ale môžu byť "prebudené" žiadosťou o spárovanie cez Bluetooth. Bola špeciálne navrhnutá pre zariadenia ako Xiaomi Mi Box, ale môže fungovať aj s inými podobnými Android TV boxmi.

Táto integrácia vytvára entitu `switch` (prepínač) v Home Assistant. 
- **Zapnutie** prepínača odošle sériu príkazov Bluetooth cez `bluetoothctl` na prebudenie zariadenia.
- **Vypnutie** prepínača volá službu `media_player.turn_off` pre prepojené zariadenie.
- Stav prepínača sa automaticky synchronizuje so stavom prepojenej entity mediálneho prehrávača.
## 🤝 Podporte Nás

Projekt MiPower je vyvíjaný s víziou pridávať hodnotu komunite s otvoreným zdrojovým kódom. Vaša podpora je kľúčová pre udržanie kontinuity a rýchlosti vývoja tohto projektu.

Ak si moju prácu ceníte, môžete ma podporiť prostredníctvom GitHub Sponsors alebo nasledujúcich platforiem. Vopred ďakujem!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternatívne môžete vidieť všetky možnosti financovania kliknutím na **tlačidlo Sponzor (❤️)** v pravom hornom rohu úložiska.

## Predpoklady

- **Home Assistant OS / Supervised / Container:** Táto integrácia vyžaduje inštaláciu Home Assistant založenú na Linuxe, kde je nástroj príkazového riadka `bluetoothctl` dostupný a prístupný. **Nebude** fungovať na inštalácii Home Assistant Core na systéme Windows.

## Inštalácia cez HACS (Odporúčané)

Táto integrácia je k dispozícii ako vlastné úložisko (custom repository) v HACS.

1.  Prejdite na svoj ovládací panel HACS.
2.  Kliknite na **Integrations** (Integrácie).
3.  Kliknite na menu s tromi bodkami v pravom hornom rohu a vyberte **"Custom repositories"** ("Vlastné úložiská").
4.  V dialógovom okne zadajte nasledujúce informácie:
    - **Repository (Úložisko):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategória):** `Integration` (Integrácia)
5.  Kliknite na **"Add"** ("Pridať").
6.  Integrácia "MiPower" sa teraz objaví vo vašom zozname HACS. Kliknite na ňu.
7.  Kliknite na tlačidlo **"Download"** ("Stiahnuť") a potom znova na **"Download"** ("Stiahnuť") v nasledujúcom okne.
8.  Po dokončení sťahovania **MUSÍTE reštartovať Home Assistant**, aby sa integrácia načítala.

## Manuálna inštalácia

Aj keď je HACS odporúčaná metóda, integráciu môžete nainštalovať aj manuálne.

1.  Prejdite na [stránku Vydaní](https://github.com/DenizOner/MiPower/releases) úložiska a stiahnite si súbor `mipower.zip` z najnovšieho vydania.
2.  Rozbaľte stiahnutý súbor.
3.  Vo vnútri rozbaleného priečinka nájdete adresár `custom_components`. Skopírujte z neho priečinok `mipower`.
4.  Vložte skopírovaný priečinok `mipower` do priečinka `custom_components` vo vašom konfiguračnom adresári Home Assistant. Ak priečinok `custom_components` neexistuje, musíte ho vytvoriť.
    - Konečná cesta by mala vyzerať takto: `.../config/custom_components/mipower/`
5.  Reštartujte Home Assistant.

## Konfigurácia

Po reštartovaní môžete pridať a nakonfigurovať prepínač MiPower.

1.  Prejdite na **Settings > Devices & Services** (Nastavenia > Zariadenia a Služby).
2.  Kliknite na tlačidlo **"+ Add Integration"** ("+ Pridať Integráciu") v pravom dolnom rohu.
3.  Vyhľadajte **"MiPower"** a kliknite naň.

### Jednoduché nastavenie (Odporúčané)

Toto je najjednoduchší spôsob konfigurácie integrácie.

1.  Po zobrazení výzvy zvoľte **"Easy Setup"** ("Jednoduché Nastavenie").
2.  Integrácia automaticky objaví mediálne prehrávače s podporou Bluetooth vo vašom systéme.
3.  Vyberte svoje cieľové zariadenie (napr. "Xiaomi Mi Box 4") z rozbaľovacieho zoznamu.
4.  Kliknite na **"Submit"** ("Odoslať").

To je všetko! Integrácia vytvorí prepínač prepojený s vaším mediálnym prehrávačom.

### Pokročilé nastavenie

Použite túto metódu, ak Jednoduché nastavenie nenájde vaše zariadenie alebo ak potrebujete nakonfigurovať pokročilé nastavenia časovania od začiatku.

1.  **Krok 1: Výber zariadenia**
    - Zvoľte **"Advanced Setup"** ("Pokročilé Nastavenie").
    - Vyberte svoj cieľový mediálny prehrávač zo zoznamu *všetkých* mediálnych prehrávačov vo vašom Home Assistant.
2.  **Krok 2: MAC adresa**
    - Integrácia sa pokúsi nájsť MAC adresu Bluetooth vybraného zariadenia. 
    - Ak sa nájde, bude predvyplnená. Overte, či je správna.
    - Ak sa nenájde, musíte MAC adresu Bluetooth vášho zariadenia zadať manuálne.
3.  **Krok 3: Nastavenia časovania**
    - Môžete nakonfigurovať rôzne časové limity a oneskorenia pre príkazy Bluetooth. Pre väčšinu používateľov sú predvolené hodnoty dostatočné.
4.  Kliknite na **"Submit"** ("Odoslať") pre dokončenie nastavenia.

## Možnosti

Po nakonfigurovaní prepínača MiPower môžete kedykoľvek upraviť nastavenia časovania.

1.  Prejdite na **Settings > Devices & Services** (Nastavenia > Zariadenia a Služby).
2.  Nájdite integráciu MiPower a kliknite na **"Configure"** ("Konfigurovať").
3.  Podľa potreby upravte posuvníky pre *debounce*, časové limity a oneskorenia.

## Vysvetlenie nastavení časovania

V ponuke konfigurácie alebo možností môžete doladiť časovanie príkazov Bluetooth. Pre väčšinu používateľov fungujú predvolené hodnoty dobre.

- **Turn-On Debounce (Potlačenie chvenia pri zapnutí):** Minimálny čas (v sekundách), ktorý musí uplynúť, kým sa príkaz 'zapnúť' môže znova vykonať. Tým sa zabráni zahlteniu zariadenia signálmi prebudenia, ak sa prepínač rýchlo prepína.

- **Turn-Off Debounce (Potlačenie chvenia pri vypnutí):** Minimálny čas (v sekundách), ktorý musí uplynúť, kým sa príkaz 'vypnúť' môže znova vykonať. 

- **Delay Between Commands (Oneskorenie medzi príkazmi):** Veľmi krátke oneskorenie (v sekundách) medzi odosielaním po sebe nasledujúcich príkazov nástroju `bluetoothctl`. Na niektorých systémoch môže pridanie malej pauzy zlepšiť spoľahlivosť.

- **Process Spawn Timeout (Časový limit spustenia procesu):** Maximálny čas (v sekundách) čakania na spustenie procesu `bluetoothctl`. Ak sa nepodarí spustiť v tomto čase, pokus o zapnutie zlyhá.

- **Pairing Timeout (Časový limit spárovania):** V zjednodušenej logike zapínania je to čas, po ktorý sa má čakať po odoslaní príkazu `pair`, predtým než sa predpokladá úspech. Dáva to zariadeniu čas na spracovanie signálu prebudenia.

- **Bluetooth Scan Duration (Trvanie skenovania Bluetooth):** Trvanie (v sekundách), počas ktorého bude integrácia skenovať zariadenia Bluetooth predtým, ako sa pokúsi odoslať príkaz na spárovanie. Dlhšie skenovanie môže pomôcť nájsť zariadenia, ktoré pomaly inzerujú svoju prítomnosť.

## Čítajte vo svojom vlastnom jazyku

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