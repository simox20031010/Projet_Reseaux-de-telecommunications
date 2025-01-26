import matplotlib.pyplot as plt
import numpy as np
import routage_adaptatif
import routage_partage_de_charge
import routage_statique

# Exécuter les simulations pour chaque méthode de routage
probabilites_blocage = {
    "Routage Adaptatif": routage_adaptatif.P_blocage,
    "Partage de Charge": routage_partage_de_charge.P_blocage,
    "Routage Statique": routage_statique.P_blocage,
}

# Créer l'histogramme
algorithmes = list(probabilites_blocage.keys())
probabilites = list(probabilites_blocage.values())

plt.figure(figsize=(10, 6))
plt.bar(algorithmes, probabilites, color=['blue', 'green', 'red'], alpha=0.7)
plt.xlabel('Algorithmes de Routage')
plt.ylabel('Probabilité de Blocage')
plt.title('Comparaison des Probabilités de Blocage entre les Algorithmes de Routage')
plt.ylim(0, 1)
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Ajouter les valeurs sur les barres
for i, prob in enumerate(probabilites):
    plt.text(i, prob + 0.02, f'{prob:.2f}', ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.show()
