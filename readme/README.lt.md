# MiPower — Home Assistant pritaikyta integracija

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** yra Home Assistant integracija, leidžianti valdyti medijos leistuvų, kurie nepalaiko tradicinio Wake-on-LAN (WOL), bet gali būti „pažadinti“ Bluetooth susiejimo užklausa, maitinimo būseną. Ji buvo specialiai sukurta tokiems įrenginiams kaip Xiaomi Mi Box, bet gali veikti ir su kitomis panašiomis Android TV dėžutėmis.

Ši integracija sukuria `switch` (jungiklio) entitį Home Assistant. 
- **Įjungus** jungiklį, per `bluetoothctl` siunčiama Bluetooth komandų seka, kad įrenginys būtų pažadintas.
- **Išjungus** jungiklį, iškviečiama `media_player.turn_off` paslauga prijungtam įrenginiui.
- Jungiklio būsena automatiškai sinchronizuojama su prijungto medijos leistuvo entiteto būsena.

## 🤝 Paremkite mus

MiPower projektas kuriamas siekiant suteikti vertę atvirojo kodo bendruomenei. Jūsų parama yra gyvybiškai svarbi siekiant išlaikyti šio projekto tęstinumą ir plėtros greitį.

Jei vertinate mano darbą, galite mane paremti per „GitHub Sponsors“ arba šias platformas. Dėkoju iš anksto!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Arba galite peržiūrėti visas finansavimo parinktis spustelėdami **rėmėjo mygtuką (❤️)** saugyklos viršutiniame dešiniajame kampe.

## Būtinos sąlygos

- **Home Assistant OS / Supervised / Container:** Šiai integracijai reikalinga „Linux“ pagrindu veikianti Home Assistant instaliacija, kurioje būtų prieinamas ir pasiekiamas `bluetoothctl` komandų eilutės įrankis. Ji **neveiks** Home Assistant Core instaliacijoje „Windows“ sistemoje.

## Diegimas per HACS (rekomenduojama)

Ši integracija pasiekiama kaip pritaikyta repozitorija HACS.

1.  Eikite į savo HACS prietaisų skydelį.
2.  Spustelėkite **Integrations** (Integracijos).
3.  Spustelėkite trijų taškų meniu viršutiniame dešiniajame kampe ir pasirinkite **"Custom repositories"** ("Pritaikytos repozitorijos").
4.  Dialogo lange įveskite šią informaciją:
    - **Repository (Repozitorija):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategorija):** `Integration` (Integracija)
5.  Spustelėkite **"Add"** ("Pridėti").
6.  "MiPower" integracija dabar pasirodys jūsų HACS sąraše. Spustelėkite ją.
7.  Spustelėkite mygtuką **"Download"** ("Atsisiųsti") ir tada dar kartą spustelėkite **"Download"** ("Atsisiųsti") kitame lange.
8.  Atsisiuntus, **turite iš naujo paleisti Home Assistant**, kad integracija būtų įkelta.

## Rankinis diegimas

Nors HACS yra rekomenduojamas metodas, integraciją galite įdiegti ir rankiniu būdu.

