# MiPower — Home Assistant カスタムインテグレーション

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** は、従来の Wake-on-LAN (WOL) をサポートしていないが、Bluetooth ペアリング要求によって「ウェイクアップ」できるメディアプレーヤーの電源状態を制御できるようにする Home Assistant のインテグレーションです。Xiaomi Mi Box のようなデバイス向けに特別に設計されましたが、他の同様の Android TV ボックスでも動作する可能性があります。

このインテグレーションは、Home Assistant に `switch` (スイッチ) エンティティを作成します。 
- スイッチを**ON**にすると、デバイスをウェイクアップするために `bluetoothctl` を介して一連の Bluetooth コマンドが送信されます。
- スイッチを**OFF**にすると、リンクされたデバイスの `media_player.turn_off` サービスが呼び出されます。
- スイッチの状態は、リンクされたメディアプレーヤーエンティティの状態と自動的に同期されます。

## 🤝 支援する

MiPower プロジェクトは、オープンソースコミュニティに価値を加えるというビジョンを持って開発されています。このプロジェクトの継続性と開発速度を維持するために、皆様のサポートが不可欠です。

私の努力を評価していただけるなら、GitHub Sponsors または以下のプラットフォームを通じて私を支援することができます。事前に感謝申し上げます！

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

または、リポジトリの右上隅にある **スポンサーボタン (❤️)** をクリックして、すべての資金調達オプションを確認できます。

## 前提条件

- **Home Assistant OS / Supervised / Container:** このインテグレーションには、`bluetoothctl` コマンドラインツールが利用可能でアクセスできる Linux ベースの Home Assistant インストールが必要です。Windows 上の Home Assistant Core インストールでは**動作しません**。

## HACS 経由でのインストール (推奨)

このインテグレーションは、HACS のカスタムリポジトリとして利用できます。

1.  HACS ダッシュボードに移動します。
2.  **Integrations** (インテグレーション) をクリックします。
3.  右上隅の三点メニューをクリックし、**"Custom repositories"** ("カスタムリポジトリ") を選択します。
4.  ダイアログボックスに、次の情報を入力します。
    - **Repository (リポジトリ):** `https://github.com/DenizOner/MiPower`
    - **Category (カテゴリ):** `Integration` (インテグレーション)
5.  **"Add"** ("追加") をクリックします。
6.  "MiPower" インテグレーションが HACS リストに表示されます。それをクリックします。
7.  **"Download"** ("ダウンロード") ボタンをクリックし、次のウィンドウで再度 **"Download"** ("ダウンロード") をクリックします。
8.  ダウンロードが完了した後、インテグレーションをロードするには**Home Assistant を再起動する必要があります**。

## 手動インストール

HACS が推奨される方法ですが、インテグレーションを手動でインストールすることもできます。

1.  リポジトリの [リリース ページ](https://github.github.com/DenizOner/MiPower/releases) にアクセスし、最新リリースから `mipower.zip` ファイルをダウンロードします。
2.  ダウンロードしたファイルを解凍します。
3.  解凍されたフォルダー内に `custom_components` ディレクトリがあります。その中にある `mipower` フォルダーをコピーします。
4.  コピーした `mipower` フォルダーを、Home Assistant の構成ディレクトリ内の `custom_components` フォルダーに貼り付けます。 `custom_components` フォルダーが存在しない場合は、作成する必要があります。
    - 最終的なパスは次のようになります: `.../config/custom_components/mipower/`
5.  Home Assistant を再起動します。

## 構成

再起動後、MiPower スイッチを追加および構成できます。

1.  **Settings > Devices & Services** (設定 > デバイスとサービス) に移動します。
2.  右下隅にある **"+ Add Integration"** ("+ インテグレーションの追加") ボタンをクリックします。
3.  **"MiPower"** を検索してクリックします。

### 簡単セットアップ (推奨)

これは、インテグレーションを構成する最も簡単な方法です。

1.  プロンプトが表示されたら、**"Easy Setup"** ("簡単セットアップ") を選択します。
2.  インテグレーションは、システム上の Bluetooth 対応メディアプレーヤーを自動的に検出します。
3.  ドロップダウンリストからターゲットデバイス (例: "Xiaomi Mi Box 4") を選択します。
4.  **"Submit"** ("送信") をクリックします。

これで完了です! インテグレーションは、メディアプレーヤーにリンクされたスイッチを作成します。

### 詳細セットアップ

簡単セットアップでデバイスが見つからない場合、または最初から詳細なタイミング設定を構成する必要がある場合は、この方法を使用します。

1.  **ステップ 1: デバイスの選択**
    - **"Advanced Setup"** ("詳細セットアップ") を選択します。
    - Home Assistant 内の *すべて* のメディアプレーヤーのリストからターゲットメディアプレーヤーを選択します。
2.  **ステップ 2: MAC アドレス**
    - インテグレーションは、選択したデバイスの Bluetooth MAC アドレスを見つけようとします。 
    - 見つかった場合、事前に入力されます。それが正しいことを確認してください。
    - 見つからない場合は、デバイスの Bluetooth MAC アドレスを手動で入力する必要があります。
3.  **ステップ 3: タイミング設定**
    - Bluetooth コマンドのさまざまなタイムアウトと遅延を構成できます。ほとんどのユーザーにとって、デフォルト値で十分です。
4.  **"Submit"** ("送信") をクリックして、セットアップを完了します。

## オプション

MiPower スイッチを構成した後、いつでもタイミング設定を調整できます。

1.  **Settings > Devices & Services** (設定 > デバイスとサービス) に移動します。
2.  MiPower インテグレーションを見つけ、**"Configure"** ("構成") をクリックします。
3.  必要に応じて、デバウンス、タイムアウト、遅延のスライダーを調整します。

## タイミング設定の説明

構成またはオプションメニューでは、Bluetooth コマンドのタイミングを微調整できます。ほとんどのユーザーにとって、デフォルト値はうまく機能します。

- **Turn-On Debounce (電源オン時のデバウンス):** '電源オン' コマンドを再度実行できるまでに経過しなければならない最小時間 (秒単位)。これにより、スイッチがすばやく切り替えられた場合に、デバイスがウェイクアップ信号でスパムされるのを防ぎます。

- **Turn-Off Debounce (電源オフ時のデバウンス):** '電源オフ' コマンドを再度実行できるまでに経過しなければならない最小時間 (秒単位)。 

- **Delay Between Commands (コマンド間の遅延):** `bluetoothctl` ユーティリティに連続したコマンドを送信する間の非常に短い遅延 (秒単位)。一部のシステムでは、小さな一時停止を追加すると信頼性が向上する場合があります。

- **Process Spawn Timeout (プロセス生成タイムアウト):** `bluetoothctl` プロセスが開始するのを待つ最大時間 (秒単位)。この時間内に開始できない場合、電源オンの試行は失敗します。

- **Pairing Timeout (ペアリングタイムアウト):** 単純化された電源オンロジックでは、これは `pair` コマンドを送信した後、成功と見なすまでに待機する時間です。デバイスにウェイクアップ信号を処理する時間を与えます。

- **Bluetooth Scan Duration (Bluetooth スキャン期間):** ペアコマンドを送信しようとする前に、インテグレーションが Bluetooth デバイスをスキャンする期間 (秒単位)。スキャン時間が長いと、存在を通知するのが遅いデバイスを見つけるのに役立つ場合があります。

## ご自身の言語で読む

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