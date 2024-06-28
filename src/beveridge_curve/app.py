# app.py
import streamlit as st
import data_loader as dl
import charts_creator as cc
import importlib.resources
import pandas as pd


def main():
    package_dir = importlib.resources.files("beveridge_curve")
    st.set_page_config(
        page_title="DBnomics Beveridge Curve",
        page_icon=str(package_dir / "images/favicon.png")
    )
    st.image(str(package_dir / "images/dbnomics.svg"), width=300)
    st.title(':blue[Beveridge\'s curve]')

    tab1, tab2 = st.tabs(['Explanations', "Charts"])
    with tab1:
        st.subheader(":blue[What is Beveridge's Curve?]")
        st.write(
            "The Beveridge curve is a graphical representation of the relationship between unemployment and job vacancy rates. It is used to visualize the inverse relationship between the job vacancy rate and the unemployment rate.")

    with tab2:
        country = st.selectbox('Select a country', ['France', 'United States', 'Germany', 'Euro Area'])

        # Initialiser les données pour obtenir la plage de dates complète
        df_fr, df_us, df_ger, df_eu = dl.prepare_data()

        # Trouver les dates minimum et maximum parmi les DataFrames
        min_date = min(df_fr['original_period'].min(), df_us['original_period'].min(), df_ger['original_period'].min(),
                       df_eu['original_period'].min())
        max_date = max(df_fr['original_period'].max(), df_us['original_period'].max(), df_ger['original_period'].max(),
                       df_eu['original_period'].max())

        # Sélection des dates avec un slider
        start_date, end_date = st.slider(
            "Select date range",
            min_value=min_date.to_pydatetime(),
            max_value=max_date.to_pydatetime(),
            value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
            format="YYYY-MM-DD"
        )

        if st.button("Enter"):
            df_fr, df_us, df_ger, df_eu = dl.prepare_data(start_date=start_date, end_date=end_date)

            # Afficher le graphique correspondant
            if country == 'France':
                st.subheader('Beveridge curve for France')
                fig = cc.plot_beveridge_curve(df_fr, 'France')
                st.plotly_chart(fig)
            elif country == 'United States':
                st.subheader('Beveridge curve for the United States')
                fig = cc.plot_beveridge_curve(df_us, 'United States')
                st.plotly_chart(fig)
            elif country == 'Germany':
                st.subheader('Beveridge curve for Germany')
                fig = cc.plot_beveridge_curve(df_ger, 'Germany')
                st.plotly_chart(fig)
            elif country == 'Euro Area':
                st.subheader('Beveridge curve for the Euro Area')
                fig = cc.plot_beveridge_curve(df_eu, 'Euro Area')
                st.plotly_chart(fig)


if __name__ == '__main__':
    main()
