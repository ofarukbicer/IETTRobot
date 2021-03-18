# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Robot.Edevat.zenginLog import log_yolla, hata_log
from pyrogram import Client, filters
from pyrogram.types import Message
from Robot.Edevat._pyrogram.pyro_yardimcilari import yanitlanan_mesaj

from Robot.Edevat.IETT import IETT

from pyrogram.types import InlineKeyboardMarkup, CallbackQuery
from Robot.Edevat._pyrogram.inline_buton_olusturucu import buton_olustur

from pyshorteners import Shortener

@Client.on_message(filters.regex(r'(.*)'))
async def komut(client:Client, message:Message):
    # < Başlangıç
    await log_yolla(client, message)
    yanit_id  = await yanitlanan_mesaj(message)
    ilk_mesaj = await message.reply("__Bekleyin..__",
        reply_to_message_id      = yanit_id,
        disable_web_page_preview = True
    )
    girilen_yazi        = message.text
    #------------------------------------------------------------- Başlangıç >

    try:
        veriler = IETT(girilen_yazi).bilgi_ver
    except KeyError:
        await ilk_mesaj.edit(f'__Sensin__ **{girilen_yazi}**')
        return

    kisalt = Shortener()

    butonlar = {
        f"{veri['durak_yeri']} ▶️ {veri['durak_yonu']}" : kisalt.qpsru.short(veri['sefer_bilgi'])
        # f"{veri['durak_yeri']} ▶️ {veri['durak_yonu']}" : veri['sefer_bilgi']
            for veri in veriler
    }

    await ilk_mesaj.edit(
        f"🚏 **{girilen_yazi.capitalize()}** __için IETT Hat Bilgileri..__",
        reply_markup=InlineKeyboardMarkup(buton_olustur(butonlar=butonlar, adet=1, link=True))
    )

@Client.on_callback_query(filters.regex(pattern=r"^bakalim$"))
async def bakalim_data(client:Client, callback_query:CallbackQuery):
    await callback_query.answer('Afferin bastın kanka', show_alert=True)