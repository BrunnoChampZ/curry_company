import streamlit as st
from utils import delivers_data as dd
from datetime import datetime
from PIL import Image

def make_sidebar(df):
    """ Esta função cria a sidebar"""
    st.header("Marketplace - Visão Entregadores")

    image = Image.open("./img/logo.jpg")
    st.sidebar.image(image, width=120)

    st.sidebar.markdown("# Cury Company")
    st.sidebar.markdown("## Cury Fastest Delivery in Town")
    st.sidebar.markdown("""---""")

    st.sidebar.markdown("Selecione uma data limite")

    date_slider = st.sidebar.slider(
    "Até qual valor?",
    value=datetime(2022, 4, 6),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format="DD-MM-YYYY"
    )

    traffic_options = st.sidebar.multiselect(
    "Quais as condições do trânsito?",
    ["Low", "Medium", "High", "Jam"],
    default = ["Low", "Medium", "High", "Jam"])

    return date_slider, traffic_options

def main():
    """ Esta função cria a página Visão Entregadores"""
    st.set_page_config(page_title='Visão Entregadores', page_icon=':truck:', layout='wide')
    
    df = dd.read_processed_data()

    date_slider, traffic_options = make_sidebar(df)

    tab1, tab2, tab3 = st.tabs(["Visão Gerencial", "_", "_"])

    with tab1:
        with st.container():
            st.title("Overall Metrics")

            col1, col2, col3, col4 = st.columns(4, gap = "large")

            with col1:
                # A maior idade dos entregadores
                col1.metric("Maior idade", df["delivery_person_age"].max())

            with col2:
                # A menor idade dos entregadores
                col2.metric("Menor idade", df["delivery_person_age"].min())
            
            with col3:
                # Nome do veículo com melhor condição
                col3.metric("Melhor condição de veículo", dd.best_vehicle_condition(df))

            with col4:
                # Nome do veículo com pior condição
                col4.metric("Pior condição de veículo", dd.worst_vehicle_condition(df))

        with st.container():
            st.markdown("""---""")
            st.title("Avaliações")

            col1, col2 = st.columns(2)
            with col1:
                # Avaliação média por entregador
                st.subheader("Avaliação média por entregador")
                st.dataframe(dd.df_avg_ratings_per_deliver(df))
            
            with col2:
                # Avaliação média por trânsito
                st.subheader("Avaliação média por trânsito")
                st.dataframe(dd.df_avg_ratings_per_traffic(df))

                st.subheader("Avaliação média por clima")
                st.dataframe(dd.df_avg_ratings_per_weather(df))
        
        with st.container():
            st.markdown("""---""")
            st.title("Top 10 Entregadores")

            col1, col2 = st.columns(2)
            with col1:
                # Top 10 entregadores mais rápidos
                st.subheader("Top 10 entregadores mais rápidos")
                st.dataframe(dd.top_10_fastest_delivers(df))
            
            with col2:
                # Top 10 entregadores mais lentos
                st.subheader("Top 10 entregadores mais lentos")
                st.dataframe(dd.top_10_slowest_delivers(df))
    
    return None

if __name__ == "__main__":
    main()