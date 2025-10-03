# MiPower — Integrasi Kustom Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** adalah integrasi Home Assistant yang memungkinkan Anda mengontrol status daya pemutar media yang tidak mendukung Wake-on-LAN (WOL) tradisional, tetapi dapat "dibangunkan" dengan permintaan pemasangan Bluetooth. Ini dirancang khusus untuk perangkat seperti Xiaomi Mi Box, tetapi dapat bekerja dengan kotak Android TV serupa lainnya.

Integrasi ini membuat entitas `switch` (sakelar) di Home Assistant. 
- **Menghidupkan** sakelar mengirimkan serangkaian perintah Bluetooth melalui `bluetoothctl` untuk membangunkan perangkat.
- **Mematikan** sakelar memanggil layanan `media_player.turn_off` untuk perangkat yang ditautkan.
- Status sakelar secara otomatis disinkronkan dengan status entitas pemutar media yang ditautkan.

## 🤝 Dukung Kami

Proyek MiPower dikembangkan dengan visi untuk menambah nilai bagi komunitas sumber terbuka. Dukungan Anda sangat penting untuk menjaga kesinambungan dan kecepatan pengembangan proyek ini.

Jika Anda menghargai upaya saya, Anda dapat mendukung saya melalui GitHub Sponsors atau platform berikut. Terima kasih sebelumnya!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Sebagai alternatif, Anda dapat melihat semua opsi pendanaan dengan mengklik **tombol Sponsor (❤️)** di sudut kanan atas repositori.

## Prasyarat

- **Home Assistant OS / Supervised / Container:** Integrasi ini membutuhkan instalasi Home Assistant berbasis Linux di mana alat baris perintah `bluetoothctl` tersedia dan dapat diakses. Ini **tidak** akan berfungsi pada instalasi Home Assistant Core di Windows.

## Instalasi melalui HACS (Direkomendasikan)

Integrasi ini tersedia sebagai repositori kustom di HACS.

1.  Navigasi ke dasbor HACS Anda.
2.  Klik **Integrations** (Integrasi).
3.  Klik menu tiga titik di sudut kanan atas dan pilih **"Custom repositories"** ("Repositori Kustom").
4.  Dalam kotak dialog, masukkan informasi berikut:
    - **Repository (Repositori):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategori):** `Integration` (Integrasi)
5.  Klik **"Add"** ("Tambah").
6.  Integrasi "MiPower" sekarang akan muncul di daftar HACS Anda. Klik di atasnya.
7.  Klik tombol **"Download"** ("Unduh") dan kemudian klik **"Download"** ("Unduh") lagi di jendela berikutnya.
8.  Setelah unduhan selesai, **Anda harus me-restart Home Assistant** agar integrasi dimuat.

## Instalasi Manual

Meskipun HACS adalah metode yang direkomendasikan, Anda juga dapat menginstal integrasi secara manual.

