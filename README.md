# Textricate
**textricate** liberates your messages from Textra's confines. This script reads [Textra SMS](https://play.google.com/store/apps/details?id=com.textra)'s messaging database, and exports SMS messages to a format understood by the popular [SMS Backup and Restore](https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore) app, in a similar vein to [several](https://github.com/sync-oz/convert-textra-db-to-xml) [existing](https://codegists.com/snippet/php/textra_sms_convertphp_kaiyao_php) [projects](https://github.com/alexisph/textra_to_xml). However, unlike these scripts, textricate maintains encoding (handling emojis properly) and additionally attempts to repair a database damaged by previous usages of these scripts or other utilities by removing duplicate messages and fixing encoding errors where possible. SMS Backup and Restore can be used to write the resulting XML file to the Android SMS provider (system database).

### How to use
1. Clone or [download](https://github.com/biqqles/textricate/archive/master.zip) this repo, and install the sole dependency, [`ftfy`](https://github.com/LuminosoInsight/python-ftfy), using `pip`
2. Copy `messages.db` from `/data/data/com.textra/databases/` on your device to the same directory as the script, using ADB or a file explorer with root permissions
3. Run `textricate.py`, and transfer the resulting XML file back to your device for restoration with SMS Backup and Restore
4. Use `Textra > Settings > About > Resync Textra` to force Textra to load a new copy of its database from the system provider
