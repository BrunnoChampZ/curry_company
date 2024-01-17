import pandas as pd
import inflection
import haversine

RAW_DATA_PATH = f"./dataset/raw/train.csv"

def rename_columns(dataframe):
    """ Esta função renomeia as colunas do dataset"""	
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new

    return df

def adjust_columns_order(dataframe):
    """ Esta função ajusta a ordem das colunas do dataset"""
    df = dataframe.copy()

    new_cols_order = [
        
        "id",
        "delivery_person",
        "delivery_person_age",
        "delivery_person_ratings",
        "restaurant_latitude",
        "restaurant_longitude",
        "delivery_location_latitude",
        "delivery_location_longitude",
        "distance(km)",
        "order_date",
        "time_orderd",
        "time_order_picked",
        "week_of_year",
        "weatherconditions",
        "road_traffic_density",
        "vehicle_condition",
        "type_of_order",
        "type_of_vehicle",
        "multiple_deliveries",
        "festival",
        "city",
        "time_taken(min)",
    ]

    return df.loc[:, new_cols_order]

def change_types(dataframe):
    """ Esta função altera os tipos das colunas do dataset"""
    df = dataframe.copy()

    df = df[df["delivery_person_age"] != "NaN "]
    df = df[df["delivery_person_ratings"] != "NaN "]
    df = df[df["time_orderd"] != "NaN "]
    df = df[df["road_traffic_density"] != "NaN "]
    df = df[df["multiple_deliveries"] != "NaN "]
    df = df[df["festival"] != "NaN "]
    df = df[df["city"] != "NaN "]

    df['delivery_person_age'] = pd.to_numeric(df['delivery_person_age'], errors='coerce')
    df['delivery_person_ratings'] = df['delivery_person_ratings'].astype(float)
    df['order_date'] = pd.to_datetime(df['order_date'], format='%d-%m-%Y')
    df['time_taken(min)'] = df['time_taken(min)'].apply(lambda x: x.split("(min)")[1]).astype(int)

    return df

def distance(dataframe):
    """ Esta função calcula a distância entre o restaurante e o cliente"""	
    df = dataframe.copy()

    df["distance(km)"] = df.apply(lambda x: haversine.haversine((x["restaurant_latitude"], x["restaurant_longitude"]), (x["delivery_location_latitude"], x["delivery_location_longitude"])), axis=1)

    return df

def week_of_year(dataframe):
    """ Esta função calcula e cria a coluna semana do ano"""
    df = dataframe.copy()

    df['week_of_year'] = df['order_date'].dt.strftime('%U')

    return df

def process_data(file_path):
    """ Esta função processa os dados"""
    df = pd.read_csv(file_path)
    df = df.dropna()
    df = rename_columns(df)
    df = change_types(df)
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df = distance(df)
    df = week_of_year(df)
    df = df.drop_duplicates()
    df = adjust_columns_order(df)
    df.to_csv("./dataset/processed/data.csv", index=False)

    return df