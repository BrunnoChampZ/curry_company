import pandas as pd
from haversine import haversine
import plotly.express as px
import numpy as np

def read_processed_data():
    """ Esta função lê o dataset processado"""
    return pd.read_csv("dataset/processed/data.csv")

def mean_distance(df2):
    """ Esta função calcula a distância média entre o restaurante e o cliente"""
    df2['distance'] = df2.apply(lambda x: haversine((x['restaurant_latitude'], x['restaurant_longitude']),
                                                          (x['delivery_location_latitude'], x['delivery_location_longitude'])), axis=1)
    
    mean_distance = np.round(df2["distance(km)"].mean(), 2)

    return mean_distance

def avg_std_time_graph_plotly(df2):
    """ Esta função cria um gráfico de barras com a média e o desvio padrão do tempo de entrega por cidade"""
    df_aux = df2.groupby("city")["time_taken(min)"].agg(["mean", "std"]).reset_index()

    fig = px.bar(df_aux, x="city", y="mean", error_y="std", title="Média e Desvio Padrão do Tempo de Entrega por Cidade",
                 labels={"mean": "Tempo Médio de Entrega (min)", "city": "Cidade", "std": "Desvio Padrão"},
                 hover_data={"mean": ":.2f", "std": ":.2f"},
                color="city",
                color_discrete_sequence=px.colors.qualitative.Plotly)
    return fig

def avg_std_time_table(df2):
    """ Esta função cria uma tabela com a média e o desvio padrão do tempo de entrega por cidade"""
    df_aux = df2.groupby(["city", "type_of_order"])["time_taken(min)"].agg(["mean", "std"]).reset_index()
    df_aux.columns = ["Cidade", "Tipo de Pedido", "Tempo médio(min)", "Desvio Padrão"]

    return df_aux

def number_delivers(df2):
    """ Esta função calcula o número de entregadores"""
    df_aux = len(df2.loc[:, "delivery_person"].unique())

    return df_aux

def avg_time_festival(df2):
    """ Esta função calcula o tempo médio de entrega nos dias de festival"""
    df_aux = df2.groupby("festival")["time_taken(min)"].mean().reset_index()
    df_aux.columns = ["Festival", "Tempo médio"]
    df_aux = np.round(df_aux.loc[df_aux["Festival"] == "Yes", "Tempo médio"]).round(2)

    return df_aux

def std_time_festival(df2):
    """ Esta função calcula o desvio padrão do tempo de entrega nos dias de festival"""
    df_aux = df2.groupby("festival")["time_taken(min)"].std().reset_index()
    df_aux.columns = ["Festival", "Desvio Padrão"]
    df_aux = np.round(df_aux.loc[df_aux["Festival"] == "Yes", "Desvio Padrão"]).round(2)

    return df_aux

def avg_time_without_festival(df2):
    """ Esta função calcula o tempo médio de entrega sem festival"""
    df_aux = df2.groupby("festival")["time_taken(min)"].mean().reset_index()
    df_aux.columns = ["Festival", "Tempo médio"]
    df_aux = np.round(df_aux.loc[df_aux["Festival"] == "No", "Tempo médio"]).round(2)

    return df_aux

def std_time_without_festival(df2):
    """ Esta função calcula o desvio padrão do tempo de entrega sem festival"""
    df_aux = df2.groupby("festival")["time_taken(min)"].std().reset_index()
    df_aux.columns = ["Festival", "Desvio Padrão"]
    df_aux = np.round(df_aux.loc[df_aux["Festival"] == "No", "Desvio Padrão"]).round(2)

    return df_aux

def avg_distance_by_city_graph(df2, fig=False):
    """ Esta função cria um gráfico de pizza com a média de distância por cidade"""
    cols = ["delivery_location_latitude", "delivery_location_longitude", "restaurant_latitude", "restaurant_longitude"]
    df2["distance"] = df2[cols].apply(lambda x: haversine((x["restaurant_latitude"], x["restaurant_longitude"]),
                                                          (x["delivery_location_latitude"], x["delivery_location_longitude"])), axis=1)

    if fig:
        avg_distance_by_city = df2.groupby("city")["distance"].mean().reset_index()
        fig = px.pie(avg_distance_by_city, names="city", values="distance", title="Média de Distância por Cidade",
                     labels= {"city": "Cidade", "distance": "Distância"}, color_discrete_sequence=px.colors.qualitative.Plotly)
        return fig
    
    return np.round(df2["distance"].mean(), 2)

def avg_std_time_on_traffic(df2):
    """ Esta função cria um gráfico de pizza com a média e o desvio padrão do tempo de entrega por condição de trânsito"""
    df_aux = df2.groupby(["city", "road_traffic_density"])["time_taken(min)"].agg(["mean", "std"]).reset_index()
    df_aux.columns = ["city", "road_traffic_density", "avg_time", "std_time"]

    fig = px.sunburst(df_aux, path=["city", "road_traffic_density"], values="avg_time", title = "Média de Tempo de Entrega por Cidade e Trânsito",
                       color="std_time", color_continuous_scale='RdBu',
                       color_continuous_midpoint=df_aux["std_time"].mean())
    return fig