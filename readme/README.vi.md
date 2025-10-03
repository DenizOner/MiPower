# MiPower — Tích hợp tùy chỉnh Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** là một tích hợp của Home Assistant cho phép bạn kiểm soát trạng thái nguồn của các trình phát media không hỗ trợ Wake-on-LAN (WOL) truyền thống nhưng có thể được "đánh thức" bằng yêu cầu ghép nối Bluetooth. Nó được thiết kế đặc biệt cho các thiết bị như Xiaomi Mi Box, nhưng có thể hoạt động với các hộp Android TV tương tự khác.

Tích hợp này tạo một thực thể `switch` (công tắc) trong Home Assistant. 
- **Bật** công tắc sẽ gửi một loạt các lệnh Bluetooth thông qua `bluetoothctl` để đánh thức thiết bị.
- **Tắt** công tắc sẽ gọi dịch vụ `media_player.turn_off` cho thiết bị được liên kết.
- Trạng thái của công tắc được tự động đồng bộ hóa với trạng thái của thực thể trình phát media được liên kết.

## 🤝 Ủng hộ

Dự án MiPower được phát triển với tầm nhìn tăng thêm giá trị cho cộng đồng mã nguồn mở. Sự ủng hộ của bạn là rất quan trọng để duy trì tính liên tục và tốc độ phát triển của dự án này.

Nếu bạn đánh giá cao nỗ lực của tôi, bạn có thể ủng hộ tôi thông qua GitHub Sponsors hoặc các nền tảng sau. Xin cảm ơn trước!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Ngoài ra, bạn có thể xem tất cả các tùy chọn tài trợ bằng cách nhấp vào **nút Nhà tài trợ (❤️)** ở góc trên bên phải của kho lưu trữ.

## Điều kiện tiên quyết

- **Home Assistant OS / Supervised / Container:** Tích hợp này yêu cầu cài đặt Home Assistant dựa trên Linux, nơi tiện ích dòng lệnh `bluetoothctl` khả dụng và có thể truy cập. Nó **SẼ KHÔNG** hoạt động trên bản cài đặt Home Assistant Core trên Windows.

## Cài đặt qua HACS (Khuyến nghị)

Tích hợp này có sẵn dưới dạng kho lưu trữ tùy chỉnh trong HACS.

1.  Điều hướng đến bảng điều khiển HACS của bạn.
2.  Nhấp vào **Integrations** (Tích hợp).
3.  Nhấp vào menu ba chấm ở góc trên bên phải và chọn **"Custom repositories"** ("Kho lưu trữ tùy chỉnh").
4.  Trong hộp thoại, nhập thông tin sau:
    - **Repository (Kho lưu trữ):** `https://github.com/DenizOner/MiPower`
    - **Category (Danh mục):** `Integration` (Tích hợp)
5.  Nhấp vào **"Add"** ("Thêm").
6.  Tích hợp "MiPower" hiện sẽ xuất hiện trong danh sách HACS của bạn. Nhấp vào nó.
7.  Nhấp vào nút **"Download"** ("Tải xuống"), sau đó nhấp lại vào **"Download"** ("Tải xuống") trong cửa sổ tiếp theo.
8.  Sau khi quá trình tải xuống hoàn tất, **bạn PHẢI khởi động lại Home Assistant** để tích hợp được tải.

## Cài đặt thủ công

Mặc dù HACS là phương pháp được khuyến nghị, bạn cũng có thể cài đặt tích hợp theo cách thủ công.

