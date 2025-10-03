# MiPower — Benutzerdefinierte Home Assistant Integration

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** ist eine Home Assistant Integration, die es Ihnen ermöglicht, den Energiestatus von Mediaplayern zu steuern, welche das traditionelle Wake-on-LAN (WOL) nicht unterstützen, aber durch eine Bluetooth-Kopplungsanfrage "aufgeweckt" werden können. Sie wurde speziell für Geräte wie die Xiaomi Mi Box entwickelt, kann aber auch mit anderen ähnlichen Android TV-Boxen funktionieren.

Diese Integration erstellt eine `switch`-Entität (Schalter) in Home Assistant. 
- **Einschalten** des Schalters sendet eine Reihe von Bluetooth-Befehlen über `bluetoothctl`, um das Gerät aufzuwecken.
- **Ausschalten** des Schalters ruft den Dienst `media_player.turn_off` für das verknüpfte Gerät auf.
- Der Zustand des Schalters wird automatisch mit dem Zustand der verknüpften Mediaplayer-Entität synchronisiert.

## 🤝 Unterstützen Sie uns

Das MiPower-Projekt wird mit der Vision entwickelt, der Open-Source-Community einen Mehrwert zu bieten. Ihre Unterstützung ist entscheidend, um die Kontinuität und Entwicklungsgeschwindigkeit dieses Projekts aufrechtzuerhalten.

Wenn Sie meine Arbeit schätzen, können Sie mich über GitHub Sponsors oder die folgenden Plattformen unterstützen. Vielen Dank im Voraus!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternativ können Sie alle Finanzierungsmöglichkeiten sehen, indem Sie auf den **Sponsor-Button (❤️)** in der oberen rechten Ecke des Repositorys klicken.

## Voraussetzungen

- **Home Assistant OS / Supervised / Container:** Diese Integration erfordert eine Linux-basierte Home Assistant Installation, bei der das Kommandozeilen-Tool `bluetoothctl` verfügbar und zugänglich ist. Sie wird **nicht** auf einer Home Assistant Core Installation unter Windows funktionieren.

## Installation über HACS (Empfohlen)

Diese Integration ist als benutzerdefiniertes Repository in HACS verfügbar.

1.  Navigieren Sie zu Ihrem HACS Dashboard.
2.  Klicken Sie auf **Integrations** (Integrationen).
3.  Klicken Sie auf das Drei-Punkte-Menü in der oberen rechten Ecke und wählen Sie **"Custom repositories"** ("Benutzerdefinierte Repositories").
4.  Geben Sie im Dialogfeld die folgenden Informationen ein:
    - **Repository (Repository):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategorie):** `Integration` (Integration)
5.  Klicken Sie auf **"Add"** ("Hinzufügen").
6.  Die "MiPower"-Integration wird nun in Ihrer HACS-Liste angezeigt. Klicken Sie darauf.
7.  Klicken Sie auf die Schaltfläche **"Download"** ("Herunterladen") und dann erneut auf **"Download"** ("Herunterladen") im nächsten Fenster.
8.  Nach Abschluss des Downloads **müssen Sie Home Assistant neu starten**, damit die Integration geladen werden kann.

## Manuelle Installation

Obwohl HACS die empfohlene Methode ist, können Sie die Integration auch manuell installieren.

