# MiPower — Home Assistant सानुकूल (कस्टम) एकत्रीकरण (इंटीग्रेशन)

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** हे एक Home Assistant एकत्रीकरण आहे जे आपल्याला पारंपारिक वेक-ऑन-लॅन (Wake-on-LAN - WOL) चे समर्थन न करणाऱ्या, परंतु ब्लूटूथ पेअरिंग (जोडणी) विनंतीद्वारे "जागृत" होऊ शकणाऱ्या मीडिया प्लेयर्सची उर्जा स्थिती नियंत्रित करण्यास अनुमती देते. हे विशेषतः Xiaomi Mi Box सारख्या उपकरणांसाठी डिझाइन केले गेले होते, परंतु इतर तत्सम Android TV बॉक्समध्ये देखील कार्य करू शकते.

हे एकत्रीकरण Home Assistant मध्ये एक `switch` (स्विच) एंटिटी तयार करते. 
- स्विच **चालू** केल्याने डिव्हाइसला जागे करण्यासाठी `bluetoothctl` द्वारे ब्लूटूथ कमांडची एक श्रृंखला पाठवली जाते.
- स्विच **बंद** केल्याने लिंक केलेल्या डिव्हाइससाठी `media_player.turn_off` सेवा कॉल होते.
- स्विचची स्थिती आपोआप लिंक केलेल्या मीडिया प्लेयर एंटिटीच्या स्थितीसह सिंक्रोनाइझ (समक्रमित) केली जाते.

## 🤝 समर्थन करा

MiPower प्रकल्पाचा विकास ओपन सोर्स समुदायामध्ये मूल्य वाढवण्याच्या दृष्टिकोनातून केला जात आहे. या प्रकल्पाची सातत्यता आणि विकासाचा वेग कायम राखण्यासाठी आपले समर्थन महत्त्वपूर्ण आहे.

जर तुम्ही माझ्या प्रयत्नांचे कौतुक करत असाल, तर तुम्ही GitHub Sponsors किंवा खालील प्लॅटफॉर्म्सद्वारे मला समर्थन देऊ शकता. आगाऊ धन्यवाद!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

पर्यायीरित्या, तुम्ही रिपॉझिटरीच्या वरच्या उजव्या कोपऱ्यातील **प्रायोजक बटणावर (❤️)** क्लिक करून सर्व फंडिंग पर्याय पाहू शकता.

## पूर्व-आवश्यकता

- **Home Assistant OS / Supervised / Container:** या एकत्रीकरणासाठी Linux-आधारित Home Assistant इंस्टॉलेशन आवश्यक आहे जिथे `bluetoothctl` कमांड-लाइन साधन उपलब्ध आणि प्रवेशयोग्य असेल. हे Windows वरील Home Assistant Core इंस्टॉलेशनवर **कार्य करणार नाही**.

## HACS द्वारे स्थापना (शिफारस केलेले)

हे एकत्रीकरण HACS मध्ये कस्टम रेपॉझिटरी म्हणून उपलब्ध आहे.

1.  आपल्या HACS डॅशबोर्डवर नेव्हिगेट करा.
2.  **Integrations** (एकत्रीकरणे) वर क्लिक करा.
3.  वरच्या उजव्या कोपऱ्यातील तीन-ठिपक्यांच्या मेनूवर क्लिक करा आणि **"Custom repositories"** ("सानुकूल रेपॉझिटरीज") निवडा.
4.  डायलॉग बॉक्समध्ये, खालील माहिती प्रविष्ट करा:
    - **Repository (रेपॉझिटरी):** `https://github.com/DenizOner/MiPower`
    - **Category (श्रेणी):** `Integration` (एकत्रीकरण)
