import pandas as pd
import datetime
import json
import csv
import matplotlib.pyplot as plt

file_path = "QuickShare_2406070143/aa94e0f5-ac35-40a7-b302-c9e12396ba8c.com.samsung.health.exercise.live_data.json"


# Open the file
def json_to_csv(json_file):
    with open(file_path, "r") as json_data:
        data = json.load(json_data)

        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
        else:
            df = pd.json_normalize(data)
            print("The data has been normalized")

        json_data.close()
    return df.to_csv("heartbeat_data_csv.csv", index=False)


# json_to_csv(file_path)

def unix_time_conversion(heartbeat_df):
    heartbeat_df["start_time"] = pd.to_datetime(heartbeat_df["start_time"], unit='ms')

    return heartbeat_df.to_csv("converted_heartbeat_data_csv.csv", index=False)


dataframe = pd.read_csv("heartbeat_data_csv.csv")
unix_time_conversion(dataframe)



def plotting_heartbeat(converted_heartbeat_df):
    converted_heartbeat_df.plot(x = "start_time")
    plt.xlabel("Time")
    plt.ylabel("BPM")
    plt.show()

    return ...

converted_unix_heartbeat = pd.read_csv("converted_heartbeat_data_csv.csv")
plotting_heartbeat(converted_unix_heartbeat)
