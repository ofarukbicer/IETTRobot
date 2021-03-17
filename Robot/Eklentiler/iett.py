# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Robot.Edevat.zenginLog import log_yolla, hata_log
from pathlib import Path
from pyrogram import Client, filters
from pyrogram.types import Message
from Robot.Edevat._pyrogram.pyro_yardimcilari import yanitlanan_mesaj
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from urllib.parse import quote
import urllib3
import requests
import json
from fake_useragent import UserAgent

@Client.on_message(filters.command(['iett'], ['!','.','/']))
async def komut(client:Client, message:Message):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    await log_yolla(client, message)
    yanit_id  = await yanitlanan_mesaj(message)
    ilk_mesaj = await message.reply("__Bekleyin..__",
        reply_to_message_id      = yanit_id,
        disable_web_page_preview = True
    )
    girilen_yazi = message.text
    hatdurak = quote(girilen_yazi[6:])
    if hatdurak == "":
        await ilk_mesaj.edit("__Arama yapabilmek için `Hat` ya da `Durak` girmelisiniz..__")
        return
    try:
        url = "https://www.iett.istanbul/tr/main/ajaxHatDurakAra/?q="+hatdurak
        kimlik = {'User-Agent': UserAgent().random}
        istek = requests.get(url, headers=kimlik, verify=False).json()
    except Exception as hata:
        await hata_log(hata, client, ilk_mesaj)
        await ilk_mesaj.edit("Veriler çekilirken bir hata oluştu.")
        return

    try:
        link_butonu = []
        if istek[0]["total_count"] != 0:
            for durak in istek[0]["items"]:
                if durak['type'] == "station":
                    link_butonu.append(
                        [
                            InlineKeyboardButton(f"🚏 {durak['name']}", url=f"https://iett.istanbul/tr/main/duraklar//-İETT-Duraktan-Geçen-Hatlar-Durak-Bilgileri-Hattın-Duraktan-Geçiş-Saatleri")
                        ]
                    )
                else:
                    continue
            await ilk_mesaj.edit(
                "Senin için bulabildiğim duraklar",
                reply_markup = InlineKeyboardMarkup(link_butonu)
            )
        else:
            await ilk_mesaj.edit("Bu değere ait durak bulamadım.")
    except Exception as hata:
        await hata_log(hata, client, ilk_mesaj)
        await ilk_mesaj.edit("Sistemsel bir hata oluştu")
        return