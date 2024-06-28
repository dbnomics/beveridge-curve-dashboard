import pandas as pd
import matplotlib.pyplot as plt

# Création du DataFrame
data = {
    'Période': ['2000-Q1', '2000-Q2', '2000-Q3', '2000-Q4', '2001-Q1', '2001-Q2', '2001-Q3', '2001-Q4',
                '2002-Q1', '2002-Q2', '2002-Q3', '2002-Q4'],
    'Taux de chômage (%)': [5.0, 5.2, 4.8, 4.5, 5.5, 5.7, 5.3, 5.0, 6.0, 6.2, 5.8, 5.5],
    'Taux de vacance d\'emploi (%)': [3.0, 2.9, 3.1, 3.3, 2.7, 2.6, 2.9, 3.0, 2.5, 2.4, 2.7, 2.9]
}

df = pd.DataFrame(data)

# Affichage du DataFrame
print(df)

# Visualisation de la courbe de Beveridge
plt.figure(figsize=(10, 6))
plt.plot(df['Taux de chômage (%)'], df['Taux de vacance d\'emploi (%)'], marker='o', linestyle='-')

for i, txt in enumerate(df['Période']):
    plt.annotate(txt, (df['Taux de chômage (%)'][i], df['Taux de vacance d\'emploi (%)'][i]))

plt.title('Courbe de Beveridge')
plt.xlabel('Taux de chômage (%)')
plt.ylabel('Taux de vacance d\'emploi (%)')
plt.grid(True)
plt.show()
