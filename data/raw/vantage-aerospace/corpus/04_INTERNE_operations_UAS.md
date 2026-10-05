---
document_id: VAS-PRO-OPS-021
titre: Procédure de préparation et conduite des opérations UAS
entreprise: Vantage Aerospace Systems SAS
version: 2.2
statut: applicable
proprietaire: Direction des Opérations UAS
approbateur: Responsable des opérations
date_effet: 2026-03-10
prochaine_revue: 2027-03-10
niveau_acces: interne
portee: politique_interne
langue: fr
faits_canaris: [CANARI-ORION-57]
---

# Procédure de préparation et conduite des opérations UAS

> **Document entièrement fictif — corpus de démonstration RAG.** Marque de contrôle : **CANARI-ORION-57**.

## Page 1/6 — Catégorie et autorisation

Toute mission de drone commence par l’identification de la catégorie réglementaire applicable : ouverte, spécifique ou certifiée. L’équipe vérifie la masse, la classe du drone, le scénario, la proximité des personnes, l’espace aérien, la hauteur, la visibilité, l’autonomie et la nature de la charge utile.

Une opération ouverte ne doit pas être utilisée pour éviter une analyse requise en catégorie spécifique. Une opération spécifique suit un scénario standard déclaré, une évaluation prédéfinie reconnue ou une autorisation fondée sur une analyse de risques. Les conditions de l’autorisation font partie des limites de mission.

Le responsable de mission conserve la preuve d’enregistrement de l’exploitant, les compétences du télépilote, les déclarations ou autorisations et les accords locaux. Si la mission traverse un autre État, les exigences transfrontalières sont vérifiées avant contractualisation finale.

Les fonctions IA embarquées sont décrites dans le dossier mission. L’équipe précise si elles recommandent, automatisent ou décident ; si elles sont nécessaires à la sécurité ; et comment les reprendre manuellement. Une fonction expérimentale ne peut modifier la trajectoire en dehors du périmètre d’essai approuvé.

Aucun vol ne débute si l’autorisation, la zone géographique ou le manuel opérateur applicable n’est pas disponible. Marque de contrôle : **CANARI-ORION-57**.

<div style="page-break-after: always;"></div>

## Page 2/6 — Dossier mission et responsabilités

Le dossier mission comprend objectifs, coordonnées, dates, équipage, aéronef, configuration, charge utile, cartes, espace aérien, météo, environnement au sol, communications, urgence, assurance et contacts. Il identifie les infrastructures critiques, rassemblements, routes, habitations et zones sensibles.

Le responsable des opérations autorise la mission. Le télépilote conserve l’autorité tactique sur le vol et peut l’interrompre. L’observateur surveille l’environnement et ne remplace pas le télépilote. Le technicien confirme la configuration et la navigabilité opérationnelle. Pour un essai IA A3, un responsable d’essai indépendant surveille les critères d’arrêt.

Le briefing attribue les appels, mots d’urgence et canaux. Le commandement est explicite en cas de perte de liaison ou de désaccord. Une pression commerciale ou la présence d’un client ne réduit jamais l’autorité d’arrêt.

Les données collectées sont limitées à l’objectif déclaré. Le responsable mission vérifie l’information du client et, lorsque nécessaire, des personnes concernées. Les zones privées non nécessaires sont exclues ou masquées par conception.

Toute modification de site, d’aéronef, de logiciel critique, de charge ou d’horaire après approbation déclenche une revue de changement. Marque de contrôle : **CANARI-ORION-57**.

<div style="page-break-after: always;"></div>

## Page 3/6 — Analyse de risques et barrières

L’analyse couvre risques au sol, risques aériens, perte de contrôle, énergie, météo, navigation, communications, facteur humain, intrusion cyber et comportement de la fonction IA. Les barrières sont spécifiques et vérifiables : zone tampon, parachute, observateur, limitation géographique, retour automatique, redondance ou suspension.

Pour une opération spécifique hors scénario standard, le dossier applique la méthode d’évaluation reconnue par l’autorité ou celle imposée dans l’autorisation. Les objectifs de sécurité opérationnelle sont reliés à des preuves de conception, de procédure, de compétence et d’essai.

