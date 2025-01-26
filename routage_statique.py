import numpy as np
import random

# Capacités des liens
capacites = [1000, 100, 100, 100, 100, 100, 100, 10, 10]

# Définition des routes statiques
routes = {
    (1, 3): [8, 9],
    (1, 2): [8],
    (2, 3): [9]
}

# Paramètres de simulation
T = 120  # Durée en minutes
lambda_taux = 55  # Appels par minute
capacites_disponibles = capacites[:]
nombre_appels_bloques = 0
nombre_appels_totaux = 0
appels_actifs = []

# Suivi du temps
intervals_temps = np.arange(0, T + 1, 1)
blocages_par_temps = []
appels_totaux_par_temps = []
temps = 0
pas_temps = 1 / 60  # 1 seconde

# Boucle de simulation
while temps < T:
    # Génération d'appels (processus de Poisson)
    if random.random() < lambda_taux * pas_temps:
        source = random.randint(1, 3)
        destination = random.randint(1, 3)
        while destination == source:
            destination = random.randint(1, 3)
        duree = random.uniform(1, 5)

        nombre_appels_totaux += 1
        route = routes.get((source, destination), [])

        # Vérification de la disponibilité de la route
        bloque = any(capacites_disponibles[lien - 1] < 1 for lien in route)

        if not bloque:
            for lien in route:
                capacites_disponibles[lien - 1] -= 1
            appels_actifs.append({'route': route, 'fin': temps + duree})
        else:
            nombre_appels_bloques += 1

    # Libération des liens lorsque les appels se terminent
    appels_a_terminer = [appel for appel in appels_actifs if appel['fin'] <= temps]
    for appel in appels_a_terminer:
        for lien in appel['route']:
            capacites_disponibles[lien - 1] += 1
        appels_actifs.remove(appel)

    # Enregistrement des statistiques
    blocages_par_temps.append(nombre_appels_bloques)
    appels_totaux_par_temps.append(nombre_appels_totaux)

    temps += pas_temps

# Calcul de la probabilité de blocage
P_blocage = nombre_appels_bloques / nombre_appels_totaux
print("Probabilité de blocage (routage statique) :", P_blocage)
