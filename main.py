# main.py
import asyncio
from datetime import datetime, timedelta
import logging
import schedule
import cachetools

from utils import (
    remove_duplicates,
    send_telegram_message,
    process_results,
    fetch_data,
    remove_old_events, process_results_prediction
)

# Configuring the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


async def main(displayed_matches_main):
    logging.info("Running main function")
    new_matches = []
    model = fetch_data()

    if model:
        results = model["data"]['TrendsTopQuery']
        new_matches.extend(process_results(results, displayed_matches_main))
        del results
    else:
        logging.error("Failed to fetch data for endpoint: trends")

    model_prediction = fetch_data(prediction=True)
    if model_prediction:
        results = model_prediction["data"]["TopPredictionsQuery"]
        new_matches.extend(process_results_prediction(results, displayed_matches_main))
        del results
    else:
        logging.error("Failed to fetch data for endpoint: predictions")

    if new_matches:
        logging.info("\nNovos eventos encontrados:")
        new_matches = remove_duplicates(new_matches)
        for match in new_matches:
            displayed_matches_main.set(match["id"], None, ttl=timedelta(days=1))  # Store with a 1-day expiration
            if isinstance(match["prediction"], list):
                match_string = (
                    f'Esporte: {match["sport_slug"]}\n'
                    f'Data: {match["brazil_match_formatted_date"]}\n'
                    f'Partida: {match["team1"]} x {match["team2"]}\n'
                    f'Odd: {match["prediction_value"]}\n'
                    f'Predição: {match["prediction"][0]} {match["prediction"][1]}'
                )
            else:
                match_string = (
                    f'Esporte: {match["sport_slug"]}\n'
                    f'Data: {match["brazil_match_formatted_date"]}\n'
                    f'Partida: {match["team1"]} x {match["team2"]}\n'
                    f'Odd: {match["prediction_value"]}\n'
                    f'Predição: {match["prediction"]["type"][0]} {match["prediction"]["type"][1]}'
                )

            logging.info(match_string)
            await send_telegram_message(match_string)

        del new_matches

    remove_old_events()


async def run_scheduled_tasks():
    logging.info("Starting scheduled tasks")
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def run_main_if_seconds_match(displayed_matches_main):
    now = datetime.now()
    if now.second in [0, 30]:
        logging.info("Running main if seconds match")
        await main(displayed_matches_main)


if __name__ == "__main__":
    logging.info("Starting script")
    displayed_matches = cachetools.TTLCache(maxsize=1000, ttl=86400)  # Create a cache with 1-day expiration
    schedule.every(1).seconds.do(lambda: asyncio.create_task(run_main_if_seconds_match(displayed_matches)))
    asyncio.run(run_scheduled_tasks())
