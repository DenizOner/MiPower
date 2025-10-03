# MiPower — Home Assistant ಕಸ್ಟಮ್ ಇಂಟಿಗ್ರೇಷನ್

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** ಎಂಬುದು Home Assistant ಇಂಟಿಗ್ರೇಷನ್ ಆಗಿದ್ದು, ಇದು ಸಾಂಪ್ರದಾಯಿಕ ವೇಕ್-ಆನ್-ಲ್ಯಾನ್ (Wake-on-LAN - WOL) ಅನ್ನು ಬೆಂಬಲಿಸದ ಆದರೆ ಬ್ಲೂಟೂತ್ ಜೋಡಣೆ (pairing) ವಿನಂತಿಯ ಮೂಲಕ "ಜಾಗೃತಗೊಳಿಸಬಹುದಾದ" ಮೀಡಿಯಾ ಪ್ಲೇಯರ್‌ಗಳ ಪವರ್ ಸ್ಥಿತಿಯನ್ನು ನಿಯಂತ್ರಿಸಲು ನಿಮಗೆ ಅನುಮತಿಸುತ್ತದೆ. ಇದನ್ನು ನಿರ್ದಿಷ್ಟವಾಗಿ Xiaomi Mi Box ನಂತಹ ಸಾಧನಗಳಿಗಾಗಿ ವಿನ್ಯಾಸಗೊಳಿಸಲಾಗಿದೆ, ಆದರೆ ಇತರ ಇದೇ ರೀತಿಯ Android TV ಬಾಕ್ಸ್‌ಗಳೊಂದಿಗೆ ಸಹ ಕಾರ್ಯನಿರ್ವಹಿಸಬಹುದು.

ಈ ಇಂಟಿಗ್ರೇಷನ್ Home Assistant ನಲ್ಲಿ ಒಂದು `switch` (ಸ್ವಿಚ್) ಎಂಟಿಟಿಯನ್ನು ರಚಿಸುತ್ತದೆ. 
- ಸ್ವಿಚ್ ಅನ್ನು **ಆನ್** ಮಾಡುವುದರಿಂದ ಸಾಧನವನ್ನು ಜಾಗೃತಗೊಳಿಸಲು `bluetoothctl` ಮೂಲಕ ಬ್ಲೂಟೂತ್ ಕಮಾಂಡ್‌ಗಳ ಸರಣಿಯನ್ನು ಕಳುಹಿಸುತ್ತದೆ.
- ಸ್ವಿಚ್ ಅನ್ನು **ಆಫ್** ಮಾಡುವುದರಿಂದ ಲಿಂಕ್ ಮಾಡಲಾದ ಸಾಧನಕ್ಕಾಗಿ `media_player.turn_off` ಸೇವೆಯನ್ನು ಕರೆಯುತ್ತದೆ.
- ಸ್ವಿಚ್ ಸ್ಥಿತಿಯು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಲಿಂಕ್ ಮಾಡಲಾದ ಮೀಡಿಯಾ ಪ್ಲೇಯರ್ ಎಂಟಿಟಿ ಸ್ಥಿತಿಯೊಂದಿಗೆ ಸಿಂಕ್ರೊನೈಸ್ ಆಗುತ್ತದೆ.

## 🤝 ಬೆಂಬಲಿಸಿ

MiPower ಯೋಜನೆಯು ಮುಕ್ತ ಮೂಲ ಸಮುದಾಯಕ್ಕೆ ಮೌಲ್ಯವನ್ನು ಸೇರಿಸುವ ದೃಷ್ಟಿಯೊಂದಿಗೆ ಅಭಿವೃದ್ಧಿಪಡಿಸಲಾಗಿದೆ. ಈ ಯೋಜನೆಯ ನಿರಂತರತೆ ಮತ್ತು ಅಭಿವೃದ್ಧಿ ವೇಗವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಲು ನಿಮ್ಮ ಬೆಂಬಲ ಅತ್ಯುತ್ಕೃಷ್ಟವಾಗಿದೆ.

