# MiPower — Home Assistant कस्टम इंटीग्रेशन

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** एक Home Assistant इंटीग्रेशन है जो आपको उन मीडिया प्लेयर्स की पावर स्थिति को नियंत्रित करने की अनुमति देता है जो पारंपरिक Wake-on-LAN (WOL) का समर्थन नहीं करते हैं, लेकिन एक ब्लूटूथ पेयरिंग अनुरोध द्वारा "जगाए" जा सकते हैं। इसे विशेष रूप से Xiaomi Mi Box जैसे उपकरणों के लिए डिज़ाइन किया गया था, लेकिन यह अन्य समान Android TV बॉक्स के साथ भी काम कर सकता है।

यह इंटीग्रेशन Home Assistant में एक `switch` (स्विच) एंटिटी बनाता है। 
- स्विच को **चालू** करने से डिवाइस को जगाने के लिए `bluetoothctl` के माध्यम से ब्लूटूथ कमांड की एक श्रृंखला भेजी जाती है।
- स्विच को **बंद** करने से लिंक किए गए डिवाइस के लिए `media_player.turn_off` सेवा को कॉल किया जाता है।
- स्विच की स्थिति स्वचालित रूप से लिंक किए गए मीडिया प्लेयर एंटिटी की स्थिति के साथ सिंक्रनाइज़ हो जाती है।

## 🤝 समर्थन करें

MiPower परियोजना को ओपन सोर्स समुदाय में मूल्य जोड़ने के दृष्टिकोण के साथ विकसित किया जा रहा है। इस परियोजना की निरंतरता और विकास की गति बनाए रखने के लिए आपका समर्थन अत्यंत महत्वपूर्ण है।

यदि आप मेरे प्रयास की सराहना करते हैं, तो आप GitHub Sponsors या निम्नलिखित प्लेटफॉर्म के माध्यम से मेरा समर्थन कर सकते हैं। अग्रिम धन्यवाद!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

वैकल्पिक रूप से, आप भंडार (repository) के ऊपरी दाएं कोने में **प्रायोजक बटन (❤️)** पर क्लिक करके सभी फंडिंग विकल्प देख सकते हैं।

## पूर्व-आवश्यकताएं

- **Home Assistant OS / Supervised / Container:** इस इंटीग्रेशन के लिए Linux-आधारित Home Assistant इंस्टॉलेशन की आवश्यकता होती है जहां `bluetoothctl` कमांड-लाइन टूल उपलब्ध और पहुंच योग्य हो। यह Windows पर Home Assistant Core इंस्टॉलेशन पर **काम नहीं करेगा**।

## HACS के माध्यम से इंस्टॉलेशन (अनुशंसित)

यह इंटीग्रेशन HACS में एक कस्टम रिपॉजिटरी के रूप में उपलब्ध है।

1.  अपने HACS डैशबोर्ड पर नेविगेट करें।
2.  **Integrations** (इंटीग्रेशन) पर क्लिक करें।
3.  ऊपरी-दाएं कोने में तीन-बिंदु वाले मेनू पर क्लिक करें और **"Custom repositories"** ("कस्टम रिपॉजिटरी") चुनें।
4.  डायलॉग बॉक्स में, निम्न जानकारी दर्ज करें:
    - **Repository (रिपॉजिटरी):** `https://github.com/DenizOner/MiPower`
    - **Category (श्रेणी):** `Integration` (इंटीग्रेशन)
5.  **"Add"** ("जोड़ें") पर क्लिक करें।
6.  "MiPower" इंटीग्रेशन अब आपकी HACS सूची में दिखाई देगा। इस पर क्लिक करें।
7.  **"Download"** ("डाउनलोड करें") बटन पर क्लिक करें और फिर अगली विंडो में फिर से **"Download"** ("डाउनलोड करें") पर क्लिक करें।
8.  डाउनलोड पूरा होने के बाद, इंटीग्रेशन लोड होने के लिए **आपको Home Assistant को पुनरारंभ करना होगा**।

## मैन्युअल इंस्टॉलेशन

हालांकि HACS अनुशंसित तरीका है, आप इंटीग्रेशन को मैन्युअल रूप से भी इंस्टॉल कर सकते हैं।

