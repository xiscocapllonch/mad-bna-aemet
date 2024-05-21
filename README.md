# WEEKLY WEATHER MAD BNA BOT

Repository to get [©AEMET](https://www.aemet.es/es/eltiempo/prediccion/municipios/barcelona-id08019)
weather predictions and publish them on telegram channels
(E.g. [Weekly Weather Mad Bna Channel](https://web.telegram.org/z/#-1002008440054)). Why? To be able to access this information
in areas of low or sporadic mobile coverage.

## INSTALL

```bash
pipenv install
```

## RUN

You must create a file called `.env` in the root folder with this environment vars or set those vars when you call the
script:

```dotenv
TELEGRAM_TOKEN=6352785479:MyTelegram-TOken
WEEKLY_FORECAST_CHAT_ID=-1002008440054
```

#### TELEGRAM_TOKEN

You will need a token for the telegram bot that writes the messages. Learn more about it here:
[https://core.telegram.org/bots/api#authorizing-your-bot](https://core.telegram.org/bots/api#authorizing-your-bot)

#### WEEKLY_FORECAST_CHAT_ID

The telegram channel where the messages will be published and in which your bot must have admin write permissions, has
an id similar to ```-10054478265423```.

```bash
pipenv run python main.py
```