5.  **"Add"** ("जोडा") वर क्लिक करा.
6.  "MiPower" एकत्रीकरण आता आपल्या HACS सूचीमध्ये दिसेल. त्यावर क्लिक करा.
7.  **"Download"** ("डाउनलोड") बटणावर क्लिक करा आणि नंतर पुढील विंडोमध्ये पुन्हा **"Download"** ("डाउनलोड") वर क्लिक करा.
8.  डाउनलोड पूर्ण झाल्यानंतर, एकत्रीकरण लोड होण्यासाठी **तुम्हाला Home Assistant रीस्टार्ट करणे आवश्यक आहे**.

## मॅन्युअल स्थापना

HACS शिफारस केलेली पद्धत असली तरी, आपण मॅन्युअली देखील एकत्रीकरण स्थापित करू शकता.

1.  रेपॉझिटरीच्या [Releases Page](https://github.com/DenizOner/MiPower/releases) वर जा आणि नवीनतम रीलिझमधून `mipower.zip` फाइल डाउनलोड करा.
2.  डाउनलोड केलेली फाइल अनझिप करा (Unzip).
3.  अनझिप केलेल्या फोल्डरमध्ये, तुम्हाला `custom_components` डिरेक्टरी मिळेल. त्यातून `mipower` फोल्डर कॉपी करा.
4.  कॉपी केलेला `mipower` फोल्डर आपल्या Home Assistant कॉन्फिगरेशन डिरेक्टरीतील `custom_components` फोल्डरमध्ये पेस्ट करा. जर `custom_components` फोल्डर अस्तित्वात नसेल, तर तुम्हाला तो तयार करावा लागेल.
    - अंतिम मार्ग असा दिसला पाहिजे: `.../config/custom_components/mipower/`
5.  Home Assistant रीस्टार्ट करा.

## कॉन्फिगरेशन

रीस्टार्ट केल्यानंतर, आपण MiPower स्विच जोडू आणि कॉन्फिगर करू शकता.

1.  **Settings > Devices & Services** (सेटिंग्ज > उपकरणे आणि सेवा) येथे जा.
2.  तळाशी उजव्या कोपऱ्यातील **"+ Add Integration"** ("+ एकत्रीकरण जोडा") बटणावर क्लिक करा.
3.  **"MiPower"** शोधा आणि त्यावर क्लिक करा.

### सुलभ सेटअप (शिफारस केलेले)

हे एकत्रीकरण कॉन्फिगर करण्याचा सर्वात सोपा मार्ग आहे.

1.  विचारले असता, **"Easy Setup"** ("सुलभ सेटअप") निवडा.
2.  एकत्रीकरण आपल्या सिस्टमवरील ब्लूटूथ-सक्षम मीडिया प्लेयर्स स्वयंचलितपणे शोधते.
3.  ड्रॉप-डाउन सूचीमधून आपले लक्ष्य डिव्हाइस (उदा. "Xiaomi Mi Box 4") निवडा.
4.  **"Submit"** ("सबमिट करा") वर क्लिक करा.

बस एवढेच! एकत्रीकरण आपल्या मीडिया प्लेयरशी लिंक केलेला स्विच तयार करेल.

### प्रगत सेटअप

जर सुलभ सेटअपला आपले डिव्हाइस सापडले नाही किंवा आपल्याला सुरुवातीपासून प्रगत टाइमिंग सेटिंग्ज कॉन्फिगर करायची असल्यास ही पद्धत वापरा.

1.  **पायरी 1: डिव्हाइस निवड**
    - **"Advanced Setup"** ("प्रगत सेटअप") निवडा.
    - आपल्या Home Assistant मधील *सर्व* मीडिया प्लेयर्सच्या सूचीमधून आपला लक्ष्य मीडिया प्लेयर निवडा.
2.  **पायरी 2: MAC ॲड्रेस**
    - एकत्रीकरण निवडलेल्या डिव्हाइसचा ब्लूटूथ MAC ॲड्रेस शोधण्याचा प्रयत्न करेल. 
    - आढळल्यास, ते पूर्व-भरलेले असेल. ते बरोबर असल्याची खात्री करा.
    - न आढळल्यास, आपल्याला आपल्या डिव्हाइसचा ब्लूटूथ MAC ॲड्रेस मॅन्युअली प्रविष्ट करावा लागेल.
3.  **पायरी 3: टाइमिंग सेटिंग्ज**
    - आपण ब्लूटूथ कमांडसाठी विविध टाइमआउट्स आणि विलंब कॉन्फिगर करू शकता. बहुतेक वापरकर्त्यांसाठी, डीफॉल्ट मूल्ये पुरेशी आहेत.
4.  सेटअप पूर्ण करण्यासाठी **"Submit"** ("सबमिट करा") वर क्लिक करा.

## पर्याय

एकदा आपण आपला MiPower स्विच कॉन्फिगर केल्यानंतर, आपण कोणत्याही वेळी टाइमिंग सेटिंग्ज समायोजित करू शकता.

1.  **Settings > Devices & Services** (सेटिंग्ज > उपकरणे आणि सेवा) येथे जा.
2.  MiPower एकत्रीकरण शोधा आणि **"Configure"** ("कॉन्फिगर करा") वर क्लिक करा.
3.  आवश्यकतेनुसार *debounce*, टाइमआउट्स आणि विलंब यासाठीचे स्लाइडर्स समायोजित करा.

## टाइमिंग सेटिंग्जचे स्पष्टीकरण

कॉन्फिगरेशन किंवा पर्याय मेनूमध्ये, आपण ब्लूटूथ कमांडच्या वेळेत बारीक बदल करू शकता. बहुतेक वापरकर्त्यांसाठी, डीफॉल्ट मूल्ये चांगली काम करतात.

- **Turn-On Debounce (चालू करण्याचा debounce):** 'चालू करा' कमांड पुन्हा कार्यान्वित करण्यापूर्वी तो किमान वेळ (सेकंदांमध्ये) आहे. स्विच त्वरीत टॉगल केल्यास डिव्हाइसला वेक-अप सिग्नलसह स्पॅम करणे हे थांबवते.

- **Turn-Off Debounce (बंद करण्याचा debounce):** 'बंद करा' कमांड पुन्हा कार्यान्वित करण्यापूर्वी तो किमान वेळ (सेकंदांमध्ये) आहे. 

- **Delay Between Commands (कमांड्समधील विलंब):** `bluetoothctl` युटिलिटीला लागोपाठ कमांड पाठवतानाचा एक अतिशय लहान विलंब (सेकंदांमध्ये). काही सिस्टमवर, थोडासा विराम जोडल्याने विश्वसनीयता सुधारू शकते.

- **Process Spawn Timeout (प्रक्रिया सुरू करण्याचा टाइमआउट):** `bluetoothctl` प्रक्रिया सुरू होण्याची वाट पाहण्याची कमाल वेळ (सेकंदांमध्ये). जर ती या वेळेत सुरू होण्यास अयशस्वी झाली, तर चालू करण्याचा प्रयत्न अयशस्वी होईल.

- **Pairing Timeout (पेअरिंग टाइमआउट):** सरलीकृत टर्न-ऑन लॉजिकमध्ये, यशस्वी झाले असे गृहीत धरण्यापूर्वी `pair` कमांड पाठवल्यानंतर थांबण्याची ही वेळ आहे. हे डिव्हाइसला वेक-अप सिग्नलवर प्रक्रिया करण्यासाठी वेळ देते.

- **Bluetooth Scan Duration (ब्लूटूथ स्कॅन कालावधी):** पेअर कमांड पाठवण्याचा प्रयत्न करण्यापूर्वी एकत्रीकरण ब्लूटूथ डिव्हाइससाठी स्कॅन करेल तो कालावधी (सेकंदांमध्ये). दीर्घ स्कॅनमुळे त्यांची उपस्थिती जाहिरात करण्यास मंद असलेल्या डिव्हाइसेसना शोधण्यास मदत होऊ शकते.

## तुमच्या स्वतःच्या भाषेत वाचा

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