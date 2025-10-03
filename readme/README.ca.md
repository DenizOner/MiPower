# MiPower — Integració personalitzada de Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** és una integració de Home Assistant que us permet controlar l'estat d'alimentació de reproductors multimèdia que no admeten el tradicional Wake-on-LAN (WOL), però que es poden "despertar" mitjançant una sol·licitud d'aparellament Bluetooth. Va ser dissenyada específicament per a dispositius com el Xiaomi Mi Box, però pot funcionar amb altres caixes de televisió Android similars.

Aquesta integració crea una entitat `switch` (interruptor) a Home Assistant. 
- **Engegar** l'interruptor envia una sèrie d'ordres Bluetooth mitjançant `bluetoothctl` per despertar el dispositiu.
- **Apagar** l'interruptor crida el servei `media_player.turn_off` per al dispositiu enllaçat.
- L'estat de l'interruptor se sincronitza automàticament amb l'estat de l'entitat del reproductor multimèdia enllaçat.

## 🤝 Doneu Suport

El projecte MiPower es desenvolupa amb la visió d'afegir valor a la comunitat de codi obert. El vostre suport és vital per mantenir la continuïtat i la velocitat de desenvolupament d'aquest projecte.

Si valoreu la meva feina, podeu donar-me suport mitjançant GitHub Sponsors o les plataformes següents. Gràcies per endavant!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternativament, podeu veure totes les opcions de finançament fent clic al **botó Patrocinador (❤️)** a la cantonada superior dreta del repositori.

## Prerequisits

- **Home Assistant OS / Supervised / Container:** Aquesta integració requereix una instal·lació de Home Assistant basada en Linux on l'eina de línia d'ordres `bluetoothctl` estigui disponible i sigui accessible. **No** funcionarà en una instal·lació de Home Assistant Core a Windows.

## Instal·lació mitjançant HACS (Recomanat)

Aquesta integració està disponible com a repositori personalitzat a HACS.

1.  Navegueu al vostre tauler HACS.
2.  Feu clic a **Integrations** (Integracions).
3.  Feu clic al menú de tres punts a la cantonada superior dreta i seleccioneu **"Custom repositories"** ("Repositoris personalitzats").
4.  Al quadre de diàleg, introduïu la informació següent:
    - **Repository (Repositori):** `https://github.com/DenizOner/MiPower`
    - **Category (Categoria):** `Integration` (Integració)
5.  Feu clic a **"Add"** ("Afegeix").
6.  La integració "MiPower" apareixerà ara a la vostra llista HACS. Feu-hi clic.
7.  Feu clic al botó **"Download"** ("Descarrega") i, a continuació, torneu a fer clic a **"Download"** ("Descarrega") a la finestra següent.
8.  Un cop finalitzada la descàrrega, **heu de reiniciar Home Assistant** perquè es carregui la integració.

## Instal·lació Manual

Tot i que HACS és el mètode recomanat, també podeu instal·lar la integració manualment.

