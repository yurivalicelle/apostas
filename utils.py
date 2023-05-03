# utils.py
import asyncio
import json
import os
import logging
from datetime import datetime, timedelta

import aiogram
import pytz
import requests
from aiogram import Bot
from googletrans import Translator
from tenacity import retry, stop_after_attempt, wait_exponential

from config import HEADERS, OPERATION_NAME, QUERY_STRING, TELEGRAM_TOKEN, CHAT_ID, QUERY_STRING_PREDICTION, \
    OPERATION_NAME_PREDICTION


async def send_telegram_message(match):
    logging.info(f"Sending message for match: {match}")
    if not is_event_already_sent(match):
        bot = Bot(token=TELEGRAM_TOKEN)
        try:
            await bot.send_message(chat_id=CHAT_ID, text=match)
            session = await bot.get_session()
            await session.close()
            add_event_to_file(match)
        except aiogram.exceptions.RetryAfter as e:
            session = await bot.get_session()
            await session.close()
            await asyncio.sleep(e.timeout)  # Sleep for the required duration
            await send_telegram_message(match)  # Retry sending the message
        except Exception:
            session = await bot.get_session()
            await session.close()
            # print(e)


def convert_timezone(date_string, from_tz, to_tz):
    logging.info(f"Converting timezone from {from_tz} to {to_tz}")
    original_tz = pytz.timezone(from_tz)
    target_tz = pytz.timezone(to_tz)

    original_datetime = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    original_datetime = original_tz.localize(original_datetime)
    target_datetime = original_datetime.astimezone(target_tz)

    return target_datetime.strftime("%Y-%m-%dT%H:%M:%S%z")


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def fetch_data(prediction=None):
    logging.info("Fetching data...")
    try:
        if prediction:
            variables = {
                "sportSlugs": [
                    "soccer",
                    "ice-hockey",
                    "basketball",
                    "tennis",
                    "futsal",
                    "mma",
                    "snooker",
                    "baseball",
                    "american-football",
                    "csgo",
                    "volleyball",
                    "rugby",
                    "handball"
                ],
                "lang": "en",
                "timezoneOffset": -180,
                "limit": 6,
                "skip": 0,
                "topMatches": True,
                "day": "today"
            }
            payload = json.dumps({
                "query": QUERY_STRING_PREDICTION,
                "operationName": OPERATION_NAME_PREDICTION,
                "variables": variables
            })
        else:
            variables = {
                "lang": "en",
                "timezoneOffset": -180,
                "sportSlug": "top"
            }

            payload = json.dumps({
                "query": QUERY_STRING,
                "operationName": OPERATION_NAME,
                "variables": variables
            })

        url = "https://scores24.live/graphql"

        response = requests.post(url, headers=HEADERS, data=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        logging.exception("Error in fetch_data")
        pass


def remove_duplicates(items):
    logging.info("Removing duplicates from items")
    items_vistos = set()
    itens_unicos = []

    for item in items:
        match_slug = item["id"]
        if match_slug not in items_vistos:
            itens_unicos.append(item)
            items_vistos.add(match_slug)

    return itens_unicos


def process_results(results, displayed_matches):
    logging.info("Processing results")
    new_matches = []

    for result in results:
        match_id = result["match"]["slug"]
        if match_id not in displayed_matches:
            match_info = create_match_info(result["match"], result["prediction"])
            new_matches.append(match_info)
            displayed_matches.add(match_id)

    # Ordena a lista new_matches com base na data
    new_matches_sorted = sorted(new_matches, key=lambda match: match["brazil_match_date"])

    return new_matches_sorted


def process_results_prediction(results, displayed_matches):
    logging.info("Processing results prediction")
    new_matches = []
    current_datetime = datetime.now(pytz.timezone("America/Sao_Paulo"))

    for result in results:
        for item in result["items"]:
            utc_match_date = item["match"]["matchDate"]
            brazil_match_date = convert_timezone(utc_match_date, "UTC", "America/Sao_Paulo")
            brazil_match_datetime = datetime.strptime(brazil_match_date, "%Y-%m-%dT%H:%M:%S%z")
            if float(item["predictionValue"]) <= 0 or brazil_match_datetime < current_datetime:
                continue
            match_id = item["match"]["slug"] + "-prediction"
            if match_id not in displayed_matches:
                match_info = create_match_info(item["match"], item["prediction"], item["predictionValue"])
                new_matches.append(match_info)
                displayed_matches.add(match_id)

    # Ordena a lista new_matches com base na data
    new_matches_sorted = sorted(new_matches, key=lambda match: match["brazil_match_date"])

    return new_matches_sorted


def create_match_info(match, prediction, prediction_value=None):
    logging.info(f"Creating match info for match: {match['slug']}")
    utc_match_date = match["matchDate"]
    brazil_match_date = convert_timezone(utc_match_date, "UTC", "America/Sao_Paulo")

    # Criar um objeto Translator
    translator = Translator()

    sport_slug = str(match["sportSlug"]).replace("-", " ").title()

    # Traduzir para português
    sport_slug = translator.translate(sport_slug, dest='pt').text

    # Converter a string em um objeto datetime
    date_object = datetime.strptime(brazil_match_date, "%Y-%m-%dT%H:%M:%S%z")

    # Formatar o objeto datetime para o formato desejado (dd/mm/YYYY H:M)
    formatted_date = date_object.strftime("%d/%m/%Y %H:%M")

    match_info = {
        "id": match["slug"] if prediction_value is None else match["slug"] + "-prediction",
        "team1": match["teams"][0]["name"],
        "team2": match["teams"][1]["name"],
        "sport_slug": str(sport_slug).title(),
        "brazil_match_date": brazil_match_date,
        "brazil_match_formatted_date": formatted_date,
        "match_slug": match["slug"],
        "prediction_value": prediction_value,
        "prediction": prediction
    }

    return match_info


def add_event_to_file(event, file_path="events_sent.json"):
    logging.info(f"Adding event to file: {event}")
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    with open(file_path, "r") as f:
        events = json.load(f)

    events.append({"event": event, "date_added": datetime.now().isoformat()})

    with open(file_path, "w") as f:
        json.dump(events, f)


def is_event_already_sent(event, file_path="events_sent.json"):
    logging.info(f"Checking if event is already sent: {event}")
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r") as f:
        events = json.load(f)

    for e in events:
        if e["event"] == event:
            return True

    return False


def remove_old_events(days_to_keep=7, file_path="events_sent.json"):
    logging.info(f"Removing old events, keeping events from last {days_to_keep} days")
    if not os.path.exists(file_path):
        return

    with open(file_path, "r") as f:
        events = json.load(f)

    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    events = [e for e in events if datetime.fromisoformat(e["date_added"]) > cutoff_date]

    with open(file_path, "w") as f:
        json.dump(events, f)