1.  Eikite į repozitorijos [Išleidimų puslapį](https://github.com/DenizOner/MiPower/releases) ir atsisiųskite `mipower.zip` failą iš naujausio leidimo.
2.  Išpakuokite atsisiųstą failą.
3.  Išpakuotame aplanke rasite `custom_components` katalogą. Nukopijuokite `mipower` aplanką iš jo.
4.  Įklijuokite nukopijuotą `mipower` aplanką į `custom_components` aplanką savo Home Assistant konfigūracijos kataloge. Jei `custom_components` aplankas neegzistuoja, turite jį sukurti.
    - Galutinis kelias turėtų atrodyti taip: `.../config/custom_components/mipower/`
5.  Iš naujo paleiskite Home Assistant.

## Konfigūracija

Po perkrovimo galite pridėti ir konfigūruoti MiPower jungiklį.

1.  Eikite į **Settings > Devices & Services** (Nustatymai > Įrenginiai ir Paslaugos).
2.  Spustelėkite mygtuką **"+ Add Integration"** ("+ Pridėti Integraciją") apatiniame dešiniajame kampe.
3.  Ieškokite **"MiPower"** ir spustelėkite jį.

### Lengvas nustatymas (rekomenduojama)

Tai yra paprasčiausias būdas konfigūruoti integraciją.

1.  Kai būsite paraginti, pasirinkite **"Easy Setup"** ("Lengvas nustatymas").
2.  Integracija automatiškai aptiks jūsų sistemoje „Bluetooth“ įgalintus medijos leistuvus.
3.  Pasirinkite savo tikslinį įrenginį (pvz., "Xiaomi Mi Box 4") iš išskleidžiamojo sąrašo.
4.  Spustelėkite **"Submit"** ("Pateikti").

Štai ir viskas! Integracija sukurs jungiklį, susietą su jūsų medijos leistuvu.

### Išplėstinis nustatymas

Naudokite šį metodą, jei lengvas nustatymas neranda jūsų įrenginio arba jei jums reikia nuo pat pradžių konfigūruoti išplėstinius laiko nustatymus.

1.  **1 žingsnis: Įrenginio pasirinkimas**
    - Pasirinkite **"Advanced Setup"** ("Išplėstinis nustatymas").
    - Pasirinkite savo tikslinį medijos leistuvą iš *visų* Home Assistant medijos leistuvų sąrašo.
2.  **2 žingsnis: MAC adresas**
    - Integracija bandys rasti pasirinkto įrenginio „Bluetooth“ MAC adresą. 
    - Jei bus rastas, jis bus iš anksto užpildytas. Patikrinkite, ar jis teisingas.
    - Jei nerastas, turite rankiniu būdu įvesti savo įrenginio „Bluetooth“ MAC adresą.
3.  **3 žingsnis: Laiko nustatymai**
    - Galite konfigūruoti įvairius laiko limitus ir vėlavimus „Bluetooth“ komandoms. Daugeliui vartotojų pakanka numatytųjų verčių.
4.  Spustelėkite **"Submit"** ("Pateikti"), kad užbaigtumėte nustatymą.

## Parinktys

Sukonfigūravę „MiPower“ jungiklį, bet kada galite koreguoti laiko nustatymus.

1.  Eikite į **Settings > Devices & Services** (Nustatymai > Įrenginiai ir Paslaugos).
2.  Raskite „MiPower“ integraciją ir spustelėkite **"Configure"** ("Konfigūruoti").
3.  Pagal poreikį sureguliuokite slankiklius *vėlavimo šalinimui (debounce)*, laiko limitams ir vėlavimams.

## Laiko nustatymų paaiškinimas

Konfigūracijos ar parinkčių meniu galite tiksliai sureguliuoti „Bluetooth“ komandų laiką. Daugeliui vartotojų numatytosios vertės veikia gerai.

- **Turn-On Debounce (Įjungimo Vėlavimo Šalinimas):** Minimalus laikas (sekundėmis), kuris turi praeiti, kol komanda „įjungti“ gali būti vėl vykdoma. Tai neleidžia užtvindyti įrenginio pabudimo signalais, jei jungiklis perjungiamas greitai.

- **Turn-Off Debounce (Išjungimo Vėlavimo Šalinimas):** Minimalus laikas (sekundėmis), kuris turi praeiti, kol komanda „išjungti“ gali būti vėl vykdoma. 

- **Delay Between Commands (Vėlavimas Tarp Komandų):** Labai trumpas vėlavimas (sekundėmis) tarp nuoseklių komandų siuntimo į `bluetoothctl` įrankį. Kai kuriose sistemose nedidelės pauzės pridėjimas gali pagerinti patikimumą.

- **Process Spawn Timeout (Proceso Paleidimo Laiko Limitas):** Maksimalus laikas (sekundėmis), per kurį laukiama, kol pasileis `bluetoothctl` procesas. Jei jis nepasileidžia per šį laiką, bandymas įjungti nepavyks.

- **Pairing Timeout (Susiejimo Laiko Limitas):** Supaprastinto įjungimo logikoje tai yra laikas, kurį reikia laukti po komandos `pair` išsiuntimo, prieš darant prielaidą, kad pavyko. Tai suteikia įrenginiui laiko apdoroti pabudimo signalą.

- **Bluetooth Scan Duration (Bluetooth Nuskaitymo Trukmė):** Trukmė (sekundėmis), kurią integracija ieškos „Bluetooth“ įrenginių prieš bandydama siųsti susiejimo komandą. Ilgesnis nuskaitymas gali padėti rasti įrenginius, kurie lėtai praneša apie savo buvimą.

## Skaitykite savo kalba

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