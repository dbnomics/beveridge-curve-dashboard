import plotly.graph_objects as go
import numpy as np

# Générer des données synthétiques
unemployment_rate = np.linspace(1, 12, 100)  # Taux de chômage de 1% à 12%
vacancies = 15 * np.exp(-0.3 * unemployment_rate)  # Fonction exponentielle décroissante

# Créer le graphique avec Plotly
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=unemployment_rate,
    y=vacancies,
    mode='lines',
    line=dict(color='blue', width=2),
    name='Courbe de Beveridge'
))

# Ajouter des titres et des labels
fig.update_layout(
    title='Beveridge Curve',
    xaxis_title='Unemployment rate (%)',
    yaxis_title='Job vacancy rate (en milliers)',
    template='plotly_white'
)

# Afficher la courbe
fig.show()

