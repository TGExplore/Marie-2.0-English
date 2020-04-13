I'm a modular Telegram group management bot named Melody.

You can find my original code  [here](https://github.com/TGExplore/Marie-2.0-English)

If you want to use this version(removed old sudo's)  
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Whit3diamond/Melody)

ENV: Use "ANYTHING"

TOKEN: Your bot token, as a string.

OWNER_ID: An integer of consisting of your owner ID

OWNER_USERNAME: Your username

DATABASE_URL: Your database URL **Leave this to heroku

MESSAGE_DUMP: optional: a chat where your replied saved messages are stored, to stop people deleting their old **No need

WEBHOOK: Use "ANYTHING"

URL: The URL your webhook should connect to (only needed for webhook mode)

SUDO_USERS: A space separated list of user_ids which should be considered sudo users

SUPPORT_USERS: A space separated list of user_ids which should be considered support users (can gban/ungban, nothing else)

WHITELIST_USERS: A space separated list of user_ids which should be considered whitelisted - they can't be banned.

DONATION_LINK: Optional: link where you would like to receive donations. **Not important

CERT_PATH: Path to your webhook certificate **No need

PORT: 8443 **This is default I don't recommend changing this.

DEL_CMDS: (True/False)Whether to delete commands from users which don't have rights to use that command

STRICT_GBAN: (True/False)Enforce gbans across new groups as well as old groups. When a gbanned user talks, he will be banned.

BAN_STICKER: Which sticker to use when banning people.

ALLOW_EXCL: Whether to allow using exclamation marks ! for commands as well as /.
