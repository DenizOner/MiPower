# MiPower — Προσαρμοσμένη Ενοποίηση για το Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

Το **MiPower** είναι μια ενοποίηση (integration) του Home Assistant που σας επιτρέπει να ελέγχετε την κατάσταση τροφοδοσίας συσκευών αναπαραγωγής πολυμέσων που δεν υποστηρίζουν το παραδοσιακό Wake-on-LAN (WOL), αλλά μπορούν να "αφυπνιστούν" μέσω μιας αίτησης ζεύξης Bluetooth. Σχεδιάστηκε ειδικά για συσκευές όπως το Xiaomi Mi Box, αλλά μπορεί να λειτουργήσει και με άλλα παρόμοια Android TV box.

Αυτή η ενοποίηση δημιουργεί μια οντότητα `switch` (διακόπτης) στο Home Assistant. 
- Η **Ενεργοποίηση** του διακόπτη στέλνει μια σειρά εντολών Bluetooth μέσω του `bluetoothctl` για να αφυπνίσει τη συσκευή.
- Η **Απενεργοποίηση** του διακόπτη καλεί την υπηρεσία `media_player.turn_off` για τη συνδεδεμένη συσκευή.
- Η κατάσταση του διακόπτη συγχρονίζεται αυτόματα με την κατάσταση της συνδεδεμένης οντότητας αναπαραγωγής πολυμέσων.

## 🤝 Υποστηρίξτε μας

Το έργο MiPower αναπτύσσεται με το όραμα να προσθέσει αξία στην κοινότητα ανοιχτού κώδικα. Η υποστήριξή σας είναι ζωτικής σημασίας για τη διατήρηση της συνέχειας και του ρυθμού ανάπτυξης αυτού του έργου.

Εάν εκτιμάτε τη δουλειά μου, μπορείτε να με υποστηρίξετε μέσω του GitHub Sponsors ή των παρακάτω πλατφορμών. Σας ευχαριστώ εκ των προτέρων!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Εναλλακτικά, μπορείτε να δείτε όλες τις επιλογές χρηματοδότησης κάνοντας κλικ στο **κουμπί Χορηγός (❤️)** στην επάνω δεξιά γωνία του αποθετηρίου.

## Προαπαιτούμενα

- **Home Assistant OS / Supervised / Container:** Αυτή η ενοποίηση απαιτεί μια εγκατάσταση Home Assistant βασισμένη σε Linux, όπου το εργαλείο γραμμής εντολών `bluetoothctl` είναι διαθέσιμο και προσβάσιμο. **Δεν** θα λειτουργήσει σε εγκατάσταση Home Assistant Core στα Windows.

## Εγκατάσταση μέσω HACS (Συνιστάται)

Αυτή η ενοποίηση είναι διαθέσιμη ως προσαρμοσμένο αποθετήριο στο HACS.

1.  Μεταβείτε στον πίνακα ελέγχου του HACS.
2.  Κάντε κλικ στο **Integrations** (Ενοποιήσεις).
3.  Κάντε κλικ στο μενού με τις τρεις κουκκίδες στην επάνω δεξιά γωνία και επιλέξτε **"Custom repositories"** ("Προσαρμοσμένα αποθετήρια").
4.  Στο παράθυρο διαλόγου, εισαγάγετε τις ακόλουθες πληροφορίες:
    - **Repository (Αποθετήριο):** `https://github.com/DenizOner/MiPower`
    - **Category (Κατηγορία):** `Integration` (Ενοποίηση)
5.  Κάντε κλικ στο **"Add"** ("Προσθήκη").
6.  Η ενοποίηση "MiPower" θα εμφανιστεί τώρα στη λίστα HACS. Κάντε κλικ σε αυτήν.
7.  Κάντε κλικ στο κουμπί **"Download"** ("Λήψη") και μετά ξανά στο **"Download"** ("Λήψη") στο επόμενο παράθυρο.
8.  Μετά την ολοκλήρωση της λήψης, **πρέπει να κάνετε επανεκκίνηση του Home Assistant** για να φορτωθεί η ενοποίηση.

