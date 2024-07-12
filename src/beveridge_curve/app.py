import importlib.resources

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu  # type: ignore

from beveridge_curve import charts_creator, data_loader


def main() -> None:
    package_dir = importlib.resources.files("beveridge_curve")
    st.set_page_config(
        page_title="DBnomics Beveridge Curve",
        page_icon=str(package_dir / "images/favicon.png"),
    )
    st.image(str(package_dir / "images/dbnomics.svg"), width=300)
    st.title(":blue[Beveridge  Curve]")

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css(package_dir / "assets/styles.css")

    st.markdown(
        """
        <style>
        hr {
            height: 1px;
            border: none;
            color: #333;
            background-color: #333;
            margin-top: 3px;
            margin-bottom: 3px;
        }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Explanations", "Beveridge Curve", "Sources"],
            icons=["book", "bar-chart", "search"],
            menu_icon=":",
            default_index=0,
        )

    if selected == "Explanations":
        st.subheader(":blue[**What is Beveridge's Curve?**]")
        st.write(
            "\n"
            "The Beveridge curve is named after the publications of William Beveridge (1879-1963).\n"
            ' He was an English economist specializing in unemployment, prices, and wages. In 1944, his essay titled "*Full Employment in a Free Society*" was published.\n'
            "In this essay, Beveridge describes the negative relationship between the job vacancy rate (the job advertisements by companies) and the unemployment rate.\n"
            "\n"
        )

        unemployment_rate = np.linspace(1, 12, 100)
        vacancies = 15 * np.exp(-0.3 * unemployment_rate)

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=unemployment_rate,
                y=vacancies,
                mode="lines",
                line=dict(color="gold", width=2),
                name="Beveridge Curve",
            )
        )

        fig.update_layout(
            title="Beveridge Curve in Theory",
            xaxis_title="Unemployment rate (%)",
            yaxis_title="Job vacancy rate (in thousands)",
            template="plotly_white",
        )

        st.plotly_chart(fig)

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

    if selected == "Beveridge Curve":
        country = st.selectbox(
            "Select a country", ["France", "United States", "Germany", "Euro Area"]
        )
        # Initialiser les données pour obtenir la plage de dates complète
        df_fr, df_us, df_ger, df_eu = data_loader.prepare_data()
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
            df_fr, df_us, df_ger, df_eu = data_loader.prepare_data(
                start_date=start_date, end_date=end_date
            )
            # Afficher le graphique correspondant
            if country == "France":
                fig = charts_creator.plot_beveridge_curve(df_fr, "France")
                st.plotly_chart(fig)
            elif country == "United States":
                fig = charts_creator.plot_beveridge_curve(df_us, "United States")
                st.plotly_chart(fig)
            elif country == "Germany":
                fig = charts_creator.plot_beveridge_curve(df_ger, "Germany")
                st.plotly_chart(fig)
            elif country == "Euro Area":
                fig = charts_creator.plot_beveridge_curve(df_eu, "Euro Area")
                st.plotly_chart(fig)

    if selected == "Sources":

        st.subheader("**Data**\n")
        st.write(
            "**France**\n"
            "- [Unemployment Ratelink](https://db.nomics.world/INSEE/CHOMAGE-TRIM-NATIONAL/T.CTTXC.TAUX.FM.0.00-.POURCENT.CVS.FALSE?tab=chart)\n"
            "- [Job Vacancy Rate](https://db.nomics.world/Eurostat/jvs_q_nace2/Q.NSA.B-S.GE10.JOBRATE.FR?tab=chart)\n"
        )

        st.write(
            "**Germany:**\n"
            "- [Unemployment Rate](https://db.nomics.world/DESTATIS/81000BV001/DG.BV4SB.ERW089?tab=chart)\n"
            "- [Job Vacancy Rate](https://db.nomics.world/Eurostat/jvs_q_nace2/Q.NSA.B-S.GE10.JOBRATE.DE?tab=chart)\n"
        )

        st.write(
            "**United States:**\n"
            "- [Unemployment Rate](https://db.nomics.world/BLS/ln/LNS14000000)\n"
            "- [Job Vacancy Rate](https://db.nomics.world/BLS/jt/JTS000000000000000JOR?tab=chart)\n"
        )

        st.write(
            "**Euro Area:**\n"
            "- [Unemployment Rate](https://db.nomics.world/OECD/MEI/EA20.LRHUTTTT.STSA.Q?tab=chart)\n"
            "- [Job Vacancy Rate](https://db.nomics.world/Eurostat/jvs_q_nace2/Q.NSA.B-S.TOTAL.JOBRATE.EA20?tab=chart)\n"
        )

        st.write(
            "Check our [Macroeconomic outlook](https://www.cepremap.fr/depot/2024/07/Macroeconomic-outlook-04-july-2024.pdf) updated every month, which presents international macroeconomic perspectives with data available on DBnomics."
        )
        st.markdown("---")

        st.write("[Source Code](https://github.com/dbnomics/beveridge-curve-dashboard)\n")
        st.write("[DBnomics](https://db.nomics.world)\n")


if __name__ == "__main__":
    main()
