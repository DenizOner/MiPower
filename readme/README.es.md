# MiPower — Integración personalizada de Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** es una integración de Home Assistant que te permite controlar el estado de energía de reproductores multimedia que no son compatibles con el tradicional Wake-on-LAN (WOL), pero que pueden ser "despertados" mediante una solicitud de emparejamiento por Bluetooth. Fue diseñada específicamente para dispositivos como el Xiaomi Mi Box, pero puede funcionar con otras cajas de Android TV similares.

Esta integración crea una entidad `switch` (interruptor) en Home Assistant. 
- **Al encender** el interruptor, se envía una serie de comandos Bluetooth a través de `bluetoothctl` para despertar el dispositivo.
- **Al apagar** el interruptor, se llama al servicio `media_player.turn_off` para el dispositivo vinculado.
- El estado del interruptor se sincroniza automáticamente con el estado de la entidad del reproductor multimedia vinculado.

## 🤝 Brinde Apoyo

El proyecto MiPower se desarrolla con la visión de agregar valor a la comunidad de código abierto. Su apoyo es vital para mantener la continuidad y el ritmo de desarrollo de este proyecto.

Si aprecia mi trabajo, puede apoyarme a través de GitHub Sponsors o las siguientes plataformas. ¡Gracias de antemano!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternativamente, puede ver todas las opciones de financiación haciendo clic en el **botón Patrocinar (❤️)** en la esquina superior derecha del repositorio.

## Requisitos Previos

- **Home Assistant OS / Supervised / Container:** Esta integración requiere una instalación de Home Assistant basada en Linux donde la herramienta de línea de comandos `bluetoothctl` esté disponible y sea accesible. **No** funcionará en una instalación de Home Assistant Core en Windows.

## Instalación a través de HACS (Recomendado)

Esta integración está disponible como un repositorio personalizado en HACS.

1.  Navega a tu panel de HACS.
2.  Haz clic en **Integrations** (Integraciones).
3.  Haz clic en el menú de tres puntos en la esquina superior derecha y selecciona **"Custom repositories"** ("Repositorios personalizados").
4.  En el cuadro de diálogo, introduce la siguiente información:
    - **Repository (Repositorio):** `https://github.com/DenizOner/MiPower`
    - **Category (Categoría):** `Integration` (Integración)
5.  Haz clic en **"Add"** ("Añadir").
6.  La integración "MiPower" aparecerá ahora en tu lista de HACS. Haz clic en ella.
7.  Haz clic en el botón **"Download"** ("Descargar") y luego haz clic de nuevo en **"Download"** ("Descargar") en la siguiente ventana.
8.  Una vez completada la descarga, **debes reiniciar Home Assistant** para que la integración se cargue.

## Instalación Manual

Aunque HACS es el método recomendado, también puedes instalar la integración manualmente.

1.  Ve a la [página de Lanzamientos](https://github.com/DenizOner/MiPower/releases) del repositorio y descarga el archivo `mipower.zip` de la última versión.
2.  Descomprime el archivo descargado.
3.  Dentro de la carpeta descomprimida, encontrarás un directorio `custom_components`. Copia la carpeta `mipower` que se encuentra dentro.
4.  Pega la carpeta `mipower` copiada en la carpeta `custom_components` de tu directorio de configuración de Home Assistant. Si la carpeta `custom_components` no existe, debes crearla.
    - La ruta final debería ser similar a: `.../config/custom_components/mipower/`
5.  Reinicia Home Assistant.

## Configuración

Después del reinicio, puedes añadir y configurar el interruptor MiPower.

1.  Ve a **Settings > Devices & Services** (Configuración > Dispositivos y Servicios).
2.  Haz clic en el botón **"+ Add Integration"** ("+ Añadir Integración") en la esquina inferior derecha.
3.  Busca **"MiPower"** y haz clic en él.

### Configuración Fácil (Recomendado)

Esta es la forma más sencilla de configurar la integración.

1.  Cuando se te pregunte, elige **"Easy Setup"** ("Configuración fácil").
2.  La integración detectará automáticamente los reproductores multimedia compatibles con Bluetooth en tu sistema.
3.  Selecciona tu dispositivo objetivo (p. ej., "Xiaomi Mi Box 4") de la lista desplegable.
4.  Haz clic en **"Submit"** ("Enviar").

¡Eso es todo! La integración creará un interruptor vinculado a tu reproductor multimedia.

### Configuración Avanzada

Utiliza este método si la Configuración Fácil no encuentra tu dispositivo o si necesitas configurar ajustes de tiempo avanzados desde el principio.

1.  **Paso 1: Selección de Dispositivo**
    - Elige **"Advanced Setup"** ("Configuración avanzada").
    - Selecciona tu reproductor multimedia objetivo de la lista de *todos* los reproductores multimedia de tu Home Assistant.
2.  **Paso 2: Dirección MAC**
    - La integración intentará encontrar la dirección Bluetooth MAC del dispositivo seleccionado. 
    - Si se encuentra, se rellenará previamente. Verifica que sea correcta.
    - Si no se encuentra, debes introducir manualmente la dirección Bluetooth MAC de tu dispositivo.
3.  **Paso 3: Ajustes de Tiempo**
    - Puedes configurar varios tiempos de espera y retrasos para los comandos Bluetooth. Para la mayoría de los usuarios, los valores predeterminados son suficientes.
4.  Haz clic en **"Submit"** ("Enviar") para completar la configuración.

## Opciones

Una vez que hayas configurado tu interruptor MiPower, puedes ajustar la configuración de tiempo en cualquier momento.

1.  Ve a **Settings > Devices & Services** (Configuración > Dispositivos y Servicios).
2.  Busca la integración MiPower y haz clic en **"Configure"** ("Configurar").
3.  Ajusta los deslizadores de *debounce*, tiempos de espera y retrasos según sea necesario.

## Explicación de los Ajustes de Tiempo

En el menú de configuración u opciones, puedes ajustar el tiempo de los comandos Bluetooth. Para la mayoría de los usuarios, los valores predeterminados funcionan bien.

- **Turn-On Debounce (Antirrebote de Encendido):** El tiempo mínimo (en segundos) que debe transcurrir antes de que el comando de 'encender' se pueda ejecutar de nuevo. Esto evita saturar el dispositivo con señales de activación si el interruptor se conmuta rápidamente.

- **Turn-Off Debounce (Antirrebote de Apagado):** El tiempo mínimo (en segundos) que debe transcurrir antes de que el comando de 'apagar' se pueda ejecutar de nuevo. 

- **Delay Between Commands (Retraso entre Comandos):** Un retraso muy corto (en segundos) entre el envío de comandos consecutivos a la utilidad `bluetoothctl`. En algunos sistemas, añadir una pequeña pausa puede mejorar la fiabilidad.

- **Process Spawn Timeout (Tiempo de Espera de Creación de Proceso):** El tiempo máximo (en segundos) para esperar a que se inicie el proceso `bluetoothctl`. Si no se inicia dentro de este tiempo, el intento de encendido fallará.

- **Pairing Timeout (Tiempo de Espera de Emparejamiento):** En la lógica de encendido simplificada, esta es la cantidad de tiempo que se espera después de enviar el comando `pair` antes de asumir el éxito. Le da tiempo al dispositivo para procesar la señal de activación.

- **Bluetooth Scan Duration (Duración del Escaneo Bluetooth):** La duración (en segundos) que la integración escaneará en busca de dispositivos Bluetooth antes de intentar enviar el comando de emparejamiento. Un escaneo más largo puede ayudar a encontrar dispositivos que tardan en anunciar su presencia.

## Lea en su propio idioma

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