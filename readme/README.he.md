# MiPower — אינטגרציה מותאמת אישית עבור Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** היא אינטגרציה של Home Assistant המאפשרת לך לשלוט במצב ההפעלה של נגני מדיה שאינם תומכים ב-Wake-on-LAN (WOL) המסורתי, אך ניתן "להעיר" אותם על ידי בקשת צימוד בלוטות'. היא תוכננה במיוחד עבור מכשירים כמו ה-Xiaomi Mi Box, אך עשויה לעבוד עם קופסאות Android TV דומות אחרות.

אינטגרציה זו יוצרת ישות `switch` (מתג) ב-Home Assistant. 
- **הדלקת** המתג שולחת סדרה של פקודות בלוטות' דרך `bluetoothctl` כדי להעיר את המכשיר.
- **כיבוי** המתג קורא לשירות `media_player.turn_off` עבור המכשיר המקושר.
- מצב המתג מסונכרן אוטומטית עם מצב ישות נגן המדיה המקושרת.

## 🤝 תמכו בנו

פרויקט MiPower מפותח עם חזון של הוספת ערך לקהילת הקוד הפתוח. תמיכתכם חיונית לשמירה על המשכיות וקצב הפיתוח של פרויקט זה.

אם אתם מעריכים את עבודתי, אתם יכולים לתמוך בי באמצעות GitHub Sponsors או הפלטפורמות הבאות. תודה מראש!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

לחלופין, תוכלו לראות את כל אפשרויות המימון על ידי לחיצה על **כפתור הספונסר (❤️)** בפינה הימנית העליונה של המאגר.

## דרישות קדם

- **Home Assistant OS / Supervised / Container:** אינטגרציה זו דורשת התקנת Home Assistant מבוססת לינוקס שבה כלי שורת הפקודה `bluetoothctl` זמין ונגיש. היא **לא** תעבוד על התקנת Home Assistant Core ב-Windows.

## התקנה באמצעות HACS (מומלץ)

אינטגרציה זו זמינה כמאגר מותאם אישית ב-HACS.

1.  נווט אל לוח המחוונים של HACS שלך.
2.  לחץ על **Integrations** (אינטגרציות).
3.  לחץ על תפריט שלוש הנקודות בפינה הימנית העליונה ובחר **"Custom repositories"** ("מאגרים מותאמים אישית").
4.  בתיבת הדו-שיח, הזן את המידע הבא:
    - **Repository (מאגר):** `https://github.com/DenizOner/MiPower`
    - **Category (קטגוריה):** `Integration` (אינטגרציה)
5.  לחץ על **"Add"** ("הוסף").
6.  האינטגרציה "MiPower" תופיע כעת ברשימת HACS שלך. לחץ עליה.
7.  לחץ על כפתור **"Download"** ("הורדה") ולאחר מכן לחץ שוב על **"Download"** ("הורדה") בחלון הבא.
8.  לאחר השלמת ההורדה, **עליך להפעיל מחדש את Home Assistant** כדי שהאינטגרציה תיטען.

## התקנה ידנית

למרות ש-HACS היא השיטה המומלצת, באפשרותך גם להתקין את האינטגרציה באופן ידני.