## Χειροκίνητη Εγκατάσταση

Αν και το HACS είναι η συνιστώμενη μέθοδος, μπορείτε επίσης να εγκαταστήσετε την ενοποίηση χειροκίνητα.

1.  Πηγαίνετε στη [σελίδα Εκδόσεων](https://github.com/DenizOner/MiPower/releases) του αποθετηρίου και κατεβάστε το αρχείο `mipower.zip` της πιο πρόσφατης έκδοσης.
2.  Αποσυμπιέστε το αρχείο που κατεβάσατε.
3.  Μέσα στον αποσυμπιεσμένο φάκελο, θα βρείτε έναν κατάλογο `custom_components`. Αντιγράψτε τον φάκελο `mipower` από μέσα του.
4.  Επικολλήστε τον αντιγραμμένο φάκελο `mipower` στον φάκελο `custom_components` του καταλόγου διαμόρφωσης του Home Assistant. Εάν ο φάκελος `custom_components` δεν υπάρχει, πρέπει να τον δημιουργήσετε.
    - Η τελική διαδρομή θα πρέπει να μοιάζει με: `.../config/custom_components/mipower/`
5.  Κάντε επανεκκίνηση του Home Assistant.

## Διαμόρφωση

Μετά την επανεκκίνηση, μπορείτε να προσθέσετε και να διαμορφώσετε τον διακόπτη MiPower.

1.  Πηγαίνετε στο **Settings > Devices & Services** (Ρυθμίσεις > Συσκευές & Υπηρεσίες).
2.  Κάντε κλικ στο κουμπί **"+ Add Integration"** ("+ Προσθήκη Ενοποίησης") στην κάτω δεξιά γωνία.
3.  Αναζητήστε το **"MiPower"** και κάντε κλικ σε αυτό.

### Εύκολη Ρύθμιση (Συνιστάται)

Αυτός είναι ο απλούστερος τρόπος διαμόρφωσης της ενοποίησης.

1.  Όταν σας ζητηθεί, επιλέξτε **"Easy Setup"** ("Εύκολη Ρύθμιση").
2.  Η ενοποίηση θα ανακαλύψει αυτόματα τις συσκευές αναπαραγωγής πολυμέσων με δυνατότητα Bluetooth στο σύστημά σας.
3.  Επιλέξτε τη συσκευή-στόχο σας (π.χ. "Xiaomi Mi Box 4") από την αναπτυσσόμενη λίστα.
4.  Κάντε κλικ στο **"Submit"** ("Υποβολή").

Αυτό είναι όλο! Η ενοποίηση θα δημιουργήσει έναν διακόπτη συνδεδεμένο με τη συσκευή αναπαραγωγής πολυμέσων σας.

### Προηγμένη Ρύθμιση

Χρησιμοποιήστε αυτήν τη μέθοδο εάν η Εύκολη Ρύθμιση δεν βρει τη συσκευή σας ή εάν χρειάζεται να διαμορφώσετε τις προηγμένες ρυθμίσεις χρονισμού από την αρχή.

1.  **Βήμα 1: Επιλογή Συσκευής**
    - Επιλέξτε **"Advanced Setup"** ("Προηγμένη Ρύθμιση").
    - Επιλέξτε τη συσκευή αναπαραγωγής πολυμέσων-στόχο σας από τη λίστα με *όλες* τις συσκευές αναπαραγωγής πολυμέσων στο Home Assistant σας.
2.  **Βήμα 2: Διεύθυνση MAC**
    - Η ενοποίηση θα προσπαθήσει να βρει τη διεύθυνση Bluetooth MAC της επιλεγμένης συσκευής. 
    - Εάν βρεθεί, θα προ-συμπληρωθεί. Επαληθεύστε ότι είναι σωστή.
    - Εάν δεν βρεθεί, πρέπει να εισαγάγετε χειροκίνητα τη διεύθυνση Bluetooth MAC της συσκευής σας.
3.  **Βήμα 3: Ρυθμίσεις Χρονισμού**
    - Μπορείτε να διαμορφώσετε διάφορα χρονικά όρια (timeouts) και καθυστερήσεις για τις εντολές Bluetooth. Για τους περισσότερους χρήστες, οι προεπιλεγμένες τιμές είναι επαρκείς.
4.  Κάντε κλικ στο **"Submit"** ("Υποβολή") για να ολοκληρώσετε τη ρύθμιση.

## Επιλογές

Αφού διαμορφώσετε τον διακόπτη MiPower, μπορείτε να προσαρμόσετε τις ρυθμίσεις χρονισμού ανά πάσα στιγμή.

1.  Πηγαίνετε στο **Settings > Devices & Services** (Ρυθμίσεις > Συσκευές & Υπηρεσίες).
2.  Βρείτε την ενοποίηση MiPower και κάντε κλικ στο **"Configure"** ("Διαμόρφωση").
3.  Προσαρμόστε τους ρυθμιστές για debouncing, timeouts και καθυστερήσεις όπως απαιτείται.

## Επεξήγηση Ρυθμίσεων Χρονισμού

Στο μενού διαμόρφωσης ή επιλογών, μπορείτε να ρυθμίσετε με ακρίβεια τον χρονισμό των εντολών Bluetooth. Για τους περισσότερους χρήστες, οι προεπιλεγμένες τιμές λειτουργούν καλά.

- **Turn-On Debounce (Καθυστέρηση Ενεργοποίησης):** Ο ελάχιστος χρόνος (σε δευτερόλεπτα) που πρέπει να παρέλθει πριν η εντολή 'ενεργοποίηση' μπορέσει να εκτελεστεί ξανά. Αυτό αποτρέπει την υπερφόρτωση της συσκευής με σήματα αφύπνισης εάν ο διακόπτης εναλλάσσεται γρήγορα.

- **Turn-Off Debounce (Καθυστέρηση Απενεργοποίησης):** Ο ελάχιστος χρόνος (σε δευτερόλεπτα) που πρέπει να παρέλθει πριν η εντολή 'απενεργοποίηση' μπορέσει να εκτελεστεί ξανά. 

- **Delay Between Commands (Καθυστέρηση Μεταξύ Εντολών):** Μια πολύ σύντομη καθυστέρηση (σε δευτερόλεπτα) μεταξύ της αποστολής διαδοχικών εντολών στο βοηθητικό πρόγραμμα `bluetoothctl`. Σε ορισμένα συστήματα, η προσθήκη μιας μικρής παύσης μπορεί να βελτιώσει την αξιοπιστία.

- **Process Spawn Timeout (Χρονικό Όριο Εκκίνησης Διαδικασίας):** Ο μέγιστος χρόνος (σε δευτερόλεπτα) αναμονής για την εκκίνηση της διαδικασίας `bluetoothctl`. Εάν αποτύχει να ξεκινήσει εντός αυτού του χρόνου, η προσπάθεια ενεργοποίησης θα αποτύχει.

- **Pairing Timeout (Χρονικό Όριο Ζεύξης):** Στην απλοποιημένη λογική ενεργοποίησης, αυτό είναι το χρονικό διάστημα που πρέπει να περιμένετε μετά την αποστολή της εντολής `pair` πριν υποτεθεί η επιτυχία. Δίνει χρόνο στη συσκευή να επεξεργαστεί το σήμα αφύπνισης.

- **Bluetooth Scan Duration (Διάρκεια Σάρωσης Bluetooth):** Η διάρκεια (σε δευτερόλεπτα) που η ενοποίηση θα σαρώνει για συσκευές Bluetooth πριν επιχειρήσει να στείλει την εντολή ζεύξης. Μια μεγαλύτερη σάρωση μπορεί να βοηθήσει στην εύρεση συσκευών που είναι αργές στην ανακοίνωση της παρουσίας τους.

## Διαβάστε στη γλώσσα σας

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