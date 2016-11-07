## Karmabot

# How it works:
This script will connect to your IRC server (localhost by default) and respond to various prompts
- Typing ++ in IRC will give karma to an item (e.g. Karmabot++)
- Typing -- in IRC will take karma away from an item (e.g. Karmabot--)
- Typing !rank and then an item will let you know how much karma it has (e.g. !rank Karmabot)
- Typing !top will list the top 5 items by karma
- Typing !bottom will list the bottom 5 items by karma
- Typing !help will print a list of options

The script uses json load/dump to periodically store existing karma in a file and load it on startup

