"""
This file handles interaction with the Toecan bike external API
"""
# imports
import requests, time, datetime

# constants
BASE_URL = "https://api.external.bike.toecan.tech/"

def get_commuting_trips(api_key, ts_start=time.time()-24*60*60*7, ts_end=time.time()):
    """
    Fetches commuting trips data from the specified API within the given time range.

    Args:
        api_key (str): The API key used for authentication.
        ts_start (int): The start timestamp (epoch) for the data retrieval. Uses the last 7 days by default.
        ts_end (int): The end timestamp (epoch) for the data retrieval. Uses the current timestamp by default.

    Returns:
        list: A list of commuting trips data retrieved from the API.
    """
    headers = {
        "token": api_key
    }
    r = requests.get(BASE_URL + "commute_trips", headers=headers, params={"ts_start": ts_start, "ts_end": ts_end})
    # raise an exception if the request was unsuccessful
    r.raise_for_status()
    return r.json()

def get_detailed_commuting_trip(api_key, trip_uuid):
    """
    Fetches detailed commuting trip data from the specified API.

    Args:
        api_key (str): The API key used for authentication.
        trip_uuid (str): The ID of the trip to be retrieved.

    Returns:
        dict: A dictionary containing detailed commuting trip data retrieved from the API.
    """
    headers = {
        "token": api_key
    }
    r = requests.get(BASE_URL + f"detailed_commute_trips/{trip_uuid}", headers=headers)
    # raise an exception if the request was unsuccessful
    r.raise_for_status()
    return r.json()

def create_csv(api_key, filepath="toecanbike_commuting_trips.csv", ts_start=time.time()-24*60*60*7, ts_end=time.time()):
    """
    Creates a CSV file containing commuting trips data from the specified API within the given time range.

    Args:
        api_key (str): The API key used for authentication.
        filepath (str): The path to the CSV file to be created. Defaults to "toecanbike_commuting_trips.csv".
        ts_start (int): The start timestamp (epoch) for the data retrieval. Uses the last 7 days by default.
        ts_end (int): The end timestamp (epoch) for the data retrieval. Uses the current timestamp by default.

    Returns:
        list: A list of commuting trips data retrieved from the API.
    """
    trips = get_commuting_trips(api_key, ts_start, ts_end)
    with open(filepath, "w") as f:
        f.write("trip_uuid,Start time,End Time,Distance (m),duration (s)\n")
        for trip in trips:
            f.write(f"{trip['trip_uuid']}, {datetime.datetime.utcfromtimestamp(trip['ts_start']).isoformat()},{datetime.datetime.utcfromtimestamp(trip['ts_end']).isoformat()},{trip['trip_distance']},{trip['duration']}\n")
    return trips




if __name__ == "__main__":
    # Example usage
    api_key = "a860ab6e-623f-49e2-a66a-b2109d16f590"
    trips = get_commuting_trips(api_key)
    trip = get_detailed_commuting_trip(api_key, trips[0]["trip_uuid"])
    trips = create_csv(api_key)




