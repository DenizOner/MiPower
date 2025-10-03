# MiPower — Comhtháthú saincheaptha Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

Is comhtháthú Home Assistant é **MiPower** a ligeann duit smacht a fháil ar stádas cumhachta na n-imreoirí meán nach dtacaíonn le Wake-on-LAN (WOL) traidisiúnta ach is féidir a "dhúiseacht" trí iarratas péireála Bluetooth. Dearadh é go sonrach le haghaidh feistí ar nós an Xiaomi Mi Box, ach d'fhéadfadh sé oibriú le boscaí Android TV eile dá samhail.

Cruthaíonn an comhtháthú seo eintiteas `switch` (lasc) i Home Assistant. 
- Seolann **Casadh AR** an lasc sraith d'orduithe Bluetooth trí `bluetoothctl` chun an gléas a dhúiseacht.
- Glaonn **Casadh AS** an lasc ar an seirbhís `media_player.turn_off` don ghléas nasctha.
- Déantar stádas an lasc a shioncronú go huathoibríoch le stádas an eintitis imreoir meán nasctha.

## 🤝 Tabhair Tacaíocht

Tá tionscadal MiPower á fhorbairt le fís chun luach a chur leis an bpobal foinse oscailte. Tá do thacaíocht ríthábhachtach chun leanúnachas agus luas forbartha an tionscadail seo a choinneáil.

Má tá meas agat ar mo shaothar, is féidir leat tacú liom trí GitHub Sponsors nó na hardáin seo a leanas. Go raibh maith agat roimh ré!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Mar mhalairt air sin, is féidir leat gach rogha maoinithe a fheiceáil trí chliceáil ar an **gcnaipe Urraitheora (❤️)** sa chúinne uachtarach ar dheis den stór.

## Réamhriachtanais

- **Home Assistant OS / Supervised / Coimeádán:** Éilíonn an comhtháthú seo suiteáil Home Assistant bunaithe ar Linux ina bhfuil an uirlis líne-ordú `bluetoothctl` ar fáil agus inrochtana. **Ní** oibreoidh sé ar shuiteáil Home Assistant Core ar Windows.

## Suiteáil trí HACS (Molta)

Tá an comhtháthú seo ar fáil mar stór saincheaptha i HACS.

1.  Téigh chuig do dháileog HACS.
2.  Cliceáil ar **Integrations** (Comhtháthuithe).
3.  Cliceáil ar an roghchlár trí phonc sa chúinne uachtarach ar dheis agus roghnaigh **"Custom repositories"** ("Stórtha saincheaptha").
4.  Sa bhosca dialóige, cuir isteach an t-eolas seo a leanas:
    - **Repository (Stór):** `https://github.com/DenizOner/MiPower`
    - **Category (Catagóir):** `Integration` (Comhtháthú)
5.  Cliceáil **"Add"** ("Cuir leis").
6.  Beidh an comhtháthú "MiPower" le feiceáil anois i do liosta HACS. Cliceáil air.
7.  Cliceáil an cnaipe **"Download"** ("Íoslódáil") agus ansin **"Download"** ("Íoslódáil") arís sa chéad fhuinneog eile.
8.  Tar éis don íoslódáil a bheith críochnaithe, **ní mór duit Home Assistant a atosú** chun an comhtháthú a luchtú.

## Suiteáil Láimhe

Cé gurb é HACS an modh molta, is féidir leat an comhtháthú a shuiteáil de láimh freisin.

