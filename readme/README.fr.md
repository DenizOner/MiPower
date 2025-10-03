# MiPower — Intégration personnalisée pour Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** est une intégration Home Assistant qui vous permet de contrôler l'état d'alimentation des lecteurs multimédias qui ne prennent pas en charge le Wake-on-LAN (WOL) traditionnel, mais qui peuvent être "réveillés" par une demande de jumelage Bluetooth. Elle a été spécifiquement conçue pour des appareils comme le Xiaomi Mi Box, mais peut fonctionner avec d'autres boîtiers Android TV similaires.

Cette intégration crée une entité `switch` (interrupteur) dans Home Assistant. 
- **L'activation** de l'interrupteur envoie une série de commandes Bluetooth via `bluetoothctl` pour réveiller l'appareil.
- **La désactivation** de l'interrupteur appelle le service `media_player.turn_off` pour l'appareil lié.
- L'état de l'interrupteur est automatiquement synchronisé avec l'état de l'entité du lecteur multimédia lié.

## 🤝 Soutenez-nous

Le projet MiPower est développé avec la vision d'ajouter de la valeur à la communauté open source. Votre soutien est vital pour maintenir la continuité et le rythme de développement de ce projet.

Si vous appréciez mon travail, vous pouvez me soutenir via GitHub Sponsors ou les plateformes suivantes. Merci d'avance !

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternativement, vous pouvez voir toutes les options de financement en cliquant sur le **bouton Sponsor (❤️)** dans le coin supérieur droit du dépôt.

## Prérequis

- **Home Assistant OS / Supervised / Container:** Cette intégration nécessite une installation Home Assistant basée sur Linux où l'outil de ligne de commande `bluetoothctl` est disponible et accessible. Elle ne fonctionnera **pas** sur une installation Home Assistant Core sous Windows.

## Installation via HACS (Recommandée)

Cette intégration est disponible en tant que référentiel personnalisé dans HACS.

1.  Naviguez jusqu'à votre tableau de bord HACS.
2.  Cliquez sur **Integrations** (Intégrations).
3.  Cliquez sur le menu à trois points dans le coin supérieur droit et sélectionnez **"Custom repositories"** ("Référentiels personnalisés").
4.  Dans la boîte de dialogue, entrez les informations suivantes :
    - **Repository (Référentiel) :** `https://github.com/DenizOner/MiPower`
    - **Category (Catégorie) :** `Integration` (Intégration)
5.  Cliquez sur **"Add"** ("Ajouter").
6.  L'intégration "MiPower" apparaîtra maintenant dans votre liste HACS. Cliquez dessus.
7.  Cliquez sur le bouton **"Download"** ("Télécharger") puis à nouveau sur **"Download"** ("Télécharger") dans la fenêtre suivante.
8.  Une fois le téléchargement terminé, vous **devez redémarrer Home Assistant** pour que l'intégration soit chargée.

## Installation Manuelle

Bien que HACS soit la méthode recommandée, vous pouvez également installer l'intégration manuellement.

