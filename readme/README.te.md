# MiPower — Home Assistant అనుకూల ఇంటిగ్రేషన్

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** అనేది Home Assistant ఇంటిగ్రేషన్, ఇది సాంప్రదాయ Wake-on-LAN (WOL)కి మద్దతు ఇవ్వని, కానీ బ్లూటూత్ జత చేసే అభ్యర్థన ద్వారా "మేల్కొల్పబడే" మీడియా ప్లేయర్‌ల పవర్ స్థితిని నియంత్రించడానికి మిమ్మల్ని అనుమతిస్తుంది. ఇది ప్రత్యేకంగా Xiaomi Mi Box వంటి పరికరాల కోసం రూపొందించబడింది, కానీ ఇతర సారూప్య Android TV బాక్స్‌లతో కూడా పని చేయవచ్చు.

ఈ ఇంటిగ్రేషన్ Home Assistantలో `switch` (స్విచ్) ఎంటిటీని సృష్టిస్తుంది. 
- స్విచ్‌ను **ఆన్ చేయడం** పరికరాన్ని మేల్కొల్పడానికి `bluetoothctl` ద్వారా బ్లూటూత్ ఆదేశాల శ్రేణిని పంపుతుంది.
- స్విచ్‌ను **ఆఫ్ చేయడం** లింక్ చేయబడిన పరికరం కోసం `media_player.turn_off` సేవను కాల్ చేస్తుంది.
- స్విచ్ యొక్క స్థితి స్వయంచాలకంగా లింక్ చేయబడిన మీడియా ప్లేయర్ ఎంటిటీ స్థితికి సమకాలీకరించబడుతుంది.

## 🤝 మద్దతు ఇవ్వండి

MiPower ప్రాజెక్ట్ ఓపెన్ సోర్స్ కమ్యూనిటీకి విలువను జోడించే దృష్టితో అభివృద్ధి చేయబడుతోంది. ఈ ప్రాజెక్ట్ యొక్క కొనసాగింపు మరియు అభివృద్ధి వేగాన్ని నిర్వహించడానికి మీ మద్దతు చాలా ముఖ్యమైనది.

మీరు నా కృషిని అభినందిస్తే, మీరు GitHub స్పాన్సర్‌లు లేదా క్రింది ప్లాట్‌ఫారమ్‌ల ద్వారా నాకు మద్దతు ఇవ్వవచ్చు. ముందుగా ధన్యవాదాలు!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

ప్రత్యామ్నాయంగా, మీరు రిపోజిటరీ యొక్క కుడి ఎగువ మూలలో ఉన్న **స్పాన్సర్ బటన్ (❤️)** పై క్లిక్ చేయడం ద్వారా అన్ని ఫైనాన్సింగ్ ఎంపికలను చూడవచ్చు.

## ముందుగా తెలుసుకోవలసినవి

- **Home Assistant OS / Supervised / Container:** ఈ ఇంటిగ్రేషన్‌కు `bluetoothctl` కమాండ్-లైన్ యుటిలిటీ అందుబాటులో మరియు ప్రాప్యత చేయగల Linux-ఆధారిత Home Assistant ఇన్‌స్టాలేషన్ అవసరం. ఇది Windowsలో Home Assistant Core ఇన్‌స్టాలేషన్‌లో **పని చేయదు**.

## HACS ద్వారా ఇన్‌స్టాలేషన్ (సిఫార్సు చేయబడింది)

ఈ ఇంటిగ్రేషన్ HACSలో అనుకూల రిపోజిటరీగా అందుబాటులో ఉంది.

1.  మీ HACS డాష్‌బోర్డ్‌కు నావిగేట్ చేయండి.
2.  **Integrations** (ఇంటిగ్రేషన్స్) పై క్లిక్ చేయండి.
3.  కుడి ఎగువ మూలలోని మూడు-చుక్కల మెనుపై క్లిక్ చేసి, **"Custom repositories"** ("అనుకూల రిపోజిటరీలు") ఎంచుకోండి.
4.  డైలాగ్ బాక్స్‌లో, ఈ క్రింది సమాచారాన్ని నమోదు చేయండి:
    - **Repository (రిపోజిటరీ):** `https://github.com/DenizOner/MiPower`
    - **Category (వర్గం):** `Integration` (ఇంటిగ్రేషన్)
