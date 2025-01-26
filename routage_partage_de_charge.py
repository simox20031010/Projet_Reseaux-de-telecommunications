import numpy as np
import random

# Capacités des liens (inchangées)
capacites = [1000, 100, 100, 100, 100, 100, 100, 10, 10]

# Poids de routage (inchangés pour garder la même logique de partage de charge)
poids = {
    (1, 3): [([2, 4], 1 / 3), ([5, 7], 1 / 3), ([8, 9], 1 / 3)],
    (2, 3): [([9], 1)],
    (1, 2): [([8], 1)],
}

# Paramètres de simulation
T = 120  # Durée en minutes
lambda_taux = 55  # Augmentation du taux d'arrivée pour augmenter légèrement la charge
capacites_disponibles = capacites[:]
nombre_appels_totaux = 0
nombre_appels_bloques = 0
appels_actifs = []

temps = 0
pas_temps = 1 / 60  # 1 seconde

# Boucle de simulation
while temps < T:
    if random.random() < lambda_taux * pas_temps:
        source = 1
        destination = 3
        duree = random.uniform(2, 7)  # Augmenter la durée moyenne des appels pour augmenter la charge

        nombre_appels_totaux += 1
        chemins = poids[(source, destination)]
        chemins.sort(key=lambda x: -x[1])  # Trier par poids décroissant
        route_trouvee = False

        for chemin, _ in chemins:
            bloque = any(capacites_disponibles[lien - 1] < 1 for lien in chemin)
            if not bloque:
                for lien in chemin:
                    capacites_disponibles[lien - 1] -= 1
                appels_actifs.append({'route': chemin, 'fin': temps + duree})
                route_trouvee = True
                break

        if not route_trouvee:
            nombre_appels_bloques += 1

    # Libérer les ressources pour les appels terminés
    appels_a_terminer = [appel for appel in appels_actifs if appel['fin'] <= temps]
    for appel in appels_a_terminer:
        for lien in appel['route']:
            capacites_disponibles[lien - 1] += 1
        appels_actifs.remove(appel)

    temps += pas_temps

# Calcul de la probabilité de blocage
P_blocage = nombre_appels_bloques / nombre_appels_totaux
print("Probabilité de blocage (routage partage de charge ):", P_blocage)
