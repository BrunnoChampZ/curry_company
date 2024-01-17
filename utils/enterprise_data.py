import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import folium.plugins


def read_processed_data():
    """ Esta função lê o dataset processado"""
    return pd.read_csv("dataset/processed/data.csv")

def country_maps():
        """ Esta função cria um mapa com a localização dos restaurantes"""
        df = read_processed_data()
        
        df_central_locations = df.groupby(['city', 'road_traffic_density']).agg({
        'restaurant_latitude': 'median',
        'restaurant_longitude': 'median'
        }).reset_index()

    # Mapeia as cores para os tipos de tráfego
        color_mapping = {'Jam': 'darkred', 'High': 'lightred', 'Medium': 'orange', 'Low': 'green'}

    # Cria o mapa
        map = folium.Map()

        for index, row in df_central_locations.iterrows():
            popup_content = f"<b>Cidade:</b> {row['city']}<br><b>Tipo de Tráfego:</b> {row['road_traffic_density']}"

            # Obtém a cor correspondente do mapeamento
            marker_color = color_mapping.get(row['road_traffic_density'], 'gray')

            folium.Marker([row['restaurant_latitude'], row['restaurant_longitude']],
                        popup=folium.Popup(popup_content, max_width=str(300)),
                        icon=folium.Icon(icon="home", color=marker_color)).add_to(map)

        folium_static(map, width=1024, height=600)

def order_share_by_week():
            """ Esta função cria um gráfico de linhas com a quantidade de pedidos por entregador por semana."""
            df = read_processed_data()

            grouped_df = (
                df[["id", "week_of_year"]]
                .groupby("week_of_year")
                .count()
                .reset_index()
                
            )

            fig = px.line(grouped_df, x = "week_of_year", y = "id", title="Pedidos por semana")
            return fig

def order_by_week():
            """ Esta função cria um gráfico de linhas com a quantidade de pedidos por semana"""
            df = read_processed_data()

            fig = px.line(df.groupby("week_of_year").size().reset_index(), x="week_of_year", y=0)

            return fig

def traffic_order_share():
            """ Esta função cria um gráfico de pizza com a quantidade de pedidos por condição de trânsito em porcentagem"""
            df = read_processed_data()

            fig = px.pie(df.groupby("road_traffic_density").size().reset_index(name="id"), 
             values="id", names="road_traffic_density",
             title="Pedidos por condição de trânsito",
            )

            return fig

def traffic_order_city():
            """ Esta função cria um gráfico de dispersão com a quantidade de pedidos por cidade"""
            df = read_processed_data()

            fig = px.scatter(df.groupby(["city", "road_traffic_density"]).size().reset_index(name="id"), 
            x="city", y="road_traffic_density", size="id", color="city", title="Pedidos por cidade e tipo de tráfego")

            return fig

def order_metric():
            """ Esta função cria um gráfico de barras com a quantidade de pedidos por dia"""
            df = read_processed_data()

            fig = px.bar(df.groupby("order_date").size().reset_index(name="id"), x="order_date", y="id")

            return fig
