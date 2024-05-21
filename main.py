import os
import asyncio
import telegram
import imgkit

from dotenv import load_dotenv

load_dotenv()

URL = 'https://www.aemet.es/es/eltiempo/prediccion/municipios/'
LOCATIONS = [
    {
        'aemet_id': 'madrid-id28079',
        'caption': 'Madrid'
    },
    {
        'aemet_id': 'cifuentes-id19086',
        'caption': 'CP1 Cifuentes'
    },
    {
        'aemet_id': 'nuevalos-id50192',
        'caption': 'CP2 Nuévalos'
    },
    {
        'aemet_id': 'belchite-id50045',
        'caption': 'CP3 Belchite'
    },
    {
        'aemet_id': 'mequinenza-id50165',
        'caption': 'CP4 Mequinenza'
    },
    {
        'aemet_id': 'santa-coloma-de-queralt-id43139',
        'caption': 'CP5 Santa Coloma de Queralt'
    },
    {
        'aemet_id': 'barcelona-id08019',
        'caption': 'Barcelona'
    }
]
TMP_IMG_PATH = 'tmp.jpg'


def get_weather_image(location_id):
    imgkit.from_url(URL + location_id, TMP_IMG_PATH, {
        'crop-y': '670',
        'crop-h': '380',
        'crop-x': '35',
        'crop-w': '960'
    })


async def main():
    telegram_token = os.getenv('TELEGRAM_TOKEN', '')
    chat_id = os.getenv('WEEKLY_FORECAST_CHAT_ID', '')

    bot = telegram.Bot(telegram_token)

    for location in LOCATIONS:
        aemet_id = location.get('aemet_id')
        caption = location.get('caption')
        caption_link = f"<a href='{URL + aemet_id}'>{caption}</a> ©AEMET"

        get_weather_image(aemet_id)
        async with bot:
            await bot.send_photo(
                photo=open(TMP_IMG_PATH, 'rb'),
                chat_id=chat_id,
                parse_mode='HTML',
                caption=caption_link
            )
            os.remove(TMP_IMG_PATH)


if __name__ == '__main__':
    asyncio.run(main())