Le risque de zone adjacente est examiné. Le plan prévoit le confinement et la réaction à une sortie de volume. La trajectoire d’urgence n’est pas dirigée vers une zone plus dangereuse que la trajectoire nominale.

La fonction IA est évaluée pour les erreurs silencieuses, le hors-domaine, la confiance excessive, la latence et la perte d’entrée. Lorsque la qualité d’image descend sous le seuil approuvé, la détection automatique est déclarée indisponible et l’opérateur applique le mode dégradé.

Les risques non couverts par des preuves suffisantes sont acceptés au niveau requis ou entraînent l’annulation. Marque de contrôle : **CANARI-ORION-57**.

<div style="page-break-after: always;"></div>

## Page 4/6 — Prévol et décision go/no-go

La revue prévol confirme identité du drone, firmware, modèle IA, paramètres, masse, batteries, hélices, capteurs, mémoire, liaison, géorepérage, identification à distance si applicable et heure système. Les empreintes logicielles sont comparées au paquet autorisé.

Le télépilote vérifie météo actuelle et prévision, NOTAM ou restrictions pertinentes, obstacles, personnes, animaux, interférences et alternatives d’atterrissage. Le test de commandes est réalisé dans une zone sûre.

Le go/no-go utilise des critères objectifs. Sont des motifs no-go : autorisation manquante, membre essentiel absent, météo hors limites, batterie non conforme, journalisation critique inactive, modèle non approuvé, carte de zone obsolète ou moyen de récupération indisponible.

Une anomalie mineure peut être acceptée si elle ne dégrade pas une barrière et si le manuel le prévoit. L’acceptation orale sans trace est interdite. Le journal mission identifie l’autorité ayant pris la décision.

Après un no-go, la mission ne reprend que lorsque la cause est corrigée et la vérification répétée. Marque de contrôle : **CANARI-ORION-57**.

<div style="page-break-after: always;"></div>

## Page 5/6 — Conduite et situations anormales

Pendant le vol, le télépilote respecte les limites déclarées ou autorisées, maintient la conscience de la situation et donne priorité aux aéronefs habités. Il interrompt l’opération si sa poursuite crée un risque pour les aéronefs, personnes, biens ou environnement.

Les modes anormaux comprennent perte de liaison, navigation dégradée, batterie faible, perte d’identification, intrusion dans la zone, alerte météo, sortie de confinement et incohérence IA. Chaque mode dispose d’une action mémorisable : maintenir, revenir, atterrir ou couper selon le manuel.

Une recommandation IA contradictoire avec l’observation humaine est ignorée et signalée. Une confiance élevée ne remplace pas les règles de séparation ni l’autorité du télépilote. Les changements automatiques de modèle pendant le vol sont interdits.

Le responsable d’essai peut prononcer « arrêt essai » ; le télépilote reprend la configuration sûre prévue. Les données nécessaires sont marquées pour analyse, sans prolonger le vol uniquement pour obtenir plus d’échantillons.

Tout événement significatif est transmis à la procédure de notification et d’analyse. Marque de contrôle : **CANARI-ORION-57**.

<div style="page-break-after: always;"></div>

## Page 6/6 — Après-vol, données et clôture

L’équipe sécurise l’aéronef, les batteries et la charge utile. Elle vérifie dommages, températures, cycles et anomalies. Les journaux sont copiés vers le stockage approuvé avec empreinte et identifiant de mission.

Le débrief compare objectifs, conditions et résultats. Les interventions humaines, alertes, pertes de qualité et écarts sont enregistrés. Un vol terminé sans accident n’est pas automatiquement un vol conforme.

Les images non nécessaires sont supprimées selon le plan de données. Les livrables client sont contrôlés pour éviter la présence de personnes, plaques, sites voisins ou informations sensibles sans justification.

Le responsable mission décide si l’aéronef est libéré pour une nouvelle mission, placé en maintenance ou immobilisé. Un défaut lié à une fonction IA suspend la version concernée jusqu’à triage.

La clôture confirme les notifications réglementaires, actions correctives et leçons apprises. Marque de contrôle : **CANARI-ORION-57**.
