# MiPower — Ukuhlanganisa Okwenzelwe Wena kwe-Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

I **MiPower** iyisihlanganisi se-Home Assistant esikuvumela ukuthi ulawule isimo samandla sabadlali bemidiya abangawusekeli u-Wake-on-LAN (WOL) wendabuko, kodwa abangakwazi "ukuvuswa" ngesicelo sokumatanisa nge-Bluetooth. Yakhelwe ngqo amadivayisi afana ne-Xiaomi Mi Box, kodwa ingasebenza namanye amabhokisi e-Android TV afanayo.

Lokhu kuhlanganisa kudala inhlangano ye-`switch` (iswishi) ku-Home Assistant. 
- **Ukuvula** iswishi kuthumela uchungechunge lwemiyalo ye-Bluetooth nge-`bluetoothctl` ukuze kuvuswe idivayisi.
- **Ukucisha** iswishi kubiza isevisi ye-`media_player.turn_off` yedivayisi exhunyiwe.
- Isimo seswishi siyavunyelaniswa ngokuzenzakalelayo nesimo senhlangano yomdlali wemidiya exhunyiwe.

## 🤝 Sekela

Iphrojekthi i-MiPower yakhiwa ngombono wokungeza inani emphakathini womthombo ovulekile. Ukusekela kwakho kubalulekile ukuze kugcinwe ukuqhubeka kanye nejubane lokuthuthuka kwalolu hlelo.

Uma ukwazisa umsebenzi wami, ungangeseka nge-GitHub Sponsors noma ngezinkundla ezilandelayo. Ngiyabonga kusengaphambili!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Ngenye indlela, ungabona zonke izinketho zokuxhasa ngezimali ngokuchofoza inkinobho **Yesponsor (❤️)** ekhoneni eliphezulu kwesokudla sendawo yokugcina.

## Izimfuneko Zangaphambili

- **I-Home Assistant OS / Egcadiwe / Isiqukathi:** Lokhu kuhlanganisa kudinga ukufakwa kwe-Home Assistant okusekelwe ku-Linux lapho insiza yomugqa womyalo i-`bluetoothctl` itholakala futhi ifinyeleleka. Ngeke **ISEBENZE** ekufakweni kwe-Home Assistant Core ku-Windows.

## Ukufaka nge-HACS (Kunconyiwe)

Lokhu kuhlanganisa kutholakala njengendawo yokugcina yangokwezifiso ku-HACS.

1.  Hamba uye kudeshibhodi yakho ye-HACS.
2.  Chofoza ku-**Integrations** (Izihlanganisi).
3.  Chofoza imenyu yamachashazi amathathu ekhoneni eliphezulu kwesokudla bese ukhetha **"Custom repositories"** ("Izindawo zokugcina zangokwezifiso").
4.  Ebhokisini lengxoxo, faka imininingwane elandelayo:
    - **Repository (Indawo yokugcina):** `https://github.com/DenizOner/MiPower`
    - **Category (Isigaba):** `Integration` (Ukuhlanganisa)
5.  Chofoza **"Add"** ("Faka").
6.  Ukuhlanganisa i-"MiPower" manje kuzovela ohlwini lwakho lwe-HACS. Chofoza kuyo.
7.  Chofoza inkinobho ethi **"Download"** ("Landa"), bese uchofoza **"Download"** ("Landa") futhi efasiteleni elilandelayo.
8.  Ngemuva kokuba ukulanda sekuqediwe, **KUFANELE uqalise kabusha i-Home Assistant** ukuze ukuhlanganisa kulayishe.

## Ukufaka Ngesandla

Yize i-HACS iyindlela enconyiwe, ungakwazi futhi ukufaka ukuhlanganisa ngesandla.

