# MiPower — Home Assistant 사용자 지정 통합

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower**는 기존의 Wake-on-LAN (WOL)을 지원하지 않지만, Bluetooth 페어링 요청을 통해 "깨울" 수 있는 미디어 플레이어의 전원 상태를 제어할 수 있게 해주는 Home Assistant 통합 기능입니다. 이 기능은 Xiaomi Mi Box와 같은 장치를 위해 특별히 설계되었지만, 다른 유사한 Android TV 박스에서도 작동할 수 있습니다.

이 통합은 Home Assistant에 `switch` (스위치) 엔티티를 생성합니다. 
- 스위치를 **켜면** 장치를 깨우기 위해 `bluetoothctl`을 통해 일련의 Bluetooth 명령이 전송됩니다.
- 스위치를 **끄면** 연결된 장치에 대해 `media_player.turn_off` 서비스를 호출합니다.
- 스위치 상태는 연결된 미디어 플레이어 엔티티 상태와 자동으로 동기화됩니다.

## 🤝 후원하기

MiPower 프로젝트는 오픈 소스 커뮤니티에 가치를 더하는 비전으로 개발되고 있습니다. 이 프로젝트의 지속성과 개발 속도를 유지하는 데 귀하의 지원이 매우 중요합니다.

제 노고를 인정해 주신다면, GitHub Sponsors 또는 다음 플랫폼을 통해 저를 지원하실 수 있습니다. 미리 감사드립니다!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

또는 저장소의 오른쪽 상단에 있는 **스폰서 버튼(❤️)**을 클릭하여 모든 후원 옵션을 확인하실 수 있습니다.

## 전제 조건

- **Home Assistant OS / Supervised / Container:** 이 통합은 `bluetoothctl` 명령줄 도구를 사용할 수 있고 액세스할 수 있는 Linux 기반 Home Assistant 설치를 필요로 합니다. Windows의 Home Assistant Core 설치에서는 **작동하지 않습니다**.

## HACS를 통한 설치 (권장)

이 통합은 HACS에서 사용자 지정 저장소로 사용할 수 있습니다.

1.  HACS 대시보드로 이동합니다.
2.  **Integrations** (통합)을 클릭합니다.
3.  오른쪽 상단 모서리에 있는 점 3개 메뉴를 클릭하고 **"Custom repositories"** ("사용자 지정 저장소")를 선택합니다.
4.  대화 상자에 다음 정보를 입력합니다.
    - **Repository (저장소):** `https://github.com/DenizOner/MiPower`
    - **Category (범주):** `Integration` (통합)
5.  **"Add"** ("추가")를 클릭합니다.
6.  "MiPower" 통합이 이제 HACS 목록에 나타납니다. 그것을 클릭합니다.
7.  **"Download"** ("다운로드") 버튼을 클릭한 다음 다음 창에서 다시 **"Download"** ("다운로드")를 클릭합니다.
8.  다운로드가 완료되면 통합을 로드하기 위해 **반드시 Home Assistant를 다시 시작해야 합니다**.

## 수동 설치

HACS가 권장되는 방법이지만, 통합을 수동으로 설치할 수도 있습니다.

