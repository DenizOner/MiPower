# MiPower — ഹോം അസിസ്റ്റന്റ് കസ്റ്റം ഇൻ്റഗ്രേഷൻ

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** എന്നത് പരമ്പരാഗത Wake-on-LAN (WOL) പിന്തുണയ്ക്കാത്ത, എന്നാൽ ഒരു ബ്ലൂടൂത്ത് പെയറിംഗ് അഭ്യർത്ഥനയിലൂടെ "ഉണർത്താൻ" കഴിയുന്ന മീഡിയാ പ്ലെയറുകളുടെ പവർ സ്റ്റാറ്റസ് നിയന്ത്രിക്കാൻ നിങ്ങളെ അനുവദിക്കുന്ന ഒരു ഹോം അസിസ്റ്റൻ്റ് ഇൻ്റഗ്രേഷനാണ്. ഇത് Xiaomi Mi Box പോലുള്ള ഉപകരണങ്ങൾക്കായി പ്രത്യേകം രൂപകൽപ്പന ചെയ്തതാണ്, എന്നാൽ മറ്റ് സമാന Android TV ബോക്സുകളിലും പ്രവർത്തിച്ചേക്കാം.

ഈ ഇൻ്റഗ്രേഷൻ ഹോം അസിസ്റ്റൻ്റിൽ ഒരു `switch` (സ്വിച്ച്) എൻ്റിറ്റി സൃഷ്ടിക്കുന്നു. 
- സ്വിച്ച് **ഓൺ** ചെയ്യുന്നത് ഉപകരണം ഉണർത്താൻ `bluetoothctl` വഴി ബ്ലൂടൂത്ത് കമാൻഡുകളുടെ ഒരു പരമ്പര അയയ്ക്കുന്നു.
- സ്വിച്ച് **ഓഫ്** ചെയ്യുന്നത് ലിങ്ക് ചെയ്ത ഉപകരണത്തിനായി `media_player.turn_off` സേവനത്തെ വിളിക്കുന്നു.
- സ്വിച്ച് നില ലിങ്ക് ചെയ്ത മീഡിയാ പ്ലെയർ എൻ്റിറ്റിയുടെ നിലയുമായി യാന്ത്രികമായി സമന്വയിപ്പിക്കപ്പെടുന്നു.

## 🤝 പിന്തുണയ്ക്കുക

ഓപ്പൺ സോഴ്‌സ് കമ്മ്യൂണിറ്റിക്ക് മൂല്യം കൂട്ടുക എന്ന കാഴ്ചപ്പാടോടെയാണ് MiPower പ്രോജക്റ്റ് വികസിപ്പിക്കുന്നത്. ഈ പ്രോജക്റ്റിന്റെ തുടർച്ചയും വികസന വേഗതയും നിലനിർത്തുന്നതിന് നിങ്ങളുടെ പിന്തുണ വളരെ പ്രധാനമാണ്.

എന്റെ പ്രയത്നത്തെ നിങ്ങൾ അഭിനന്ദിക്കുന്നുണ്ടെങ്കിൽ, GitHub സ്പോൺസർമാർ വഴിയോ അല്ലെങ്കിൽ താഴെക്കൊടുത്തിട്ടുള്ള പ്ലാറ്റ്‌ഫോമുകൾ വഴിയോ നിങ്ങൾക്ക് എന്നെ പിന്തുണയ്ക്കാം. മുൻകൂട്ടി നന്ദി!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

പകരമായി, റിപ്പോസിറ്ററിയുടെ മുകളിൽ വലത് കോണിലുള്ള **സ്പോൺസർ ബട്ടൺ (❤️)** ക്ലിക്കുചെയ്യുന്നതിലൂടെ നിങ്ങൾക്ക് എല്ലാ ധനസഹായ ഓപ്ഷനുകളും കാണാനാകും.

## മുൻവ്യവസ്ഥകൾ

