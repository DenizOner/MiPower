# MiPower — Integración personalizada de Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** é unha integración de Home Assistant que permite controlar o estado de enerxía de reprodutores multimedia que non son compatibles co tradicional Wake-on-LAN (WOL), pero que poden ser "espertados" mediante unha solicitude de emparellamento por Bluetooth. Foi deseñada especificamente para dispositivos como o Xiaomi Mi Box, pero pode funcionar con outras caixas de Android TV similares.

Esta integración crea unha entidade `switch` (interruptor) en Home Assistant. 
- **Ao acender** o interruptor, envíase unha serie de comandos Bluetooth a través de `bluetoothctl` para espertar o dispositivo.
- **Ao apagar** o interruptor, chámase ao servizo `media_player.turn_off` para o dispositivo vinculado.
- O estado do interruptor sincronízase automaticamente co estado da entidade do reprodutor multimedia vinculado.

## 🤝 Ofreza Apoio

O proxecto MiPower desenvólvese coa visión de engadir valor á comunidade de código aberto. O seu apoio é vital para manter a continuidade e a velocidade de desenvolvemento deste proxecto.

Se aprecia o meu traballo, pode apoiarme a través de GitHub Sponsors ou as seguintes plataformas. Grazas de antemán!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Como alternativa, pode ver todas as opcións de financiamento facendo clic no **botón Patrocinador (❤️)** na esquina superior dereita do repositorio.

## Requisitos Previos

- **Home Assistant OS / Supervised / Container:** Esta integración require unha instalación de Home Assistant baseada en Linux onde a ferramenta de liña de comandos `bluetoothctl` estea dispoñible e sexa accesible. **Non** funcionará nunha instalación de Home Assistant Core en Windows.

## Instalación a través de HACS (Recomendado)

Esta integración está dispoñible como un repositorio personalizado en HACS.

1.  Navega ata o teu panel de HACS.
2.  Fai clic en **Integrations** (Integracións).
3.  Fai clic no menú de tres puntos na esquina superior dereita e selecciona **"Custom repositories"** ("Repositorios personalizados").
4.  No cadro de diálogo, introduce a seguinte información:
    - **Repository (Repositorio):** `https://github.com/DenizOner/MiPower`
    - **Category (Categoría):** `Integration` (Integración)
5.  Fai clic en **"Add"** ("Engadir").
6.  A integración "MiPower" aparecerá agora na túa lista de HACS. Fai clic nela.
7.  Fai clic no botón **"Download"** ("Descargar") e logo fai clic de novo en **"Download"** ("Descargar") na seguinte xanela.
8.  Unha vez completada a descarga, **debes reiniciar Home Assistant** para que a integración se poida cargar.

## Instalación Manual

Aínda que HACS é o método recomendado, tamén podes instalar a integración manualmente.

1.  Vai á [páxina de Lanzamentos](https://github.com/DenizOner/MiPower/releases) do repositorio e descarga o ficheiro `mipower.zip` da última versión.
2.  Descomprime o ficheiro descargado.
3.  Dentro do cartafol descomprimido, atoparás un directorio `custom_components`. Copia o cartafol `mipower` que se atopa dentro.
4.  Pega o cartafol `mipower` copiado no cartafol `custom_components` do teu directorio de configuración de Home Assistant. Se o cartafol `custom_components` non existe, debes crealo.
    - A ruta final debería ser similar a: `.../config/custom_components/mipower/`
5.  Reinicia Home Assistant.

## Configuración

Despois do reinicio, podes engadir e configurar o interruptor MiPower.

1.  Vai a **Settings > Devices & Services** (Configuración > Dispositivos e Servizos).
2.  Fai clic no botón **"+ Add Integration"** ("+ Engadir Integración") na esquina inferior dereita.
3.  Busca **"MiPower"** e fai clic nel.

### Configuración doada (Recomendado)

Esta é a forma máis sinxela de configurar a integración.

1.  Cando se che pregunte, escolle **"Easy Setup"** ("Configuración doada").
2.  A integración descubrirá automaticamente os reprodutores multimedia compatibles con Bluetooth no teu sistema.
3.  Selecciona o teu dispositivo obxectivo (p. ex., "Xiaomi Mi Box 4") na lista despregable.
4.  Fai clic en **"Submit"** ("Enviar").

Iso é todo! A integración creará un interruptor vinculado ao teu reprodutor multimedia.

### Configuración Avanzada

Usa este método se a Configuración Doada non atopa o teu dispositivo ou se necesitas configurar axustes de tempo avanzados dende o principio.

1.  **Paso 1: Selección do Dispositivo**
    - Escolle **"Advanced Setup"** ("Configuración avanzada").
    - Selecciona o teu reprodutor multimedia obxectivo da lista de *todos* os reprodutores multimedia no teu Home Assistant.
2.  **Paso 2: Enderezo MAC**
    - A integración tentará atopar o enderezo MAC Bluetooth do dispositivo seleccionado. 
    - Se se atopa, preencherase. Verifica que sexa correcto.
    - Se non se atopa, debes introducir manualmente o enderezo MAC Bluetooth do teu dispositivo.
3.  **Paso 3: Axustes de Tempo**
    - Podes configurar varios tempos de espera e atrasos para os comandos Bluetooth. Para a maioría dos usuarios, os valores predeterminados son suficientes.
4.  Fai clic en **"Submit"** ("Enviar") para completar a configuración.

## Opcións

Unha vez que teñas configurado o teu interruptor MiPower, podes axustar a configuración de tempo en calquera momento.

1.  Vai a **Settings > Devices & Services** (Configuración > Dispositivos e Servizos).
2.  Busca a integración MiPower e fai clic en **"Configure"** ("Configurar").
3.  Axusta os deslizadores para *debounce*, tempos de espera e atrasos segundo sexa necesario.

## Explicación dos Axustes de Tempo

No menú de configuración ou opcións, podes axustar con precisión o tempo dos comandos Bluetooth. Para a maioría dos usuarios, os valores predeterminados funcionan ben.

- **Turn-On Debounce (Antirrebote de Acendido):** O tempo mínimo (en segundos) que debe transcorrer antes de que o comando de 'acender' se poida executar de novo. Isto evita saturar o dispositivo con sinais de activación se o interruptor se conmuta rapidamente.

- **Turn-Off Debounce (Antirrebote de Apagado):** O tempo mínimo (en segundos) que debe transcorrer antes de que o comando de 'apagar' se poida executar de novo. 

- **Delay Between Commands (Atraso entre Comandos):** Un atraso moi curto (en segundos) entre o envío de comandos consecutivos á utilidade `bluetoothctl`. Nalgúns sistemas, engadir unha pequena pausa pode mellorar a fiabilidade.

- **Process Spawn Timeout (Tempo de Espera de Creación de Proceso):** O tempo máximo (en segundos) para esperar a que se inicie o proceso `bluetoothctl`. Se non se inicia dentro deste tempo, o intento de acendido fallará.

- **Pairing Timeout (Tempo de Espera de Emparellamento):** Na lóxica de acendido simplificada, esta é a cantidade de tempo que se espera despois de enviar o comando `pair` antes de asumir o éxito. Dálle tempo ao dispositivo para procesar o sinal de activación.

- **Bluetooth Scan Duration (Duración da Exploración Bluetooth):** A duración (en segundos) que a integración explorará en busca de dispositivos Bluetooth antes de intentar enviar o comando de emparellamento. Unha exploración máis longa pode axudar a atopar dispositivos que son lentos para anunciar a súa presenza.

## Lea no seu propio idioma

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