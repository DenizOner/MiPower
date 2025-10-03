# MiPower — Integrasi Custom Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** adalah integrasi Home Assistant yang membolehkan anda mengawal status kuasa pemain media yang tidak menyokong Wake-on-LAN (WOL) tradisional tetapi boleh "dikejutkan" oleh permintaan pasangan Bluetooth. Ia direka khas untuk peranti seperti Xiaomi Mi Box, tetapi mungkin berfungsi dengan kotak Android TV serupa yang lain.

Integrasi ini mencipta entiti `switch` (suis) dalam Home Assistant. 
- **MENGHIDUPKAN** suis menghantar satu siri arahan Bluetooth melalui `bluetoothctl` untuk mengejutkan peranti.
- **MEMATIKAN** suis memanggil perkhidmatan `media_player.turn_off` untuk peranti yang dipautkan.
- Status suis disegerakkan secara automatik dengan status entiti pemain media yang dipautkan.

## 🤝 Beri Sokongan

Projek MiPower dibangunkan dengan visi untuk menambah nilai kepada komuniti sumber terbuka. Sokongan anda amat penting untuk mengekalkan kesinambungan dan kelajuan pembangunan projek ini.

Jika anda menghargai usaha saya, anda boleh menyokong saya melalui GitHub Sponsors atau platform berikut. Terima kasih terlebih dahulu!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Sebagai alternatif, anda boleh melihat semua pilihan pembiayaan dengan mengklik **butang Penaja (❤️)** di penjuru kanan atas repositori.

## Pra-syarat

- **Home Assistant OS / Supervised / Container:** Integrasi ini memerlukan pemasangan Home Assistant berasaskan Linux di mana alat baris perintah `bluetoothctl` tersedia dan boleh diakses. Ia **TIDAK** akan berfungsi pada pemasangan Home Assistant Core di Windows.

## Pemasangan Melalui HACS (Disyorkan)

Integrasi ini tersedia sebagai repositori custom dalam HACS.

1.  Navigasi ke Papan Pemuka HACS anda.
2.  Klik pada **Integrations** (Integrasi).
3.  Klik pada menu tiga titik di penjuru kanan atas dan pilih **"Custom repositories"** ("Repositori Custom").
4.  Dalam kotak dialog, masukkan maklumat berikut:
    - **Repository (Repositori):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategori):** `Integration` (Integrasi)
5.  Klik **"Add"** ("Tambah").
6.  Integrasi "MiPower" kini akan muncul dalam senarai HACS anda. Klik padanya.
7.  Klik butang **"Download"** ("Muat Turun") dan kemudian klik **"Download"** ("Muat Turun") sekali lagi dalam tetingkap seterusnya.
8.  Setelah muat turun selesai, **anda MESTI memulakan semula Home Assistant** agar integrasi dimuatkan.

## Pemasangan Manual

Walaupun HACS adalah kaedah yang disyorkan, anda juga boleh memasang integrasi secara manual.

