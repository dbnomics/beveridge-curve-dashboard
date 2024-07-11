import importlib.resources

import streamlit as st
from PIL import Image

from . import charts_creator as cc
from . import data_loader as dl


def main():
    package_dir = importlib.resources.files("beveridge_curve")
    st.set_page_config(
        page_title="DBnomics Beveridge Curve",
        page_icon=str(package_dir / "images/favicon.png"),
    )
    st.image(str(package_dir / "images/dbnomics.svg"), width=300)
    st.title(":blue[Beveridge  Curve]")

    tab1, tab2 = st.tabs(["Explanations", "Charts"])
    with tab1:
        st.subheader(":blue[**What is Beveridge's Curve?**]")
        st.write(
            "\n"
            "The Beveridge curve is named after the publications of William Beveridge (1879-1963).\n"
            ' He was an English economist specializing in unemployment, prices, and wages. In 1944, his essay titled "*Full Employment in a Free Society*" was published.\n'
            "In this essay, Beveridge describes the negative relationship between the job vacancy rate (the job advertisements by companies) and the unemployment rate.\n"
            "\n"
        )
        beveridge_example = Image.open(package_dir / "images/beveridge_example.png")
        st.image(
            beveridge_example,
            caption="Beveridge Curve in theory",
            use_column_width=True,
            output_format="PNG",
            width=200
        )
        st.write(
            "\n"
            "\n"
            "\n"
            "**What is its usefulness for economists and policy choices?**\n"
            "\n"
            "\n"
            'For economists, it allows the analysis of "frictional" unemployment.\n'
            "This is short-term unemployment that occurs during the period needed to find a new job.\n"
            "It is different from cyclical unemployment (which occurs during a recession) and structural unemployment (due to structural changes).\n"
            "\n"
            "For a long time, the Walrasian model (neoclassical model) was the paradigm: the labor market was perfect.\n"
            'Thus, "frictional" unemployment could not exist: a vacant job was immediately filled by a new worker.\n'
            "However, unemployment is present and even very significant in our contemporary economies.\n"
            "Frictional unemployment, therefore, explains a more or less significant part of unemployment.\n"
            "\n"
            "\n"
            "**Why is the job vacancy rate high when the unemployment rate is low?**\n"
            "\n"
            "A low unemployment rate generally indicates a period of economic growth.\n"
            "The number of jobs created exceeds the labor supply, resulting in an increase in the job vacancy rate.\n"
            "Therefore, during a recession, the unemployment rate increases and the job vacancy rate decreases: the labor supply exceeds the labor demand.\n"
            "\n"
            "**Why is the job vacancy rate high when the unemployment rate is low?**\n"
            "\n"
            "A low unemployment rate generally indicates a period of economic growth.\n"
            "The number of jobs created exceeds the labor supply, leading to an increase in the job vacancy rate.\n"
            "\n"
            "Therefore, during a recession, the unemployment rate increases, and the job vacancy rate decreases: the labor supply exceeds the labor demand.\n"
            "Thus, it is not good for an economy to have both a high unemployment rate and a high number of job vacancies simultaneously.\n"
            "This means that even when many positions are available and the workforce is available, unemployment remains high.\n"
            "\n"
            'An expression has emerged: the Beveridge curve has become "drunk" in many countries in recent years.\n'
            "This is due to the explosion of involuntary unemployment. Indeed, in the United States, it can be observed that the Beveridge curve has changed shape over the last decade.\n"
        )

    with tab2:
        country = st.selectbox(
            "Select a country", ["France", "United States", "Germany", "Euro Area"]
        )

        # Initialiser les données pour obtenir la plage de dates complète
        df_fr, df_us, df_ger, df_eu = dl.prepare_data()

        # Trouver les dates minimum et maximum parmi les DataFrames
        min_date = min(
            df_fr["original_period"].min(),
            df_us["original_period"].min(),
            df_ger["original_period"].min(),
            df_eu["original_period"].min(),
        )
        max_date = max(
            df_fr["original_period"].max(),
            df_us["original_period"].max(),
            df_ger["original_period"].max(),
            df_eu["original_period"].max(),
        )

        # Sélection des dates avec un slider
        start_date, end_date = st.slider(
            "Select date range",
            min_value=min_date.to_pydatetime(),
            max_value=max_date.to_pydatetime(),
            value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
            format="YYYY-MM",
        )

        if st.button("Enter"):
            df_fr, df_us, df_ger, df_eu = dl.prepare_data(
                start_date=start_date, end_date=end_date
            )

            # Afficher le graphique correspondant
            if country == "France":
                st.subheader("Beveridge curve for France")
                fig = cc.plot_beveridge_curve(df_fr, "France")
                st.plotly_chart(fig)
            elif country == "United States":
                st.subheader("Beveridge curve for the United States")
                fig = cc.plot_beveridge_curve(df_us, "United States")
                st.plotly_chart(fig)
            elif country == "Germany":
                st.subheader("Beveridge curve for Germany")
                fig = cc.plot_beveridge_curve(df_ger, "Germany")
                st.plotly_chart(fig)
            elif country == "Euro Area":
                st.subheader("Beveridge curve for the Euro Area")
                fig = cc.plot_beveridge_curve(df_eu, "Euro Area")
                st.plotly_chart(fig)


if __name__ == "__main__":
    main()
