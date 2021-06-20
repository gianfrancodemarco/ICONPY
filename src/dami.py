import pandas as pd
import math


def get_oldest(dates):
    import dateutil.parser
    import datetime

    if len(dates.split(",")) == 1:
        return dates

    try:
        timestamps = []
        for date in dates.split(","):
            timestamps.append(datetime.datetime.timestamp(dateutil.parser.parse(date)))
        return (datetime.datetime.fromtimestamp(0) + datetime.timedelta(seconds=min(timestamps))).isoformat()
    except Exception as x:
        print(x)
        print(dates)


def get_cluster_sorted():
    df = pd.read_csv("C://Users//demarcog//Desktop//new dami//cluster_1.csv")
    df = df.append(df.sum(numeric_only=True), ignore_index=True)
    df = df.sort_values(by=249, axis=1, ascending=False)

    df = df.drop(df.columns[[0, 1, 2, 1341, 1342, 1343, 1344]], axis=1)
    df = df.drop(df.index[:-1])
    df.to_csv("C://Users//demarcog//Desktop//new dami//cluster_1_sorted.csv")

    for column in df:
        count = list(df[column])[-1]
        if math.isnan(count) or count < 10 or 'award' in column.lower():
            del df[column]

    df.loc[249].plot.bar()
