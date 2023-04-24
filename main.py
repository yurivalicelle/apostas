import asyncio

from config import ENDPOINTS
from utils import (
    remove_duplicates,
    send_telegram_message,
    process_results,
    fetch_data,
    process_results_prediction,
    load_events_with_timestamps,
    save_event_with_timestamp
)


async def main():
    displayed_matches = load_events_with_timestamps()

    new_matches = []
    for query_type, min_facts_count, sport_slug in ENDPOINTS:
        model = fetch_data(query_type, sport_slug)

        if model:
            results = model["data"]["trends"]["result"]
            new_matches.extend(process_results(results, min_facts_count, displayed_matches))
        else:
            print(f"Failed to fetch data for endpoint: {query_type}")

    model_prediction = fetch_data(prediction=True)
    if model_prediction:
        results = model_prediction["data"]["SportPrediction"]
        new_matches.extend(process_results_prediction(results, displayed_matches))
    else:
        print(f"Failed to fetch data for endpoint: predictions")

    if new_matches:
        print("\nNovos eventos encontrados:")
        new_matches = remove_duplicates(new_matches)
        for match in new_matches:
            match_string = f'{match["sport_slug"]} {match["brazil_match_date"]} {match["match_slug"]} {match["prediction_value"]} {match["prediction"]}'

            print(match_string)
            await send_telegram_message(match_string)
            save_event_with_timestamp(match["id"], match["brazil_match_date"])


if __name__ == "__main__":
    asyncio.run(main())