5.  **"Add"** ("జోడించు") పై క్లిక్ చేయండి.
6.  "MiPower" ఇంటిగ్రేషన్ ఇప్పుడు మీ HACS జాబితాలో కనిపిస్తుంది. దానిపై క్లిక్ చేయండి.
7.  **"Download"** ("డౌన్‌లోడ్") బటన్‌పై క్లిక్ చేయండి, ఆపై తదుపరి విండోలో మళ్లీ **"Download"** ("డౌన్‌లోడ్") పై క్లిక్ చేయండి.
8.  డౌన్‌లోడ్ పూర్తయిన తర్వాత, ఇంటిగ్రేషన్ లోడ్ కావడానికి **మీరు తప్పనిసరిగా Home Assistantను పునఃప్రారంభించాలి**.

## మాన్యువల్ ఇన్‌స్టాలేషన్

HACS సిఫార్సు చేయబడిన పద్ధతి అయినప్పటికీ, మీరు మాన్యువల్‌గా కూడా ఇంటిగ్రేషన్‌ను ఇన్‌స్టాల్ చేయవచ్చు.

1.  రిపోజిటరీ యొక్క [Releases page (విడుదల పేజీ)](https://github.com/DenizOner/MiPower/releases)కి వెళ్లి, తాజా విడుదల నుండి `mipower.zip` ఫైల్‌ను డౌన్‌లోడ్ చేయండి.
2.  డౌన్‌లోడ్ చేసిన ఫైల్‌ను అన్జిప్ చేయండి.
3.  అన్జిప్ చేసిన ఫోల్డర్ లోపల, మీరు `custom_components` డైరెక్టరీని కనుగొంటారు. దాని లోపల నుండి `mipower` ఫోల్డర్‌ను కాపీ చేయండి.
4.  కాపీ చేసిన `mipower` ఫోల్డర్‌ను మీ Home Assistant కాన్ఫిగరేషన్ డైరెక్టరీలోని `custom_components` ఫోల్డర్‌లో అతికించండి. `custom_components` ఫోల్డర్ లేకపోతే, మీరు దానిని సృష్టించాలి.
    - తుది మార్గం ఇలా ఉండాలి: `.../config/custom_components/mipower/`
5.  Home Assistantను పునఃప్రారంభించండి.

## కాన్ఫిగరేషన్

పునఃప్రారంభించిన తర్వాత, మీరు MiPower స్విచ్‌ను జోడించవచ్చు మరియు కాన్ఫిగర్ చేయవచ్చు.

1.  **Settings > Devices & Services** (సెట్టింగ్‌లు > పరికరాలు & సేవలు)కి వెళ్లండి.
2.  దిగువ కుడి మూలలో ఉన్న **"+ Add Integration"** ("+ ఇంటిగ్రేషన్ జోడించు") బటన్‌పై క్లిక్ చేయండి.
3.  **"MiPower"** కోసం శోధించి, దానిపై క్లిక్ చేయండి.

### సులభమైన సెటప్ (సిఫార్సు చేయబడింది)

ఇది ఇంటిగ్రేషన్‌ను కాన్ఫిగర్ చేయడానికి సులభమైన మార్గం.

1.  ప్రాంప్ట్ చేసినప్పుడు, **"Easy Setup"** ("సులభమైన సెటప్") ఎంచుకోండి.
2.  ఇంటిగ్రేషన్ మీ సిస్టమ్‌లోని బ్లూటూత్-ప్రారంభించబడిన మీడియా ప్లేయర్‌లను స్వయంచాలకంగా కనుగొంటుంది.
3.  డ్రాప్‌డౌన్ జాబితా నుండి మీ లక్ష్య పరికరాన్ని (ఉదా., "Xiaomi Mi Box 4") ఎంచుకోండి.
4.  **"Submit"** ("సమర్పించు") పై క్లిక్ చేయండి.

అంతే! ఇంటిగ్రేషన్ మీ మీడియా ప్లేయర్‌కు లింక్ చేయబడిన స్విచ్‌ను సృష్టిస్తుంది.

### అధునాతన సెటప్

సులభమైన సెటప్ మీ పరికరాన్ని కనుగొనలేకపోతే లేదా మీరు ప్రారంభం నుండే అధునాతన సమయ సెట్టింగ్‌లను కాన్ఫిగర్ చేయవలసి వస్తే ఈ పద్ధతిని ఉపయోగించండి.

1.  **దశ 1: పరికర ఎంపిక**
    - **"Advanced Setup"** ("అధునాతన సెటప్") ఎంచుకోండి.
    - మీ Home Assistantలోని *అన్ని* మీడియా ప్లేయర్‌ల జాబితా నుండి మీ లక్ష్య మీడియా ప్లేయర్‌ను ఎంచుకోండి.
2.  **దశ 2: MAC చిరునామా**
    - ఇంటిగ్రేషన్ ఎంచుకున్న పరికరం యొక్క బ్లూటూత్ MAC చిరునామాను కనుగొనడానికి ప్రయత్నిస్తుంది. 
    - కనుగొనబడితే, అది ముందుగా నింపబడుతుంది. అది సరైనదని ధృవీకరించండి.
    - కనుగొనబడకపోతే, మీరు మీ పరికరం యొక్క బ్లూటూత్ MAC చిరునామాను మాన్యువల్‌గా నమోదు చేయాలి.
3.  **దశ 3: సమయ సెట్టింగ్‌లు**
    - మీరు బ్లూటూత్ ఆదేశాల కోసం వివిధ సమయ పరిమితులను మరియు ఆలస్యాలను కాన్ఫిగర్ చేయవచ్చు. చాలా మంది వినియోగదారులకు, డిఫాల్ట్ విలువలు సరిపోతాయి.
4.  సెటప్‌ను పూర్తి చేయడానికి **"Submit"** ("సమర్పించు") పై క్లిక్ చేయండి.

## ఎంపికలు

మీరు మీ MiPower స్విచ్‌ను కాన్ఫిగర్ చేసిన తర్వాత, మీరు ఎప్పుడైనా సమయ సెట్టింగ్‌లను సర్దుబాటు చేయవచ్చు.

1.  **Settings > Devices & Services** (సెట్టింగ్‌లు > పరికరాలు & సేవలు)కి వెళ్లండి.
2.  MiPower ఇంటిగ్రేషన్‌ను కనుగొని **"Configure"** ("కాన్ఫిగర్ చేయి") పై క్లిక్ చేయండి.
3.  అవసరమైన విధంగా *debounce*, సమయ పరిమితులు మరియు ఆలస్యాల కోసం స్లయిడర్‌లను సర్దుబాటు చేయండి.

## సమయ సెట్టింగ్‌ల వివరణ

కాన్ఫిగరేషన్ లేదా ఎంపికల మెనులో, మీరు బ్లూటూత్ ఆదేశాల సమయాన్ని చక్కగా ట్యూన్ చేయవచ్చు. చాలా మంది వినియోగదారులకు, డిఫాల్ట్ విలువలు బాగా పని చేస్తాయి.

- **Turn-On Debounce (ఆన్ డీబౌన్స్):** 'ఆన్ చేయి' ఆదేశాన్ని మళ్లీ అమలు చేయడానికి ముందు గడిచే కనీస సమయం (సెకన్లలో). స్విచ్ త్వరగా టోగుల్ చేయబడితే, ఇది పరికరానికి వేక్-అప్ సిగ్నల్‌లను స్పామింగ్‌ను నిరోధిస్తుంది.

- **Turn-Off Debounce (ఆఫ్ డీబౌన్స్):** 'ఆఫ్ చేయి' ఆదేశాన్ని మళ్లీ అమలు చేయడానికి ముందు గడిచే కనీస సమయం (సెకన్లలో). 

- **Delay Between Commands (ఆదేశాల మధ్య ఆలస్యం):** `bluetoothctl` యుటిలిటీకి వరుస ఆదేశాలను పంపడం మధ్య చాలా తక్కువ ఆలస్యం (సెకన్లలో). కొన్ని సిస్టమ్‌లలో, చిన్న విరామాన్ని జోడించడం విశ్వసనీయతను మెరుగుపరుస్తుంది.

- **Process Spawn Timeout (ప్రాసెస్ స్పాన్ సమయ పరిమితి):** `bluetoothctl` ప్రాసెస్ ప్రారంభించడానికి వేచి ఉండే గరిష్ట సమయం (సెకన్లలో). ఈ సమయంలో ప్రారంభించడంలో విఫలమైతే, ఆన్ ప్రయత్నం విఫలమవుతుంది.

- **Pairing Timeout (జత చేసే సమయ పరిమితి):** సరళీకృత ఆన్ లాజిక్‌లో, ఇది విజయాన్ని ఊహించడానికి ముందు `pair` ఆదేశాన్ని పంపిన తర్వాత వేచి ఉండే సమయం. వేక్-అప్ సిగ్నల్‌ను ప్రాసెస్ చేయడానికి ఇది పరికరానికి సమయాన్ని ఇస్తుంది.

- **Bluetooth Scan Duration (బ్లూటూత్ స్కాన్ వ్యవధి):** జత చేసే ఆదేశాన్ని పంపడానికి ప్రయత్నించే ముందు ఇంటిగ్రేషన్ బ్లూటూత్ పరికరాల కోసం స్కాన్ చేసే వ్యవధి (సెకన్లలో). ఎక్కువ స్కాన్ వాటి ఉనికిని ప్రకటించడానికి నెమ్మదిగా ఉన్న పరికరాలను కనుగొనడంలో సహాయపడుతుంది.

## మీ స్వంత భాషలో చదవండి

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