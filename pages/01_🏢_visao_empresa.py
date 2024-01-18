import streamlit as st
from datetime import datetime
from PIL import Image
from utils import enterprise_data as ed

def make_sidebar(df):
    """ Esta função cria a sidebar"""
    st.header("Marketplace - Visão Empresa")

    image = Image.open("./img/logo.jpg")
    st.sidebar.image(image, width=120)

    st.sidebar.markdown("# Cury Company")
    st.sidebar.markdown("## Cury Fastest Delivery in Town")
    st.sidebar.markdown("""---""")

    st.sidebar.markdown("# Selecione uma data limite")

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
    """ Esta função cria a página Visão Empresa"""
    st.set_page_config(page_title='Visão Empresa', page_icon=':graph:', layout='wide')

    df = ed.read_processed_data()

    date_slider, traffic_options = make_sidebar(df)

    st.dataframe(df)

    tab1, tab2, tab3 = st.tabs(["Visão Gerencial", "Visão Tática", "Visão Geográfica"])

    with tab1:
        with st.container():
            # Order Metric
            fig = ed.order_metric()
            st.markdown("# Orders by Day")
            st.plotly_chart(fig, use_container_width=True)
            
        with st.container():
            col1, col2 = st.columns(2)  
            
            with col1:
                fig = ed.traffic_order_share()
                st.header("Traffic Order Share")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = ed.traffic_order_city()
                st.header("Traffic Order City")
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        with st.container():
            st.markdown("# Order by Week")
            fig = ed.order_by_week()
            st.plotly_chart(fig, use_container_width=True)
        
        with st.container():
            st.markdown("# Order Share by Week")
            fig = ed.order_by_week()
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("# Country Maps")
        ed.country_maps()
    
    return None

if __name__ == "__main__":
    main()