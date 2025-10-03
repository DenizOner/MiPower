# MiPower — Niestandardowa integracja Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** to integracja Home Assistant, która umożliwia kontrolowanie stanu zasilania odtwarzaczy multimedialnych, które nie obsługują tradycyjnej funkcji Wake-on-LAN (WOL), ale mogą zostać "wybudzone" przez żądanie parowania Bluetooth. Została zaprojektowana specjalnie dla urządzeń takich jak Xiaomi Mi Box, ale może działać z innymi podobnymi urządzeniami Android TV Box.

Ta integracja tworzy encję `switch` (przełącznik) w Home Assistant. 
- **Włączenie** przełącznika wysyła serię poleceń Bluetooth za pośrednictwem `bluetoothctl`, aby wybudzić urządzenie.
- **Wyłączenie** przełącznika wywołuje usługę `media_player.turn_off` dla powiązanego urządzenia.
- Stan przełącznika jest automatycznie synchronizowany ze stanem powiązanej encji odtwarzacza multimedialnego.

## 🤝 Wesprzyj Nas

Projekt MiPower jest rozwijany z wizją dodawania wartości do społeczności open source. Twoje wsparcie ma kluczowe znaczenie dla utrzymania ciągłości i tempa rozwoju tego projektu.

Jeśli doceniasz moją pracę, możesz mnie wesprzeć za pośrednictwem GitHub Sponsors lub następujących platform. Dziękuję z góry!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternatywnie, możesz zobaczyć wszystkie opcje finansowania, klikając **przycisk Sponsora (❤️)** w prawym górnym rogu repozytorium.

## Wymagania wstępne

- **Home Assistant OS / Supervised / Container:** Ta integracja wymaga instalacji Home Assistant opartej na systemie Linux, gdzie narzędzie wiersza poleceń `bluetoothctl` jest dostępne i osiągalne. **NIE** będzie działać w instalacji Home Assistant Core na systemie Windows.

## Instalacja za pomocą HACS (Zalecane)

Ta integracja jest dostępna jako niestandardowe repozytorium w HACS.

1.  Przejdź do swojego pulpitu HACS.
2.  Kliknij **Integrations** (Integracje).
3.  Kliknij menu z trzema kropkami w prawym górnym rogu i wybierz **"Custom repositories"** ("Niestandardowe repozytoria").
4.  W oknie dialogowym wprowadź następujące informacje:
    - **Repository (Repozytorium):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategoria):** `Integration` (Integracja)
5.  Kliknij **"Add"** ("Dodaj").
6.  Integracja "MiPower" pojawi się teraz na Twojej liście HACS. Kliknij na nią.
7.  Kliknij przycisk **"Download"** ("Pobierz"), a następnie ponownie **"Download"** ("Pobierz") w następnym oknie.
8.  Po zakończeniu pobierania, **musisz ponownie uruchomić Home Assistant**, aby integracja została załadowana.

## Instalacja ręczna

Chociaż HACS jest zalecaną metodą, możesz również zainstalować integrację ręcznie.