1.  Gehen Sie zur [Releases-Seite](https://github.com/DenizOner/MiPower/releases) des Repositorys und laden Sie die Datei `mipower.zip` der neuesten Version herunter.
2.  Entpacken Sie die heruntergeladene Datei.
3.  Im entpackten Ordner finden Sie ein `custom_components`-Verzeichnis. Kopieren Sie den Ordner `mipower` daraus.
4.  Fügen Sie den kopierten `mipower`-Ordner in den `custom_components`-Ordner in Ihrem Home Assistant Konfigurationsverzeichnis ein. Wenn der Ordner `custom_components` nicht existiert, müssen Sie ihn erstellen.
    - Der endgültige Pfad sollte wie folgt aussehen: `.../config/custom_components/mipower/`
5.  Starten Sie Home Assistant neu.

## Konfiguration

Nach dem Neustart können Sie den MiPower-Schalter hinzufügen und konfigurieren.

1.  Gehen Sie zu **Settings > Devices & Services** (Einstellungen > Geräte & Dienste).
2.  Klicken Sie auf die Schaltfläche **"+ Add Integration"** ("+ Integration hinzufügen") in der unteren rechten Ecke.
3.  Suchen Sie nach **"MiPower"** und klicken Sie darauf.

### Einfache Einrichtung (Empfohlen)

Dies ist der einfachste Weg, die Integration zu konfigurieren.

1.  Wählen Sie bei Aufforderung **"Easy Setup"** ("Einfache Einrichtung").
2.  Die Integration erkennt automatisch Bluetooth-fähige Mediaplayer in Ihrem System.
3.  Wählen Sie Ihr Zielgerät (z.B. "Xiaomi Mi Box 4") aus der Dropdown-Liste.
4.  Klicken Sie auf **"Submit"** ("Senden").

Das war's! Die Integration erstellt einen mit Ihrem Mediaplayer verknüpften Schalter.

### Erweiterte Einrichtung

Verwenden Sie diese Methode, wenn die Einfache Einrichtung Ihr Gerät nicht findet oder wenn Sie erweiterte Timing-Einstellungen von Anfang an konfigurieren müssen.

1.  **Schritt 1: Geräteauswahl**
    - Wählen Sie **"Advanced Setup"** ("Erweiterte Einrichtung").
    - Wählen Sie Ihren Ziel-Mediaplayer aus der Liste *aller* Mediaplayer in Ihrem Home Assistant.
2.  **Schritt 2: MAC-Adresse**
    - Die Integration versucht, die Bluetooth MAC-Adresse des ausgewählten Geräts zu finden. 
    - Wenn sie gefunden wird, wird sie vorab ausgefüllt. Überprüfen Sie, ob sie korrekt ist.
    - Wenn sie nicht gefunden wird, müssen Sie die Bluetooth MAC-Adresse Ihres Geräts manuell eingeben.
3.  **Schritt 3: Timing-Einstellungen**
    - Sie können verschiedene Timeouts und Verzögerungen für die Bluetooth-Befehle konfigurieren. Für die meisten Benutzer sind die Standardwerte ausreichend.
4.  Klicken Sie auf **"Submit"** ("Senden"), um die Einrichtung abzuschließen.

## Optionen

Nachdem Sie Ihren MiPower-Schalter konfiguriert haben, können Sie die Timing-Einstellungen jederzeit anpassen.

1.  Gehen Sie zu **Settings > Devices & Services** (Einstellungen > Geräte & Dienste).
2.  Suchen Sie die MiPower-Integration und klicken Sie auf **"Configure"** ("Konfigurieren").
3.  Passen Sie die Schieberegler für "debounce", Timeouts und Verzögerungen nach Bedarf an.

## Erklärung der Timing-Einstellungen

Im Konfigurations- oder Optionsmenü können Sie das Timing der Bluetooth-Befehle feinabstimmen. Für die meisten Benutzer funktionieren die Standardwerte gut.

- **Turn-On Debounce (Einschalt-Entprellung):** Die minimale Zeit (in Sekunden), die vergehen muss, bevor der 'Einschalt'-Befehl erneut ausgeführt werden kann. Dies verhindert, dass das Gerät mit Wecksignalen zugespammt wird, wenn der Schalter schnell umgeschaltet wird.

- **Turn-Off Debounce (Ausschalt-Entprellung):** Die minimale Zeit (in Sekunden), die vergehen muss, bevor der 'Ausschalt'-Befehl erneut ausgeführt werden kann. 

- **Delay Between Commands (Verzögerung zwischen Befehlen):** Eine sehr kurze Verzögerung (in Sekunden) zwischen dem Senden aufeinanderfolgender Befehle an das `bluetoothctl`-Dienstprogramm. Auf einigen Systemen kann das Hinzufügen einer kleinen Pause die Zuverlässigkeit verbessern.

- **Process Spawn Timeout (Prozessstart-Timeout):** Die maximale Zeit (in Sekunden), die auf den Start des `bluetoothctl`-Prozesses gewartet wird. Wenn er innerhalb dieser Zeit nicht startet, schlägt der Einschaltversuch fehl.

- **Pairing Timeout (Kopplungs-Timeout):** In der vereinfachten Einschalt-Logik ist dies die Zeitspanne, die nach dem Senden des `pair`-Befehls gewartet wird, bevor von Erfolg ausgegangen wird. Es gibt dem Gerät Zeit, das Wecksignal zu verarbeiten.

- **Bluetooth Scan Duration (Bluetooth-Scan-Dauer):** Die Dauer (in Sekunden), während der die Integration nach Bluetooth-Geräten sucht, bevor versucht wird, den Kopplungsbefehl zu senden. Ein längerer Scan kann helfen, Geräte zu finden, die ihre Präsenz nur langsam ankündigen.

## Lesen Sie in Ihrer Sprache

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