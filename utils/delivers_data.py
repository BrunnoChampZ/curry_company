import pandas as pd

def read_processed_data():
    """ Esta função lê o dataset processado"""
    return pd.read_csv("dataset/processed/data.csv")

def df_avg_ratings_per_deliver(df2):
    """ Esta função calcula a média de avaliações por entregador"""
    return df2.loc[:,["delivery_person","delivery_person_ratings"]].groupby("delivery_person").mean().reset_index()

def df_avg_ratings_per_traffic(df2):
    """ Esta função calcula a média de avaliações por trânsito"""
    df_aux = df2.loc[:, ["delivery_person_ratings","road_traffic_density"]].groupby("road_traffic_density").agg({"delivery_person_ratings": ["mean", "std"]}).reset_index()
    df_aux.columns = ["road_traffic_density", "delivery_person_ratings_mean", "delivery_person_ratings_std"]
    return df_aux

def df_avg_ratings_per_weather(df2):
    """ Esta função calcula a média de avaliações por clima"""
    df_aux = df2.loc[:, ["delivery_person_ratings","weatherconditions"]].groupby("weatherconditions").agg({"delivery_person_ratings": ["mean", "std"]}).reset_index()
    df_aux.columns = ["weatherconditions", "delivery_person_ratings_mean", "delivery_person_ratings_std"]
    return df_aux

def top_10_fastest_delivers(df2):
    """ Esta função calcula os 10 entregadores mais rápidos por cidade"""
    df_aux = df2.groupby(['city', 'delivery_person'])['time_taken(min)'].mean().sort_values().groupby('city').head(10).reset_index()
    return df_aux

def top_10_slowest_delivers(df2):
    """ Esta função calcula os 10 entregadores mais lentos por cidade"""
    df_aux = df2.groupby(['city', 'delivery_person'])['time_taken(min)'].mean().sort_values(ascending=False).groupby('city').head(10).reset_index()
    return df_aux

def best_vehicle_condition(df2):
    """ Esta função mostra o nome da melhor condição de veículo"""
    return df2.groupby("type_of_vehicle")["vehicle_condition"].median().idxmax()

def worst_vehicle_condition(df2):
    """ Esta função mostra o nome da pior condição de veículo"""
    return df2.groupby("type_of_vehicle")["vehicle_condition"].median().idxmin()
