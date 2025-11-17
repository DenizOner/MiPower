# MiPower — Home Assistant Custom Integration

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

---

**MiPower** is a Home Assistant integration that allows you to control the power state of media players that don't support traditional Wake-on-LAN (WOL), but can be "woken up" with a Bluetooth pairing request. It's specifically designed for devices like Xiaomi Mi Box, but may work with other similar Android TV boxes.

This integration creates a `switch` entity in Home Assistant:
- **TURNING ON** the switch wakes up the device by sending a series of Bluetooth commands via `bluetoothctl`
- **TURNING OFF** the switch calls the `media_player.turn_off` service for the linked device
- The switch state automatically synchronizes with the linked media player entity's state

## 🤝 Support the Project

MiPower is developed with the vision of contributing value to the open-source community. Your support is vital to maintain this project's continuity and development speed.

If you appreciate my work, you can support me through GitHub Sponsorships or the platforms below. Thank you in advance!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternatively, you can click the **Sponsor button (❤️)** in the top right corner of the repository to see all funding options.

## Prerequisites

- **Home Assistant OS / Supervised / Container:** This integration requires a Linux-based Home Assistant installation where the `bluetoothctl` command-line tool is available and accessible. It **DOES NOT WORK** on Windows-based Home Assistant Core installations.

## Installation via HACS (Recommended)

This integration is available as a custom repository in HACS.

1.  Go to your HACS control panel.
2.  Click on **Integrations**.
3.  Click the three dots in the top right corner and select **"Custom repositories"**.
4.  Enter the following information in the dialog:
    - **Repository:** `https://github.com/DenizOner/MiPower`
    - **Category:** `Integration`
5.  Click **"Add"**.
6.  "MiPower" integration will now appear in your HACS list. Click on it.
7.  Click **"Download"** and then **"Download"** again in the next window.
8.  After download completes, **RESTART HOME ASSISTANT** for the integration to load.

## Manual Installation

Although HACS is the recommended method, you can also install the integration manually.

1.  Download or clone this repository to your local machine.
2.  Copy the `custom_components/mipower` folder from the repository.
3.  Paste the copied `mipower` folder into your Home Assistant configuration directory's `custom_components` folder. Create the `custom_components` folder if it doesn't exist.
    - The final path should look like: `.../config/custom_components/mipower/`
4.  Restart Home Assistant.

## Configuration

After restarting, you can add and configure the MiPower switch.

1.  Go to **Settings > Devices & Services**.
2.  Click the **"+ Add Integration"** button in the bottom right corner.
3.  Search for **"MiPower"** and click on it.

### Easy Setup (Recommended)

This is the simplest way to configure the integration.

1.  When prompted, select **"Easy Setup"**.
2.  The integration will automatically discover Bluetooth-enabled media players in your system.
3.  Select your target device (e.g., "Xiaomi Mi Box 4") from the dropdown list.
4.  Click **"Submit"**.

That's it! The integration will create a switch linked to your media player.

### Advanced Setup

Use this method if Easy Setup doesn't find your device or if you need to configure advanced timing settings from the start.

1.  **Step 1: Device Selection**
    - Select **"Advanced Setup"**.
    - Choose your target media player from the list of *all* media players in your Home Assistant.
2.  **Step 2: MAC Address**
    - The integration will try to find the Bluetooth MAC Address of the selected device.
    - If found, it will be pre-filled. Make sure it's correct.
    - If not found, you'll need to manually enter your device's Bluetooth MAC Address.
3.  **Step 3: Timing Settings**
    - You can configure various timeouts and delays for Bluetooth commands. Default values work well for most users.
4.  Click **"Submit"** to complete the setup.

## Options

After configuring your MiPower switch, you can adjust timing settings at any time.

1.  Go to **Settings > Devices & Services**.
2.  Find the MiPower integration and click **"Configure"**.
3.  Adjust the sliders for *debounce*, timeouts, and delays as needed.

## Diagnostics

If you're experiencing issues with your MiPower integration, you can access detailed diagnostics information:

1.  Go to **Settings > Devices & Services**.
2.  Find the MiPower integration and click on it.
3.  Click the **"System Options"** (three dots) menu in the top right corner.
4.  Select **"Download Diagnostics"** to get comprehensive troubleshooting information including:
   - Your current configuration settings
   - Discovered Bluetooth devices
   - Media player discovery results
   - Entity information and status

## Timing Settings Explanation

In the configuration or options menu, you can fine-tune the timing of Bluetooth commands. Default values work well for most users.

- **Turn-On Debounce (seconds):** Minimum time that must pass before the 'turn-on' command can be executed again. This prevents spamming the device with wake-up signals if the switch is toggled rapidly. Also serves as the overall timeout for the wake-up operation - if the device doesn't respond within this time, the operation fails.

- **Turn-Off Debounce (seconds):** Minimum time that must pass before the 'turn-off' command can be executed again.

- **Inter-Step Delay (seconds):** Delay between major steps in the wake-up process. This gives each step time to complete properly.

- **Process Spawn Timeout (seconds):** Maximum time to wait for the `bluetoothctl` process to start. If it doesn't start within this time, the wake-up attempt fails.

- **Bluetooth Signal Duration (seconds):** How long the Bluetooth pairing signal is broadcast. If the media player becomes available during this broadcast, the signal stops early to avoid unnecessary Bluetooth activity.

- **Bluetooth Scan Duration (seconds):** How long to scan for Bluetooth devices before attempting to send pairing commands. Longer scans help find devices that announce their presence slowly.

- **Bluetooth Scan Stop Timeout (seconds):** Maximum time to wait for the scan to stop cleanly.

The integration uses a smart wake-up algorithm:
1. Checks if the media player is already on/available before sending any Bluetooth commands
2. Broadcasts pairing signals for the configured duration (or stops early if device becomes available)
3. Waits for the device to fully wake up, with timeout = `on_debounce - total_elapsed_time`
4. Provides detailed logging for troubleshooting