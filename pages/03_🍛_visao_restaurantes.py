import streamlit as st
from utils import restaurants_data as dd
from datetime import datetime
from PIL import Image

def make_sidebar(df):
    """ Esta função cria a sidebar"""
    st.header("Marketplace - Visão Restaurantes")

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
    """ Esta função cria a página Visão Restaurantes"""
    st.set_page_config(page_title='Visão Entregadores', page_icon=':truck:', layout='wide')

    df = dd.read_processed_data()

    date_slider, traffic_options = make_sidebar(df)

    tab1, tab2, tab3 = st.tabs(["Visão Gerencial", "_", "_"])

    with tab1:
        with st.container():
            st.title("Overall Metrics")

            col1, col2, col3, col4, col5, col6 = st.columns(6)

            with col1:
                # Número de entregadores
                col1.metric("Entregadores", dd.number_delivers(df))
            
            with col2:
                # A distância média entre restaurante e cliente
                col2.metric("Distância média (km)", dd.mean_distance(df))

            with col3:
                # Tempo médio de entrega nos dias de festival
                col3.metric("Tempo Médio de Entrega c/ Festival", dd.avg_time_festival(df))
            
            with col4:
                # Desvio padrão do tempo de entrega nos dias de festival
                col4.metric("Desvio Padrão de Entrega c/ Festival", dd.std_time_festival(df))
            
            with col5:
                # Tempo médio de entrega sem festival
                col5.metric("Tempo Médio de Entrega s/ Festival", dd.avg_time_without_festival(df))
            
            with col6:
                # Desvio padrão do tempo de entrega sem festival
                col6.metric("Desvio Padrão de Entrega s/ Festival", dd.std_time_without_festival(df))

        with st.container():
            st.markdown("""---""")
            st.title("Avaliações")

            col1, col2 = st.columns(2)
            with col1:
                fig = dd.avg_std_time_graph_plotly(df)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.dataframe(dd.avg_std_time_table(df))

        with st.container():
            st.markdown("""---""")
            st.title("Distribuição do Tempo de Entrega")

            col1, col2 = st.columns(2)

            with col1:
                fig = dd.avg_distance_by_city_graph(df, fig=True)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = dd.avg_std_time_on_traffic(df)
                st.plotly_chart(fig, use_container_width=True)
    return None

if __name__ == "__main__":
    main()