1.  Téigh go dtí [leathanach na nEisiúintí](https://github.com/DenizOner/MiPower/releases) den stór agus íoslódáil an comhad `mipower.zip` ón eisiúint is déanaí.
2.  Díphacáil an comhad íoslódáilte.
3.  Taobh istigh den fhillteán díphacáilte, gheobhaidh tú eolaire `custom_components`. Cóipeáil an fillteán `mipower` óna lár.
4.  Greamaigh an fillteán `mipower` cóipeáilte isteach san fhillteán `custom_components` i d'eolaire cumraíochta Home Assistant. Mura bhfuil an fillteán `custom_components` ann, ní mór duit é a chruthú.
    - Ba chóir go mbeadh an cosán deiridh cosúil le: `.../config/custom_components/mipower/`
5.  Atosaigh Home Assistant.

## Cumraíocht

Tar éis atosú, is féidir leat an lasc MiPower a chur leis agus a chumrú.

1.  Téigh go **Settings > Devices & Services** (Socruithe > Gléasanna & Seirbhísí).
2.  Cliceáil an cnaipe **"+ Add Integration"** ("+ Cuir Comhtháthú leis") sa chúinne íochtarach ar dheis.
3.  Cuardaigh **"MiPower"** agus cliceáil air.

### Socrú Éasca (Molta)

Is é seo an bealach is simplí chun an comhtháthú a chumrú.

1.  Nuair a spreagtar tú, roghnaigh **"Easy Setup"** ("Socrú Éasca").
2.  Déanfaidh an comhtháthú imreoirí meán cumasaithe Bluetooth ar do chóras a fhionnadh go huathoibríoch.
3.  Roghnaigh do ghléas sprice (m.sh., "Xiaomi Mi Box 4") ón liosta anuas.
4.  Cliceáil **"Submit"** ("Cuir isteach").

Sin é! Cruthóidh an comhtháthú lasc atá nasctha le d'imreoir meán.

### Socrú Casta

Úsáid an modh seo mura bhfaigheann an Socrú Éasca do ghléas nó má theastaíonn uait socruithe uainiúcháin casta a chumrú ón tús.

1.  **Céim 1: Roghnú Gléas**
    - Roghnaigh **"Advanced Setup"** ("Socrú Casta").
    - Roghnaigh d'imreoir meán sprice ón liosta de *gach* imreoir meán i do Home Assistant.
2.  **Céim 2: Seoladh MAC**
    - Déanfaidh an comhtháthú iarracht Seoladh MAC Bluetooth an ghléis roghnaithe a aimsiú. 
    - Má aimsítear é, déanfar réamhlíonadh air. Fíoraigh go bhfuil sé ceart.
    - Mura n-aimsítear é, ní mór duit Seoladh MAC Bluetooth do ghléis a chur isteach de láimh.
3.  **Céim 3: Socruithe Uainiúcháin**
    - Is féidir leat teorainneacha ama agus moilleanna éagsúla a chumrú le haghaidh na n-orduithe Bluetooth. I gcás fhormhór na n-úsáideoirí, is leor na luachanna réamhshocraithe.
4.  Cliceáil **"Submit"** ("Cuir isteach") chun an socrú a chríochnú.

## Roghanna

Tar éis duit do lasc MiPower a chumrú, is féidir leat na socruithe uainiúcháin a choigeartú am ar bith.

1.  Téigh go **Settings > Devices & Services** (Socruithe > Gléasanna & Seirbhísí).
2.  Faigh an comhtháthú MiPower agus cliceáil **"Configure"** ("Cumraigh").
3.  Coigeartaigh na sleamhnáin le haghaidh *debounce*, teorainneacha ama, agus moilleanna de réir mar is gá.

## Míniú ar na Socruithe Uainiúcháin

Sa roghchlár cumraíochta nó roghanna, is féidir leat uainiú na n-orduithe Bluetooth a mhionchoigeartú. I gcás fhormhór na n-úsáideoirí, oibríonn na luachanna réamhshocraithe go maith.

- **Turn-On Debounce (Debounce Cas-Air):** An t-íos-am (i soicindí) nach mór a rith sular féidir an t-ordú 'cas ar' a fhorghníomhú arís. Cuireann sé seo cosc ar ró-ualú a dhéanamh ar an bhfeiste le comharthaí dúiseachta má dhéantar an lasc a scoránaigh go tapa.

- **Turn-Off Debounce (Debounce Cas-As):** An t-íos-am (i soicindí) nach mór a rith sular féidir an t-ordú 'cas as' a fhorghníomhú arís. 

- **Delay Between Commands (Moill Idir Orduithe):** Moill an-ghearr (i soicindí) idir orduithe comhleanúnacha a sheoladh chuig an bhfóntas `bluetoothctl`. Ar roinnt córas, d'fhéadfadh feabhas a chur ar iontaofacht má chuirtear sos beag leis.

- **Process Spawn Timeout (Teorainn Ama ar Fhágáil Próisis):** An t-uasmhéid ama (i soicindí) le fanacht le tús a chur le próiseas `bluetoothctl`. Mura n-éiríonn leis tosú laistigh den am seo, theipfidh ar an iarracht casadh air.

- **Pairing Timeout (Teorainn Ama ar Phéireáil):** Sa loighic simplíoch cas-air, is é seo an méid ama le fanacht tar éis an t-ordú `pair` a sheoladh sula nglactar leis go bhfuil sé rathúil. Tugann sé am don ghléas an comhartha dúiseachta a phróiseáil.

- **Bluetooth Scan Duration (Fad Scanadh Bluetooth):** An fad (i soicindí) a ndéanfaidh an comhtháthú scanadh le haghaidh gléasanna Bluetooth sula ndéanfaidh sé iarracht an t-ordú péireála a sheoladh. Is féidir le scanadh níos faide cabhrú le feistí a aimsiú atá mall chun a láithreacht a fhógairt.

## Léigh i do theanga féin

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