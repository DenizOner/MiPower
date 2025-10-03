# MiPower — Integrazione personalizzata di Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** è un'integrazione di Home Assistant che ti permette di controllare lo stato di alimentazione dei lettori multimediali che non supportano il tradizionale Wake-on-LAN (WOL), ma che possono essere "risvegliati" da una richiesta di accoppiamento Bluetooth. È stata specificamente progettata per dispositivi come Xiaomi Mi Box, ma può funzionare con altri box Android TV simili.

Questa integrazione crea un'entità `switch` (interruttore) in Home Assistant. 
- **L'accensione** dell'interruttore invia una serie di comandi Bluetooth tramite `bluetoothctl` per risvegliare il dispositivo.
- **Lo spegnimento** dell'interruttore richiama il servizio `media_player.turn_off` per il dispositivo collegato.
- Lo stato dell'interruttore è sincronizzato automaticamente con lo stato dell'entità del lettore multimediale collegato.

## 🤝 Sostienici

Il progetto MiPower è sviluppato con la visione di aggiungere valore alla comunità open source. Il tuo supporto è vitale per mantenere la continuità e la velocità di sviluppo di questo progetto.

Se apprezzi il mio lavoro, puoi sostenermi tramite GitHub Sponsors o le seguenti piattaforme. Grazie in anticipo!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

In alternativa, puoi vedere tutte le opzioni di finanziamento cliccando sul **pulsante Sponsor (❤️)** nell'angolo in alto a destra del repository.

## Prerequisiti

- **Home Assistant OS / Supervised / Container:** Questa integrazione richiede un'installazione di Home Assistant basata su Linux dove lo strumento da riga di comando `bluetoothctl` sia disponibile e accessibile. **Non** funzionerà su un'installazione di Home Assistant Core su Windows.

## Installazione tramite HACS (Raccomandata)

Questa integrazione è disponibile come repository personalizzato in HACS.

1.  Naviga alla tua dashboard HACS.
2.  Clicca su **Integrations** (Integrazioni).
3.  Clicca sul menu a tre puntini nell'angolo in alto a destra e seleziona **"Custom repositories"** ("Repository personalizzati").
4.  Nel box di dialogo, inserisci le seguenti informazioni:
    - **Repository (Repository):** `https://github.com/DenizOner/MiPower`
    - **Category (Categoria):** `Integration` (Integrazione)
5.  Clicca **"Add"** ("Aggiungi").
6.  L'integrazione "MiPower" apparirà ora nella tua lista HACS. Clicca su di essa.
7.  Clicca il pulsante **"Download"** ("Scarica") e poi clicca di nuovo **"Download"** ("Scarica") nella finestra successiva.
8.  Una volta completato il download, **devi riavviare Home Assistant** affinché l'integrazione venga caricata.

## Installazione Manuale

Sebbene HACS sia il metodo raccomandato, puoi anche installare l'integrazione manualmente.