- **Home Assistant OS / Supervised / Container:** ഈ ഇൻ്റഗ്രേഷന് `bluetoothctl` കമാൻഡ്-ലൈൻ ഉപകരണം ലഭ്യമായതും ആക്‌സസ് ചെയ്യാനാകുന്നതുമായ ഒരു Linux അധിഷ്ഠിത ഹോം അസിസ്റ്റൻ്റ് ഇൻസ്റ്റാളേഷൻ ആവശ്യമാണ്. ഇത് Windows-ലെ ഹോം അസിസ്റ്റൻ്റ് കോർ ഇൻസ്റ്റാളേഷനിൽ **പ്രവർത്തിക്കില്ല**.

## HACS വഴി ഇൻസ്റ്റാൾ ചെയ്യൽ (ശുപാർശ ചെയ്യുന്നത്)

ഈ ഇൻ്റഗ്രേഷൻ HACS-ൽ ഒരു കസ്റ്റം റെപ്പോസിറ്ററിയായി ലഭ്യമാണ്.

1.  നിങ്ങളുടെ HACS ഡാഷ്‌ബോർഡിലേക്ക് പോകുക.
2.  **Integrations** (ഇൻ്റഗ്രേഷനുകൾ) ക്ലിക്ക് ചെയ്യുക.
3.  മുകളിൽ വലത് കോണിലുള്ള മൂന്ന്-ഡോട്ട് മെനു ക്ലിക്ക് ചെയ്ത് **"Custom repositories"** ("കസ്റ്റം റെപ്പോസിറ്ററികൾ") തിരഞ്ഞെടുക്കുക.
4.  ഡയലോഗ് ബോക്സിൽ, ഇനിപ്പറയുന്ന വിവരങ്ങൾ നൽകുക:
    - **Repository (റെപ്പോസിറ്ററി):** `https://github.com/DenizOner/MiPower`
    - **Category (വിഭാഗം):** `Integration` (ഇൻ്റഗ്രേഷൻ)
5.  **"Add"** ("ചേർക്കുക") ക്ലിക്ക് ചെയ്യുക.
6.  "MiPower" ഇൻ്റഗ്രേഷൻ ഇപ്പോൾ നിങ്ങളുടെ HACS ലിസ്റ്റിൽ ദൃശ്യമാകും. അതിൽ ക്ലിക്ക് ചെയ്യുക.
7.  **"Download"** ("ഡൗൺലോഡ്") ബട്ടൺ ക്ലിക്ക് ചെയ്യുക, തുടർന്ന് അടുത്ത വിൻഡോയിൽ വീണ്ടും **"Download"** ("ഡൗൺലോഡ്") ക്ലിക്ക് ചെയ്യുക.
8.  ഡൗൺലോഡ് പൂർത്തിയായ ശേഷം, ഇൻ്റഗ്രേഷൻ ലോഡ് ചെയ്യുന്നതിന് **നിങ്ങൾ ഹോം അസിസ്റ്റൻ്റ് പുനരാരംഭിക്കണം**.

## മാനുവൽ ഇൻസ്റ്റാളേഷൻ

HACS ശുപാർശ ചെയ്യുന്ന രീതിയാണെങ്കിലും, നിങ്ങൾക്ക് ഇൻ്റഗ്രേഷൻ മാനുവൽ ആയും ഇൻസ്റ്റാൾ ചെയ്യാം.

