# MiPower — การรวม Home Assistant แบบกำหนดเอง

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** คือการรวม Home Assistant ที่ช่วยให้คุณสามารถควบคุมสถานะพลังงานของเครื่องเล่นมีเดียที่ไม่รองรับ Wake-on-LAN (WOL) แบบดั้งเดิม แต่สามารถ "ปลุก" ได้ด้วยคำขอจับคู่ Bluetooth ได้ รับการออกแบบมาโดยเฉพาะสำหรับอุปกรณ์อย่าง Xiaomi Mi Box แต่อาจใช้งานได้กับกล่อง Android TV อื่นๆ ที่คล้ายกัน

การรวมนี้จะสร้างเอนทิตี `switch` (สวิตช์) ใน Home Assistant 
- การ **เปิด** สวิตช์จะส่งชุดคำสั่ง Bluetooth ผ่าน `bluetoothctl` เพื่อปลุกอุปกรณ์
- การ **ปิด** สวิตช์จะเรียกใช้บริการ `media_player.turn_off` สำหรับอุปกรณ์ที่เชื่อมโยง
- สถานะของสวิตช์จะถูกซิงโครไนซ์โดยอัตโนมัติกับสถานะของเอนทิตีเครื่องเล่นมีเดียที่เชื่อมโยง

## 🤝 สนับสนุน

โครงการ MiPower ได้รับการพัฒนาด้วยวิสัยทัศน์ที่จะเพิ่มคุณค่าให้กับชุมชนโอเพนซอร์ส การสนับสนุนของคุณมีความสำคัญอย่างยิ่งต่อการรักษาความต่อเนื่องและความเร็วในการพัฒนาของโครงการนี้

หากคุณชื่นชมความพยายามของฉัน คุณสามารถสนับสนุนฉันผ่าน GitHub Sponsors หรือแพลตฟอร์มต่อไปนี้ ขอขอบคุณล่วงหน้า!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

หรือคุณสามารถดูตัวเลือกการระดมทุนทั้งหมดได้โดยคลิกที่ **ปุ่มผู้สนับสนุน (❤️)** ที่มุมขวาบนของพื้นที่เก็บข้อมูล

## ข้อกำหนดเบื้องต้น

- **Home Assistant OS / Supervised / Container:** การรวมนี้ต้องการการติดตั้ง Home Assistant ที่ใช้ Linux ซึ่งเครื่องมือบรรทัดคำสั่ง `bluetoothctl` พร้อมใช้งานและเข้าถึงได้ จะ **ไม่** ทำงานในการติดตั้ง Home Assistant Core บน Windows

## การติดตั้งผ่าน HACS (แนะนำ)

การรวมนี้มีให้เป็นพื้นที่เก็บข้อมูลที่กำหนดเอง (custom repository) ใน HACS

1.  นำทางไปยังแดชบอร์ด HACS ของคุณ
2.  คลิกที่ **Integrations** (การรวม)
3.  คลิกที่เมนูสามจุดที่มุมขวาบนและเลือก **"Custom repositories"** ("พื้นที่เก็บข้อมูลที่กำหนดเอง")
4.  ในกล่องโต้ตอบ ให้ป้อนข้อมูลต่อไปนี้:
    - **Repository (พื้นที่เก็บข้อมูล):** `https://github.com/DenizOner/MiPower`
    - **Category (หมวดหมู่):** `Integration` (การรวม)
5.  คลิก **"Add"** ("เพิ่ม")
6.  การรวม "MiPower" จะปรากฏในรายการ HACS ของคุณแล้ว คลิกที่มัน
7.  คลิกปุ่ม **"Download"** ("ดาวน์โหลด") จากนั้นคลิก **"Download"** ("ดาวน์โหลด") อีกครั้งในหน้าต่างถัดไป
8.  หลังจากดาวน์โหลดเสร็จสิ้น **คุณต้องรีสตาร์ท Home Assistant** เพื่อโหลดการรวม

## การติดตั้งด้วยตนเอง

แม้ว่า HACS จะเป็นวิธีที่แนะนำ แต่คุณก็สามารถติดตั้งการรวมด้วยตนเองได้

