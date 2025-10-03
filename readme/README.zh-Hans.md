# MiPower — Home Assistant 自定义集成

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** 是一个 Home Assistant 集成，它允许您控制不支持传统 Wake-on-LAN (WOL)，但可以通过蓝牙配对请求“唤醒”的媒体播放器的电源状态。它专为 **小米盒子 (Xiaomi Mi Box)** 等设备设计，但也可能适用于其他类似的 Android 电视盒。

此集成在 Home Assistant 中创建一个 `switch`（开关）实体。 
- **开启** 开关会通过 `bluetoothctl` 发送一系列蓝牙命令来唤醒设备。
- **关闭** 开关会为链接的设备调用 `media_player.turn_off` 服务。
- 开关的状态会自动与链接的媒体播放器实体的状态同步。

## 🤝 贡献支持

MiPower 项目的开发愿景是为开源社区增加价值。您的支持对于保持该项目的持续性和开发速度至关重要。

如果您赞赏我的工作，可以通过 GitHub Sponsors 或以下平台支持我。提前致谢！

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

或者，您可以点击仓库右上角的 **赞助商按钮 (❤️)** 来查看所有资助选项。

## 先决条件

- **Home Assistant OS / Supervised / Container:** 此集成需要基于 Linux 的 Home Assistant 安装，其中 `bluetoothctl` 命令行工具可用且可访问。它 **不** 会在 Windows 上的 Home Assistant Core 安装中运行。

## 通过 HACS 安装（推荐）

此集成在 HACS 中作为自定义仓库提供。

1.  导航到您的 HACS 仪表板。
2.  点击 **Integrations**（集成）。
3.  点击右上角的三点菜单，选择 **"Custom repositories"**（“自定义仓库”）。
4.  在对话框中，输入以下信息：
    - **Repository (仓库):** `https://github.com/DenizOner/MiPower`
    - **Category (类别):** `Integration` (集成)
5.  点击 **"Add"**（“添加”）。
6.  “MiPower” 集成现在将出现在您的 HACS 列表中。点击它。
7.  点击 **"Download"**（“下载”）按钮，然后在下一个窗口中再次点击 **"Download"**（“下载”）。
8.  下载完成后，**您必须重新启动 Home Assistant** 才能加载集成。

## 手动安装

虽然 HACS 是推荐的方法，您也可以手动安装集成。

1.  访问仓库的 [Releases page (发布页面)](https://github.com/DenizOner/MiPower/releases) 并从最新版本下载 `mipower.zip` 文件。
2.  解压下载的文件。
3.  在解压后的文件夹内，您会找到一个 `custom_components` 目录。复制其中的 `mipower` 文件夹。
4.  将复制的 `mipower` 文件夹粘贴到您的 Home Assistant 配置目录中的 `custom_components` 文件夹内。如果 `custom_components` 文件夹不存在，您需要创建它。
    - 最终路径应如下所示：`.../config/custom_components/mipower/`
5.  重新启动 Home Assistant。

## 配置

重新启动后，您可以添加和配置 MiPower 开关。

1.  转到 **Settings > Devices & Services**（设置 > 设备与服务）。
2.  点击右下角的 **"+ Add Integration"**（“+ 添加集成”）按钮。
3.  搜索 **"MiPower"** 并点击它。

### 简易设置（推荐）

这是配置集成的最简单方法。

1.  出现提示时，选择 **"Easy Setup"**（“简易设置”）。
2.  集成将自动发现您系统上启用蓝牙的媒体播放器。
3.  从下拉列表中选择您的目标设备（例如，“Xiaomi Mi Box 4”）。
4.  点击 **"Submit"**（“提交”）。

就是这样！集成将创建一个链接到您的媒体播放器的开关。

### 高级设置

如果简易设置找不到您的设备，或者您需要从一开始就配置高级时序设置，请使用此方法。

1.  **步骤 1：设备选择**
    - 选择 **"Advanced Setup"**（“高级设置”）。
    - 从 Home Assistant 中 *所有* 媒体播放器的列表中选择您的目标媒体播放器。
2.  **步骤 2：MAC 地址**
    - 集成将尝试找到所选设备的蓝牙 MAC 地址。 
    - 如果找到，它将预先填写。请验证其是否正确。
    - 如果未找到，您必须手动输入设备的蓝牙 MAC 地址。
3.  **步骤 3：时序设置**
    - 您可以为蓝牙命令配置各种超时和延迟。对于大多数用户，默认值是足够的。
4.  点击 **"Submit"**（“提交”）完成设置。

## 选项

配置 MiPower 开关后，您可以随时调整时序设置。

1.  转到 **Settings > Devices & Services**（设置 > 设备与服务）。
2.  找到 MiPower 集成并点击 **"Configure"**（“配置”）。
3.  根据需要调整 *debounce*、超时和延迟的滑块。

## 时序设置说明

在配置或选项菜单中，您可以微调蓝牙命令的时序。对于大多数用户，默认值工作良好。

- **Turn-On Debounce (开启去抖动):** 必须经过的最小时间（以秒为单位），然后才能再次执行“开启”命令。如果开关被快速切换，这可以防止设备被唤醒信号垃圾邮件。

- **Turn-Off Debounce (关闭去抖动):** 必须经过的最小时间（以秒为单位），然后才能再次执行“关闭”命令。 

- **Delay Between Commands (命令之间的延迟):** 向 `bluetoothctl` 实用程序发送连续命令之间的非常短的延迟（以秒为单位）。在某些系统上，增加一个小暂停可以提高可靠性。

- **Process Spawn Timeout (进程启动超时):** 等待 `bluetoothctl` 进程启动的最长时间（以秒为单位）。如果在此时间内启动失败，则开启尝试将失败。

- **Pairing Timeout (配对超时):** 在简化的开启逻辑中，这是在发送 `pair` 命令后，假定成功之前要等待的时间。它为设备处理唤醒信号提供了时间。

- **Bluetooth Scan Duration (蓝牙扫描持续时间):** 集成在尝试发送配对命令之前扫描蓝牙设备的持续时间（以秒为单位）。更长的扫描可能有助于找到那些缓慢广播其存在的设备。

## 阅读您的语言版本

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