1.  Hamba uye [ekhasini le-Releases](https://github.com/DenizOner/MiPower/releases) lendawo yokugcina bese ulanda ifayela elithi `mipower.zip` ekukhishweni kwakamuva.
2.  Vula ifayela elilandiwe.
3.  Ngaphakathi kwefolda evuliwe, uzothola uhla lwemibhalo lwe-`custom_components`. Kopisha ifolda ye-`mipower` ngaphakathi kwayo.
4.  Namathisela ifolda ye-`mipower` ekopishiwe kufolda ye-`custom_components` kuhla lwemibhalo lwakho lokucushwa kwe-Home Assistant. Uma ifolda ye-`custom_components` ingekho, udinga ukuyidala.
    - Indlela yokugcina kufanele ibukeke kanje: `.../config/custom_components/mipower/`
5.  Qalisa kabusha i-Home Assistant.

## Ukucushwa

Ngemuva kokuqalisa kabusha, ungakwazi ukwengeza futhi ulungiselele iswishi ye-MiPower.

1.  Hamba uye ku-**Settings > Devices & Services** (Izilungiselelo > Amadivayisi Nezinsizakalo).
2.  Chofoza inkinobho ethi **"+ Add Integration"** ("+ Engeza Ukuhlanganisa") ekhoneni elingezansi kwesokudla.
3.  Sesha **"MiPower"** bese uchofoza kuyo.

### Ukusetha Okulula (Kunconyiwe)

Lena indlela elula yokulungisa ukuhlanganisa.

1.  Uma utshelwa, khetha **"Easy Setup"** ("Ukusetha Okulula").
2.  Ukuhlanganisa kuzothola ngokuzenzakalelayo abadlali bemidiya abanikwe amandla i-Bluetooth kusistimu yakho.
3.  Khetha idivayisi yakho eqondiwe (isb., "Xiaomi Mi Box 4") ohlwini lokudonsela phansi.
4.  Chofoza **"Submit"** ("Hambisa").

Yilokho! Ukuhlanganisa kuzodala iswishi exhunywe kumdlali wemidiya wakho.

### Ukusetha Okuthuthukile

Sebenzisa le ndlela uma Ukusetha Okulula kungatholi idivayisi yakho noma uma udinga ukulungisa izilungiselelo zesikhathi esithuthukile kusukela ekuqaleni.

1.  **Isinyathelo 1: Ukukhetha Idivayisi**
    - Khetha **"Advanced Setup"** ("Ukusetha Okuthuthukile").
    - Khetha umdlali wemidiya oqondiwe ohlwini lwabo *bonke* abadlali bemidiya ku-Home Assistant yakho.
2.  **Isinyathelo 2: Ikheli le-MAC**
    - Ukuhlanganisa kuzozama ukuthola Ikheli le-Bluetooth MAC ledivayisi ekhethiwe. 
    - Uma litholwa, lizofakwa ngaphambili. Qinisekisa ukuthi lilungile.
    - Uma lingatholakali, kufanele ufake mathupha Ikheli le-Bluetooth MAC ledivayisi yakho.
3.  **Isinyathelo 3: Izilungiselelo Zesikhathi**
    - Ungakwazi ukulungisa izikhathi ezahlukene zokuphelelwa yisikhathi (timeouts) nokubambezeleka kwemiyalo ye-Bluetooth. Kubasebenzisi abaningi, amanani azenzakalelayo anele.
4.  Chofoza **"Submit"** ("Hambisa") ukuze uqedele ukusetha.

## Izinketho

Ngemuva kokuthi usulungiselele iswishi yakho ye-MiPower, ungakwazi ukulungisa izilungiselelo zesikhathi nganoma yisiphi isikhathi.

1.  Hamba uye ku-**Settings > Devices & Services** (Izilungiselelo > Amadivayisi Nezinsizakalo).
2.  Thola ukuhlanganisa i-MiPower bese uchofoza **"Configure"** ("Lungiselela").
3.  Lungisa izilayidi ze-*debounce*, isikhathi sokuphelelwa, kanye nokubambezeleka njengoba kudingeka.

## Izilungiselelo Zesikhathi Ezichaziwe

Kumenyu yokucushwa noma yezinketho, ungakwazi ukulungisa kahle isikhathi semiyalo ye-Bluetooth. Kubasebenzisi abaningi, amanani azenzakalelayo asebenza kahle.

- **Turn-On Debounce (Isikhathi sokuvula esihlungiwe):** Isikhathi esincane (ngemizuzwana) okufanele sidlule ngaphambi kokuba umyalo othi 'vula' ukwazi ukuphinda wenziwe. Lokhu kuvimbela ukuthumela ugaxekile kudivayisi ngezimpawu zokuvuka uma iswishi ivulwa ngokushesha.

- **Turn-Off Debounce (Isikhathi sokucisha esihlungiwe):** Isikhathi esincane (ngemizuzwana) okufanele sidlule ngaphambi kokuba umyalo othi 'cisha' ukwazi ukuphinda wenziwe. 

- **Delay Between Commands (Ukubambezeleka Phakathi Kwemiyalo):** Ukubambezeleka okufushane kakhulu (ngemizuzwana) phakathi kokuthumela imiyalo elandelanayo kusensiza ye-`bluetoothctl`. Kwezinye izinhlelo, ukwengeza ikhefu elincane kungathuthukisa ukuthembeka.

- **Process Spawn Timeout (Isikhathi sokuphelelwa kokuqalwa kwenqubo):** Isikhathi esiphezulu (ngemizuzwana) sokulinda ukuthi inqubo ye-`bluetoothctl` iqale. Uma yehluleka ukuqala ngalesi sikhathi, umzamo wokuvula uzohluleka.

- **Pairing Timeout (Isikhathi sokuphelelwa kokumatanisa):** Engqondweni elula yokuvula, lesi isikhathi okumele silinde ngaso ngemuva kokuthumela umyalo othi `pair` ngaphambi kokucabanga impumelelo. Kunikeza idivayisi isikhathi sokucubungula isignali yokuvuka.

- **Bluetooth Scan Duration (Ubude Besikhathi Sokuskena I-Bluetooth):** Ubude besikhathi (ngemizuzwana) lapho ukuhlanganisa kuzoskena khona amadivayisi e-Bluetooth ngaphambi kokuzama ukuthumela umyalo wokumatanisa. Ukuskena isikhathi eside kungasiza ukuthola amadivayisi ahamba kancane ukuze amemezele ubukhona bawo.

## Funda ngolimi lwakho

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