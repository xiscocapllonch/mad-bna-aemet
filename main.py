import os
import asyncio
from datetime import datetime, timezone

from dotenv import load_dotenv
from telegram import Bot
from playwright.async_api import async_playwright

load_dotenv()

URL = 'https://www.aemet.es/en/eltiempo/prediccion/municipios/'
LOCATIONS = [
    {'aemet_id': 'castellvell-del-camp-id43042', 'caption': 'CP0 Castellvell del Camp'},
    {'aemet_id': 'vic-id08298', 'caption': 'CP0 208 Vic'},
    {'aemet_id': 'puigcerda-id17141', 'caption': 'CP1 34 Puigcerdà'},
    {'aemet_id': 'sabinanigo-id22199', 'caption': 'CP2 53 Sabiñánigo'},
    {'aemet_id': 'barbastro-id22048', 'caption': 'CP2 176 Barbastro'},
    {'aemet_id': 'tortosa-id43155', 'caption': 'CP2 359 Tortosa'}
]
TMP_IMG_PATH = 'tmp.jpg'


async def get_weather_image(location_id):
    full_url = URL + location_id
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1024, 'height': 1150})
        await page.goto(full_url, timeout=60000)
        await page.wait_for_timeout(500)
        await page.screenshot(path=TMP_IMG_PATH, clip={"x": 32, "y": 655, "width": 962, "height": 1100})
        await browser.close()


async def main():
    telegram_token = os.getenv('TELEGRAM_TOKEN', '')
    chat_id = os.getenv('WEEKLY_FORECAST_CHAT_ID', '')
    bot = Bot(telegram_token)

    formatted_now = datetime.now(timezone.utc).strftime("%H:%M on %b %d")
    header_text = (
        f"Forecast updated at {formatted_now} UTC. Weather for the Check Points defined in the route"
        f" between Madrid and Barcelona. Updates every 6 hours.\n\n"
        f"<a href='{URL}'>©AEMET</a>"
    )

    async with bot:
        await bot.send_message(
            text=header_text,
            parse_mode='HTML',
            chat_id=chat_id
        )

        for location in LOCATIONS:
            aemet_id = location['aemet_id']
            caption = location['caption']
            caption_link = (
                f"<a href='{URL + aemet_id}'>{caption}</a> --> "
                f"<a href='{URL}horas/{aemet_id}'> Hourly detail</a>"
            )

            await get_weather_image(aemet_id)

            await bot.send_photo(
                photo=open(TMP_IMG_PATH, 'rb'),
                chat_id=chat_id,
                parse_mode='HTML',
                caption=caption_link
            )

            os.remove(TMP_IMG_PATH)


if __name__ == '__main__':
    asyncio.run(main())