1.  Pergi ke [Halaman Keluaran](https://github.com/DenizOner/MiPower/releases) repositori dan muat turun fail `mipower.zip` dari keluaran terkini.
2.  Nyahzip (unzip) fail yang dimuat turun.
3.  Di dalam folder yang dinyahzip, anda akan menemui direktori `custom_components`. Salin folder `mipower` daripadanya.
4.  Tampal folder `mipower` yang disalin ke dalam folder `custom_components` dalam direktori konfigurasi Home Assistant anda. Sekiranya folder `custom_components` tidak wujud, anda perlu menciptanya.
    - Laluan akhir harus kelihatan seperti: `.../config/custom_components/mipower/`
5.  Mulakan semula Home Assistant.

## Konfigurasi

Selepas dimulakan semula, anda boleh menambah dan mengkonfigurasi suis MiPower.

1.  Pergi ke **Settings > Devices & Services** (Tetapan > Peranti & Perkhidmatan).
2.  Klik butang **"+ Add Integration"** ("+ Tambah Integrasi") di penjuru kanan bawah.
3.  Cari **"MiPower"** dan klik padanya.

### Persediaan Mudah (Disyorkan)

Ini adalah cara termudah untuk mengkonfigurasi integrasi.

1.  Apabila diminta, pilih **"Easy Setup"** ("Persediaan Mudah").
2.  Integrasi secara automatik akan menemui pemain media yang didayakan Bluetooth pada sistem anda.
3.  Pilih peranti sasaran anda (cth., "Xiaomi Mi Box 4") dari senarai juntai bawah.
4.  Klik **"Submit"** ("Hantar").

Itu sahaja! Integrasi akan mencipta suis yang dipautkan ke pemain media anda.

### Persediaan Lanjutan

Gunakan kaedah ini jika Persediaan Mudah tidak menemui peranti anda atau jika anda perlu mengkonfigurasi tetapan masa lanjutan dari awal.

1.  **Langkah 1: Pemilihan Peranti**
    - Pilih **"Advanced Setup"** ("Persediaan Lanjutan").
    - Pilih pemain media sasaran anda dari senarai *semua* pemain media dalam Home Assistant anda.
2.  **Langkah 2: Alamat MAC**
    - Integrasi akan cuba mencari Alamat MAC Bluetooth peranti yang dipilih. 
    - Sekiranya ditemui, ia akan dipraisi. Sahkan bahawa ia betul.
    - Sekiranya tidak ditemui, anda mesti memasukkan Alamat MAC Bluetooth peranti anda secara manual.
3.  **Langkah 3: Tetapan Masa**
    - Anda boleh mengkonfigurasi pelbagai tamat masa (timeouts) dan kelewatan untuk arahan Bluetooth. Bagi kebanyakan pengguna, nilai lalai sudah mencukupi.
4.  Klik **"Submit"** ("Hantar") untuk menyelesaikan persediaan.

## Pilihan

Setelah anda mengkonfigurasi suis MiPower anda, anda boleh menyesuaikan tetapan masa pada bila-bila masa.

1.  Pergi ke **Settings > Devices & Services** (Tetapan > Peranti & Perkhidmatan).
2.  Cari integrasi MiPower dan klik **"Configure"** ("Konfigurasi").
3.  Laraskan peluncur untuk *debounce*, tamat masa, dan kelewatan mengikut keperluan.

## Penjelasan Tetapan Masa

Dalam menu konfigurasi atau pilihan, anda boleh menyelaraskan masa arahan Bluetooth. Bagi kebanyakan pengguna, nilai lalai berfungsi dengan baik.

- **Turn-On Debounce (Debounce Hidupkan):** Masa minimum (dalam saat) yang mesti berlalu sebelum arahan 'hidupkan' boleh dilaksanakan lagi. Ini menghalang spamming peranti dengan isyarat kejutkan jika suis dialihkan dengan pantas.

- **Turn-Off Debounce (Debounce Matikan):** Masa minimum (dalam saat) yang mesti berlalu sebelum arahan 'matikan' boleh dilaksanakan lagi. 

- **Delay Between Commands (Kelewatan Antara Arahan):** Kelewatan yang sangat pendek (dalam saat) antara penghantaran arahan berturut-turut kepada utiliti `bluetoothctl`. Pada sesetengah sistem, menambahkan jeda kecil boleh meningkatkan kebolehpercayaan.

- **Process Spawn Timeout (Tamat Masa Pemunculan Proses):** Masa maksimum (dalam saat) untuk menunggu proses `bluetoothctl` bermula. Jika ia gagal bermula dalam masa ini, percubaan menghidupkan akan gagal.

- **Pairing Timeout (Tamat Masa Berpasangan):** Dalam logik menghidupkan yang dipermudah, ini adalah jumlah masa untuk menunggu selepas menghantar arahan `pair` sebelum menganggap kejayaan. Ia memberi masa kepada peranti untuk memproses isyarat kejutkan.

- **Bluetooth Scan Duration (Tempoh Imbasan Bluetooth):** Tempoh (dalam saat) integrasi akan mengimbas peranti Bluetooth sebelum cuba menghantar arahan pasangan. Imbasan yang lebih lama dapat membantu mencari peranti yang lambat untuk mengiklankan kehadiran mereka.

## Baca dalam bahasa anda sendiri

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