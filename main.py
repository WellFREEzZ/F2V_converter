import os
from telethon import TelegramClient, events, utils, types
from converter import wav_to_ogg, mp3_to_ogg, b_wf
import settings

bot = TelegramClient('bot', api_id=settings.api_id, api_hash=settings.api_hash)


def prepare(path, fmt):
    if fmt is None:
        return path
    if fmt == 'wav':
        r = wav_to_ogg(path)
        os.remove(path)
        return r
    if fmt == 'mp3':
        r = mp3_to_ogg(path)
        os.remove(path)
        return r


@bot.on(events.NewMessage())
async def ma(event):
    msg = event.message
    if msg.media:
        if 'audio' in msg.media.document.mime_type:
            fmt = None
            if 'wav' in msg.media.document.mime_type:
                fmt = 'wav'
            elif 'mpeg' in msg.media.document.mime_type:
                fmt = 'mp3'

            p_ = await bot.download_media(message=event.message,
                                          file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
            prst = prepare(p_, fmt)
            print(prst)
            wf, dur = b_wf(prst)

            r_ = await bot.send_file(event.sender.id, prst, voice_note=True,
                                     reply_to=event,
                                     attributes=[types.DocumentAttributeAudio(
                                         duration=dur,
                                         voice=True,
                                         waveform=bytes(wf)  # bytes(wf)
                                     )])
            os.remove(prst)


if __name__ == '__main__':
    bot.start(bot_token=settings.bot_token)
    bot.loop.run_forever()