1.  עבור אל [דף המהדורות](https://github.com/DenizOner/MiPower/releases) של המאגר והורד את קובץ `mipower.zip` מהמהדורה האחרונה.
2.  חלץ את הקובץ שהורדת.
3.  בתוך התיקייה שחולצה, תמצא ספריית `custom_components`. העתק את התיקייה `mipower` מתוכה.
4.  הדבק את התיקייה `mipower` שהועתקה לתוך תיקיית `custom_components` בספריית התצורה של Home Assistant שלך. אם תיקיית `custom_components` אינה קיימת, עליך ליצור אותה.
    - הנתיב הסופי אמור להיראות כך: `.../config/custom_components/mipower/`
5.  הפעל מחדש את Home Assistant.

## תצורה

לאחר ההפעלה מחדש, תוכל להוסיף ולהגדיר את מתג MiPower.

1.  עבור אל **Settings > Devices & Services** (הגדרות > מכשירים ושירותים).
2.  לחץ על כפתור **"+ Add Integration"** ("+ הוסף אינטגרציה") בפינה הימנית התחתונה.
3.  חפש את **"MiPower"** ולחץ עליו.

### הגדרה קלה (מומלץ)

זוהי הדרך הפשוטה ביותר להגדיר את האינטגרציה.

1.  כאשר תתבקש, בחר **"Easy Setup"** ("הגדרה קלה").
2.  האינטגרציה תגלה אוטומטית נגני מדיה עם תמיכת בלוטות' במערכת שלך.
3.  בחר את מכשיר היעד שלך (לדוגמה, "Xiaomi Mi Box 4") מהרשימה הנפתחת.
4.  לחץ על **"Submit"** ("שלח").

זה הכל! האינטגרציה תיצור מתג המקושר לנגן המדיה שלך.

### הגדרה מתקדמת

השתמש בשיטה זו אם ההגדרה הקלה לא מוצאת את המכשיר שלך או אם אתה צריך להגדיר הגדרות תזמון מתקדמות מההתחלה.

1.  **שלב 1: בחירת מכשיר**
    - בחר **"Advanced Setup"** ("הגדרה מתקדמת").
    - בחר את נגן המדיה המיועד שלך מתוך רשימת *כל* נגני המדיה ב-Home Assistant שלך.
2.  **שלב 2: כתובת MAC**
    - האינטגרציה תנסה למצוא את כתובת ה-Bluetooth MAC של המכשיר הנבחר. 
    - אם נמצא, הוא ימולא מראש. ודא שהוא נכון.
    - אם לא נמצא, עליך להזין ידנית את כתובת ה-Bluetooth MAC של המכשיר שלך.
3.  **שלב 3: הגדרות תזמון**
    - באפשרותך להגדיר פסק זמן ועיכובים שונים עבור פקודות הבלוטות'. עבור רוב המשתמשים, ערכי ברירת המחדל מספיקים.
4.  לחץ על **"Submit"** ("שלח") כדי להשלים את ההגדרה.

## אפשרויות

לאחר שהגדרת את מתג MiPower שלך, תוכל לכוונן את הגדרות התזמון בכל עת.

1.  עבור אל **Settings > Devices & Services** (הגדרות > מכשירים ושירותים).
2.  מצא את אינטגרציית MiPower ולחץ על **"Configure"** ("קונפג").
3.  כוונן את המחוונים עבור *debounce*, פסק זמן ועיכובים לפי הצורך.

## הסבר על הגדרות תזמון

בתפריט התצורה או האפשרויות, תוכל לכוונן את התזמון של פקודות הבלוטות'. עבור רוב המשתמשים, ערכי ברירת המחדל עובדים היטב.

- **Turn-On Debounce (השהיית הדלקה):** הזמן המינימלי (בשניות) שחייב לעבור לפני שניתן יהיה לבצע שוב את הפקודה 'הדלק'. זה מונע הצפה של המכשיר באותות השכמה אם המתג מופעל במהירות.

- **Turn-Off Debounce (השהיית כיבוי):** הזמן המינימלי (בשניות) שחייב לעבור לפני שניתן יהיה לבצע שוב את הפקודה 'כבה'. 

- **Delay Between Commands (עיכוב בין פקודות):** עיכוב קצר מאוד (בשניות) בין שליחת פקודות רצופות לכלי `bluetoothctl`. במערכות מסוימות, הוספת הפסקה קטנה יכולה לשפר את האמינות.

- **Process Spawn Timeout (פסק זמן להפעלת תהליך):** הזמן המקסימלי (בשניות) להמתין להתחלת תהליך `bluetoothctl`. אם הוא לא מצליח להתחיל בתוך זמן זה, ניסיון ההדלקה ייכשל.

- **Pairing Timeout (פסק זמן צימוד):** בלוגיקת ההדלקה הפשוטה, זהו משך הזמן שיש להמתין לאחר שליחת הפקודה `pair` לפני הנחת הצלחה. זה נותן למכשיר זמן לעבד את אות ההשכמה.

- **Bluetooth Scan Duration (משך סריקת בלוטות'):** משך הזמן (בשניות) שהאינטגרציה תסרוק אחר מכשירי בלוטות' לפני שתנסה לשלוח את פקודת הצימוד. סריקה ארוכה יותר יכולה לעזור למצוא מכשירים שאיטיים בפרסום נוכחותם.

## קראו בשפה שלכם

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