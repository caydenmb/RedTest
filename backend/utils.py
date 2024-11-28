import requests
from datetime import datetime, timedelta
import pytz
import logging

logger = logging.getLogger(__name__)

# API key and URL for PackDraw
api_key = "8cbb2008-f672-454b-907d-aebab8a81485"
url_template = "https://packdraw.com/api/v1/affiliates/leaderboard?after={start_time}&before={end_time}&apiKey={api_key}"
eastern = pytz.timezone("US/Eastern")

def fetch_leaderboard_data(sponsor):
    try:
        # Define start and end times
        start_time = datetime(2024, 11, 1, 0, 0, 0, tzinfo=eastern).isoformat()
        end_time = datetime.now(tz=eastern) - timedelta(seconds=15)
        logger.debug(f"Start time: {start_time}, End time: {end_time}")

        # Format URL with parameters
        url = url_template.format(start_time=start_time, end_time=end_time.isoformat(), api_key=api_key)
        logger.info(f"Fetching leaderboard data for sponsor: {sponsor} from URL: {url}")
        
        response = requests.get(url)
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response content: {response.text}")

        if response.status_code == 200:
            data = response.json()
            if 'leaderboard' in data:
                sorted_data = sorted(data['leaderboard'], key=lambda x: x['wagerAmount'], reverse=True)
                logger.info(f"Successfully fetched and sorted leaderboard data for sponsor: {sponsor}")
                return sorted_data[:11], 200
        logger.error(f"Failed to fetch leaderboard data for sponsor: {sponsor}, status code: {response.status_code}")
        return {"error": f"Failed to fetch leaderboard data. Status code: {response.status_code}"}, response.status_code

    except requests.exceptions.RequestException as req_error:
        logger.exception(f"RequestException occurred while fetching leaderboard data for sponsor: {sponsor}: {req_error}")
        return {"error": f"RequestException: {str(req_error)}"}, 500
    except Exception as e:
        logger.exception(f"An unexpected error occurred while fetching leaderboard data for sponsor: {sponsor}: {e}")
        return {"error": f"Unexpected error: {str(e)}"}, 500