1.  Aneu a la [pàgina de Llançaments](https://github.com/DenizOner/MiPower/releases) del repositori i descarregueu el fitxer `mipower.zip` de l'últim llançament.
2.  Descomprimiu el fitxer descarregat.
3.  Dins de la carpeta descomprimida, trobareu un directori `custom_components`. Copieu-ne la carpeta `mipower`.
4.  Enganxeu la carpeta `mipower` copiada a la carpeta `custom_components` del vostre directori de configuració de Home Assistant. Si la carpeta `custom_components` no existeix, l'heu de crear.
    - El camí final hauria de ser similar a: `.../config/custom_components/mipower/`
5.  Reinicieu Home Assistant.

## Configuració

Després de reiniciar, podeu afegir i configurar l'interruptor MiPower.

1.  Aneu a **Settings > Devices & Services** (Configuració > Dispositius i Serveis).
2.  Feu clic al botó **"+ Add Integration"** ("+ Afegeix integració") a la cantonada inferior dreta.
3.  Cerqueu **"MiPower"** i feu-hi clic.

### Configuració Fàcil (Recomanada)

Aquesta és la manera més senzilla de configurar la integració.

1.  Quan se us demani, trieu **"Easy Setup"** ("Configuració fàcil").
2.  La integració descobrirà automàticament els reproductors multimèdia amb Bluetooth al vostre sistema.
3.  Seleccioneu el vostre dispositiu objectiu (per exemple, "Xiaomi Mi Box 4") a la llista desplegable.
4.  Feu clic a **"Submit"** ("Envia").

Això és tot! La integració crearà un interruptor enllaçat al vostre reproductor multimèdia.

### Configuració Avançada

Utilitzeu aquest mètode si la Configuració Fàcil no troba el vostre dispositiu o si necessiteu configurar la configuració de temps avançada des del principi.

1.  **Pas 1: Selecció del Dispositiu**
    - Trieu **"Advanced Setup"** ("Configuració avançada").
    - Seleccioneu el vostre reproductor multimèdia objectiu de la llista de *tots* els reproductors multimèdia del vostre Home Assistant.
2.  **Pas 2: Adreça MAC**
    - La integració intentarà trobar l'adreça Bluetooth MAC del dispositiu seleccionat. 
    - Si es troba, es pre-omplirà. Verifiqueu que sigui correcta.
    - Si no es troba, heu d'introduir manualment l'adreça Bluetooth MAC del vostre dispositiu.
3.  **Pas 3: Configuració de Temps**
    - Podeu configurar diversos temps d'espera i retards per a les ordres Bluetooth. Per a la majoria d'usuaris, els valors predeterminats són suficients.
4.  Feu clic a **"Submit"** ("Envia") per completar la configuració.

## Opcions

Un cop hàgiu configurat el vostre interruptor MiPower, podeu ajustar la configuració de temps en qualsevol moment.

1.  Aneu a **Settings > Devices & Services** (Configuració > Dispositius i Serveis).
2.  Cerqueu la integració MiPower i feu clic a **"Configure"** ("Configura").
3.  Ajusteu els lliscadors per a "debounce", temps d'espera i retards segons sigui necessari.

## Explicació de la Configuració de Temps

Al menú de configuració o opcions, podeu ajustar el temps de les ordres Bluetooth. Per a la majoria d'usuaris, els valors predeterminats funcionen bé.

- **Turn-On Debounce (Debounce d'Engegada):** El temps mínim (en segons) que ha de passar abans que l'ordre "engegar" es pugui executar de nou. Això evita saturar el dispositiu amb senyals de despertar si l'interruptor es commuta ràpidament.

- **Turn-Off Debounce (Debounce d'Apagat):** El temps mínim (en segons) que ha de passar abans que l'ordre "apagar" es pugui executar de nou. 

- **Delay Between Commands (Retard entre Ordres):** Un retard molt curt (en segons) entre l'enviament d'ordres consecutives a la utilitat `bluetoothctl`. En alguns sistemes, afegir una petita pausa pot millorar la fiabilitat.

- **Process Spawn Timeout (Temps d'Espera d'Inici de Procés):** El temps màxim (en segons) per esperar que s'iniciï el procés `bluetoothctl`. Si no s'inicia dins d'aquest temps, l'intent d'engegada fallarà.

- **Pairing Timeout (Temps d'Espera d'Aparellament):** En la lògica d'engegada simplificada, aquesta és la quantitat de temps a esperar després d'enviar l'ordre `pair` abans d'assumir l'èxit. Dóna temps al dispositiu per processar el senyal de despertar.

- **Bluetooth Scan Duration (Durada de l'Escaneig Bluetooth):** La durada (en segons) que la integració escanejarà dispositius Bluetooth abans d'intentar enviar l'ordre d'aparellament. Un escaneig més llarg pot ajudar a trobar dispositius que són lents a anunciar la seva presència.

## Llegeix en el teu propi idioma

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