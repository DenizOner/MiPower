# MiPower — Home Assistant egyedi integráció

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

A **MiPower** egy Home Assistant integráció, amely lehetővé teszi a hagyományos Wake-on-LAN (WOL) funkciót nem támogató, de Bluetooth párosítási kérésre "felébreszthető" média lejátszók áramállapotának vezérlését. Kifejezetten olyan eszközökhöz tervezték, mint a Xiaomi Mi Box, de más hasonló Android TV boxokkal is működhet.

Ez az integráció létrehoz egy `switch` (kapcsoló) entitást a Home Assistantben. 
- A kapcsoló **BEkapcsolása** Bluetooth parancsok sorozatát küldi a `bluetoothctl` segédprogramon keresztül az eszköz felébresztéséhez.
- A kapcsoló **KIkapcsolása** meghívja a `media_player.turn_off` szolgáltatást a kapcsolt eszközhöz.
- A kapcsoló állapota automatikusan szinkronizálódik a kapcsolt média lejátszó entitás állapotával.

## 🤝 Támogass Minket

A MiPower projektet azzal a céllal fejlesztjük, hogy értéket adjunk a nyílt forráskódú közösségnek. Támogatásod létfontosságú a projekt folytonosságának és fejlesztési sebességének fenntartásához.

Ha nagyra értékeled a munkámat, támogathatsz a GitHub Sponsorson vagy az alábbi platformokon keresztül. Előre is köszönöm!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternatív megoldásként a tárhely jobb felső sarkában található **Támogató gombra (❤️)** kattintva megtekintheted az összes finanszírozási lehetőséget.

## Előfeltételek

- **Home Assistant OS / Supervised / Container:** Ez az integráció Linux-alapú Home Assistant telepítést igényel, ahol a `bluetoothctl` parancssori eszköz elérhető és hozzáférhető. **Nem** fog működni a Home Assistant Core Windows-alapú telepítésén.

## Telepítés HACS-en keresztül (Ajánlott)

Ez az integráció egyedi tárolóként érhető el a HACS-ben.

1.  Navigáljon a HACS irányítópultjához.
2.  Kattintson az **Integrations** (Integrációk) menüpontra.
3.  Kattintson a jobb felső sarokban lévő hárompontos menüre, és válassza az **"Custom repositories"** ("Egyedi tárolók") lehetőséget.
4.  A párbeszédpanelen adja meg a következő információkat:
    - **Repository (Tároló):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategória):** `Integration` (Integráció)
5.  Kattintson az **"Add"** ("Hozzáadás") gombra.
6.  A "MiPower" integráció most megjelenik a HACS listájában. Kattintson rá.
7.  Kattintson a **"Download"** ("Letöltés") gombra, majd a következő ablakban kattintson ismét a **"Download"** ("Letöltés") gombra.
8.  A letöltés befejezése után **újra kell indítania a Home Assistantet** az integráció betöltéséhez.

## Manuális telepítés

Bár a HACS az ajánlott módszer, az integrációt manuálisan is telepítheti.