1.  रिपॉजिटरी के [रिलीज़ पेज](https://github.com/DenizOner/MiPower/releases) पर जाएं और नवीनतम रिलीज़ से `mipower.zip` फ़ाइल डाउनलोड करें।
2.  डाउनलोड की गई फ़ाइल को अनज़िप करें।
3.  अनज़िप किए गए फ़ोल्डर के अंदर, आपको एक `custom_components` डायरेक्टरी मिलेगी। उसमें से `mipower` फ़ोल्डर को कॉपी करें।
4.  कॉपी किए गए `mipower` फ़ोल्डर को अपने Home Assistant कॉन्फ़िगरेशन डायरेक्टरी में `custom_components` फ़ोल्डर में पेस्ट करें। यदि `custom_components` फ़ोल्डर मौजूद नहीं है, तो आपको इसे बनाना होगा।
    - अंतिम पथ इस तरह दिखना चाहिए: `.../config/custom_components/mipower/`
5.  Home Assistant को पुनरारंभ करें।

## कॉन्फ़िगरेशन

पुनरारंभ करने के बाद, आप MiPower स्विच को जोड़ और कॉन्फ़िगर कर सकते हैं।

1.  **Settings > Devices & Services** (सेटिंग्स > डिवाइस और सेवाएं) पर जाएं।
2.  निचले-दाएं कोने में **"+ Add Integration"** ("+ इंटीग्रेशन जोड़ें") बटन पर क्लिक करें।
3.  **"MiPower"** खोजें और उस पर क्लिक करें।

### आसान सेटअप (अनुशंसित)

यह इंटीग्रेशन को कॉन्फ़िगर करने का सबसे सरल तरीका है।

1.  पूछे जाने पर, **"Easy Setup"** ("आसान सेटअप") चुनें।
2.  इंटीग्रेशन स्वचालित रूप से आपके सिस्टम पर ब्लूटूथ-सक्षम मीडिया प्लेयर्स को खोज लेगा।
3.  ड्रॉपडाउन सूची से अपना लक्ष्य डिवाइस (उदाहरण के लिए, "Xiaomi Mi Box 4") चुनें।
4.  **"Submit"** ("सबमिट करें") पर क्लिक करें।

बस! इंटीग्रेशन आपके मीडिया प्लेयर से लिंक किया गया एक स्विच बनाएगा।

### उन्नत सेटअप

यदि आसान सेटअप आपके डिवाइस को नहीं ढूंढता है या यदि आपको शुरू से ही उन्नत समय सेटिंग्स को कॉन्फ़िगर करने की आवश्यकता है तो इस विधि का उपयोग करें।

1.  **चरण 1: डिवाइस चयन**
    - **"Advanced Setup"** ("उन्नत सेटअप") चुनें।
    - अपने Home Assistant में *सभी* मीडिया प्लेयर्स की सूची से अपना लक्ष्य मीडिया प्लेयर चुनें।
2.  **चरण 2: MAC पता**
    - इंटीग्रेशन चयनित डिवाइस के ब्लूटूथ MAC पते को खोजने का प्रयास करेगा। 
    - यदि पाया जाता है, तो यह पहले से भर जाएगा। सत्यापित करें कि यह सही है।
    - यदि नहीं पाया जाता है, तो आपको अपने डिवाइस का ब्लूटूथ MAC पता मैन्युअल रूप से दर्ज करना होगा।
3.  **चरण 3: समय सेटिंग्स**
    - आप ब्लूटूथ कमांड के लिए विभिन्न टाइमआउट और देरी को कॉन्फ़िगर कर सकते हैं। अधिकांश उपयोगकर्ताओं के लिए, डिफ़ॉल्ट मान पर्याप्त हैं।
4.  सेटअप पूरा करने के लिए **"Submit"** ("सबमिट करें") पर क्लिक करें।

## विकल्प

एक बार जब आप अपने MiPower स्विच को कॉन्फ़िगर कर लेते हैं, तो आप किसी भी समय समय सेटिंग्स को समायोजित कर सकते हैं।

1.  **Settings > Devices & Services** (सेटिंग्स > डिवाइस और सेवाएं) पर जाएं।
2.  MiPower इंटीग्रेशन ढूंढें और **"Configure"** ("कॉन्फ़िगर करें") पर क्लिक करें।
3.  आवश्यकतानुसार *debounce*, टाइमआउट और देरी के लिए स्लाइडर्स को समायोजित करें।

## समय सेटिंग्स की व्याख्या

कॉन्फ़िगरेशन या विकल्प मेनू में, आप ब्लूटूथ कमांड के समय को ठीक कर सकते हैं। अधिकांश उपयोगकर्ताओं के लिए, डिफ़ॉल्ट मान अच्छी तरह से काम करते हैं।

- **Turn-On Debounce (चालू करने का Debounce):** 'चालू करें' कमांड को फिर से निष्पादित करने से पहले गुजरने वाला न्यूनतम समय (सेकंड में)। यदि स्विच को तेज़ी से टॉगल किया जाता है तो यह डिवाइस को वेक-अप सिग्नल के साथ स्पैम होने से रोकता है।

- **Turn-Off Debounce (बंद करने का Debounce):** 'बंद करें' कमांड को फिर से निष्पादित करने से पहले गुजरने वाला न्यूनतम समय (सेकंड में)। 

- **Delay Between Commands (कमांड के बीच देरी):** `bluetoothctl` यूटिलिटी को लगातार कमांड भेजने के बीच एक बहुत छोटा विलंब (सेकंड में)। कुछ सिस्टमों पर, एक छोटा विराम जोड़ने से विश्वसनीयता में सुधार हो सकता है।

- **Process Spawn Timeout (प्रोसेस स्पॉन टाइमआउट):** `bluetoothctl` प्रक्रिया के शुरू होने का इंतजार करने का अधिकतम समय (सेकंड में)। यदि यह इस समय के भीतर शुरू होने में विफल रहता है, तो चालू करने का प्रयास विफल हो जाएगा।

- **Pairing Timeout (पेयरिंग टाइमआउट):** सरलीकृत टर्न-ऑन लॉजिक में, यह `pair` कमांड भेजने के बाद सफलता मानने से पहले इंतजार करने का समय है। यह डिवाइस को वेक-अप सिग्नल को संसाधित करने का समय देता है।

- **Bluetooth Scan Duration (ब्लूटूथ स्कैन अवधि):** वह अवधि (सेकंड में) जिसके लिए इंटीग्रेशन पेयर कमांड भेजने का प्रयास करने से पहले ब्लूटूथ डिवाइस के लिए स्कैन करेगा। एक लंबा स्कैन उन उपकरणों को खोजने में मदद कर सकता है जो अपनी उपस्थिति का विज्ञापन करने में धीमे हैं।

## अपनी भाषा में पढ़ें

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