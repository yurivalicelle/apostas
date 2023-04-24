# utils.py
import asyncio
import json
from datetime import datetime

import aiogram
import pytz
import requests
from aiogram import Bot
from tenacity import retry, stop_after_attempt, wait_exponential

from config import HEADERS, OPERATION_NAME, QUERY_STRING, TELEGRAM_TOKEN, CHAT_ID, QUERY_STRING_PREDICTION, \
    OPERATION_NAME_PREDICTION


async def send_telegram_message(match):
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        await bot.send_message(chat_id=CHAT_ID, text=match)
        session = await bot.get_session()
        await session.close()
    except aiogram.exceptions.RetryAfter as e:
        session = await bot.get_session()
        await session.close()
        await asyncio.sleep(e.timeout)  # Sleep for the required duration
        await send_telegram_message(match)  # Retry sending the message


def convert_timezone(date_string, from_tz, to_tz):
    original_tz = pytz.timezone(from_tz)
    target_tz = pytz.timezone(to_tz)

    original_datetime = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    original_datetime = original_tz.localize(original_datetime)
    target_datetime = original_datetime.astimezone(target_tz)

    return target_datetime.strftime("%Y-%m-%dT%H:%M:%S%z")


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def fetch_data(query_type=None, sport_slug=None, prediction=None):
    try:
        if prediction:
            variables = {
                "sportSlugs": [
                    "soccer",
                    "basketball",
                    "tennis",
                    "ice-hockey",
                    "volleyball",
                    "handball",
                    "baseball",
                    "american-football",
                    "rugby",
                    "mma",
                    "futsal",
                    "snooker",
                    "csgo"
                ],
                "lang": "en",
                "timezoneOffset": -180,
                "limit": 6,
                "skip": 0
            }
            payload = json.dumps({
                "query": QUERY_STRING_PREDICTION,
                "operationName": OPERATION_NAME_PREDICTION,
                "variables": variables
            })
        else:
            assert query_type in ['nearest', 'safe'], "Invalid query type. Must be one of 'nearest', 'safe'"
            variables = {
                "sortType": query_type,
                "skip": 0,
                "limit": 50000,
                "langSlug": "en",
                "timezoneOffset": -180,
                "includeFilter": False,
                "includeDays": False,
                "includeMarkets": False,
                "includeLeagueTypes": False,
                "includeLeagues": False,
                "includeSports": False,
                "includeResults": True,
                "includeHasDoubles": False
            }

            payload = json.dumps({
                "query": QUERY_STRING,
                "operationName": OPERATION_NAME,
                "variables": variables
            })
            if sport_slug:
                variables["sportSlug"] = sport_slug

        url = "https://scores24.live/graphql"

        response = requests.post(url, headers=HEADERS, data=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # print(f"Error: {e}")
        # raise
        pass


def remove_duplicates(items):
    items_vistos = set()
    itens_unicos = []

    for item in items:
        match_slug = item["id"]
        if match_slug not in items_vistos:
            itens_unicos.append(item)
            items_vistos.add(match_slug)

    return itens_unicos


def process_results(results, min_facts_count, displayed_matches):
    new_matches = []

    for result in results:
        match_id = result["id"]

        if result["factsCount"] > min_facts_count:
            if result["match"]["sportSlug"] == "soccer" and result["factsCount"] <= 4:
                continue
            utc_match_date = result["match"]["matchDate"]
            brazil_match_date = convert_timezone(utc_match_date, "UTC", "America/Sao_Paulo")

            match_info = {
                "id": match_id,
                "sport_slug": result["match"]["sportSlug"],
                "brazil_match_date": brazil_match_date,
                "match_slug": result["match"]["slug"],
                "prediction_value": result["prediction"]["value"],
                "prediction": result["prediction"]
            }

            if match_id not in displayed_matches:
                new_matches.append(match_info)
                displayed_matches.add(match_id)

    # Ordena a lista new_matches com base na data
    new_matches_sorted = sorted(new_matches, key=lambda match: match["brazil_match_date"])

    return new_matches_sorted


def process_results_prediction(results, displayed_matches):
    new_matches = []

    for result in results:
        for item in result["items"]:
            if float(item["predictionValue"]) <= 0:
                continue
            match_id = item["match"]["slug"]
            utc_match_date = item["match"]["matchDate"]
            brazil_match_date = convert_timezone(utc_match_date, "UTC", "America/Sao_Paulo")

            match_info = {
                "id": match_id,
                "sport_slug": result["slug"],
                "brazil_match_date": brazil_match_date,
                "match_slug": item["match"]["slug"],
                "prediction_value": item["predictionValue"],
                "prediction": item["prediction"]
            }

            if match_id not in displayed_matches:
                new_matches.append(match_info)
                displayed_matches.add(match_id)

    # Ordena a lista new_matches com base na data
    new_matches_sorted = sorted(new_matches, key=lambda match: match["brazil_match_date"])

    return new_matches_sorted


def save_event_ids(event_ids, filename="event_ids.txt"):
    with open(filename, "w") as file:
        for event_id in event_ids:
            file.write(f"{event_id}\n")


def load_event_ids(filename="event_ids.txt"):
    event_ids = set()
    try:
        with open(filename, "r") as file:
            for line in file:
                event_ids.add(line.strip())
    except FileNotFoundError:
        pass  # O arquivo ainda não existe, então retorne um conjunto vazio
    return event_ids