1.  Látogasson el a tároló [Kiadások oldalára](https://github.com/DenizOner/MiPower/releases), és töltse le a `mipower.zip` fájlt a legújabb kiadásból.
2.  Csomagolja ki a letöltött fájlt.
3.  A kicsomagolt mappában talál egy `custom_components` könyvtárat. Másolja ki belőle a `mipower` mappát.
4.  Illessze be a másolt `mipower` mappát a Home Assistant konfigurációs könyvtárának `custom_components` mappájába. Ha a `custom_components` mappa nem létezik, létre kell hoznia.
    - A végső útvonalnak így kell kinéznie: `.../config/custom_components/mipower/`
5.  Indítsa újra a Home Assistantet.

## Konfiguráció

Az újraindítás után hozzáadhatja és konfigurálhatja a MiPower kapcsolót.

1.  Lépjen a **Settings > Devices & Services** (Beállítások > Eszközök és szolgáltatások) menüpontra.
2.  Kattintson a **"+ Add Integration"** ("+ Integráció hozzáadása") gombra a jobb alsó sarokban.
3.  Keresse meg a **"MiPower"** lehetőséget, és kattintson rá.

### Egyszerű beállítás (Ajánlott)

Ez az integráció konfigurálásának legegyszerűbb módja.

1.  Amikor a rendszer kéri, válassza az **"Easy Setup"** ("Egyszerű beállítás") lehetőséget.
2.  Az integráció automatikusan felfedezi a Bluetooth-képes média lejátszókat a rendszerében.
3.  Válassza ki a cél eszközt (pl. "Xiaomi Mi Box 4") a legördülő listából.
4.  Kattintson a **"Submit"** ("Küldés") gombra.

Ennyi! Az integráció létrehoz egy, a média lejátszójához kapcsolt kapcsolót.

### Speciális beállítás

Használja ezt a módszert, ha az Egyszerű beállítás nem találja az eszközét, vagy ha már a kezdetektől fogva speciális időzítési beállításokat kell konfigurálnia.

1.  **1. lépés: Eszköz kiválasztása**
    - Válassza az **"Advanced Setup"** ("Speciális beállítás") lehetőséget.
    - Válassza ki a cél média lejátszót a Home Assistant *összes* média lejátszójának listájából.
2.  **2. lépés: MAC cím**
    - Az integráció megpróbálja megtalálni a kiválasztott eszköz Bluetooth MAC címét. 
    - Ha megtalálja, előre kitöltődik. Ellenőrizze, hogy helyes-e.
    - Ha nem található, manuálisan kell megadnia az eszköz Bluetooth MAC címét.
3.  **3. lépés: Időzítési beállítások**
    - Különböző időtúllépéseket és késleltetéseket konfigurálhat a Bluetooth parancsokhoz. A legtöbb felhasználó számára az alapértelmezett értékek elegendőek.
4.  Kattintson a **"Submit"** ("Küldés") gombra a beállítás befejezéséhez.

## Opciók

Miután konfigurálta a MiPower kapcsolót, bármikor módosíthatja az időzítési beállításokat.

1.  Lépjen a **Settings > Devices & Services** (Beállítások > Eszközök és szolgáltatások) menüpontra.
2.  Keresse meg a MiPower integrációt, és kattintson a **"Configure"** ("Konfigurálás") gombra.
3.  Szükség szerint állítsa be a *debounce*, időtúllépések és késleltetések csúszkáit.

## Időzítési beállítások magyarázata

A konfigurációs vagy opciós menüben finomhangolhatja a Bluetooth parancsok időzítését. A legtöbb felhasználó számára az alapértelmezett értékek jól működnek.

- **Turn-On Debounce (Bekapcsolási Debounce):** Az az minimális idő (másodpercben), aminek el kell telnie, mielőtt a 'bekapcsolás' parancs ismét végrehajtható lenne. Ez megakadályozza az eszköz ébresztőjelekkel való spam-elését, ha a kapcsolót gyorsan váltogatják.

- **Turn-Off Debounce (Kikapcsolási Debounce):** Az az minimális idő (másodpercben), aminek el kell telnie, mielőtt a 'kikapcsolás' parancs ismét végrehajtható lenne. 

- **Delay Between Commands (Késleltetés a parancsok között):** Nagyon rövid késleltetés (másodpercben) a sorozatos parancsok `bluetoothctl` segédprogramnak történő küldése között. Egyes rendszereken egy kis szünet hozzáadása javíthatja a megbízhatóságot.

- **Process Spawn Timeout (Folyamatindítási időtúllépés):** A `bluetoothctl` folyamat indításának maximális várakozási ideje (másodpercben). Ha ezen időn belül nem indul el, a bekapcsolási kísérlet sikertelen lesz.

- **Pairing Timeout (Párosítási időtúllépés):** Az egyszerűsített bekapcsolási logikában ez az az időtartam, ameddig a `pair` parancs elküldése után várni kell a siker feltételezése előtt. Időt ad az eszköznek az ébresztőjel feldolgozására.

- **Bluetooth Scan Duration (Bluetooth szkennelés időtartama):** Az az időtartam (másodpercben), ameddig az integráció Bluetooth eszközöket keres, mielőtt megpróbálná elküldeni a párosítási parancsot. A hosszabb szkennelés segíthet megtalálni azokat az eszközöket, amelyek lassan hirdetik a jelenlétüket.

## Olvass a saját nyelveden

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