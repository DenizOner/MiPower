# MiPower — Пользовательская интеграция Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** — это интеграция Home Assistant, которая позволяет управлять состоянием питания медиаплееров, не поддерживающих традиционный Wake-on-LAN (WOL), но которые могут быть «разбужены» запросом на сопряжение Bluetooth. Он был специально разработан для таких устройств, как Xiaomi Mi Box, но может работать и с другими аналогичными приставками Android TV.

Эта интеграция создает сущность `switch` (переключатель) в Home Assistant. 
- **Включение** переключателя отправляет серию команд Bluetooth через `bluetoothctl`, чтобы разбудить устройство.
- **Выключение** переключателя вызывает службу `media_player.turn_off` для связанного устройства.
- Состояние переключателя автоматически синхронизируется с состоянием связанной сущности медиаплеера.

## 🤝 Поддержите нас

Проект MiPower разрабатывается с целью повышения ценности сообщества открытого исходного кода. Ваша поддержка жизненно важна для поддержания непрерывности и скорости развития этого проекта.

Если вы цените мой труд, вы можете поддержать меня через GitHub Sponsors или следующие платформы. Заранее спасибо!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

В качестве альтернативы вы можете увидеть все варианты финансирования, нажав на **кнопку Спонсора (❤️)** в правом верхнем углу репозитория.

## Предварительные условия

- **Home Assistant OS / Supervised / Container:** Для этой интеграции требуется установка Home Assistant на базе Linux, где доступен и доступен инструмент командной строки `bluetoothctl`. Он **не** будет работать на установке Home Assistant Core в Windows.

## Установка через HACS (Рекомендуется)

Эта интеграция доступна в виде пользовательского репозитория в HACS.

1.  Перейдите на панель управления HACS.
2.  Нажмите **Integrations** (Интеграции).
3.  Нажмите меню с тремя точками в правом верхнем углу и выберите **"Custom repositories"** ("Пользовательские репозитории").
4.  В диалоговом окне введите следующую информацию:
    - **Repository (Репозиторий):** `https://github.com/DenizOner/MiPower`
    - **Category (Категория):** `Integration` (Интеграция)
5.  Нажмите **"Add"** ("Добавить").
6.  Интеграция "MiPower" теперь появится в вашем списке HACS. Нажмите на нее.
7.  Нажмите кнопку **"Download"** ("Скачать"), а затем снова **"Download"** ("Скачать") в следующем окне.
8.  После завершения загрузки **вы ДОЛЖНЫ перезапустить Home Assistant**, чтобы интеграция была загружена.

## Ручная установка

Хотя HACS является рекомендуемым методом, вы также можете установить интеграцию вручную.

1.  Перейдите на [страницу релизов](https://github.com/DenizOner/MiPower/releases) репозитория и загрузите файл `mipower.zip` из последнего релиза.
2.  Распакуйте загруженный файл.
3.  Внутри распакованной папки вы найдете каталог `custom_components`. Скопируйте из него папку `mipower`.
4.  Вставьте скопированную папку `mipower` в папку `custom_components` в каталоге конфигурации Home Assistant. Если папка `custom_components` не существует, вам нужно ее создать.
    - Конечный путь должен выглядеть примерно так: `.../config/custom_components/mipower/`
5.  Перезапустите Home Assistant.

## Конфигурация

После перезапуска вы можете добавить и настроить переключатель MiPower.

1.  Перейдите в **Settings > Devices & Services** (Настройки > Устройства и Службы).
2.  Нажмите кнопку **"+ Add Integration"** ("+ Добавить Интеграцию") в правом нижнем углу.
3.  Найдите **"MiPower"** и нажмите на нее.

### Простая настройка (Рекомендуется)

Это самый простой способ настройки интеграции.

1.  При появлении запроса выберите **"Easy Setup"** ("Простая Настройка").
2.  Интеграция автоматически обнаружит медиаплееры с поддержкой Bluetooth в вашей системе.
3.  Выберите целевое устройство (например, "Xiaomi Mi Box 4") из раскрывающегося списка.
4.  Нажмите **"Submit"** ("Отправить").

Вот и все! Интеграция создаст переключатель, связанный с вашим медиаплеером.

### Расширенная настройка

Используйте этот метод, если Простая настройка не находит ваше устройство или если вам нужно настроить расширенные параметры времени с самого начала.

1.  **Шаг 1: Выбор устройства**
    - Выберите **"Advanced Setup"** ("Расширенная Настройка").
    - Выберите целевой медиаплеер из списка *всех* медиаплееров в вашем Home Assistant.
2.  **Шаг 2: MAC-адрес**
    - Интеграция попытается найти MAC-адрес Bluetooth выбранного устройства. 
    - Если он найден, он будет предварительно заполнен. Убедитесь, что он правильный.
    - Если он не найден, вы должны ввести MAC-адрес Bluetooth вашего устройства вручную.
3.  **Шаг 3: Настройки времени**
    - Вы можете настроить различные тайм-ауты и задержки для команд Bluetooth. Для большинства пользователей значений по умолчанию достаточно.
4.  Нажмите **"Submit"** ("Отправить"), чтобы завершить настройку.

## Опции

После настройки переключателя MiPower вы можете в любое время настроить параметры времени.

1.  Перейдите в **Settings > Devices & Services** (Настройки > Устройства и Службы).
2.  Найдите интеграцию MiPower и нажмите **"Configure"** ("Настроить").
3.  Отрегулируйте ползунки для *debounce*, тайм-аутов и задержек по мере необходимости.

## Объяснение настроек времени

В меню конфигурации или опций вы можете точно настроить время команд Bluetooth. Для большинства пользователей значения по умолчанию работают хорошо.

- **Turn-On Debounce (Защита от дребезга при включении):** Минимальное время (в секундах), которое должно пройти до того, как команда «включить» может быть выполнена снова. Это предотвращает отправку устройству спама с сигналами пробуждения, если переключатель быстро переключается.

- **Turn-Off Debounce (Защита от дребезга при выключении):** Минимальное время (в секундах), которое должно пройти до того, как команда «выключить» может быть выполнена снова. 

- **Delay Between Commands (Задержка между командами):** Очень короткая задержка (в секундах) между отправкой последовательных команд утилите `bluetoothctl`. В некоторых системах добавление небольшой паузы может повысить надежность.

- **Process Spawn Timeout (Тайм-аут запуска процесса):** Максимальное время (в секундах) ожидания запуска процесса `bluetoothctl`. Если он не запустится в течение этого времени, попытка включения завершится неудачей.

- **Pairing Timeout (Тайм-аут сопряжения):** В упрощенной логике включения это время, которое нужно подождать после отправки команды `pair`, прежде чем считать ее успешной. Это дает устройству время на обработку сигнала пробуждения.

- **Bluetooth Scan Duration (Продолжительность сканирования Bluetooth):** Продолжительность (в секундах), в течение которой интеграция будет сканировать устройства Bluetooth, прежде чем пытаться отправить команду сопряжения. Более длительное сканирование может помочь найти устройства, которые медленно объявляют о своем присутствии.

## Читайте на своем языке

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