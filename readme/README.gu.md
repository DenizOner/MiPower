# MiPower — Home Assistant કસ્ટમ ઇન્ટિગ્રેશન

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** એ Home Assistant ઇન્ટિગ્રેશન છે જે તમને મીડિયા પ્લેયર્સની પાવર સ્થિતિને નિયંત્રિત કરવાની મંજૂરી આપે છે જે પરંપરાગત Wake-on-LAN (WOL) ને સપોર્ટ કરતા નથી પરંતુ બ્લૂટૂથ પેરિંગ વિનંતી દ્વારા "જાગી" શકે છે. તે ખાસ કરીને Xiaomi Mi Box જેવા ઉપકરણો માટે ડિઝાઇન કરવામાં આવ્યું હતું, પરંતુ તે અન્ય સમાન Android TV બોક્સ સાથે પણ કામ કરી શકે છે.

આ ઇન્ટિગ્રેશન Home Assistant માં એક `switch` (સ્વિચ) એન્ટિટી બનાવે છે. 
- સ્વિચને **ચાલુ** કરવાથી ઉપકરણને જગાડવા માટે `bluetoothctl` દ્વારા બ્લૂટૂથ કમાન્ડ્સની શ્રેણી મોકલવામાં આવે છે.
- સ્વિચને **બંધ** કરવાથી લિંક કરેલ ઉપકરણ માટે `media_player.turn_off` સેવાને કૉલ કરવામાં આવે છે.
- સ્વિચની સ્થિતિ આપમેળે લિંક કરેલ મીડિયા પ્લેયર એન્ટિટીની સ્થિતિ સાથે સમન્વયિત થાય છે.

## 🤝 સમર્થન કરો

MiPower પ્રોજેક્ટ ઓપન સોર્સ સમુદાયમાં મૂલ્ય ઉમેરવાના વિઝન સાથે વિકસાવવામાં આવી રહ્યો છે. આ પ્રોજેક્ટની સાતત્યતા અને વિકાસની ગતિ જાળવી રાખવા માટે તમારું સમર્થન મહત્ત્વપૂર્ણ છે.

જો તમે મારા પ્રયત્નોની કદર કરો છો, તો તમે GitHub Sponsors અથવા નીચે આપેલા પ્લેટફોર્મ્સ દ્વારા મને સમર્થન આપી શકો છો. અગાઉથી આભાર!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

વૈકલ્પિક રીતે, તમે રિપોઝીટરીના ઉપરના જમણા ખૂણે **સ્પોન્સર બટન (❤️)** પર ક્લિક કરીને તમામ ફંડિંગ વિકલ્પો જોઈ શકો છો.

## પૂર્વજરૂરીયાતો

- **Home Assistant OS / Supervised / Container:** આ ઇન્ટિગ્રેશનને Linux-આધારિત Home Assistant ઇન્સ્ટોલેશનની જરૂર છે જ્યાં `bluetoothctl` કમાન્ડ-લાઇન ટૂલ ઉપલબ્ધ અને સુલભ હોય. તે Windows પરના Home Assistant Core ઇન્સ્ટોલેશન પર **કામ કરશે નહીં**.

## HACS દ્વારા ઇન્સ્ટોલેશન (ભલામણ કરેલ)

આ ઇન્ટિગ્રેશન HACS માં કસ્ટમ રિપોઝીટરી તરીકે ઉપલબ્ધ છે.

1.  તમારા HACS ડેશબોર્ડ પર નેવિગેટ કરો.
2.  **Integrations** (ઇન્ટિગ્રેશન્સ) પર ક્લિક કરો.
3.  ઉપર-જમણા ખૂણે ત્રણ-બિંદુઓવાળા મેનૂ પર ક્લિક કરો અને **"Custom repositories"** ("કસ્ટમ રિપોઝીટરીઝ") પસંદ કરો.
4.  ડાયલોગ બોક્સમાં, નીચેની માહિતી દાખલ કરો:
    - **Repository (રિપોઝીટરી):** `https://github.com/DenizOner/MiPower`
    - **Category (કેટેગરી):** `Integration` (ઇન્ટિગ્રેશન)
5.  **"Add"** ("ઉમેરો") પર ક્લિક કરો.
6.  "MiPower" ઇન્ટિગ્રેશન હવે તમારી HACS સૂચિમાં દેખાશે. તેના પર ક્લિક કરો.
7.  **"Download"** ("ડાઉનલોડ") બટન પર ક્લિક કરો અને પછી આગલી વિંડોમાં ફરીથી **"Download"** ("ડાઉનલોડ") પર ક્લિક કરો.
8.  ડાઉનલોડ પૂર્ણ થયા પછી, ઇન્ટિગ્રેશન લોડ થવા માટે **તમારે Home Assistant ને પુનઃપ્રારંભ કરવું આવશ્યક છે**.

