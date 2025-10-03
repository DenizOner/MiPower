# MiPower — Vlastní integrace Home Assistanta

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** je integrace pro Home Assistant, která vám umožňuje ovládat stav napájení mediálních přehrávačů, které nepodporují tradiční Wake-on-LAN (WOL), ale mohou být "probuzeny" požadavkem na spárování přes Bluetooth. Byla navržena speciálně pro zařízení jako Xiaomi Mi Box, ale může fungovat i s jinými podobnými Android TV boxy.

Tato integrace vytvoří entitu typu `switch` (přepínač) v Home Assistantu. 
- **Zapnutí** přepínače odešle sérii Bluetooth příkazů přes `bluetoothctl` k probuzení zařízení.
- **Vypnutí** přepínače zavolá službu `media_player.turn_off` pro propojené zařízení.
- Stav přepínače se automaticky synchronizuje se stavem propojené entity mediálního přehrávače.

## 🤝 Podpořte Nás

Projekt MiPower je vyvíjen s vizí přidávat hodnotu komunitě s otevřeným zdrojovým kódem. Vaše podpora je klíčová pro udržení kontinuity a rychlosti vývoje tohoto projektu.

Pokud si mé práce ceníte, můžete mě podpořit prostřednictvím GitHub Sponsors nebo následujících platforem. Předem děkuji!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternativně můžete vidět všechny možnosti financování kliknutím na **tlačítko Sponzor (❤️)** v pravém horním rohu úložiště.

## Předpoklady

- **Home Assistant OS / Supervised / Container:** Tato integrace vyžaduje instalaci Home Assistanta založenou na Linuxu, kde je dostupný a přístupný nástroj příkazového řádku `bluetoothctl`. **Nebude** fungovat na instalaci Home Assistant Core ve Windows.

## Instalace přes HACS (Doporučeno)

Tato integrace je k dispozici jako vlastní repozitář v HACS.

1.  Přejděte na svůj HACS dashboard.
2.  Klikněte na **Integrations** (Integrace).
3.  Klikněte na menu se třemi tečkami v pravém horním rohu a vyberte **"Custom repositories"** ("Vlastní repozitáře").
4.  V dialogovém okně zadejte následující informace:
    - **Repository (Repozitář):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategorie):** `Integration` (Integrace)
5.  Klikněte na **"Add"** ("Přidat").
6.  Integrace "MiPower" se nyní objeví ve vašem HACS seznamu. Klikněte na ni.
7.  Klikněte na tlačítko **"Download"** ("Stáhnout") a poté znovu na **"Download"** ("Stáhnout") v následujícím okně.
8.  Po dokončení stahování **musíte restartovat Home Assistant**, aby se integrace načetla.

## Manuální instalace

Ačkoli je HACS doporučenou metodou, můžete integraci nainstalovat i ručně.

1.  Přejděte na [stránku Vydání](https://github.com/DenizOner/MiPower/releases) repozitáře a stáhněte soubor `mipower.zip` z nejnovějšího vydání.
2.  Rozbalte stažený soubor.
3.  Uvnitř rozbalené složky najdete adresář `custom_components`. Zkopírujte z něj složku `mipower`.
4.  Vloženou složku `mipower` vložte do složky `custom_components` ve vašem konfiguračním adresáři Home Assistanta. Pokud složka `custom_components` neexistuje, musíte ji vytvořit.
    - Konečná cesta by měla vypadat takto: `.../config/custom_components/mipower/`
5.  Restartujte Home Assistant.

## Konfigurace

Po restartu můžete přidat a nakonfigurovat přepínač MiPower.

1.  Přejděte na **Settings > Devices & Services** (Nastavení > Zařízení a Služby).
2.  Klikněte na tlačítko **"+ Add Integration"** ("+ Přidat integraci") v pravém dolním rohu.
3.  Vyhledejte **"MiPower"** a klikněte na ni.

### Snadné nastavení (Doporučeno)

Jedná se o nejjednodušší způsob konfigurace integrace.

1.  Po výzvě zvolte **"Easy Setup"** ("Snadné nastavení").
2.  Integrace automaticky objeví mediální přehrávače s podporou Bluetooth ve vašem systému.
3.  Vyberte své cílové zařízení (např. "Xiaomi Mi Box 4") z rozbalovacího seznamu.
4.  Klikněte na **"Submit"** ("Odeslat").

To je vše! Integrace vytvoří přepínač propojený s vaším mediálním přehrávačem.

### Pokročilé nastavení

Tuto metodu použijte, pokud Snadné nastavení nenajde vaše zařízení nebo pokud potřebujete konfigurovat pokročilé nastavení časování od začátku.

1.  **Krok 1: Výběr zařízení**
    - Zvolte **"Advanced Setup"** ("Pokročilé nastavení").
    - Vyberte svůj cílový mediální přehrávač ze seznamu *všech* mediálních přehrávačů ve vašem Home Assistantu.
2.  **Krok 2: MAC adresa**
    - Integrace se pokusí najít Bluetooth MAC adresu vybraného zařízení. 
    - Pokud bude nalezena, bude předvyplněna. Ověřte, že je správná.
    - Pokud nebude nalezena, musíte Bluetooth MAC adresu svého zařízení zadat ručně.
3.  **Krok 3: Nastavení časování**
    - Můžete konfigurovat různé časové limity a zpoždění pro Bluetooth příkazy. Pro většinu uživatelů jsou výchozí hodnoty dostačující.
4.  Klikněte na **"Submit"** ("Odeslat") pro dokončení nastavení.

## Možnosti

Jakmile nakonfigurujete přepínač MiPower, můžete nastavení časování kdykoli upravit.

1.  Přejděte na **Settings > Devices & Services** (Nastavení > Zařízení a Služby).
2.  Najděte integraci MiPower a klikněte na **"Configure"** ("Konfigurovat").
3.  Podle potřeby upravte posuvníky pro tlumení, časové limity a zpoždění.

## Vysvětlení nastavení časování

V nabídce konfigurace nebo možností můžete doladit časování Bluetooth příkazů. Pro většinu uživatelů fungují výchozí hodnoty dobře.

- **Turn-On Debounce (Tlumení zapnutí):** Minimální čas (v sekundách), který musí uplynout, než se příkaz 'zapnout' může znovu provést. Tím se zabrání spamování zařízení probouzecími signály, pokud je přepínač rychle přepínán.

- **Turn-Off Debounce (Tlumení vypnutí):** Minimální čas (v sekundách), který musí uplynout, než se příkaz 'vypnout' může znovu provést. 

- **Delay Between Commands (Zpoždění mezi příkazy):** Velmi krátké zpoždění (v sekundách) mezi odesláním po sobě jdoucích příkazů do utility `bluetoothctl`. Na některých systémech může přidání malé pauzy zlepšit spolehlivost.

- **Process Spawn Timeout (Časový limit spuštění procesu):** Maximální čas (v sekundách), po který se čeká na spuštění procesu `bluetoothctl`. Pokud se v tomto čase nespustí, pokus o zapnutí selže.

- **Pairing Timeout (Časový limit párování):** Ve zjednodušené logice zapnutí se jedná o dobu, po kterou se čeká po odeslání příkazu `pair`, než se předpokládá úspěch. Poskytuje zařízení čas na zpracování probouzecího signálu.

- **Bluetooth Scan Duration (Doba trvání skenování Bluetooth):** Doba (v sekundách), po kterou bude integrace skenovat Bluetooth zařízení před pokusem o odeslání příkazu pro párování. Delší skenování může pomoci najít zařízení, která pomalu oznamují svou přítomnost.

## Čtěte ve svém vlastním jazyce

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