1.  റെപ്പോസിറ്ററിയുടെ [റിലീസ് പേജിലേക്ക്](https://github.com/DenizOner/MiPower/releases) പോയി ഏറ്റവും പുതിയ റിലീസിൽ നിന്ന് `mipower.zip` ഫയൽ ഡൗൺലോഡ് ചെയ്യുക.
2.  ഡൗൺലോഡ് ചെയ്ത ഫയൽ അൺസിപ്പ് ചെയ്യുക.
3.  അൺസിപ്പ് ചെയ്ത ഫോൾഡറിനുള്ളിൽ, നിങ്ങൾക്കൊരു `custom_components` ഡയറക്‌ടറി കാണാം. അതിനുള്ളിൽ നിന്ന് `mipower` ഫോൾഡർ പകർത്തി എടുക്കുക.
4.  പകർത്തിയ `mipower` ഫോൾഡർ നിങ്ങളുടെ ഹോം അസിസ്റ്റൻ്റ് കോൺഫിഗറേഷൻ ഡയറക്‌ടറിയിലെ `custom_components` ഫോൾഡറിലേക്ക് ഒട്ടിക്കുക. `custom_components` ഫോൾഡർ നിലവിലില്ലെങ്കിൽ, നിങ്ങൾ അത് സൃഷ്ടിക്കേണ്ടതുണ്ട്.
    - അവസാന പാത ഇങ്ങനെയായിരിക്കണം: `.../config/custom_components/mipower/`
5.  ഹോം അസിസ്റ്റൻ്റ് പുനരാരംഭിക്കുക.

## കോൺഫിഗറേഷൻ

പുനരാരംഭിച്ച ശേഷം, നിങ്ങൾക്ക് MiPower സ്വിച്ച് ചേർക്കാനും കോൺഫിഗർ ചെയ്യാനും കഴിയും.

1.  **Settings > Devices & Services** (ക്രമീകരണങ്ങൾ > ഉപകരണങ്ങളും സേവനങ്ങളും) എന്നതിലേക്ക് പോകുക.
2.  താഴെ വലത് കോണിലുള്ള **"+ Add Integration"** ("+ ഇൻ്റഗ്രേഷൻ ചേർക്കുക") ബട്ടൺ ക്ലിക്ക് ചെയ്യുക.
3.  **"MiPower"** എന്ന് തിരഞ്ഞ് അതിൽ ക്ലിക്ക് ചെയ്യുക.

### എളുപ്പമുള്ള സജ്ജീകരണം (ശുപാർശ ചെയ്യുന്നത്)

ഇൻ്റഗ്രേഷൻ കോൺഫിഗർ ചെയ്യുന്നതിനുള്ള ഏറ്റവും ലളിതമായ മാർഗ്ഗമാണിത്.

1.  ആവശ്യപ്പെടുമ്പോൾ, **"Easy Setup"** ("എളുപ്പമുള്ള സജ്ജീകരണം") തിരഞ്ഞെടുക്കുക.
2.  ഇൻ്റഗ്രേഷൻ നിങ്ങളുടെ സിസ്റ്റത്തിലെ ബ്ലൂടൂത്ത് പ്രവർത്തനക്ഷമമാക്കിയ മീഡിയാ പ്ലെയറുകൾ യാന്ത്രികമായി കണ്ടെത്തുന്നു.
3.  ഡ്രോപ്പ്-ഡൗൺ ലിസ്റ്റിൽ നിന്ന് നിങ്ങളുടെ ടാർഗെറ്റ് ഉപകരണം (ഉദാഹരണത്തിന്, "Xiaomi Mi Box 4") തിരഞ്ഞെടുക്കുക.
4.  **"Submit"** ("സമർപ്പിക്കുക") ക്ലിക്ക് ചെയ്യുക.

അത്രയേയുള്ളൂ! ഇൻ്റഗ്രേഷൻ നിങ്ങളുടെ മീഡിയാ പ്ലെയറുമായി ലിങ്ക് ചെയ്ത ഒരു സ്വിച്ച് സൃഷ്ടിക്കും.

### വിപുലമായ സജ്ജീകരണം

എളുപ്പമുള്ള സജ്ജീകരണം നിങ്ങളുടെ ഉപകരണം കണ്ടെത്തുന്നില്ലെങ്കിലോ അല്ലെങ്കിൽ തുടക്കം മുതൽ വിപുലമായ സമയ ക്രമീകരണങ്ങൾ കോൺഫിഗർ ചെയ്യേണ്ടതുണ്ടെങ്കിലോ ഈ രീതി ഉപയോഗിക്കുക.

1.  **ഘട്ടം 1: ഉപകരണം തിരഞ്ഞെടുക്കൽ**
    - **"Advanced Setup"** ("വിപുലമായ സജ്ജീകരണം") തിരഞ്ഞെടുക്കുക.
    - നിങ്ങളുടെ ഹോം അസിസ്റ്റൻ്റിലെ *എല്ലാ* മീഡിയാ പ്ലെയറുകളുടെയും ലിസ്റ്റിൽ നിന്ന് നിങ്ങളുടെ ടാർഗെറ്റ് മീഡിയാ പ്ലെയർ തിരഞ്ഞെടുക്കുക.
2.  **ഘട്ടം 2: MAC വിലാസം**
    - തിരഞ്ഞെടുത്ത ഉപകരണത്തിൻ്റെ ബ്ലൂടൂത്ത് MAC വിലാസം കണ്ടെത്താൻ ഇൻ്റഗ്രേഷൻ ശ്രമിക്കും. 
    - കണ്ടെത്തിയാൽ, അത് മുൻകൂട്ടി പൂരിപ്പിക്കും. അത് ശരിയാണോയെന്ന് പരിശോധിക്കുക.
    - കണ്ടെത്തിയില്ലെങ്കിൽ, നിങ്ങളുടെ ഉപകരണത്തിൻ്റെ ബ്ലൂടൂത്ത് MAC വിലാസം നിങ്ങൾ സ്വമേധയാ നൽകണം.
3.  **ഘട്ടം 3: സമയ ക്രമീകരണങ്ങൾ**
    - ബ്ലൂടൂത്ത് കമാൻഡുകൾക്കായി നിങ്ങൾക്ക് വിവിധ ടൈംഔട്ടുകളും കാലതാമസങ്ങളും കോൺഫിഗർ ചെയ്യാൻ കഴിയും. മിക്ക ഉപയോക്താക്കൾക്കും, ഡിഫോൾട്ട് മൂല്യങ്ങൾ മതിയാകും.
4.  സജ്ജീകരണം പൂർത്തിയാക്കാൻ **"Submit"** ("സമർപ്പിക്കുക") ക്ലിക്ക് ചെയ്യുക.

## ഓപ്ഷനുകൾ

നിങ്ങൾ MiPower സ്വിച്ച് കോൺഫിഗർ ചെയ്തുകഴിഞ്ഞാൽ, നിങ്ങൾക്ക് എപ്പോൾ വേണമെങ്കിലും സമയ ക്രമീകരണങ്ങൾ ക്രമീകരിക്കാൻ കഴിയും.

1.  **Settings > Devices & Services** (ക്രമീകരണങ്ങൾ > ഉപകരണങ്ങളും സേവനങ്ങളും) എന്നതിലേക്ക് പോകുക.
2.  MiPower ഇൻ്റഗ്രേഷൻ കണ്ടെത്തി **"Configure"** ("കോൺഫിഗർ ചെയ്യുക") ക്ലിക്ക് ചെയ്യുക.
3.  ആവശ്യത്തിനനുസരിച്ച് *debounce*, ടൈംഔട്ടുകൾ, കാലതാമസങ്ങൾ എന്നിവയ്ക്കുള്ള സ്ലൈഡറുകൾ ക്രമീകരിക്കുക.

## സമയ ക്രമീകരണങ്ങളുടെ വിശദീകരണം

കോൺഫിഗറേഷൻ അല്ലെങ്കിൽ ഓപ്ഷനുകൾ മെനുവിൽ, നിങ്ങൾക്ക് ബ്ലൂടൂത്ത് കമാൻഡുകളുടെ സമയം നന്നായി ക്രമീകരിക്കാൻ കഴിയും. മിക്ക ഉപയോക്താക്കൾക്കും, ഡിഫോൾട്ട് മൂല്യങ്ങൾ നന്നായി പ്രവർത്തിക്കുന്നു.

- **Turn-On Debounce (ഓൺ ചെയ്യാനുള്ള കാലതാമസം):** 'ഓൺ ചെയ്യുക' കമാൻഡ് വീണ്ടും എക്സിക്യൂട്ട് ചെയ്യുന്നതിന് മുമ്പ് കടന്നുപോകേണ്ട ഏറ്റവും കുറഞ്ഞ സമയം (സെക്കൻഡിൽ). സ്വിച്ച് വേഗത്തിൽ ടോഗിൾ ചെയ്യുകയാണെങ്കിൽ വേക്കപ്പ് സിഗ്നലുകൾ ഉപയോഗിച്ച് ഉപകരണത്തിൽ സ്പാം ചെയ്യുന്നത് ഇത് തടയുന്നു.

- **Turn-Off Debounce (ഓഫ് ചെയ്യാനുള്ള കാലതാമസം):** 'ഓഫ് ചെയ്യുക' കമാൻഡ് വീണ്ടും എക്സിക്യൂട്ട് ചെയ്യുന്നതിന് മുമ്പ് കടന്നുപോകേണ്ട ഏറ്റവും കുറഞ്ഞ സമയം (സെക്കൻഡിൽ). 

- **Delay Between Commands (കമാൻഡുകൾക്കിടയിലെ കാലതാമസം):** `bluetoothctl` യൂട്ടിലിറ്റിയിലേക്ക് തുടർച്ചയായ കമാൻഡുകൾ അയയ്ക്കുന്നതിനിടയിലുള്ള വളരെ ചെറിയ കാലതാമസം (സെക്കൻഡിൽ). ചില സിസ്റ്റങ്ങളിൽ, ഒരു ചെറിയ ഇടവേള ചേർക്കുന്നത് വിശ്വാസ്യത മെച്ചപ്പെടുത്താൻ കഴിയും.

- **Process Spawn Timeout (പ്രോസസ്സ് തുടങ്ങാനുള്ള ടൈംഔട്ട്):** `bluetoothctl` പ്രോസസ്സ് ആരംഭിക്കാൻ കാത്തിരിക്കാനുള്ള പരമാവധി സമയം (സെക്കൻഡിൽ). ഈ സമയത്തിനുള്ളിൽ അത് ആരംഭിക്കുന്നതിൽ പരാജയപ്പെട്ടാൽ, ഓൺ ചെയ്യാനുള്ള ശ്രമം പരാജയപ്പെടും.

- **Pairing Timeout (പെയറിംഗ് ടൈംഔട്ട്):** ലളിതമാക്കിയ ടേൺ-ഓൺ ലോജിക്കിൽ, `pair` കമാൻഡ് അയച്ച ശേഷം വിജയിച്ചുവെന്ന് അനുമാനിക്കുന്നതിന് മുമ്പ് കാത്തിരിക്കേണ്ട സമയമാണിത്. വേക്കപ്പ് സിഗ്നൽ പ്രോസസ്സ് ചെയ്യാൻ ഇത് ഉപകരണത്തിന് സമയം നൽകുന്നു.

- **Bluetooth Scan Duration (ബ്ലൂടൂത്ത് സ്കാൻ ദൈർഘ്യം):** പെയർ കമാൻഡ് അയയ്ക്കാൻ ശ്രമിക്കുന്നതിന് മുമ്പ് ഇൻ്റഗ്രേഷൻ ബ്ലൂടൂത്ത് ഉപകരണങ്ങൾക്കായി സ്കാൻ ചെയ്യുന്ന ദൈർഘ്യം (സെക്കൻഡിൽ). ഒരു നീണ്ട സ്കാൻ, തങ്ങളുടെ സാന്നിധ്യം പരസ്യപ്പെടുത്താൻ മന്ദഗതിയിലുള്ള ഉപകരണങ്ങളെ കണ്ടെത്താൻ സഹായിക്കും.

## നിങ്ങളുടെ സ്വന്തം ഭാഷയിൽ വായിക്കുക

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