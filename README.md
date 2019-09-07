# textricate
**textricate**  is a script which extracts SMS messages from [Textra SMS](https://play.google.com/store/apps/details?id=com.textra) and exports them to a format understood by the popular [SMS Backup and Restore](https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore), in a similar vein to [several](https://github.com/sync-oz/convert-textra-db-to-xml) [existing](https://codegists.com/snippet/php/textra_sms_convertphp_kaiyao_php) [projects](https://github.com/alexisph/textra_to_xml). However, unlike these solutions, textricate maintains encoding (handling emojis properly) and additionally attempts to repair a database damaged by previous usages of these scripts by removing duplicate messages and fixing encoding errors where possible. SMS Backup and Restore can be used to write the resulting XML file to the Android SMS provider (system database).

### Why this is useful

On initialisation, Textra takes a copy of Android's SMS database in its own database for improved performance. Several situations can lead to this database becoming desynchronised from the Android provider and your messages being stuck inside Textra, the most obvious of which being that you have a backup of Textra's app data but not your messages themselves. textricate allows you to extract messages from Textra's database and write them to the system database so that they can be used by other apps.

### How to use
1. Clone or [download](https://github.com/biqqles/textricate/archive/master.zip) this repo and install the sole dependency, [`ftfy`](https://github.com/LuminosoInsight/python-ftfy), using `pip`
2. Copy `messages.db` from `/data/data/com.textra/databases/` on your device to the same directory as the script using ADB (i.e. `adb pull /data/data/com.textra/databases/messages.db`)
3. Run `textricate.py` and transfer the resulting XML file back to your device (e.g. `adb push textricate.xml /sdcard/`)
4. Restore with SMS Backup and Restore
5. Use `Textra > Settings > About > Resync Textra` to force Textra to load a new copy of its database from the system provider
