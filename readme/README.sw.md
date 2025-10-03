# MiPower — Usanifu Maalum wa Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)

--- 

**MiPower** ni usanifu wa Home Assistant unaokuruhusu kudhibiti hali ya umeme ya vicheza media ambavyo haviungi mkono Wake-on-LAN (WOL) ya jadi lakini vinaweza "kuamshwa" kwa ombi la kuoanisha la Bluetooth. Iliundwa mahsusi kwa vifaa kama vile Xiaomi Mi Box, lakini inaweza kufanya kazi na visanduku vingine vya Android TV vinavyofanana.

Usanifu huu huunda huluki ya `switch` (swichi) katika Home Assistant. 
- **Kuwasha** swichi hutuma mfululizo wa amri za Bluetooth kupitia `bluetoothctl` ili kuamsha kifaa.
- **Kuzima** swichi huita huduma ya `media_player.turn_off` kwa kifaa kilichounganishwa.
- Hali ya swichi husawazishwa kiotomatiki na hali ya huluki ya kicheza media kilichounganishwa.

## 🤝 Saidia

Mradi wa MiPower unaendelezwa kwa dira ya kuongeza thamani kwa jumuiya ya chanzo huria. Msaada wako ni muhimu sana katika kudumisha mwendelezo na kasi ya maendeleo ya mradi huu.

Ikiwa unathamini juhudi yangu, unaweza kunisaidia kupitia GitHub Sponsors au majukwaa yafuatayo. Asante mapema!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Vinginevyo, unaweza kuona chaguzi zote za ufadhili kwa kubofya **kitufe cha Mfadhili (❤️)** kwenye kona ya juu kulia ya hifadhi.

## Masharti

- **Home Assistant OS / Supervised / Container:** Usanifu huu unahitaji usakinishaji wa Home Assistant unaotegemea Linux ambapo huduma ya mstari wa amri ya `bluetoothctl` inapatikana na kufikiwa. **HAUTAFANYA KAZI** kwenye usakinishaji wa Home Assistant Core kwenye Windows.

## Usakinishaji kupitia HACS (Inapendekezwa)

Usanifu huu unapatikana kama hazina maalum katika HACS.

1.  Nenda kwenye dashibodi yako ya HACS.
2.  Bofya **Integrations** (Usanifu).
3.  Bofya menyu ya nukta tatu kwenye kona ya juu kulia na uchague **"Custom repositories"** ("Hazina Maalum").
4.  Katika kisanduku cha mazungumzo, ingiza maelezo yafuatayo:
    - **Repository (Hazina):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategoria):** `Integration` (Usanifu)
5.  Bofya **"Add"** ("Ongeza").
6.  Usanifu wa "MiPower" sasa utaonekana kwenye orodha yako ya HACS. Bofya juu yake.
7.  Bofya kitufe cha **"Download"** ("Pakua"), kisha bofya tena **"Download"** ("Pakua") kwenye dirisha linalofuata.
8.  Baada ya upakuaji kukamilika, **LAZIMA uanze upya Home Assistant** ili usanifu upakie.

## Usakinishaji wa Mwongozo

Ingawa HACS ni njia inayopendekezwa, unaweza pia kusakinisha usanifu mwenyewe.