ನೀವು ನನ್ನ ಕೆಲಸವನ್ನು ಪ್ರಶಂಸಿಸಿದರೆ, ನೀವು GitHub Sponsors ಅಥವಾ ಕೆಳಗಿನ ಪ್ಲಾಟ್‌ಫಾರ್ಮ್‌ಗಳ ಮೂಲಕ ನನಗೆ ಬೆಂಬಲ ನೀಡಬಹುದು. ಮುಂಚಿತವಾಗಿ ಧನ್ಯವಾದಗಳು!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

ಪರ್ಯಾಯವಾಗಿ, ರೆಪೊಸಿಟರಿಯ ಮೇಲಿನ ಬಲ ಮೂಲೆಯಲ್ಲಿರುವ **ಪ್ರಾಯೋಜಕ ಬಟನ್ (❤️)** ಅನ್ನು ಕ್ಲಿಕ್ ಮಾಡುವ ಮೂಲಕ ನೀವು ಎಲ್ಲಾ ಹಣಕಾಸು ಆಯ್ಕೆಗಳನ್ನು ನೋಡಬಹುದು.

## ಪೂರ್ವಾಪೇಕ್ಷಿತಗಳು

- **Home Assistant OS / Supervised / Container:** ಈ ಇಂಟಿಗ್ರೇಷನ್‌ಗೆ `bluetoothctl` ಕಮಾಂಡ್-ಲೈನ್ ಉಪಕರಣವು ಲಭ್ಯವಿರುವ ಮತ್ತು ಪ್ರವೇಶಿಸಬಹುದಾದ Linux-ಆಧಾರಿತ Home Assistant ಇನ್‌ಸ್ಟಾಲೇಶನ್ ಅಗತ್ಯವಿದೆ. ಇದು Windows ನಲ್ಲಿನ Home Assistant Core ಇನ್‌ಸ್ಟಾಲೇಶನ್‌ನಲ್ಲಿ **ಕಾರ್ಯನಿರ್ವಹಿಸುವುದಿಲ್ಲ**.

## HACS ಮೂಲಕ ಇನ್‌ಸ್ಟಾಲೇಶನ್ (ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ)

ಈ ಇಂಟಿಗ್ರೇಷನ್ HACS ನಲ್ಲಿ ಕಸ್ಟಮ್ ರೆಪೊಸಿಟರಿಯಾಗಿ ಲಭ್ಯವಿದೆ.

1.  ನಿಮ್ಮ HACS ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ನ್ಯಾವಿಗೇಟ್ ಮಾಡಿ.
2.  **Integrations** (ಇಂಟಿಗ್ರೇಷನ್‌ಗಳು) ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ.
3.  ಮೇಲಿನ-ಬಲ ಮೂಲೆಯಲ್ಲಿರುವ ಮೂರು-ಡಾಟ್ ಮೆನು ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ ಮತ್ತು **"Custom repositories"** ("ಕಸ್ಟಮ್ ರೆಪೊಸಿಟರಿಗಳು") ಆಯ್ಕೆಮಾಡಿ.
4.  ಡೈಲಾಗ್ ಬಾಕ್ಸ್‌ನಲ್ಲಿ, ಈ ಕೆಳಗಿನ ಮಾಹಿತಿಯನ್ನು ನಮೂದಿಸಿ:
    - **Repository (ರೆಪೊಸಿಟರಿ):** `https://github.com/DenizOner/MiPower`
    - **Category (ವರ್ಗ):** `Integration` (ಇಂಟಿಗ್ರೇಷನ್)
5.  **"Add"** ("ಸೇರಿಸಿ") ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ.
6.  "MiPower" ಇಂಟಿಗ್ರೇಷನ್ ಈಗ ನಿಮ್ಮ HACS ಪಟ್ಟಿಯಲ್ಲಿ ಕಾಣಿಸಿಕೊಳ್ಳುತ್ತದೆ. ಅದರ ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ.
7.  **"Download"** ("ಡೌನ್‌ಲೋಡ್") ಬಟನ್ ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ ಮತ್ತು ನಂತರ ಮುಂದಿನ ವಿಂಡೋದಲ್ಲಿ ಮತ್ತೆ **"Download"** ("ಡೌನ್‌ಲೋಡ್") ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ.
8.  ಡೌನ್‌ಲೋಡ್ ಪೂರ್ಣಗೊಂಡ ನಂತರ, ಇಂಟಿಗ್ರೇಷನ್ ಲೋಡ್ ಆಗಲು **ನೀವು ಹೋಮ್ ಅಸಿಸ್ಟೆಂಟ್ ಅನ್ನು ಮರುಪ್ರಾರಂಭಿಸಬೇಕು**.