1.  ไปที่ [หน้าการเผยแพร่ (Releases page)](https://github.com/DenizOner/MiPower/releases) ของพื้นที่เก็บข้อมูล และดาวน์โหลดไฟล์ `mipower.zip` จากการเผยแพร่ล่าสุด
2.  แตกไฟล์ที่ดาวน์โหลดมา
3.  ภายในโฟลเดอร์ที่แตกไฟล์ คุณจะพบไดเร็กทอรี `custom_components` คัดลอกโฟลเดอร์ `mipower` จากภายใน
4.  วางโฟลเดอร์ `mipower` ที่คัดลอกไว้ในโฟลเดอร์ `custom_components` ในไดเร็กทอรีการกำหนดค่า Home Assistant ของคุณ หากโฟลเดอร์ `custom_components` ไม่มีอยู่ คุณจะต้องสร้างมัน
    - เส้นทางสุดท้ายควรมีลักษณะดังนี้: `.../config/custom_components/mipower/`
5.  รีสตาร์ท Home Assistant

## การกำหนดค่า

หลังจากรีสตาร์ท คุณสามารถเพิ่มและกำหนดค่าสวิตช์ MiPower ได้

1.  ไปที่ **Settings > Devices & Services** (การตั้งค่า > อุปกรณ์และบริการ)
2.  คลิกปุ่ม **"+ Add Integration"** ("+ เพิ่มการรวม") ที่มุมล่างขวา
3.  ค้นหา **"MiPower"** และคลิกที่มัน

### การตั้งค่าแบบง่าย (แนะนำ)

นี่เป็นวิธีที่ง่ายที่สุดในการกำหนดค่าการรวม

1.  เมื่อได้รับแจ้ง ให้เลือก **"Easy Setup"** ("การตั้งค่าแบบง่าย")
2.  การรวมจะค้นพบเครื่องเล่นมีเดียที่เปิดใช้งาน Bluetooth บนระบบของคุณโดยอัตโนมัติ
3.  เลือกอุปกรณ์เป้าหมายของคุณ (เช่น "Xiaomi Mi Box 4") จากรายการดรอปดาวน์
4.  คลิก **"Submit"** ("ส่ง")

แค่นั้นแหละ! การรวมจะสร้างสวิตช์ที่เชื่อมโยงกับเครื่องเล่นมีเดียของคุณ

### การตั้งค่าขั้นสูง

ใช้วิธีนี้หากการตั้งค่าแบบง่ายไม่พบอุปกรณ์ของคุณ หรือหากคุณต้องการกำหนดค่าการตั้งค่าเวลาขั้นสูงตั้งแต่เริ่มต้น

1.  **ขั้นตอนที่ 1: การเลือกอุปกรณ์**
    - เลือก **"Advanced Setup"** ("การตั้งค่าขั้นสูง")
    - เลือกเครื่องเล่นมีเดียเป้าหมายของคุณจากรายการ *ทั้งหมด* ของเครื่องเล่นมีเดียใน Home Assistant ของคุณ
2.  **ขั้นตอนที่ 2: ที่อยู่ MAC**
    - การรวมจะพยายามค้นหาที่อยู่ Bluetooth MAC ของอุปกรณ์ที่เลือก 
    - หากพบ จะมีการกรอกไว้ล่วงหน้า ตรวจสอบว่าเป็นข้อมูลที่ถูกต้อง
    - หากไม่พบ คุณต้องป้อนที่อยู่ Bluetooth MAC ของอุปกรณ์ของคุณด้วยตนเอง
3.  **ขั้นตอนที่ 3: การตั้งค่าเวลา**
    - คุณสามารถกำหนดค่าการหมดเวลา (timeouts) และความล่าช้าต่างๆ สำหรับคำสั่ง Bluetooth ได้ สำหรับผู้ใช้ส่วนใหญ่ ค่าเริ่มต้นก็เพียงพอแล้ว
4.  คลิก **"Submit"** ("ส่ง") เพื่อเสร็จสิ้นการตั้งค่า

## ตัวเลือก

หลังจากที่คุณกำหนดค่าสวิตช์ MiPower แล้ว คุณสามารถปรับการตั้งค่าเวลาได้ตลอดเวลา

1.  ไปที่ **Settings > Devices & Services** (การตั้งค่า > อุปกรณ์และบริการ)
2.  ค้นหาการรวม MiPower และคลิก **"Configure"** ("กำหนดค่า")
3.  ปรับแถบเลื่อนสำหรับ *debounce*, การหมดเวลา และความล่าช้าตามความจำเป็น

## คำอธิบายการตั้งค่าเวลา

ในเมนูการกำหนดค่าหรือตัวเลือก คุณสามารถปรับเวลาของคำสั่ง Bluetooth ได้อย่างละเอียด สำหรับผู้ใช้ส่วนใหญ่ ค่าเริ่มต้นจะทำงานได้ดี

- **Turn-On Debounce (การดีบาวซ์การเปิด):** เวลาขั้นต่ำ (เป็นวินาที) ที่ต้องผ่านก่อนที่คำสั่ง 'เปิด' จะสามารถดำเนินการได้อีกครั้ง เพื่อป้องกันการสแปมอุปกรณ์ด้วยสัญญาณปลุกหากสวิตช์ถูกสลับอย่างรวดเร็ว

- **Turn-Off Debounce (การดีบาวซ์การปิด):** เวลาขั้นต่ำ (เป็นวินาที) ที่ต้องผ่านก่อนที่คำสั่ง 'ปิด' จะสามารถดำเนินการได้อีกครั้ง 

- **Delay Between Commands (ความล่าช้าระหว่างคำสั่ง):** ความล่าช้าสั้นมาก (เป็นวินาที) ระหว่างการส่งคำสั่งต่อเนื่องไปยังเครื่องมือ `bluetoothctl` ในบางระบบ การเพิ่มการหยุดชั่วคราวเล็กน้อยสามารถปรับปรุงความน่าเชื่อถือได้

- **Process Spawn Timeout (การหมดเวลาการสร้างกระบวนการ):** เวลาสูงสุด (เป็นวินาที) ที่จะรอให้กระบวนการ `bluetoothctl` เริ่มต้น หากไม่สามารถเริ่มต้นภายในเวลานี้ ความพยายามในการเปิดจะล้มเหลว

- **Pairing Timeout (การหมดเวลาการจับคู่):** ในตรรกะการเปิดแบบง่าย นี่คือระยะเวลาที่จะรอหลังจากส่งคำสั่ง `pair` ก่อนที่จะถือว่าสำเร็จ ซึ่งจะทำให้อุปกรณ์มีเวลาประมวลผลสัญญาณปลุก

- **Bluetooth Scan Duration (ระยะเวลาการสแกน Bluetooth):** ระยะเวลา (เป็นวินาที) ที่การรวมจะสแกนหาอุปกรณ์ Bluetooth ก่อนที่จะพยายามส่งคำสั่งจับคู่ การสแกนที่นานขึ้นสามารถช่วยค้นหาอุปกรณ์ที่โฆษณาตนเองช้าได้

## อ่านในภาษาของคุณเอง

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