1.  Truy cập [trang Phát hành (Releases page)](https://github.com/DenizOner/MiPower/releases) của kho lưu trữ và tải xuống tệp `mipower.zip` từ bản phát hành mới nhất.
2.  Giải nén tệp đã tải xuống.
3.  Bên trong thư mục đã giải nén, bạn sẽ tìm thấy thư mục `custom_components`. Sao chép thư mục `mipower` từ bên trong nó.
4.  Dán thư mục `mipower` đã sao chép vào thư mục `custom_components` trong thư mục cấu hình Home Assistant của bạn. Nếu thư mục `custom_components` không tồn tại, bạn cần tạo nó.
    - Đường dẫn cuối cùng sẽ trông như thế này: `.../config/custom_components/mipower/`
5.  Khởi động lại Home Assistant.

## Cấu hình

Sau khi khởi động lại, bạn có thể thêm và cấu hình công tắc MiPower.

1.  Truy cập **Settings > Devices & Services** (Cài đặt > Thiết bị & Dịch vụ).
2.  Nhấp vào nút **"+ Add Integration"** ("+ Thêm Tích hợp") ở góc dưới bên phải.
3.  Tìm kiếm **"MiPower"** và nhấp vào nó.

### Thiết lập dễ dàng (Khuyến nghị)

Đây là cách đơn giản nhất để cấu hình tích hợp.

1.  Khi được nhắc, hãy chọn **"Easy Setup"** ("Thiết lập dễ dàng").
2.  Tích hợp sẽ tự động phát hiện các trình phát media được bật Bluetooth trên hệ thống của bạn.
3.  Chọn thiết bị mục tiêu của bạn (ví dụ: "Xiaomi Mi Box 4") từ danh sách thả xuống.
4.  Nhấp vào **"Submit"** ("Gửi").

Vậy là xong! Tích hợp sẽ tạo ra một công tắc được liên kết với trình phát media của bạn.

### Thiết lập nâng cao

Sử dụng phương pháp này nếu Thiết lập dễ dàng không tìm thấy thiết bị của bạn hoặc nếu bạn cần cấu hình các cài đặt thời gian nâng cao ngay từ đầu.

1.  **Bước 1: Chọn thiết bị**
    - Chọn **"Advanced Setup"** ("Thiết lập nâng cao").
    - Chọn trình phát media mục tiêu của bạn từ danh sách *tất cả* các trình phát media trong Home Assistant của bạn.
2.  **Bước 2: Địa chỉ MAC**
    - Tích hợp sẽ cố gắng tìm Địa chỉ MAC Bluetooth của thiết bị đã chọn. 
    - Nếu tìm thấy, nó sẽ được điền sẵn. Xác minh rằng nó là chính xác.
    - Nếu không tìm thấy, bạn phải nhập thủ công Địa chỉ MAC Bluetooth của thiết bị của mình.
3.  **Bước 3: Cài đặt thời gian**
    - Bạn có thể cấu hình các khoảng thời gian chờ (timeouts) và độ trễ khác nhau cho các lệnh Bluetooth. Đối với hầu hết người dùng, các giá trị mặc định là đủ.
4.  Nhấp vào **"Submit"** ("Gửi") để hoàn tất thiết lập.

## Tùy chọn

Sau khi bạn cấu hình công tắc MiPower của mình, bạn có thể điều chỉnh các cài đặt thời gian bất cứ lúc nào.

1.  Truy cập **Settings > Devices & Services** (Cài đặt > Thiết bị & Dịch vụ).
2.  Tìm tích hợp MiPower và nhấp vào **"Configure"** ("Cấu hình").
3.  Điều chỉnh các thanh trượt cho *debounce*, thời gian chờ và độ trễ khi cần.

## Giải thích về Cài đặt thời gian

Trong menu cấu hình hoặc tùy chọn, bạn có thể tinh chỉnh thời gian của các lệnh Bluetooth. Đối với hầu hết người dùng, các giá trị mặc định hoạt động tốt.

- **Turn-On Debounce (Khử nhiễu khi Bật):** Thời gian tối thiểu (bằng giây) phải trôi qua trước khi lệnh 'bật' có thể được thực thi lại. Điều này ngăn chặn việc spam thiết bị bằng tín hiệu đánh thức nếu công tắc được chuyển đổi nhanh chóng.

- **Turn-Off Debounce (Khử nhiễu khi Tắt):** Thời gian tối thiểu (bằng giây) phải trôi qua trước khi lệnh 'tắt' có thể được thực thi lại. 

- **Delay Between Commands (Độ trễ giữa các Lệnh):** Một độ trễ rất ngắn (bằng giây) giữa việc gửi các lệnh liên tiếp đến tiện ích `bluetoothctl`. Trên một số hệ thống, việc thêm một khoảng dừng nhỏ có thể cải thiện độ tin cậy.

- **Process Spawn Timeout (Thời gian chờ Khởi tạo Tiến trình):** Thời gian tối đa (bằng giây) để chờ tiến trình `bluetoothctl` bắt đầu. Nếu nó không thể bắt đầu trong thời gian này, nỗ lực bật sẽ thất bại.

- **Pairing Timeout (Thời gian chờ Ghép nối):** Trong logic bật đơn giản hóa, đây là khoảng thời gian chờ sau khi gửi lệnh `pair` trước khi giả định thành công. Nó cho thiết bị thời gian xử lý tín hiệu đánh thức.

- **Bluetooth Scan Duration (Thời lượng Quét Bluetooth):** Thời lượng (bằng giây) mà tích hợp sẽ quét các thiết bị Bluetooth trước khi cố gắng gửi lệnh ghép nối. Quét lâu hơn có thể giúp tìm thấy các thiết bị chậm quảng cáo sự hiện diện của chúng.

## Đọc bằng ngôn ngữ của riêng bạn

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