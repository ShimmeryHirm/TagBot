from telethon import events, TelegramClient
from telethon.sessions import StringSession

import config

client = TelegramClient(StringSession(config.STRING_SESSION), config.API_ID, config.API_HASH).start()


@client.on(events.NewMessage())
async def handler(event):
    if event.text.startswith('@all ') or event.text == '@all':
        _, *args = event.text.split(maxsplit=1)
        args = args[0] + ' ' if args else ""
        participants = await client.get_participants(event.chat_id)
        mentions = []
        for participant in participants:
            if args:
                mentions.append(f'<a href="tg://user?id={participant.id}">\u2060</a>')
            else:
                name = participant.first_name
                mentions.append(f'<a href="tg://user?id={participant.id}">{name}</a> ')

        mentions = [mentions[i:i + 5] for i in range(0, len(mentions), 5)]
        for mention in mentions:
            await event.respond(args + ''.join(mention) + f' ({mentions.index(mention) + 1}/{len(mentions)})',
                                parse_mode='html')


try:
    client.run_until_disconnected()
finally:
    client.disconnect()