1.  Buka [Halaman Rilis](https://github.com/DenizOner/MiPower/releases) repositori dan unduh file `mipower.zip` dari rilis terbaru.
2.  Ekstrak file yang diunduh.
3.  Di dalam folder yang diekstrak, Anda akan menemukan direktori `custom_components`. Salin folder `mipower` dari dalamnya.
4.  Tempel folder `mipower` yang disalin ke dalam folder `custom_components` di direktori konfigurasi Home Assistant Anda. Jika folder `custom_components` tidak ada, Anda harus membuatnya.
    - Jalur akhir akan terlihat seperti ini: `.../config/custom_components/mipower/`
5.  Restart Home Assistant.

## Konfigurasi

Setelah restart, Anda dapat menambahkan dan mengkonfigurasi sakelar MiPower.

1.  Buka **Settings > Devices & Services** (Pengaturan > Perangkat & Layanan).
2.  Klik tombol **"+ Add Integration"** ("+ Tambah Integrasi") di sudut kanan bawah.
3.  Cari **"MiPower"** dan klik di atasnya.

### Pengaturan Mudah (Direkomendasikan)

Ini adalah cara paling sederhana untuk mengkonfigurasi integrasi.

1.  Ketika diminta, pilih **"Easy Setup"** ("Pengaturan Mudah").
2.  Integrasi akan secara otomatis menemukan pemutar media berkemampuan Bluetooth di sistem Anda.
3.  Pilih perangkat target Anda (misalnya, "Xiaomi Mi Box 4") dari daftar tarik-turun.
4.  Klik **"Submit"** ("Kirim").

Itu saja! Integrasi akan membuat sakelar yang ditautkan ke pemutar media Anda.

### Pengaturan Lanjutan

Gunakan metode ini jika Pengaturan Mudah tidak menemukan perangkat Anda atau jika Anda perlu mengkonfigurasi pengaturan waktu lanjutan dari awal.

1.  **Langkah 1: Pemilihan Perangkat**
    - Pilih **"Advanced Setup"** ("Pengaturan Lanjutan").
    - Pilih pemutar media target Anda dari daftar *semua* pemutar media di Home Assistant Anda.
2.  **Langkah 2: Alamat MAC**
    - Integrasi akan mencoba menemukan Alamat MAC Bluetooth dari perangkat yang dipilih. 
    - Jika ditemukan, itu akan diisi sebelumnya. Verifikasi bahwa itu benar.
    - Jika tidak ditemukan, Anda harus memasukkan Alamat MAC Bluetooth perangkat Anda secara manual.
3.  **Langkah 3: Pengaturan Waktu**
    - Anda dapat mengkonfigurasi berbagai batas waktu (*timeouts*) dan penundaan untuk perintah Bluetooth. Untuk sebagian besar pengguna, nilai default sudah cukup.
4.  Klik **"Submit"** ("Kirim") untuk menyelesaikan pengaturan.

## Opsi

Setelah Anda mengkonfigurasi sakelar MiPower Anda, Anda dapat menyesuaikan pengaturan waktu kapan saja.

1.  Buka **Settings > Devices & Services** (Pengaturan > Perangkat & Layanan).
2.  Temukan integrasi MiPower dan klik **"Configure"** ("Konfigurasi").
3.  Sesuaikan slider untuk *debounce*, batas waktu, dan penundaan sesuai kebutuhan.

## Penjelasan Pengaturan Waktu

Di menu konfigurasi atau opsi, Anda dapat menyempurnakan pengaturan waktu perintah Bluetooth. Untuk sebagian besar pengguna, nilai default bekerja dengan baik.

- **Turn-On Debounce (Debounce Menghidupkan):** Waktu minimum (dalam detik) yang harus berlalu sebelum perintah 'hidupkan' dapat dieksekusi lagi. Ini mencegah perangkat dibanjiri sinyal bangun jika sakelar dihidupkan/dimatikan dengan cepat.

- **Turn-Off Debounce (Debounce Mematikan):** Waktu minimum (dalam detik) yang harus berlalu sebelum perintah 'matikan' dapat dieksekusi lagi. 

- **Delay Between Commands (Penundaan Antar Perintah):** Penundaan yang sangat singkat (dalam detik) antara pengiriman perintah berturut-turut ke utilitas `bluetoothctl`. Pada beberapa sistem, menambahkan jeda kecil dapat meningkatkan keandalan.

- **Process Spawn Timeout (Batas Waktu Pembuatan Proses):** Waktu maksimum (dalam detik) untuk menunggu proses `bluetoothctl` dimulai. Jika gagal dimulai dalam waktu ini, upaya menghidupkan akan gagal.

- **Pairing Timeout (Batas Waktu Pemasangan):** Dalam logika menghidupkan yang disederhanakan, ini adalah jumlah waktu untuk menunggu setelah mengirim perintah `pair` sebelum mengasumsikan keberhasilan. Ini memberi perangkat waktu untuk memproses sinyal bangun.

- **Bluetooth Scan Duration (Durasi Pemindaian Bluetooth):** Durasi (dalam detik) di mana integrasi akan memindai perangkat Bluetooth sebelum mencoba mengirim perintah pemasangan. Pemindaian yang lebih lama dapat membantu menemukan perangkat yang lambat untuk mengiklankan keberadaan mereka.

## Baca dalam bahasa Anda sendiri

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