1.  Rendez-vous sur la [page des versions](https://github.com/DenizOner/MiPower/releases) du référentiel et téléchargez le fichier `mipower.zip` de la dernière version.
2.  Décompressez le fichier téléchargé.
3.  À l'intérieur du dossier décompressé, vous trouverez un répertoire `custom_components`. Copiez le dossier `mipower` qui s'y trouve.
4.  Collez le dossier `mipower` copié dans le dossier `custom_components` de votre répertoire de configuration Home Assistant. Si le dossier `custom_components` n'existe pas, vous devez le créer.
    - Le chemin final devrait ressembler à : `.../config/custom_components/mipower/`
5.  Redémarrez Home Assistant.

## Configuration

Après le redémarrage, vous pouvez ajouter et configurer l'interrupteur MiPower.

1.  Accédez à **Settings > Devices & Services** (Paramètres > Appareils et Services).
2.  Cliquez sur le bouton **"+ Add Integration"** ("+ Ajouter une intégration") dans le coin inférieur droit.
3.  Recherchez **"MiPower"** et cliquez dessus.

### Configuration Facile (Recommandée)

C'est le moyen le plus simple de configurer l'intégration.

1.  Lorsque vous y êtes invité, choisissez **"Easy Setup"** ("Configuration facile").
2.  L'intégration découvrira automatiquement les lecteurs multimédias compatibles Bluetooth sur votre système.
3.  Sélectionnez votre appareil cible (par exemple, "Xiaomi Mi Box 4") dans la liste déroulante.
4.  Cliquez sur **"Submit"** ("Soumettre").

C'est tout ! L'intégration créera un interrupteur lié à votre lecteur multimédia.

### Configuration Avancée

Utilisez cette méthode si la Configuration Facile ne trouve pas votre appareil ou si vous devez configurer des paramètres de temporisation avancés dès le départ.

1.  **Étape 1 : Sélection de l'appareil**
    - Choisissez **"Advanced Setup"** ("Configuration avancée").
    - Sélectionnez votre lecteur multimédia cible dans la liste de *tous* les lecteurs multimédias de votre Home Assistant.
2.  **Étape 2 : Adresse MAC**
    - L'intégration tentera de trouver l'adresse MAC Bluetooth de l'appareil sélectionné. 
    - Si elle est trouvée, elle sera pré-remplie. Vérifiez qu'elle est correcte.
    - Si elle n'est pas trouvée, vous devez saisir manuellement l'adresse MAC Bluetooth de votre appareil.
3.  **Étape 3 : Paramètres de temporisation**
    - Vous pouvez configurer divers délais d'attente (*timeouts*) et retards pour les commandes Bluetooth. Pour la plupart des utilisateurs, les valeurs par défaut sont suffisantes.
4.  Cliquez sur **"Submit"** ("Soumettre") pour terminer la configuration.

## Options

Une fois que vous avez configuré votre interrupteur MiPower, vous pouvez ajuster les paramètres de temporisation à tout moment.

1.  Accédez à **Settings > Devices & Services** (Paramètres > Appareils et Services).
2.  Trouvez l'intégration MiPower et cliquez sur **"Configure"** ("Configurer").
3.  Ajustez les curseurs pour l'anti-rebond (*debounce*), les délais d'attente et les retards si nécessaire.

## Explication des paramètres de temporisation

Dans le menu de configuration ou d'options, vous pouvez affiner la temporisation des commandes Bluetooth. Pour la plupart des utilisateurs, les valeurs par défaut fonctionnent bien.

- **Turn-On Debounce (Anti-rebond à l'activation) :** Le temps minimum (en secondes) qui doit s'écouler avant que la commande 'allumer' puisse être exécutée à nouveau. Cela empêche de saturer l'appareil avec des signaux de réveil si l'interrupteur est basculé rapidement.

- **Turn-Off Debounce (Anti-rebond à la désactivation) :** Le temps minimum (en secondes) qui doit s'écouler avant que la commande 'éteindre' puisse être exécutée à nouveau. 

- **Delay Between Commands (Délai entre les commandes) :** Un très court délai (en secondes) entre l'envoi de commandes consécutives à l'utilitaire `bluetoothctl`. Sur certains systèmes, l'ajout d'une petite pause peut améliorer la fiabilité.

- **Process Spawn Timeout (Délai d'attente de création de processus) :** Le temps maximum (en secondes) à attendre pour que le processus `bluetoothctl` démarre. S'il ne démarre pas dans ce délai, la tentative d'allumage échouera.

- **Pairing Timeout (Délai d'attente de jumelage) :** Dans la logique d'activation simplifiée, c'est le temps à attendre après l'envoi de la commande `pair` avant de supposer le succès. Cela donne à l'appareil le temps de traiter le signal de réveil.

- **Bluetooth Scan Duration (Durée de balayage Bluetooth) :** La durée (en secondes) pendant laquelle l'intégration recherchera les appareils Bluetooth avant de tenter d'envoyer la commande de jumelage. Un balayage plus long peut aider à trouver les appareils qui sont lents à annoncer leur présence.

## Lisez dans votre propre langue

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