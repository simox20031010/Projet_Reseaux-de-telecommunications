import numpy as np
import random
from networkx import Graph, shortest_path

# Capacités des liens
capacites = [1000, 100, 100, 100, 100, 100, 100, 10, 10]

# Liens du réseau
liens = [
    (1, 4, 1),
    (1, 5, 2),
    (2, 4, 3),
    (2, 6, 4),
    (3, 5, 5),
    (3, 6, 6),
    (4, 5, 7),
    (4, 7, 8),
    (5, 7, 9),
]

# Paramètres
T = 120  # Durée en minutes
lambda_taux = 55  # Appels par minute
capacites_disponibles = capacites[:]
nombre_appels_totaux = 0
nombre_appels_bloques = 0
appels_actifs = []
temps = 0
pas_temps = 1 / 60  # 1 seconde

# Création de la matrice d'adjacence
nb_noeuds = max(max(lien[0], lien[1]) for lien in liens)
graph = Graph()
graph.add_weighted_edges_from([(lien[0], lien[1], 1) for lien in liens])

while temps < T:
    if random.random() < lambda_taux * pas_temps:
        source, destination = random.sample(range(1, 4), 2)
        duree = random.uniform(1, 5)
        nombre_appels_totaux += 1

        try:
            chemin = shortest_path(graph, source, destination, weight="weight")
            bloque = False
            liens_utilises = []
            for i in range(len(chemin) - 1):
                lien = next(
                    l[2] for l in liens if {chemin[i], chemin[i + 1]} == {l[0], l[1]}
                )
                liens_utilises.append(lien)
                if capacites_disponibles[lien - 1] < 1:
                    bloque = True
                    break

            if bloque:
                nombre_appels_bloques += 1
            else:
                for lien in liens_utilises:
                    capacites_disponibles[lien - 1] -= 1
                appels_actifs.append({'route': liens_utilises, 'fin': temps + duree})

        except Exception:
            nombre_appels_bloques += 1

    appels_a_liberer = [appel for appel in appels_actifs if appel['fin'] <= temps]
    for appel in appels_a_liberer:
        for lien in appel['route']:
            capacites_disponibles[lien - 1] += 1
        appels_actifs.remove(appel)

    temps += pas_temps

P_blocage = nombre_appels_bloques / nombre_appels_totaux
print("Probabilité de blocage (adaptatif) :", P_blocage)
