import pandas as pd
from dbnomics import fetch_series


def load_unemployment_series():
    unemployment_series_ger = fetch_series("DESTATIS/81000BV001/DG.BV4SB.ERW089")
    unemployment_series_us = fetch_series("BLS/ln/LNS14000000")
    unemployment_series_fr = fetch_series(
        "INSEE/CHOMAGE-TRIM-NATIONAL/T.CTTXC.TAUX.FM.0.00-.POURCENT.CVS.FALSE"
    )
    unemployment_series_eu = fetch_series("OECD/MEI/EA20.LRHUTTTT.STSA.Q")
    return (
        unemployment_series_ger,
        unemployment_series_us,
        unemployment_series_fr,
        unemployment_series_eu,
    )



def load_job_vacancy_series():
    job_vacancy_ger = fetch_series("Eurostat/jvs_q_nace2/Q.NSA.B-S.GE10.JOBRATE.DE")
    job_vacancy_us = fetch_series("BLS/jt/JTS000000000000000JOR")
    job_vacancy_fr = fetch_series("Eurostat/jvs_q_nace2/Q.NSA.B-S.GE10.JOBRATE.FR")
    job_vacancy_eu = fetch_series("Eurostat/jvs_q_nace2/Q.NSA.B-S.TOTAL.JOBRATE.EA20")
    return job_vacancy_ger, job_vacancy_us, job_vacancy_fr, job_vacancy_eu


def prepare_data(start_date=None, end_date=None):
    # Load data
    (
        unemployment_series_ger,
        unemployment_series_us,
        unemployment_series_fr,
        unemployment_series_eu,
    ) = load_unemployment_series()
    job_vacancy_ger, job_vacancy_us, job_vacancy_fr, job_vacancy_eu = (
        load_job_vacancy_series()
    )

    # Prepare data for each country
    # France
    col_job_fr = ["original_period", "value", "Geopolitical entity (reporting)"]
    col_un_fr = ["original_period", "value", "Reference area"]
    job_vacancy_fr = job_vacancy_fr[col_job_fr].rename(columns={"value": "job vacancy"})
    unemployment_series_fr = unemployment_series_fr[col_un_fr].rename(
        columns={"value": "unemployment rate"}
    )
    df_fr = pd.merge(
        job_vacancy_fr, unemployment_series_fr, on="original_period", how="left"
    ).dropna()
    df_fr["original_period"] = pd.to_datetime(df_fr["original_period"])

    # USA
    col_job_us = ["original_period", "value", "State"]
    col_un_us = ["original_period", "value"]
    job_vacancy_us = job_vacancy_us[col_job_us].rename(columns={"value": "job vacancy"})
    unemployment_series_us = unemployment_series_us[col_un_us].rename(
        columns={"value": "unemployment rate"}
    )
    unemployment_series_us["Country"] = "United States"
    df_us = pd.merge(
        job_vacancy_us, unemployment_series_us, on="original_period", how="left"
    ).dropna()
    df_us["original_period"] = pd.to_datetime(df_us["original_period"])

    # Germany
    col_job_ger = ["original_period", "value", "Geopolitical entity (reporting)"]
    col_un_ger = ["original_period", "value", "Germany"]
    job_vacancy_ger = job_vacancy_ger[col_job_ger].rename(
        columns={"value": "job vacancy"}
    )
    unemployment_series_ger = unemployment_series_ger[col_un_ger].rename(
        columns={"value": "unemployment rate"}
    )
    df_ger = pd.merge(
        job_vacancy_ger, unemployment_series_ger, on="original_period", how="left"
    ).dropna()
    df_ger["original_period"] = pd.to_datetime(df_ger["original_period"])

    # Euro Area
    col_job_eu = ["original_period", "value", "Geopolitical entity (reporting)"]
    col_un_eu = ["original_period", "value", "Country"]
    job_vacancy_eu = job_vacancy_eu[col_job_eu].rename(columns={"value": "job vacancy"})
    unemployment_series_eu = unemployment_series_eu[col_un_eu].rename(
        columns={"value": "unemployment rate"}
    )
    df_eu = pd.merge(
        job_vacancy_eu, unemployment_series_eu, on="original_period", how="left"
    ).dropna()
    df_eu["original_period"] = pd.to_datetime(df_eu["original_period"])

    # Filter data by date if specified
    if start_date:
        df_fr = df_fr[df_fr["original_period"] >= start_date]
        df_us = df_us[df_us["original_period"] >= start_date]
        df_ger = df_ger[df_ger["original_period"] >= start_date]
        df_eu = df_eu[df_eu["original_period"] >= start_date]
    if end_date:
        df_fr = df_fr[df_fr["original_period"] <= end_date]
        df_us = df_us[df_us["original_period"] <= end_date]
        df_ger = df_ger[df_ger["original_period"] <= end_date]
        df_eu = df_eu[df_eu["original_period"] <= end_date]

    return df_fr, df_us, df_ger, df_eu
