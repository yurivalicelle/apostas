# main.py
import asyncio
import logging
import sys
from datetime import datetime

import schedule

from config import Configuration
from utils import UtilsFacade, ProcessResults, ProcessResultsPrediction, remove_old_events

config = Configuration()
utils = UtilsFacade(ProcessResults)  # Pass the class, not an instance
utils_prediction = UtilsFacade(ProcessResultsPrediction)  # Pass the class, not an instance


# Configuring the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)


async def main():
    logging.info("Running main function")
    new_matches = []
    # model = fetch_data()
    model = utils.fetch_data()

    if model:
        results = model["data"]['TrendsTopQuery']
        new_matches.extend(utils.process_results(results))
        del results
    else:
        logging.error("Failed to fetch data for endpoint: trends")

    model_prediction = utils.fetch_data(prediction=True)
    if model_prediction:
        results = model_prediction["data"]["TopPredictionsQuery"]
        new_matches.extend(utils_prediction.process_results(results))
        del results
    else:
        logging.error("Failed to fetch data for endpoint: predictions")

    if new_matches:
        logging.info("\nNovos eventos encontrados:")
        for match in new_matches:
            favorite_teams = ['Atlanta Braves', 'Colorado Avalanche', 'Chicago Bulls', 'Dallas Cowboys']
            if match["sport_slug"] == 'Futebol' or match["team1"] in favorite_teams or match["team2"] in favorite_teams:
                match_id = match["id"]
                if isinstance(match["prediction"], list):
                    match_string = (
                        f'Esporte: {match["sport_slug"]}\n'
                        f'Data: {match["brazil_match_formatted_date"]}\n'
                        f'Partida: {match["team1"]} x {match["team2"]}\n'
                        f'Odd: {match["prediction_value"]}\n'
                        f'Predição: {match["fact"]}{match["prediction"][0]} {match["prediction"][1]}'
                    )
                else:
                    prediction = match["prediction"]["prediction"]
                    match_string = (
                        f'Esporte: {match["sport_slug"]}\n'
                        f'Data: {match["brazil_match_formatted_date"]}\n'
                        f'Partida: {match["team1"]} x {match["team2"]}\n'
                        f'Odd: {match["prediction_value"]}\n'
                        f'Predição: {match["fact"]}{prediction["type"][0]} {prediction["type"][1]}'
                    )

                logging.info(match_string)
                await utils.send_telegram_message(match_string, match_id)

        del new_matches

    remove_old_events()


async def run_scheduled_tasks():
    logging.info("Starting scheduled tasks")
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def run_main_if_seconds_match():
    now = datetime.now()
    if now.second in [0, 30]:
        logging.info("Running main if seconds match")
        await main()


if __name__ == "__main__":
    logging.info("Starting script")
    schedule.every(1).seconds.do(lambda: asyncio.create_task(run_main_if_seconds_match()))
    asyncio.run(run_scheduled_tasks())
