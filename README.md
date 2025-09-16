# MiPower — Home Assistant custom integration

[![Release](https://img.shields.io/github/v/release/DenizOner/MiPower?label=release)](https://github.com/DenizOner/MiPower/releases)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.8%2B-41BDF5)](https://www.home-assistant.io/)
[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)
[![HACS](https://img.shields.io/badge/HACS-Integration-blue)](https://hacs.xyz/)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower)](https://github.com/DenizOner/MiPower/issues)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

**MiPower** is a focused Home Assistant custom integration that provides a switch platform to send wake/power signals to devices like Mi Box / Android TV boxes. It intentionally focuses on signaling (wake/power), not on long-lived pairing/remote control connections.

---

## Highlights

- Easy setup using existing `media_player` devices.
- Advanced setup for manual configuration (Display name, MAC, device selection).
- Full Options-flow support (options gear visible after setup).
- Per-entry coordinator model (each config entry has its own coordinator and options).
- `__pycache__` cleanup service available: `mipower.cleanup_pycache`.
- Diagnostics support and options for tuning debounce and connection behavior.

---

## Requirements & Compatibility

- Home Assistant: tested with **2025.9.3**, but backwards compatibility starts from `2021.12.0` per manifest.  
- Python dependency: `pexpect`.
- Platforms: `switch`.
- Integration type: local push / UI config flow.

---

## Installation

### HACS (recommended)
1. Add this repository to HACS (Integrations → Custom repositories → add repo URL).  
2. Install the integration from HACS.  
3. Restart Home Assistant.

### Manual
1. Copy the `custom_components/mipower/` folder into `config/custom_components/`.  
2. Restart Home Assistant.

---

## Quick Setup (UI)

1. Settings → Devices & Services → Add Integration → **MiPower**.  
2. Choose between **Easy setup** (select a `media_player` device only) or **Advanced setup** (enter Display name, MAC, select device, and tune advanced options).  
3. After creation, the **Options (gear)** is available on the integration panel to adjust parameters.

---

## Entity Behavior

- Entity name format: `MiPower - <media_player name>`.  
- Entity icon: `mdi:power`.  
- Unique ID format: `mipower_<MAC_without_colons_uppercase>` (e.g. `mipower_E0B655526C00`).  
- Each config entry has a dedicated coordinator to support multiple devices and options per entry.

---

## Diagnostics & Debugging

- Diagnostics available from the integration panel (entry-level).  
- Service `mipower.cleanup_pycache` available under Developer Tools → Services.  

---

## Contributing & Issues

- Please file issues on GitHub: [Issues](https://github.com/DenizOner/MiPower/issues).  
- Pull requests welcome — keep code modular and test changes against a recent Home Assistant instance.

---

## License

This project is released under the **MIT License**. See the `LICENSE` file in the repo.