1.  Przejdź do [strony wydań](https://github.com/DenizOner/MiPower/releases) repozytorium i pobierz plik `mipower.zip` z najnowszej wersji.
2.  Rozpakuj pobrany plik.
3.  Wewnątrz rozpakowanego folderu znajdziesz katalog `custom_components`. Skopiuj z niego folder `mipower`.
4.  Wklej skopiowany folder `mipower` do folderu `custom_components` w katalogu konfiguracyjnym Home Assistant. Jeśli folder `custom_components` nie istnieje, musisz go utworzyć.
    - Ostateczna ścieżka powinna wyglądać następująco: `.../config/custom_components/mipower/`
5.  Uruchom ponownie Home Assistant.

## Konfiguracja

Po ponownym uruchomieniu możesz dodać i skonfigurować przełącznik MiPower.

1.  Przejdź do **Settings > Devices & Services** (Ustawienia > Urządzenia i Usługi).
2.  Kliknij przycisk **"+ Add Integration"** ("+ Dodaj Integrację") w prawym dolnym rogu.
3.  Wyszukaj **"MiPower"** i kliknij na nią.

### Łatwa konfiguracja (Zalecane)

To najprostszy sposób konfiguracji integracji.

1.  Po wyświetleniu monitu wybierz **"Easy Setup"** ("Łatwa Konfiguracja").
2.  Integracja automatycznie wykryje odtwarzacze multimedialne obsługujące Bluetooth w Twoim systemie.
3.  Wybierz swoje urządzenie docelowe (np. "Xiaomi Mi Box 4") z listy rozwijanej.
4.  Kliknij **"Submit"** ("Prześlij").

To wszystko! Integracja utworzy przełącznik powiązany z Twoim odtwarzaczem multimedialnym.

### Zaawansowana konfiguracja

Użyj tej metody, jeśli Łatwa konfiguracja nie znajdzie Twojego urządzenia lub jeśli musisz od razu skonfigurować zaawansowane ustawienia czasowe.

1.  **Krok 1: Wybór urządzenia**
    - Wybierz **"Advanced Setup"** ("Zaawansowana Konfiguracja").
    - Wybierz swój docelowy odtwarzacz multimedialny z listy *wszystkich* odtwarzaczy multimedialnych w Home Assistant.
2.  **Krok 2: Adres MAC**
    - Integracja spróbuje znaleźć adres MAC Bluetooth wybranego urządzenia. 
    - Jeśli zostanie znaleziony, zostanie wstępnie wypełniony. Sprawdź, czy jest poprawny.
    - Jeśli nie zostanie znaleziony, musisz ręcznie wprowadzić adres MAC Bluetooth swojego urządzenia.
3.  **Krok 3: Ustawienia czasowe**
    - Możesz skonfigurować różne limity czasu (timeouts) i opóźnienia dla poleceń Bluetooth. Dla większości użytkowników wartości domyślne są wystarczające.
4.  Kliknij **"Submit"** ("Prześlij"), aby zakończyć konfigurację.

## Opcje

Po skonfigurowaniu przełącznika MiPower możesz w dowolnym momencie dostosować ustawienia czasowe.

1.  Przejdź do **Settings > Devices & Services** (Ustawienia > Urządzenia i Usługi).
2.  Znajdź integrację MiPower i kliknij **"Configure"** ("Konfiguruj").
3.  Dostosuj suwaki dla *debounce*, limitów czasu i opóźnień w razie potrzeby.

## Wyjaśnienie Ustawień Czasowych

W menu konfiguracji lub opcji możesz dokładnie dostroić czas poleceń Bluetooth. Dla większości użytkowników wartości domyślne działają dobrze.

- **Turn-On Debounce (Tłumienie drgań przy włączaniu):** Minimalny czas (w sekundach), który musi upłynąć, zanim polecenie 'włącz' będzie mogło zostać ponownie wykonane. Zapobiega to spamowaniu urządzenia sygnałami wybudzania, jeśli przełącznik jest szybko przełączany.

- **Turn-Off Debounce (Tłumienie drgań przy wyłączaniu):** Minimalny czas (w sekundach), który musi upłynąć, zanim polecenie 'wyłącz' będzie mogło zostać ponownie wykonane. 

- **Delay Between Commands (Opóźnienie między poleceniami):** Bardzo krótkie opóźnienie (w sekundach) między wysyłaniem kolejnych poleceń do narzędzia `bluetoothctl`. W niektórych systemach dodanie niewielkiej pauzy może poprawić niezawodność.

- **Process Spawn Timeout (Limit czasu uruchomienia procesu):** Maksymalny czas (w sekundach) oczekiwania na uruchomienie procesu `bluetoothctl`. Jeśli nie uda się go uruchomić w tym czasie, próba włączenia zakończy się niepowodzeniem.

- **Pairing Timeout (Limit czasu parowania):** W uproszczonej logice włączania, jest to czas oczekiwania po wysłaniu polecenia `pair` przed założeniem sukcesu. Daje to urządzeniu czas na przetworzenie sygnału wybudzania.

- **Bluetooth Scan Duration (Czas trwania skanowania Bluetooth):** Czas (w sekundach), przez jaki integracja będzie skanować w poszukiwaniu urządzeń Bluetooth, zanim spróbuje wysłać polecenie parowania. Dłuższe skanowanie może pomóc w znalezieniu urządzeń, które wolno ogłaszają swoją obecność.

## Czytaj w swoim języku

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