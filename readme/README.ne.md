# MiPower — गृह सहायक (Home Assistant) अनुकूलन एकीकरण

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** एउटा गृह सहायक (Home Assistant) एकीकरण हो जसले तपाईंलाई परम्परागत Wake-on-LAN (WOL) लाई समर्थन नगर्ने, तर ब्लुटुथ जोडी बनाउने (pairing) अनुरोधद्वारा "जाग्न" सक्ने मिडिया प्लेयरहरूको पावर स्थिति नियन्त्रण गर्न अनुमति दिन्छ। यो विशेष गरी Xiaomi Mi Box जस्ता उपकरणहरूको लागि डिजाइन गरिएको थियो, तर अन्य समान एन्ड्रोइड टिभी बक्सहरूसँग पनि काम गर्न सक्छ।

यो एकीकरणले गृह सहायकमा एउटा `switch` (स्विच) इन्टिटी सिर्जना गर्दछ। 
- स्विच **अन** गर्दा उपकरणलाई जगाउन `bluetoothctl` मार्फत ब्लुटुथ कमाण्डहरूको एक श्रृंखला पठाइन्छ।
- स्विच **अफ** गर्दा लिङ्क गरिएको उपकरणको लागि `media_player.turn_off` सेवा आह्वान गर्दछ।
- स्विचको स्थिति स्वचालित रूपमा लिङ्क गरिएको मिडिया प्लेयर इन्टिटीको स्थितिसँग सिंक्रोनाइज हुन्छ।

## 🤝 सहयोग गर्नुहोस्

MiPower परियोजना खुला स्रोत समुदायमा मूल्य थप्ने दृष्टिकोणका साथ विकास भइरहेको छ। यस परियोजनाको निरन्तरता र विकासको गति कायम राख्न तपाईंको सहयोग महत्त्वपूर्ण छ।

यदि तपाईं मेरो प्रयासको कदर गर्नुहुन्छ भने, तपाईंले GitHub Sponsors वा निम्न प्लेटफर्महरू मार्फत मलाई सहयोग गर्न सक्नुहुन्छ। अग्रिम धन्यवाद!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

वैकल्पिक रूपमा, तपाईंले भण्डारको माथिल्लो दायाँ कुनामा रहेको **प्रायोजक बटन (❤️)** मा क्लिक गरेर सबै कोष विकल्पहरू हेर्न सक्नुहुन्छ।

## पूर्व शर्तहरू

- **Home Assistant OS / Supervised / Container:** यो एकीकरणलाई Linux-आधारित गृह सहायक स्थापना चाहिन्छ जहाँ `bluetoothctl` कमाण्ड-लाइन उपकरण उपलब्ध र पहुँचयोग्य छ। यो Windows मा गृह सहायक कोर स्थापनामा **काम गर्दैन**।

## HACS मार्फत स्थापना (सिफारिस गरिएको)

यो एकीकरण HACS मा अनुकूलन रिपोजिटरीको रूपमा उपलब्ध छ।

1.  तपाईंको HACS ड्यासबोर्डमा जानुहोस्।
2.  **Integrations** (एकीकरणहरू) मा क्लिक गर्नुहोस्।
3.  माथिल्लो दाहिने कुनामा रहेको तीन-डट मेनुमा क्लिक गर्नुहोस् र **"Custom repositories"** ("अनुकूलन रिपोजिटरीहरू") चयन गर्नुहोस्।
4.  संवाद बाकसमा, निम्न जानकारी प्रविष्ट गर्नुहोस्:
    - **Repository (रिपोजिटरी):** `https://github.com/DenizOner/MiPower`
    - **Category (श्रेणी):** `Integration` (एकीकरण)
5.  **"Add"** ("थप्नुहोस्") मा क्लिक गर्नुहोस्।
6.  "MiPower" एकीकरण अब तपाईंको HACS सूचीमा देखा पर्नेछ। यसमा क्लिक गर्नुहोस्।
7.  **"Download"** ("डाउनलोड") बटनमा क्लिक गर्नुहोस् र त्यसपछि अर्को विन्डोमा फेरि **"Download"** ("डाउनलोड") मा क्लिक गर्नुहोस्।
8.  डाउनलोड पूरा भएपछि, एकीकरण लोड गर्नको लागि **तपाईंले गृह सहायकलाई पुन: सुरु गर्नुपर्छ**।

