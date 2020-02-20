## Custom calendar with Python
The main idea is to create custom calendar and using a huge screen let people know about different events. My idea is to put the screen on the wall in the dining room so my colleagues could see a little information about upcoming events.
To do so I decided to generate HTML page with Python. To add some event telegram bot was created. Events are collected in csv-file

# My plans

-clean up calendar code
-add features to telegram bot ("gui"-calendar, rights for different kinds of users, etc.)
-create server part
etc

Current structure is:
telegbot_events.py - Telegram bot
newWebValendar.py - generation of web-page