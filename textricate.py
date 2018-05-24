"""
Copyright © 2018 biqqles.

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

This script exports Textra's messaging database to an XML file understood by SMS Backup and Restore. Copy Textra's
messaging database at `/data/data/com.textra/databases/messaging.db` to the same directory as this script and run. 
Copy the resulting textricate.xml back onto the device and restore with SMS Backup and Restore. For more details
see README.md. Requires ftfy.
"""

from collections import OrderedDict, defaultdict
import sqlite3
import time

from ftfy import fix_encoding

query = '''SELECT messages.*, convos.display_name, convos.lookup_key
           FROM convos, messages
           WHERE convos._id = messages.convo_id'''

start_time = time.time()

# load Textra's messaging database
db = sqlite3.connect('messaging.db')
db_messages = db.execute(query)
db_messages.row_factory = sqlite3.Row  # make columns accessible by name

messages = defaultdict(list)  # messages, grouped by time

# convert from Textra's schema to SMS Backup and Restore's
for m in db_messages:
    if m['text']:  # filter empty messages
        text = fix_encoding(m['text']).replace('"', '&quot;')  # repair encoding and prepare for XML conversion
        message = OrderedDict([
            ('protocol', 0),
            ('address', m['lookup_key'].replace('^', '')),
            ('date', m['ts']),
            ('type', m['direction'] + 1),  # Textra uses 0 for received and 1 for sent; SMS B&R uses 1 and 2
            ('subject', 'null'),
            ('body', text),
            ('toa', 'null'),
            ('sc_toa', 'null'),
            ('service_center', m['message_center_ts']),
            ('read', '1'),
            ('status', '0'),
            ('readable_date', time.strftime('%d %b %Y %H:%M:%S GMT', time.gmtime(m['ts'] // 1000))),
            ('contact_name', m['display_name']),  # not required, but we may as well try to get it. Also readable_date
            ('locked', 0)
        ])
        
        # group messages of the same direction by timestamp: ts has millisecond precision so it's extremely unlikely
        # this will result in a message being grouped improperly. To reduce this chance as much as possible, direction
        # is also taken into account
        messages[m['ts'], m['direction']].append(message)

# remove duplicates (messages with the same timestamp): take the message with the largest byte count and assume it
# encodes the most valid information
for k, v in messages.items():
    if len(v) > 1:
        messages[k].sort(key=lambda s: s['body'].encode('utf-8'), reverse=True)
    messages[k] = messages[k][0]
    
count = len(messages)

# form XML. Each <sms /> element is made up of the key/value pairs of each OrderedDict defined above
lines = [
    '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n',
    '<smses count="{}" backup_date="{}">\n'.format(count, round(start_time * 1000)),
    *[' <sms {} />\n'.format(' '.join('{}="{}"'.format(k, v) for k, v in m.items())) for m in messages.values()],
    '</smses>'
    ]

with open('textricate.xml', 'w') as f:
    f.writelines(lines)

print('textricate: exported {} messages in {:.2f} seconds'.format(count, time.time() - start_time))