## મેન્યુઅલ ઇન્સ્ટોલેશન

જ્યારે HACS ભલામણ કરેલ પદ્ધતિ છે, તમે ઇન્ટિગ્રેશનને મેન્યુઅલી પણ ઇન્સ્ટોલ કરી શકો છો.

1.  રિપોઝીટરીના [રીલીઝ પેજ](https://github.com/DenizOner/MiPower/releases) પર જાઓ અને નવીનતમ રીલીઝમાંથી `mipower.zip` ફાઇલ ડાઉનલોડ કરો.
2.  ડાઉનલોડ કરેલ ફાઇલને અનઝિપ કરો.
3.  અનઝિપ કરેલ ફોલ્ડરની અંદર, તમને એક `custom_components` ડિરેક્ટરી મળશે. તેમાંથી `mipower` ફોલ્ડરની નકલ કરો.
4.  નકલ કરેલ `mipower` ફોલ્ડરને તમારા Home Assistant રૂપરેખાંકન ડિરેક્ટરીમાં `custom_components` ફોલ્ડરમાં પેસ્ટ કરો. જો `custom_components` ફોલ્ડર અસ્તિત્વમાં નથી, તો તમારે તેને બનાવવું પડશે.
    - અંતિમ પાથ આના જેવો દેખાવો જોઈએ: `.../config/custom_components/mipower/`
5.  Home Assistant ને પુનઃપ્રારંભ કરો.

## રૂપરેખાંકન

પુનઃપ્રારંભ કર્યા પછી, તમે MiPower સ્વિચ ઉમેરી અને રૂપરેખાંકિત કરી શકો છો.

1.  **Settings > Devices & Services** (સેટિંગ્સ > ઉપકરણો અને સેવાઓ) પર જાઓ.
2.  નીચે-જમણા ખૂણે **"+ Add Integration"** ("+ ઇન્ટિગ્રેશન ઉમેરો") બટન પર ક્લિક કરો.
3.  **"MiPower"** શોધો અને તેના પર ક્લિક કરો.

### સરળ સેટઅપ (ભલામણ કરેલ)

ઇન્ટિગ્રેશનને ગોઠવવાનો આ સૌથી સરળ રસ્તો છે.

1.  પૂછવામાં આવે ત્યારે, **"Easy Setup"** ("સરળ સેટઅપ") પસંદ કરો.
2.  ઇન્ટિગ્રેશન આપમેળે તમારી સિસ્ટમ પર બ્લૂટૂથ-સક્ષમ મીડિયા પ્લેયર્સને શોધી કાઢશે.
3.  ડ્રોપડાઉન સૂચિમાંથી તમારું લક્ષ્ય ઉપકરણ (દા.ત., "Xiaomi Mi Box 4") પસંદ કરો.
4.  **"Submit"** ("સબમિટ કરો") પર ક્લિક કરો.

બસ! ઇન્ટિગ્રેશન તમારા મીડિયા પ્લેયર સાથે લિંક કરેલ સ્વિચ બનાવશે.

### એડવાન્સ સેટઅપ

જો સરળ સેટઅપ તમારું ઉપકરણ ન શોધે અથવા જો તમારે શરૂઆતથી એડવાન્સ સમય સેટિંગ્સને ગોઠવવાની જરૂર હોય તો આ પદ્ધતિનો ઉપયોગ કરો.

1.  **પગલું 1: ઉપકરણ પસંદગી**
    - **"Advanced Setup"** ("એડવાન્સ સેટઅપ") પસંદ કરો.
    - તમારા Home Assistant માં *તમામ* મીડિયા પ્લેયર્સની સૂચિમાંથી તમારું લક્ષ્ય મીડિયા પ્લેયર પસંદ કરો.
2.  **પગલું 2: MAC સરનામું**
    - ઇન્ટિગ્રેશન પસંદ કરેલ ઉપકરણનું બ્લૂટૂથ MAC સરનામું શોધવાનો પ્રયાસ કરશે. 
    - જો મળે, તો તે પૂર્વ-ભરાઈ જશે. ચકાસો કે તે સાચું છે.
    - જો ન મળે, તો તમારે તમારા ઉપકરણનું બ્લૂટૂથ MAC સરનામું મેન્યુઅલી દાખલ કરવું આવશ્યક છે.
3.  **પગલું 3: સમય સેટિંગ્સ**
    - તમે બ્લૂટૂથ કમાન્ડ્સ માટે વિવિધ ટાઇમઆઉટ્સ અને વિલંબને ગોઠવી શકો છો. મોટાભાગના વપરાશકર્તાઓ માટે, ડિફોલ્ટ મૂલ્યો પૂરતા છે.
4.  સેટઅપ પૂર્ણ કરવા માટે **"Submit"** ("સબમિટ કરો") પર ક્લિક કરો.

## વિકલ્પો

તમારા MiPower સ્વિચને ગોઠવ્યા પછી, તમે કોઈપણ સમયે સમય સેટિંગ્સને સમાયોજિત કરી શકો છો.

1.  **Settings > Devices & Services** (સેટિંગ્સ > ઉપકરણો અને સેવાઓ) પર જાઓ.
2.  MiPower ઇન્ટિગ્રેશન શોધો અને **"Configure"** ("રૂપરેખાંકિત કરો") પર ક્લિક કરો.
3.  જરૂર મુજબ *debounce*, ટાઇમઆઉટ્સ અને વિલંબ માટે સ્લાઇડર્સને સમાયોજિત કરો.

## સમય સેટિંગ્સ સમજૂતી

રૂપરેખાંકન અથવા વિકલ્પો મેનૂમાં, તમે બ્લૂટૂથ કમાન્ડ્સના સમયને ફાઇન-ટ્યુન કરી શકો છો. મોટાભાગના વપરાશકર્તાઓ માટે, ડિફોલ્ટ મૂલ્યો સારી રીતે કામ કરે છે.

- **Turn-On Debounce (ચાલુ કરવા માટે Debounce):** 'ચાલુ કરો' કમાન્ડ ફરીથી એક્ઝિક્યુટ થઈ શકે તે પહેલાં પસાર થવો જોઈએ તે ન્યૂનતમ સમય (સેકન્ડમાં). જો સ્વિચ ઝડપથી ટૉગલ થાય તો આ ઉપકરણને જાગૃતિ સંકેતોથી સ્પામ થવાથી અટકાવે છે.

- **Turn-Off Debounce (બંધ કરવા માટે Debounce):** 'બંધ કરો' કમાન્ડ ફરીથી એક્ઝિક્યુટ થઈ શકે તે પહેલાં પસાર થવો જોઈએ તે ન્યૂનતમ સમય (સેકન્ડમાં). 

- **Delay Between Commands (કમાન્ડ્સ વચ્ચે વિલંબ):** `bluetoothctl` યુટિલિટીને ક્રમિક કમાન્ડ્સ મોકલવા વચ્ચેનો ખૂબ જ ટૂંકો વિલંબ (સેકન્ડમાં). કેટલીક સિસ્ટમ્સ પર, નાનો વિરામ ઉમેરવાથી વિશ્વસનીયતા સુધરી શકે છે.

- **Process Spawn Timeout (પ્રોસેસ સ્પૉન ટાઇમઆઉટ):** `bluetoothctl` પ્રક્રિયા શરૂ થવા માટે રાહ જોવાનો મહત્તમ સમય (સેકન્ડમાં). જો તે આ સમયમાં શરૂ થવામાં નિષ્ફળ જાય, તો ચાલુ કરવાનો પ્રયાસ નિષ્ફળ જશે.

- **Pairing Timeout (પેરિંગ ટાઇમઆઉટ):** સરળ બનાવેલ ટર્ન-ઑન લોજિકમાં, `pair` કમાન્ડ મોકલ્યા પછી સફળતા ધારણ કરતા પહેલા રાહ જોવાનો આ સમયગાળો છે. તે ઉપકરણને જાગૃતિ સંકેત પર પ્રક્રિયા કરવા માટે સમય આપે છે.

- **Bluetooth Scan Duration (બ્લૂટૂથ સ્કેન અવધિ):** બ્લૂટૂથ ઉપકરણો માટે ઇન્ટિગ્રેશન સ્કેન કરશે તે અવધિ (સેકન્ડમાં) પેર કમાન્ડ મોકલવાનો પ્રયાસ કરતા પહેલા. લાંબો સ્કેન એવા ઉપકરણોને શોધવામાં મદદ કરી શકે છે જે તેમની હાજરીની જાહેરાત કરવામાં ધીમા હોય છે.

## તમારી પોતાની ભાષામાં વાંચો

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