1.  Nenda kwenye [ukurasa wa Matoleo (Releases page)](https://github.com/DenizOner/MiPower/releases) wa hazina na upakue faili ya `mipower.zip` kutoka kwa toleo la hivi karibuni.
2.  Fungua (Unzip) faili iliyopakuliwa.
3.  Ndani ya folda iliyofunguliwa, utapata saraka ya `custom_components`. Nakili folda ya `mipower` kutoka ndani yake.
4.  Bandika folda ya `mipower` iliyonakiliwa kwenye folda ya `custom_components` kwenye saraka yako ya usanidi wa Home Assistant. Ikiwa folda ya `custom_components` haipo, unahitaji kuiunda.
    - Njia ya mwisho inapaswa kuonekana kama hii: `.../config/custom_components/mipower/`
5.  Anzisha upya Home Assistant.

## Usanidi

Baada ya kuanza upya, unaweza kuongeza na kusanidi swichi ya MiPower.

1.  Nenda kwa **Settings > Devices & Services** (Mipangilio > Vifaa na Huduma).
2.  Bofya kitufe cha **"+ Add Integration"** ("+ Ongeza Usanifu") kwenye kona ya chini kulia.
3.  Tafuta **"MiPower"** na ubofye juu yake.

### Usanidi Rahisi (Inapendekezwa)

Hii ndiyo njia rahisi zaidi ya kusanidi usanifu.

1.  Unapoombwa, chagua **"Easy Setup"** ("Usanidi Rahisi").
2.  Usanifu utagundua kiotomatiki vicheza media vilivyowezeshwa na Bluetooth kwenye mfumo wako.
3.  Chagua kifaa chako unachokilenga (k.m., "Xiaomi Mi Box 4") kutoka kwenye orodha kunjuzi.
4.  Bofya **"Submit"** ("Wasilisha").

Hiyo ndiyo! Usanifu utaunda swichi iliyounganishwa na kicheza media chako.

### Usanidi wa Juu

Tumia njia hii ikiwa Usanidi Rahisi hautapata kifaa chako au ikiwa unahitaji kusanidi mipangilio ya muda wa juu tangu mwanzo.

1.  **Hatua ya 1: Uchaguzi wa Kifaa**
    - Chagua **"Advanced Setup"** ("Usanidi wa Juu").
    - Chagua kicheza media chako unachokilenga kutoka kwenye orodha ya *vicheza media vyote* katika Home Assistant yako.
2.  **Hatua ya 2: Anwani ya MAC**
    - Usanifu utajaribu kupata Anwani ya Bluetooth MAC ya kifaa kilichochaguliwa. 
    - Ikipatikana, itajazwa mapema. Hakikisha kuwa ni sahihi.
    - Ikiwa haipatikani, lazima uingize Anwani ya Bluetooth MAC ya kifaa chako mwenyewe.
3.  **Hatua ya 3: Mipangilio ya Muda**
    - Unaweza kusanidi muda wa kupitisha na ucheleweshaji mbalimbali kwa amri za Bluetooth. Kwa watumiaji wengi, thamani chaguomsingi zinatosha.
4.  Bofya **"Submit"** ("Wasilisha") ili kukamilisha usanidi.

## Chaguzi

Baada ya kusanidi swichi yako ya MiPower, unaweza kurekebisha mipangilio ya muda wakati wowote.

1.  Nenda kwa **Settings > Devices & Services** (Mipangilio > Vifaa na Huduma).
2.  Tafuta usanifu wa MiPower na ubofye **"Configure"** ("Sanidi").
3.  Rekebisha vitelezi vya *debounce*, muda wa kupitisha, na ucheleweshaji kama inahitajika.

## Maelezo ya Mipangilio ya Muda

Katika usanidi au menyu ya chaguzi, unaweza kurekebisha muda wa amri za Bluetooth. Kwa watumiaji wengi, thamani chaguomsingi hufanya kazi vizuri.

- **Turn-On Debounce (Kuchelewa kwa Kuwasha):** Muda wa chini (katika sekunde) ambao lazima upite kabla ya amri ya 'washa' kutekelezwa tena. Hii huzuia kutuma ishara nyingi za kuamsha kifaa ikiwa swichi inabadilishwa haraka.

- **Turn-Off Debounce (Kuchelewa kwa Kuzima):** Muda wa chini (katika sekunde) ambao lazima upite kabla ya amri ya 'zima' kutekelezwa tena. 

- **Delay Between Commands (Kuchelewa Kati ya Amri):** Kuchelewa kifupi sana (katika sekunde) kati ya kutuma amri mfululizo kwa huduma ya `bluetoothctl`. Kwenye baadhi ya mifumo, kuongeza pause ndogo kunaweza kuboresha uaminifu.

- **Process Spawn Timeout (Muda wa Kupitisha wa Kuanzisha Mchakato):** Muda wa juu (katika sekunde) wa kusubiri mchakato wa `bluetoothctl` kuanza. Ikiwa inashindwa kuanza ndani ya muda huu, jaribio la kuwasha litashindwa.

- **Pairing Timeout (Muda wa Kupitisha wa Kuoanisha):** Katika mantiki iliyorahisishwa ya kuwasha, huu ni muda wa kusubiri baada ya kutuma amri ya `pair` kabla ya kudhani mafanikio. Inakipa kifaa muda wa kuchakata ishara ya kuamsha.

- **Bluetooth Scan Duration (Muda wa Kuskani kwa Bluetooth):** Muda (katika sekunde) ambao usanifu utasaka vifaa vya Bluetooth kabla ya kujaribu kutuma amri ya kuoanisha. Kuskani kwa muda mrefu kunaweza kusaidia kupata vifaa ambavyo huchelewa kutangaza uwepo wao.

## Soma kwa lugha yako mwenyewe

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