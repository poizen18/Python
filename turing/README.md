# Turing

## How it works:
This script will connect to your IRC server (localhost by default) and respond to various prompts:
- Typing ++ in IRC will give karma to an item (e.g. Turing++)
- Typing -- in IRC will take karma away from an item (e.g. Turing--)
- Typing !rank and then an item will let you know how much karma it has (e.g. !rank Turing)
- Typing !top will list the top 5 items by karma
- Typing !bottom will list the bottom 5 items by karma
- Typing !weather City,State will provide weather info (e.g. !weather Bend,OR)
- Typing !help will print a list of options

## Notes:

- This script will check every 15 minutes for earthquakes around the world and report them in IRC.
- The script uses json load/dump to periodically store existing karma in a file and load it on startup.

### [The script is named after Alan Turing]