## म्यानुअल स्थापना

यद्यपि HACS सिफारिस गरिएको विधि हो, तपाईं म्यानुअल रूपमा पनि एकीकरण स्थापना गर्न सक्नुहुन्छ।

1.  रिपोजिटरीको [Releases Page](https://github.com/DenizOner/MiPower/releases) मा जानुहोस् र नवीनतम रिलीजबाट `mipower.zip` फाइल डाउनलोड गर्नुहोस्।
2.  डाउनलोड गरिएको फाइल अनजिप गर्नुहोस्।
3.  अनजिप गरिएको फोल्डर भित्र, तपाईंले `custom_components` निर्देशिका फेला पार्नुहुनेछ। त्यसबाट `mipower` फोल्डर प्रतिलिपि गर्नुहोस्।
4.  प्रतिलिपि गरिएको `mipower` फोल्डरलाई तपाईंको गृह सहायक कन्फिगरेसन निर्देशिकामा रहेको `custom_components` फोल्डरमा टाँस्नुहोस्। यदि `custom_components` फोल्डर अवस्थित छैन भने, तपाईंले यसलाई सिर्जना गर्नुपर्छ।
    - अन्तिम मार्ग यसरी देखिनु पर्छ: `.../config/custom_components/mipower/`
5.  गृह सहायक पुन: सुरु गर्नुहोस्।

## कन्फिगरेसन

पुनः सुरु गरेपछि, तपाईं MiPower स्विच थप्न र कन्फिगर गर्न सक्नुहुन्छ।

1.  **Settings > Devices & Services** (सेटिङहरू > उपकरण र सेवाहरू) मा जानुहोस्।
2.  तल दायाँ कुनामा रहेको **"+ Add Integration"** ("+ एकीकरण थप्नुहोस्") बटनमा क्लिक गर्नुहोस्।
3.  **"MiPower"** खोजी गर्नुहोस् र यसमा क्लिक गर्नुहोस्।

### सजिलो सेटअप (सिफारिस गरिएको)

यो एकीकरण कन्फिगर गर्ने सबैभन्दा सरल तरिका हो।

1.  प्रम्प्ट गर्दा, **"Easy Setup"** ("सजिलो सेटअप") चयन गर्नुहोस्।
2.  एकीकरणले तपाईंको प्रणालीमा ब्लुटुथ-सक्षम मिडिया प्लेयरहरू स्वचालित रूपमा पत्ता लगाउँदछ।
3.  ड्रप-डाउन सूचीबाट आफ्नो लक्षित उपकरण (उदाहरणका लागि, "Xiaomi Mi Box 4") चयन गर्नुहोस्।
4.  **"Submit"** ("पेश गर्नुहोस्") मा क्लिक गर्नुहोस्।

त्यति हो! एकीकरणले तपाईंको मिडिया प्लेयरमा लिङ्क गरिएको स्विच सिर्जना गर्नेछ।

### उन्नत सेटअप

यदि सजिलो सेटअपले तपाईंको उपकरण फेला पार्न सकेन वा तपाईंले सुरुदेखि नै उन्नत समय सेटिङहरू कन्फिगर गर्नुपर्छ भने यो विधि प्रयोग गर्नुहोस्।

1.  **चरण 1: उपकरण चयन**
    - **"Advanced Setup"** ("उन्नत सेटअप") चयन गर्नुहोस्।
    - तपाईंको गृह सहायकमा रहेका *सबै* मिडिया प्लेयरहरूको सूचीबाट आफ्नो लक्षित मिडिया प्लेयर चयन गर्नुहोस्।
2.  **चरण 2: MAC ठेगाना**
    - एकीकरणले चयन गरिएको उपकरणको ब्लुटुथ MAC ठेगाना फेला पार्ने प्रयास गर्नेछ। 
    - यदि फेला पर्यो भने, यो पूर्व-भरिएको हुनेछ। यो सही छ भनी प्रमाणित गर्नुहोस्।
    - यदि फेला परेन भने, तपाईंले आफ्नो उपकरणको ब्लुटुथ MAC ठेगाना म्यानुअल रूपमा प्रविष्ट गर्नुपर्छ।
3.  **चरण 3: समय सेटिङहरू**
    - तपाईं ब्लुटुथ कमाण्डहरूको लागि विभिन्न टाइमआउटहरू र ढिलाइहरू कन्फिगर गर्न सक्नुहुन्छ। धेरै जसो प्रयोगकर्ताहरूको लागि, पूर्वनिर्धारित मानहरू पर्याप्त छन्।
4.  सेटअप पूरा गर्न **"Submit"** ("पेश गर्नुहोस्") मा क्लिक गर्नुहोस्।

## विकल्पहरू

एकपटक तपाईंले आफ्नो MiPower स्विच कन्फिगर गरिसकेपछि, तपाईं कुनै पनि समयमा समय सेटिङहरू समायोजन गर्न सक्नुहुन्छ।

1.  **Settings > Devices & Services** (सेटिङहरू > उपकरण र सेवाहरू) मा जानुहोस्।
2.  MiPower एकीकरण फेला पार्नुहोस् र **"Configure"** ("कन्फिगर गर्नुहोस्") मा क्लिक गर्नुहोस्।
3.  आवश्यकता अनुसार *debounce*, टाइमआउटहरू, र ढिलाइहरूको लागि स्लाइडरहरू समायोजन गर्नुहोस्।

## समय सेटिङहरूको व्याख्या

कन्फिगरेसन वा विकल्प मेनुमा, तपाईं ब्लुटुथ कमाण्डहरूको समयलाई राम्रोसँग मिलाउन सक्नुहुन्छ। धेरै जसो प्रयोगकर्ताहरूको लागि, पूर्वनिर्धारित मानहरू राम्रोसँग काम गर्छन्।

- **Turn-On Debounce (अन गर्ने डिबाउन्स):** 'अन गर्ने' कमाण्ड फेरि कार्यान्वयन गर्न सक्नु अघि बित्नु पर्ने न्यूनतम समय (सेकेन्डमा)। यदि स्विच छिटो टगल गरियो भने वेक-अप संकेतहरूको साथ उपकरणलाई स्प्यामिङ गर्नबाट यसले रोक्छ।

- **Turn-Off Debounce (अफ गर्ने डिबाउन्स):** 'अफ गर्ने' कमाण्ड फेरि कार्यान्वयन गर्न सक्नु अघि बित्नु पर्ने न्यूनतम समय (सेकेन्डमा)। 

- **Delay Between Commands (कमाण्डहरू बीचको ढिलाइ):** `bluetoothctl` उपयोगितामा लगातार कमाण्डहरू पठाउने बीचको धेरै छोटो ढिलाइ (सेकेन्डमा)। केही प्रणालीहरूमा, सानो विराम थप्दा विश्वसनीयता सुधार गर्न सक्छ।

- **Process Spawn Timeout (प्रक्रिया सुरु हुने टाइमआउट):** `bluetoothctl` प्रक्रिया सुरु हुनको लागि पर्खने अधिकतम समय (सेकेन्डमा)। यदि यो समय भित्र सुरु गर्न असफल भयो भने, अन गर्ने प्रयास असफल हुनेछ।

- **Pairing Timeout (जोडी बनाउने टाइमआउट):** सरलीकृत टर्न-अन तर्कमा, `pair` कमाण्ड पठाएपछि सफलता मान्नु अघि पर्खने समय यो हो। यसले उपकरणलाई वेक-अप संकेत प्रक्रिया गर्न समय दिन्छ।

- **Bluetooth Scan Duration (ब्लुटुथ स्क्यान अवधि):** जोडी कमाण्ड पठाउने प्रयास गर्नु अघि एकीकरणले ब्लुटुथ उपकरणहरूको लागि स्क्यान गर्ने अवधि (सेकेन्डमा)। लामो स्क्यानले आफ्नो उपस्थिति विज्ञापन गर्न ढिलो हुने उपकरणहरू फेला पार्न मद्दत गर्न सक्छ।

## आफ्नै भाषामा पढ्नुहोस्

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