1.  Vai alla [pagina delle Rilasci](https://github.com/DenizOner/MiPower/releases) del repository e scarica il file `mipower.zip` dall'ultima versione.
2.  Decomprimi il file scaricato.
3.  All'interno della cartella decompressa, troverai una directory `custom_components`. Copia la cartella `mipower` al suo interno.
4.  Incolla la cartella `mipower` copiata nella cartella `custom_components` della tua directory di configurazione di Home Assistant. Se la cartella `custom_components` non esiste, devi crearla.
    - Il percorso finale dovrebbe assomigliare a: `.../config/custom_components/mipower/`
5.  Riavvia Home Assistant.

## Configurazione

Dopo il riavvio, puoi aggiungere e configurare l'interruttore MiPower.

1.  Vai su **Settings > Devices & Services** (Impostazioni > Dispositivi e Servizi).
2.  Clicca il pulsante **"+ Add Integration"** ("+ Aggiungi Integrazione") nell'angolo in basso a destra.
3.  Cerca **"MiPower"** e clicca su di esso.

### Configurazione Facile (Raccomandata)

Questo è il modo più semplice per configurare l'integrazione.

1.  Quando richiesto, scegli **"Easy Setup"** ("Configurazione Facile").
2.  L'integrazione scoprirà automaticamente i lettori multimediali abilitati al Bluetooth sul tuo sistema.
3.  Seleziona il tuo dispositivo target (ad esempio, "Xiaomi Mi Box 4") dall'elenco a discesa.
4.  Clicca **"Submit"** ("Invia").

Questo è tutto! L'integrazione creerà un interruttore collegato al tuo lettore multimediale.

### Configurazione Avanzata

Utilizza questo metodo se la Configurazione Facile non trova il tuo dispositivo o se devi configurare impostazioni di temporizzazione avanzate fin dall'inizio.

1.  **Passo 1: Selezione del Dispositivo**
    - Scegli **"Advanced Setup"** ("Configurazione Avanzata").
    - Seleziona il tuo lettore multimediale target dalla lista di *tutti* i lettori multimediali nel tuo Home Assistant.
2.  **Passo 2: Indirizzo MAC**
    - L'integrazione tenterà di trovare l'Indirizzo MAC Bluetooth del dispositivo selezionato. 
    - Se trovato, sarà precompilato. Verifica che sia corretto.
    - Se non trovato, devi inserire manualmente l'Indirizzo MAC Bluetooth del tuo dispositivo.
3.  **Passo 3: Impostazioni di Temporizzazione**
    - Puoi configurare vari timeout e ritardi per i comandi Bluetooth. Per la maggior parte degli utenti, i valori predefiniti sono sufficienti.
4.  Clicca **"Submit"** ("Invia") per completare la configurazione.

## Opzioni

Una volta configurato il tuo interruttore MiPower, puoi regolare le impostazioni di temporizzazione in qualsiasi momento.

1.  Vai su **Settings > Devices & Services** (Impostazioni > Dispositivi e Servizi).
2.  Trova l'integrazione MiPower e clicca su **"Configure"** ("Configura").
3.  Regola i cursori per *debounce*, timeout e ritardi come necessario.

## Spiegazione delle Impostazioni di Temporizzazione

Nel menu di configurazione o opzioni, puoi regolare finemente la temporizzazione dei comandi Bluetooth. Per la maggior parte degli utenti, i valori predefiniti funzionano bene.

- **Turn-On Debounce (Anti-rimbalzo All'accensione):** Il tempo minimo (in secondi) che deve trascorrere prima che il comando 'accendi' possa essere eseguito di nuovo. Ciò impedisce di intasare il dispositivo con segnali di risveglio se l'interruttore viene azionato rapidamente.

- **Turn-Off Debounce (Anti-rimbalzo Allo Spegnimento):** Il tempo minimo (in secondi) che deve trascorrere prima che il comando 'spegni' possa essere eseguito di nuovo. 

- **Delay Between Commands (Ritardo tra i Comandi):** Un ritardo molto breve (in secondi) tra l'invio di comandi consecutivi all'utilità `bluetoothctl`. Su alcuni sistemi, l'aggiunta di una piccola pausa può migliorare l'affidabilità.

- **Process Spawn Timeout (Timeout Avvio Processo):** Il tempo massimo (in secondi) da attendere per l'avvio del processo `bluetoothctl`. Se non riesce ad avviarsi entro questo tempo, il tentativo di accensione fallirà.

- **Pairing Timeout (Timeout di Accoppiamento):** Nella logica di accensione semplificata, questa è la quantità di tempo da attendere dopo l'invio del comando `pair` prima di assumere il successo. Dà tempo al dispositivo di elaborare il segnale di risveglio.

- **Bluetooth Scan Duration (Durata Scansione Bluetooth):** La durata (in secondi) per cui l'integrazione cercherà i dispositivi Bluetooth prima di tentare di inviare il comando di accoppiamento. Una scansione più lunga può aiutare a trovare dispositivi che sono lenti a pubblicizzare la loro presenza.

## Leggi nella tua lingua

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