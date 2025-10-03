# MiPower — Спеціальна інтеграція Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** — це інтеграція Home Assistant, яка дозволяє керувати станом живлення медіаплеєрів, що не підтримують традиційний Wake-on-LAN (WOL), але можуть бути "розбуджені" запитом на створення пари Bluetooth. Вона була спеціально розроблена для таких пристроїв, як Xiaomi Mi Box, але може працювати і з іншими подібними приставками Android TV.

Ця інтеграція створює сутність `switch` (перемикач) у Home Assistant. 
- **Увімкнення** перемикача надсилає серію команд Bluetooth через `bluetoothctl`, щоб розбудити пристрій.
- **Вимкнення** перемикача викликає службу `media_player.turn_off` для пов'язаного пристрою.
- Стан перемикача автоматично синхронізується зі станом пов'язаної сутності медіаплеєра.

## 🤝 Підтримайте нас

Проект MiPower розробляється з метою підвищення цінності спільноти відкритого вихідного коду. Ваша підтримка є життєво важливою для підтримки безперервності та швидкості розвитку цього проекту.

Якщо ви цінуєте мою роботу, ви можете підтримати мене через GitHub Sponsors або наступні платформи. Дякую заздалегідь!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Як альтернативу, ви можете побачити всі варіанти фінансування, натиснувши на **кнопку Спонсора (❤️)** у верхньому правому куті репозиторію.

## Передумови

- **Home Assistant OS / Supervised / Container:** Ця інтеграція вимагає встановлення Home Assistant на базі Linux, де доступний і доступний інструмент командного рядка `bluetoothctl`. Вона **НЕ** працюватиме на установці Home Assistant Core на Windows.

## Встановлення через HACS (Рекомендовано)

Ця інтеграція доступна як спеціальний репозиторій у HACS.

1.  Перейдіть на інформаційну панель HACS.
2.  Натисніть **Integrations** (Інтеграції).
3.  Натисніть меню з трьома крапками у верхньому правому куті та виберіть **"Custom repositories"** ("Спеціальні репозиторії").
4.  У діалоговому вікні введіть таку інформацію:
    - **Repository (Репозиторій):** `https://github.com/DenizOner/MiPower`
    - **Category (Категорія):** `Integration` (Інтеграція)
5.  Натисніть **"Add"** ("Додати").
6.  Інтеграція "MiPower" тепер з'явиться у вашому списку HACS. Натисніть на неї.
7.  Натисніть кнопку **"Download"** ("Завантажити"), а потім знову **"Download"** ("Завантажити") у наступному вікні.
8.  Після завершення завантаження **ви ПОВИННІ перезапустити Home Assistant**, щоб інтеграція завантажилася.

## Ручне встановлення

Хоча HACS є рекомендованим методом, ви також можете встановити інтеграцію вручну.

1.  Перейдіть на [сторінку релізів](https://github.com/DenizOner/MiPower/releases) репозиторію та завантажте файл `mipower.zip` з останнього релізу.
2.  Розпакуйте завантажений файл.
3.  Усередині розпакованої папки ви знайдете каталог `custom_components`. Скопіюйте з нього папку `mipower`.
4.  Вставте скопійовану папку `mipower` у папку `custom_components` у каталозі конфігурації Home Assistant. Якщо папка `custom_components` не існує, вам потрібно її створити.
    - Кінцевий шлях має виглядати так: `.../config/custom_components/mipower/`
5.  Перезапустіть Home Assistant.

## Конфігурація

Після перезапуску ви можете додати та налаштувати перемикач MiPower.

1.  Перейдіть до **Settings > Devices & Services** (Налаштування > Пристрої та Служби).
2.  Натисніть кнопку **"+ Add Integration"** ("+ Додати Інтеграцію") у нижньому правому куті.
3.  Знайдіть **"MiPower"** і натисніть на неї.

### Просте налаштування (Рекомендовано)

Це найпростіший спосіб налаштування інтеграції.

1.  При запиті виберіть **"Easy Setup"** ("Просте Налаштування").
2.  Інтеграція автоматично виявить медіаплеєри з підтримкою Bluetooth у вашій системі.
3.  Виберіть цільовий пристрій (наприклад, "Xiaomi Mi Box 4") зі спадного списку.
4.  Натисніть **"Submit"** ("Надіслати").

Ось і все! Інтеграція створить перемикач, пов'язаний з вашим медіаплеєром.

### Розширене налаштування

Використовуйте цей метод, якщо Просте налаштування не знаходить ваш пристрій або якщо вам потрібно налаштувати розширені параметри часу з самого початку.

1.  **Крок 1: Вибір пристрою**
    - Виберіть **"Advanced Setup"** ("Розширене Налаштування").
    - Виберіть цільовий медіаплеєр зі списку *всіх* медіаплеєрів у вашому Home Assistant.
2.  **Крок 2: MAC-адреса**
    - Інтеграція спробує знайти Bluetooth MAC-адресу вибраного пристрою. 
    - Якщо її знайдено, вона буде попередньо заповнена. Перевірте, чи вона правильна.
    - Якщо її не знайдено, ви повинні ввести Bluetooth MAC-адресу вашого пристрою вручну.
3.  **Крок 3: Налаштування часу**
    - Ви можете налаштувати різні тайм-аути та затримки для команд Bluetooth. Для більшості користувачів значень за замовчуванням достатньо.
4.  Натисніть **"Submit"** ("Надіслати"), щоб завершити налаштування.

## Опції

Після налаштування перемикача MiPower ви можете в будь-який час налаштувати параметри часу.

1.  Перейдіть до **Settings > Devices & Services** (Налаштування > Пристрої та Служби).
2.  Знайдіть інтеграцію MiPower і натисніть **"Configure"** ("Налаштувати").
3.  Відрегулюйте повзунки для *debounce*, тайм-аутів і затримок за потреби.

## Пояснення налаштувань часу

У меню конфігурації або опцій ви можете точно налаштувати час команд Bluetooth. Для більшості користувачів значення за замовчуванням працюють добре.

- **Turn-On Debounce (Захист від коливань при увімкненні):** Мінімальний час (у секундах), який має пройти до того, як команда «увімкнути» може бути виконана знову. Це запобігає надсиланню спаму із сигналами пробудження пристрою, якщо перемикач швидко перемикається.

- **Turn-Off Debounce (Захист від коливань при вимкненні):** Мінімальний час (у секундах), який має пройти до того, як команда «вимкнути» може бути виконана знову. 

- **Delay Between Commands (Затримка між командами):** Дуже коротка затримка (у секундах) між надсиланням послідовних команд утиліті `bluetoothctl`. У деяких системах додавання невеликої паузи може підвищити надійність.

- **Process Spawn Timeout (Тайм-аут запуску процесу):** Максимальний час (у секундах) очікування запуску процесу `bluetoothctl`. Якщо він не запуститься протягом цього часу, спроба увімкнення завершиться невдачею.

- **Pairing Timeout (Тайм-аут створення пари):** У спрощеній логіці увімкнення це час, який потрібно почекати після надсилання команди `pair`, перш ніж вважати її успішною. Це дає пристрою час на обробку сигналу пробудження.

- **Bluetooth Scan Duration (Тривалість сканування Bluetooth):** Тривалість (у секундах), протягом якої інтеграція скануватиме пристрої Bluetooth, перш ніж намагатися надіслати команду створення пари. Довше сканування може допомогти знайти пристрої, які повільно оголошують про свою присутність.

## Читайте своєю мовою

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