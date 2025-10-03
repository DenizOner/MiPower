# MiPower — Home Assistant 自訂整合

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** 是一個 Home Assistant 整合，它允許您控制不支援傳統 Wake-on-LAN (WOL)，但可以透過藍牙配對請求「喚醒」的媒體播放器之電源狀態。它專門為 **小米盒子 (Xiaomi Mi Box)** 等裝置設計，但也可能適用於其他類似的 Android 電視盒。

此整合在 Home Assistant 中建立一個 `switch`（開關）實體。 
- **開啟** 開關會透過 `bluetoothctl` 發送一系列藍牙命令來喚醒裝置。
- **關閉** 開關會為連結的裝置呼叫 `media_player.turn_off` 服務。
- 開關的狀態會自動與連結的媒體播放器實體的狀態同步。

## 🤝 貢獻支持

MiPower 專案的開發願景是為開源社群增加價值。您的支持對於保持該專案的持續性和開發速度至關重要。

如果您讚賞我的工作，可以透過 GitHub Sponsors 或以下平台支持我。提前致謝！

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

或者，您可以點擊儲存庫右上角的 **贊助商按鈕 (❤️)** 來查看所有資助選項。

## 先決條件

- **Home Assistant OS / Supervised / Container:** 此整合需要基於 Linux 的 Home Assistant 安裝，其中 `bluetoothctl` 命令列公用程式可用且可存取。它 **將無法** 在 Windows 上的 Home Assistant Core 安裝中運作。

## 透過 HACS 安裝（建議）

此整合在 HACS 中作為自訂儲存庫提供。

1.  導航到您的 HACS 儀表板。
2.  點擊 **Integrations**（整合）。
3.  點擊右上角的三點選單，選擇 **"Custom repositories"**（“自訂儲存庫”）。
4.  在對話框中，輸入以下資訊：
    - **Repository (儲存庫):** `https://github.com/DenizOner/MiPower`
    - **Category (類別):** `Integration` (整合)
5.  點擊 **"Add"**（“新增”）。
6.  “MiPower” 整合現在將出現在您的 HACS 列表中。點擊它。
7.  點擊 **"Download"**（“下載”）按鈕，然後在下一個視窗中再次點擊 **"Download"**（“下載”）。
8.  下載完成後，**您必須重新啟動 Home Assistant** 才能載入整合。

## 手動安裝

儘管 HACS 是建議的方法，您也可以手動安裝整合。

1.  前往儲存庫的 [Releases page (發佈頁面)](https://github.com/DenizOner/MiPower/releases) 並從最新版本下載 `mipower.zip` 檔案。
2.  解壓縮下載的檔案。
3.  在解壓縮後的資料夾內，您會找到一個 `custom_components` 目錄。複製其中的 `mipower` 資料夾。
4.  將複製的 `mipower` 資料夾貼到您的 Home Assistant 設定目錄中的 `custom_components` 資料夾內。如果 `custom_components` 資料夾不存在，您需要建立它。
    - 最終路徑應如下所示：`.../config/custom_components/mipower/`
5.  重新啟動 Home Assistant。

## 設定

重新啟動後，您可以新增和設定 MiPower 開關。

1.  前往 **Settings > Devices & Services**（設定 > 裝置與服務）。
2.  點擊右下角的 **"+ Add Integration"**（“+ 新增整合”）按鈕。
3.  搜尋 **"MiPower"** 並點擊它。

### 簡易設定（建議）

這是設定整合的最簡單方法。

1.  出現提示時，選擇 **"Easy Setup"**（“簡易設定”）。
2.  整合將自動發現在您系統上啟用藍牙的媒體播放器。
3.  從下拉式清單中選擇您的目標裝置（例如，“Xiaomi Mi Box 4”）。
4.  點擊 **"Submit"**（“提交”）。

就是這樣！整合將建立一個連結到您的媒體播放器的開關。

### 進階設定

如果簡易設定找不到您的裝置，或者您需要從一開始就設定進階計時設定，請使用此方法。

1.  **步驟 1：裝置選擇**
    - 選擇 **"Advanced Setup"**（“進階設定”）。
    - 從 Home Assistant 中 *所有* 媒體播放器的列表中選擇您的目標媒體播放器。
2.  **步驟 2：MAC 位址**
    - 整合將嘗試找到所選裝置的藍牙 MAC 位址。 
    - 如果找到，它將預先填入。請驗證其是否正確。
    - 如果未找到，您必須手動輸入裝置的藍牙 MAC 位址。
3.  **步驟 3：計時設定**
    - 您可以為藍牙命令設定各種超時和延遲。對於大多數使用者，預設值是足夠的。
4.  點擊 **"Submit"**（“提交”）完成設定。

## 選項

設定 MiPower 開關後，您可以隨時調整計時設定。

1.  前往 **Settings > Devices & Services**（設定 > 裝置與服務）。
2.  找到 MiPower 整合並點擊 **"Configure"**（“設定”）。
3.  根據需要調整 *debounce*、超時和延遲的滑桿。

## 計時設定說明

在設定或選項選單中，您可以微調藍牙命令的計時。對於大多數使用者，預設值運作良好。

- **Turn-On Debounce (開啟去抖動):** 必須經過的最小時間（以秒為單位），然後才能再次執行「開啟」命令。如果開關被快速切換，這可以防止裝置被喚醒訊號垃圾郵件。

- **Turn-Off Debounce (關閉去抖動):** 必須經過的最小時間（以秒為單位），然後才能再次執行「關閉」命令。 

- **Delay Between Commands (命令之間的延遲):** 向 `bluetoothctl` 公用程式發送連續命令之間的非常短的延遲（以秒為單位）。在某些系統上，增加一個小暫停可以提高可靠性。

- **Process Spawn Timeout (程序啟動超時):** 等待 `bluetoothctl` 程序啟動的最長時間（以秒為單位）。如果在此時間內啟動失敗，則開啟嘗試將失敗。

- **Pairing Timeout (配對超時):** 在簡化的開啟邏輯中，這是發送 `pair` 命令後，假定成功之前要等待的時間。它為裝置處理喚醒訊號提供了時間。

- **Bluetooth Scan Duration (藍牙掃描持續時間):** 整合在嘗試發送配對命令之前掃描藍牙裝置的持續時間（以秒為單位）。更長的掃描可能助於找到那些緩慢廣播其存在的裝置。

## 閱讀您的語言版本

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