1.  저장소의 [릴리스 페이지](https://github.com/DenizOner/MiPower/releases)로 이동하여 최신 릴리스에서 `mipower.zip` 파일을 다운로드합니다.
2.  다운로드한 파일의 압축을 풉니다.
3.  압축이 풀린 폴더 안에 `custom_components` 디렉토리가 있습니다. 그 안에 있는 `mipower` 폴더를 복사합니다.
4.  복사한 `mipower` 폴더를 Home Assistant 구성 디렉토리의 `custom_components` 폴더에 붙여넣습니다. `custom_components` 폴더가 없으면 생성해야 합니다.
    - 최종 경로는 다음과 같아야 합니다: `.../config/custom_components/mipower/`
5.  Home Assistant를 다시 시작합니다.

## 구성

다시 시작한 후 MiPower 스위치를 추가하고 구성할 수 있습니다.

1.  **Settings > Devices & Services** (설정 > 장치 및 서비스)로 이동합니다.
2.  오른쪽 하단 모서리에 있는 **"+ Add Integration"** ("+ 통합 추가") 버튼을 클릭합니다.
3.  **"MiPower"**를 검색하여 클릭합니다.

### 간편 설정 (권장)

이것이 통합을 구성하는 가장 간단한 방법입니다.

1.  요청이 표시되면 **"Easy Setup"** ("간편 설정")을 선택합니다.
2.  통합은 시스템에서 Bluetooth 지원 미디어 플레이어를 자동으로 검색합니다.
3.  드롭다운 목록에서 대상 장치(예: "Xiaomi Mi Box 4")를 선택합니다.
4.  **"Submit"** ("제출")을 클릭합니다.

이게 다입니다! 통합은 미디어 플레이어에 연결된 스위치를 생성합니다.

### 고급 설정

간편 설정이 장치를 찾지 못하거나 처음부터 고급 타이밍 설정을 구성해야 하는 경우 이 방법을 사용합니다.

1.  **1단계: 장치 선택**
    - **"Advanced Setup"** ("고급 설정")을 선택합니다.
    - Home Assistant의 *모든* 미디어 플레이어 목록에서 대상 미디어 플레이어를 선택합니다.
2.  **2단계: MAC 주소**
    - 통합은 선택한 장치의 Bluetooth MAC 주소를 찾으려고 시도합니다. 
    - 찾으면 미리 채워집니다. 올바른지 확인하십시오.
    - 찾을 수 없는 경우 장치의 Bluetooth MAC 주소를 수동으로 입력해야 합니다.
3.  **3단계: 타이밍 설정**
    - Bluetooth 명령에 대한 다양한 시간 초과 및 지연을 구성할 수 있습니다. 대부분의 사용자에게 기본값이 충분합니다.
4.  **"Submit"** ("제출")을 클릭하여 설정을 완료합니다.

## 옵션

MiPower 스위치를 구성한 후 언제든지 타이밍 설정을 조정할 수 있습니다.

1.  **Settings > Devices & Services** (설정 > 장치 및 서비스)로 이동합니다.
2.  MiPower 통합을 찾아 **"Configure"** ("구성")을 클릭합니다.
3.  필요에 따라 *디바운스*, 시간 초과 및 지연 슬라이더를 조정합니다.

## 타이밍 설정 설명

구성 또는 옵션 메뉴에서 Bluetooth 명령의 타이밍을 미세 조정할 수 있습니다. 대부분의 사용자에게 기본값이 잘 작동합니다.

- **Turn-On Debounce (켜기 디바운스):** '켜기' 명령을 다시 실행할 수 있을 때까지 지나야 하는 최소 시간(초). 이는 스위치가 빠르게 토글될 경우 장치가 웨이크업 신호로 스팸되는 것을 방지합니다.

- **Turn-Off Debounce (끄기 디바운스):** '끄기' 명령을 다시 실행할 수 있을 때까지 지나야 하는 최소 시간(초). 

- **Delay Between Commands (명령 간 지연):** `bluetoothctl` 유틸리티에 연속 명령을 보내는 사이의 매우 짧은 지연(초). 일부 시스템에서는 작은 일시 중지를 추가하면 안정성이 향상될 수 있습니다.

- **Process Spawn Timeout (프로세스 생성 시간 초과):** `bluetoothctl` 프로세스가 시작되기를 기다리는 최대 시간(초). 이 시간 내에 시작하지 못하면 켜기 시도는 실패합니다.

- **Pairing Timeout (페어링 시간 초과):** 단순화된 켜기 로직에서, `pair` 명령을 보낸 후 성공으로 간주하기 전에 기다리는 시간입니다. 장치에 웨이크업 신호를 처리할 시간을 제공합니다.

- **Bluetooth Scan Duration (Bluetooth 스캔 기간):** 페어 명령을 보내려고 시도하기 전에 통합이 Bluetooth 장치를 검색할 기간(초). 더 긴 스캔은 존재를 알리는 데 느린 장치를 찾는 데 도움이 될 수 있습니다.

## 귀하의 언어로 읽기

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