## ಮ್ಯಾನುಯಲ್ ಇನ್‌ಸ್ಟಾಲೇಶನ್

HACS ಶಿಫಾರಸು ಮಾಡಲಾದ ವಿಧಾನವಾಗಿದ್ದರೂ, ನೀವು ಇಂಟಿಗ್ರೇಷನ್ ಅನ್ನು ಮ್ಯಾನುಯಲ್ ಆಗಿ ಸಹ ಇನ್‌ಸ್ಟಾಲ್ ಮಾಡಬಹುದು.

1.  ರೆಪೊಸಿಟರಿಯ [ಬಿಡುಗಡೆ ಪುಟ](https://github.com/DenizOner/MiPower/releases) ಕ್ಕೆ ಹೋಗಿ ಮತ್ತು ಇತ್ತೀಚಿನ ಬಿಡುಗಡೆಯಿಂದ `mipower.zip` ಫೈಲ್ ಅನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ.
2.  ಡೌನ್‌ಲೋಡ್ ಮಾಡಿದ ಫೈಲ್ ಅನ್ನು ಅನ್ಜಿಪ್ ಮಾಡಿ.
3.  ಅನ್ಜಿಪ್ ಮಾಡಿದ ಫೋಲ್ಡರ್ ಒಳಗೆ, ನೀವು `custom_components` ಡೈರೆಕ್ಟರಿಯನ್ನು ಕಾಣಬಹುದು. ಅದರಿಂದ `mipower` ಫೋಲ್ಡರ್ ಅನ್ನು ನಕಲಿಸಿ.
4.  ನಕಲಿಸಿದ `mipower` ಫೋಲ್ಡರ್ ಅನ್ನು ನಿಮ್ಮ ಹೋಮ್ ಅಸಿಸ್ಟೆಂಟ್ ಕಾನ್ಫಿಗರೇಶನ್ ಡೈರೆಕ್ಟರಿಯಲ್ಲಿರುವ `custom_components` ಫೋಲ್ಡರ್‌ಗೆ ಅಂಟಿಸಿ. `custom_components` ಫೋಲ್ಡರ್ ಅಸ್ತಿತ್ವದಲ್ಲಿ ಇಲ್ಲದಿದ್ದರೆ, ನೀವು ಅದನ್ನು ರಚಿಸಬೇಕು.
    - ಅಂತಿಮ ಮಾರ್ಗವು ಹೀಗಿರಬೇಕು: `.../config/custom_components/mipower/`
5.  ಹೋಮ್ ಅಸಿಸ್ಟೆಂಟ್ ಅನ್ನು ಮರುಪ್ರಾರಂಭಿಸಿ.

## ಕಾನ್ಫಿಗರೇಶನ್

ಮರುಪ್ರಾರಂಭದ ನಂತರ, ನೀವು MiPower ಸ್ವಿಚ್ ಅನ್ನು ಸೇರಿಸಬಹುದು ಮತ್ತು ಕಾನ್ಫಿಗರ್ ಮಾಡಬಹುದು.

1.  **Settings > Devices & Services** (ಸೆಟ್ಟಿಂಗ್‌ಗಳು > ಸಾಧನಗಳು ಮತ್ತು ಸೇವೆಗಳು) ಗೆ ಹೋಗಿ.
2.  ಕೆಳಗಿನ-ಬಲ ಮೂಲೆಯಲ್ಲಿರುವ **"+ Add Integration"** ("+ ಇಂಟಿಗ್ರೇಷನ್ ಸೇರಿಸಿ") ಬಟನ್ ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ.
3.  **"MiPower"** ಅನ್ನು ಹುಡುಕಿ ಮತ್ತು ಅದರ ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ.

### ಸುಲಭ ಸೆಟಪ್ (ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ)

ಇಂಟಿಗ್ರೇಷನ್ ಅನ್ನು ಕಾನ್ಫಿಗರ್ ಮಾಡುವ ಸರಳ ವಿಧಾನ ಇದು.

1.  ಪ್ರೇರೇಪಿಸಿದಾಗ, **"Easy Setup"** ("ಸುಲಭ ಸೆಟಪ್") ಆಯ್ಕೆಮಾಡಿ.
2.  ಇಂಟಿಗ್ರೇಷನ್ ನಿಮ್ಮ ಸಿಸ್ಟಮ್‌ನಲ್ಲಿ ಬ್ಲೂಟೂತ್-ಸಕ್ರಿಯಗೊಳಿಸಿದ ಮೀಡಿಯಾ ಪ್ಲೇಯರ್‌ಗಳನ್ನು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಕಂಡುಕೊಳ್ಳುತ್ತದೆ.
3.  ಡ್ರಾಪ್‌ಡೌನ್ ಪಟ್ಟಿಯಿಂದ ನಿಮ್ಮ ಗುರಿ ಸಾಧನವನ್ನು (ಉದಾಹರಣೆಗೆ, "Xiaomi Mi Box 4") ಆಯ್ಕೆಮಾಡಿ.
4.  **"Submit"** ("ಸಲ್ಲಿಸಿ") ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ.

ಅಷ್ಟೇ! ಇಂಟಿಗ್ರೇಷನ್ ನಿಮ್ಮ ಮೀಡಿಯಾ ಪ್ಲೇಯರ್‌ಗೆ ಲಿಂಕ್ ಮಾಡಲಾದ ಸ್ವಿಚ್ ಅನ್ನು ರಚಿಸುತ್ತದೆ.

### ಸುಧಾರಿತ ಸೆಟಪ್

ಸುಲಭ ಸೆಟಪ್ ನಿಮ್ಮ ಸಾಧನವನ್ನು ಕಂಡುಹಿಡಿಯದಿದ್ದರೆ ಅಥವಾ ಮೊದಲಿನಿಂದಲೂ ಸುಧಾರಿತ ಟೈಮಿಂಗ್ ಸೆಟ್ಟಿಂಗ್‌ಗಳನ್ನು ಕಾನ್ಫಿಗರ್ ಮಾಡುವ ಅಗತ್ಯವಿದ್ದರೆ ಈ ವಿಧಾನವನ್ನು ಬಳಸಿ.

1.  **ಹಂತ 1: ಸಾಧನ ಆಯ್ಕೆ**
    - **"Advanced Setup"** ("ಸುಧಾರಿತ ಸೆಟಪ್") ಆಯ್ಕೆಮಾಡಿ.
    - ನಿಮ್ಮ Home Assistant ನಲ್ಲಿನ *ಎಲ್ಲಾ* ಮೀಡಿಯಾ ಪ್ಲೇಯರ್‌ಗಳ ಪಟ್ಟಿಯಿಂದ ನಿಮ್ಮ ಗುರಿ ಮೀಡಿಯಾ ಪ್ಲೇಯರ್ ಅನ್ನು ಆಯ್ಕೆ ಮಾಡಿ.
2.  **ಹಂತ 2: MAC ವಿಳಾಸ**
    - ಇಂಟಿಗ್ರೇಷನ್ ಆಯ್ಕೆಮಾಡಿದ ಸಾಧನದ ಬ್ಲೂಟೂತ್ MAC ವಿಳಾಸವನ್ನು ಹುಡುಕಲು ಪ್ರಯತ್ನಿಸುತ್ತದೆ. 
    - ಕಂಡುಬಂದರೆ, ಅದನ್ನು ಮೊದಲೇ ಭರ್ತಿ ಮಾಡಲಾಗುತ್ತದೆ. ಅದು ಸರಿಯಾಗಿದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ.
    - ಕಂಡುಬಂದಿಲ್ಲವಾದರೆ, ನಿಮ್ಮ ಸಾಧನದ ಬ್ಲೂಟೂತ್ MAC ವಿಳಾಸವನ್ನು ನೀವು ಮ್ಯಾನುಯಲ್ ಆಗಿ ನಮೂದಿಸಬೇಕು.
3.  **ಹಂತ 3: ಟೈಮಿಂಗ್ ಸೆಟ್ಟಿಂಗ್‌ಗಳು**
    - ಬ್ಲೂಟೂತ್ ಕಮಾಂಡ್‌ಗಳಿಗಾಗಿ ನೀವು ವಿವಿಧ ಟೈಮ್‌ಔಟ್‌ಗಳು ಮತ್ತು ವಿಳಂಬಗಳನ್ನು ಕಾನ್ಫಿಗರ್ ಮಾಡಬಹುದು. ಹೆಚ್ಚಿನ ಬಳಕೆದಾರರಿಗೆ, ಡೀಫಾಲ್ಟ್ ಮೌಲ್ಯಗಳು ಸಾಕಾಗುತ್ತದೆ.
4.  ಸೆಟಪ್ ಪೂರ್ಣಗೊಳಿಸಲು **"Submit"** ("ಸಲ್ಲಿಸಿ") ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ.

## ಆಯ್ಕೆಗಳು

ಒಮ್ಮೆ ನೀವು ನಿಮ್ಮ MiPower ಸ್ವಿಚ್ ಅನ್ನು ಕಾನ್ಫಿಗರ್ ಮಾಡಿದ ನಂತರ, ನೀವು ಯಾವುದೇ ಸಮಯದಲ್ಲಿ ಟೈಮಿಂಗ್ ಸೆಟ್ಟಿಂಗ್‌ಗಳನ್ನು ಹೊಂದಿಸಬಹುದು.

1.  **Settings > Devices & Services** (ಸೆಟ್ಟಿಂಗ್‌ಗಳು > ಸಾಧನಗಳು ಮತ್ತು ಸೇವೆಗಳು) ಗೆ ಹೋಗಿ.
2.  MiPower ಇಂಟಿಗ್ರೇಷನ್ ಅನ್ನು ಹುಡುಕಿ ಮತ್ತು **"Configure"** ("ಕಾನ್ಫಿಗರ್ ಮಾಡಿ") ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ.
3.  ಅಗತ್ಯವಿರುವಂತೆ *debounce*, ಟೈಮ್‌ಔಟ್‌ಗಳು ಮತ್ತು ವಿಳಂಬಗಳಿಗಾಗಿ ಸ್ಲೈಡರ್‌ಗಳನ್ನು ಹೊಂದಿಸಿ.

## ಟೈಮಿಂಗ್ ಸೆಟ್ಟಿಂಗ್‌ಗಳ ವಿವರಣೆ

ಕಾನ್ಫಿಗರೇಶನ್ ಅಥವಾ ಆಯ್ಕೆಗಳ ಮೆನುವಿನಲ್ಲಿ, ನೀವು ಬ್ಲೂಟೂತ್ ಕಮಾಂಡ್‌ಗಳ ಟೈಮಿಂಗ್ ಅನ್ನು ಫೈನ್-ಟ್ಯೂನ್ ಮಾಡಬಹುದು. ಹೆಚ್ಚಿನ ಬಳಕೆದಾರರಿಗೆ, ಡೀಫಾಲ್ಟ್ ಮೌಲ್ಯಗಳು ಉತ್ತಮವಾಗಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತವೆ.

- **Turn-On Debounce (ಆನ್ ಮಾಡುವ ಡಿಬೌನ್ಸ್):** 'ಆನ್ ಮಾಡಿ' ಕಮಾಂಡ್ ಅನ್ನು ಮತ್ತೆ ಕಾರ್ಯಗತಗೊಳಿಸಲು ಸಾಧ್ಯವಾಗುವ ಮೊದಲು ಕಳೆಯಬೇಕಾದ ಕನಿಷ್ಠ ಸಮಯ (ಸೆಕೆಂಡುಗಳಲ್ಲಿ). ಸ್ವಿಚ್ ಅನ್ನು ತ್ವರಿತವಾಗಿ ಟಾಗಲ್ ಮಾಡಿದರೆ ಇದು ಸಾಧನವನ್ನು ವೇಕ್-ಅಪ್ ಸಿಗ್ನಲ್‌ಗಳೊಂದಿಗೆ ಸ್ಪ್ಯಾಮಿಂಗ್ ಮಾಡುವುದನ್ನು ತಡೆಯುತ್ತದೆ.

- **Turn-Off Debounce (ಆಫ್ ಮಾಡುವ ಡಿಬೌನ್ಸ್):** 'ಆಫ್ ಮಾಡಿ' ಕಮಾಂಡ್ ಅನ್ನು ಮತ್ತೆ ಕಾರ್ಯಗತಗೊಳಿಸಲು ಸಾಧ್ಯವಾಗುವ ಮೊದಲು ಕಳೆಯಬೇಕಾದ ಕನಿಷ್ಠ ಸಮಯ (ಸೆಕೆಂಡುಗಳಲ್ಲಿ). 

- **Delay Between Commands (ಕಮಾಂಡ್‌ಗಳ ನಡುವಿನ ವಿಳಂಬ):** `bluetoothctl` ಯುಟಿಲಿಟಿಗೆ ಸತತ ಕಮಾಂಡ್‌ಗಳನ್ನು ಕಳುಹಿಸುವ ನಡುವಿನ ಬಹಳ ಕಡಿಮೆ ವಿಳಂಬ (ಸೆಕೆಂಡುಗಳಲ್ಲಿ). ಕೆಲವು ಸಿಸ್ಟಮ್‌ಗಳಲ್ಲಿ, ಸಣ್ಣ ವಿರಾಮವನ್ನು ಸೇರಿಸುವುದರಿಂದ ವಿಶ್ವಾಸಾರ್ಹತೆಯನ್ನು ಸುಧಾರಿಸಬಹುದು.

- **Process Spawn Timeout (ಪ್ರಕ್ರಿಯೆ ಹುಟ್ಟಿಸುವ ಟೈಮ್‌ಔಟ್):** `bluetoothctl` ಪ್ರಕ್ರಿಯೆಯು ಪ್ರಾರಂಭವಾಗಲು ಕಾಯುವ ಗರಿಷ್ಠ ಸಮಯ (ಸೆಕೆಂಡುಗಳಲ್ಲಿ). ಈ ಸಮಯದೊಳಗೆ ಅದು ಪ್ರಾರಂಭಿಸಲು ವಿಫಲವಾದರೆ, ಆನ್ ಮಾಡುವ ಪ್ರಯತ್ನವು ವಿಫಲಗೊಳ್ಳುತ್ತದೆ.

- **Pairing Timeout (ಜೋಡಣೆ ಟೈಮ್‌ಔಟ್):** ಸರಳೀಕೃತ ಟರ್ನ್-ಆನ್ ತರ್ಕದಲ್ಲಿ, ಯಶಸ್ಸನ್ನು ಊಹಿಸುವ ಮೊದಲು `pair` ಕಮಾಂಡ್ ಕಳುಹಿಸಿದ ನಂತರ ಕಾಯಬೇಕಾದ ಸಮಯ ಇದು. ಇದು ಸಾಧನಕ್ಕೆ ವೇಕ್-ಅಪ್ ಸಿಗ್ನಲ್ ಅನ್ನು ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲು ಸಮಯವನ್ನು ನೀಡುತ್ತದೆ.

- **Bluetooth Scan Duration (ಬ್ಲೂಟೂತ್ ಸ್ಕ್ಯಾನ್ ಅವಧಿ):** ಜೋಡಣೆ ಕಮಾಂಡ್ ಕಳುಹಿಸಲು ಪ್ರಯತ್ನಿಸುವ ಮೊದಲು ಇಂಟಿಗ್ರೇಷನ್ ಬ್ಲೂಟೂತ್ ಸಾಧನಗಳಿಗಾಗಿ ಸ್ಕ್ಯಾನ್ ಮಾಡುವ ಅವಧಿ (ಸೆಕೆಂಡುಗಳಲ್ಲಿ). ದೀರ್ಘವಾದ ಸ್ಕ್ಯಾನ್ ತಮ್ಮ ಉಪಸ್ಥಿತಿಯನ್ನು ಜಾಹೀರಾತು ಮಾಡಲು ನಿಧಾನವಾಗಿರುವ ಸಾಧನಗಳನ್ನು ಕಂಡುಹಿಡಿಯಲು ಸಹಾಯ ಮಾಡಬಹುದು.

## ನಿಮ್ಮ ಸ್ವಂತ ಭಾಷೆಯಲ್ಲಿ ಓದಿ

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