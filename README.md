# MiPower — Home Assistant custom integration

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** is a Home Assistant integration that allows you to control the power state of media players that do not support traditional Wake-on-LAN (WOL) but can be "woken up" by a Bluetooth pairing request. It was specifically designed for devices like the Xiaomi Mi Box, but may work with other similar Android TV boxes.

This integration creates a `switch` entity in Home Assistant. 
- **Turning ON** the switch sends a series of Bluetooth commands via `bluetoothctl` to wake the device up.
- **Turning OFF** the switch calls the `media_player.turn_off` service for the linked device.
- The state of the switch is automatically synchronized with the state of the linked media player entity.

## 🤝 Support

The MiPower project is developed with the vision of adding value to the open source community. Your support is vital to maintaining the continuity and development speed of this project.

If you appreciate my effort, you can support me via GitHub Sponsors or the following platforms. Thank you in advance!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternatively, you can see all funding options by clicking the **Sponsor button (❤️)** in the top right corner of the repository.

## Prerequisites

- **Home Assistant OS / Supervised / Container:** This integration requires a Linux-based Home Assistant installation where the `bluetoothctl` command-line tool is available and accessible. It will **not** work on a Home Assistant Core installation on Windows.

## Installation via HACS (Recomended)

This integration is available as a custom repository in HACS.

1.  Navigate to your HACS dashboard.
2.  Click on **Integrations**.
3.  Click the three-dots menu in the top-right corner and select **"Custom repositories"**.
4.  In the dialog box, enter the following information:
    - **Repository:** `https://github.com/DenizOner/MiPower`
    - **Category:** `Integration`
5.  Click **"Add"**.
6.  The "MiPower" integration will now appear in your HACS list. Click on it.
7.  Click the **"Download"** button and then **"Download"** again in the next window.
8.  After the download is complete, you **must restart Home Assistant** for the integration to be loaded.

## Manual Installation

While HACS is the recommended method, you can also install the integration manually.

1.  Go to the [Releases page](https://github.com/DenizOner/MiPower/releases) of the repository and download the `mipower.zip` file from the latest release.
2.  Unzip the downloaded file.
3.  Inside the unzipped folder, you will find a `custom_components` directory. Copy the `mipower` folder from within it.
4.  Paste the copied `mipower` folder into the `custom_components` folder in your Home Assistant configuration directory. If the `custom_components` folder does not exist, you need to create it.
    - The final path should look like: `.../config/custom_components/mipower/`
5.  Restart Home Assistant.

## Configuration

After restarting, you can add and configure the MiPower switch.

1.  Go to **Settings > Devices & Services**.
2.  Click the **"+ Add Integration"** button in the bottom-right corner.
3.  Search for **"MiPower"** and click on it.

### Easy Setup (Recommended)

This is the simplest way to configure the integration.

1.  When prompted, choose **"Easy Setup"**.
2.  The integration will automatically discover Bluetooth-enabled media players on your system.
3.  Select your target device (e.g., "Xiaomi Mi Box 4") from the dropdown list.
4.  Click **"Submit"**.

That's it! The integration will create a switch linked to your media player.

### Advanced Setup

Use this method if the Easy Setup does not find your device or if you need to configure advanced timing settings from the start.

1.  **Step 1: Device Selection**
    - Choose **"Advanced Setup"**.
    - Select your target media player from the list of *all* media players in your Home Assistant.
2.  **Step 2: MAC Address**
    - The integration will try to find the Bluetooth MAC address of the selected device. 
    - If found, it will be pre-filled. Verify that it is correct.
    - If not found, you must enter the Bluetooth MAC address of your device manually.
3.  **Step 3: Timing Settings**
    - You can configure various timeouts and delays for the Bluetooth commands. For most users, the default values are sufficient.
4.  Click **"Submit"** to complete the setup.

## Options

After you have configured your MiPower switch, you can adjust the timing settings at any time.

1.  Go to **Settings > Devices & Services**.
2.  Find the MiPower integration and click **"Configure"**.
3.  Adjust the sliders for debounce, timeouts, and delays as needed.

## Timing Settings Explained

In the configuration or options menu, you can fine-tune the timing of the Bluetooth commands. For most users, the default values work well.

- **Turn-On Debounce:** The minimum time (in seconds) that must pass before the 'turn on' command can be executed again. This prevents spamming the device with wake-up signals if the switch is toggled rapidly.

- **Turn-Off Debounce:** The minimum time (in seconds) that must pass before the 'turn off' command can be executed again. 

- **Delay Between Commands:** A very short delay (in seconds) between sending consecutive commands to the `bluetoothctl` utility. On some systems, adding a small pause can improve reliability.

- **Process Spawn Timeout:** The maximum time (in seconds) to wait for the `bluetoothctl` process to start. If it fails to start within this time, the turn-on attempt will fail.

- **Pairing Timeout:** In the simplified turn-on logic, this is the amount of time to wait after sending the `pair` command before assuming success. It gives the device time to process the wake-up signal.

- **Bluetooth Scan Duration:** The duration (in seconds) that the integration will scan for Bluetooth devices before attempting to send the pair command. A longer scan can help find devices that are slow to advertise their presence.

## Read in your own language

*   [Afrikaans](readme/README.af.md)
*   [العربية (Arabic)](readme/README.ar.md)
*   [български (Bulgarian)](readme/README.bg.md)
*   [বাংলা (Bengali)](readme/README.bn.md)
*   [Català (Catalan)](readme/README.ca.md)
*   [Čeština (Czech)](readme/README.cs.md)
*   [Dansk (Danish)](readme/README.da.md)
*   [Deutsch (German)](readme/README.de.md)
*   [Deutsch (Schweiz) (German, Switzerland)](readme/README.de-CH.md)
*   [Ελληνικά (Greek)](readme/README.el.md)
*   [English](README.md)
*   [Español (Spanish)](readme/README.es.md)
*   [Eesti (Estonian)](readme/README.et.md)
*   [Euskara (Basque)](readme/README.eu.md)
*   [فارسی (Persian)](readme/README.fa.md)
*   [Suomi (Finnish)](readme/README.fi.md)
*   [Français (French)](readme/README.fr.md)
*   [Gaeilge (Irish)](readme/README.ga.md)
*   [Galego (Galician)](readme/README.gl.md)
*   [ગુજરાતી (Gujarati)](readme/README.gu.md)
*   [עברית (Hebrew)](readme/README.he.md)
*   [हिन्दी (Hindi)](readme/README.hi.md)
*   [Hrvatski (Croatian)](readme/README.hr.md)
*   [Magyar (Hungarian)](readme/README.hu.md)
*   [Bahasa Indonesia (Indonesian)](readme/README.id.md)
*   [Íslenska (Icelandic)](readme/README.is.md)
*   [Italiano (Italian)](readme/README.it.md)
*   [日本語 (Japanese)](readme/README.ja.md)
*   [ქართული (Georgian)](readme/README.ka.md)
*   [ಕನ್ನಡ (Kannada)](readme/README.kn.md)
*   [한국어 (Korean)](readme/README.ko.md)
*   [Kernewek (Cornish)](readme/README.kw.md)
*   [Lëtzebuergesch (Luxembourgish)](readme/README.lb.md)
*   [Lietuvių (Lithuanian)](readme/README.lt.md)
*   [Latviešu (Latvian)](readme/README.lv.md)
*   [മലയാളം (Malayalam)](readme/README.ml.md)
*   [Монгол (Mongolian)](readme/README.mn.md)
*   [मराठी (Marathi)](readme/README.mr.md)
*   [Bahasa Melayu (Malay)](readme/README.ms.md)
*   [Norsk bokmål (Norwegian Bokmål)](readme/README.nb.md)
*   [नेपाली (Nepali)](readme/README.ne.md)
*   [Nederlands (Dutch)](readme/README.nl.md)
*   [Polski (Polish)](readme/README.pl.md)
*   [Português (Portuguese)](readme/README.pt.md)
*   [Português (Brasil) (Portuguese, Brazil)](readme/README.pt-BR.md)
*   [Română (Romanian)](readme/README.ro.md)
*   [Русский (Russian)](readme/README.ru.md)
*   [Slovenčina (Slovak)](readme/README.sk.md)
*   [Slovenščina (Slovenian)](readme/README.sl.md)
*   [Српски (Serbian)](readme/README.sr.md)
*   [Srpski (latinica) (Serbian, Latin)](readme/README.sr-Latn.md)
*   [Svenska (Swedish)](readme/README.sv.md)
*   [Kiswahili (Swahili)](readme/README.sw.md)
*   [తెలుగు (Telugu)](readme/README.te.md)
*   [ไทย (Thai)](readme/README.th.md)
*   [Türkçe (Turkish)](readme/README.tr.md)
*   [Українська (Ukrainian)](readme/README.uk.md)
*   [اردو (Urdu)](readme/README.ur.md)
*   [Tiếng Việt (Vietnamese)](readme/README.vi.md)
*   [简体中文 (Simplified Chinese)](readme/README.zh-CN.md)
*   [繁體中文 (香港) (Traditional Chinese, Hong Kong)](readme/README.zh-HK.md)

---