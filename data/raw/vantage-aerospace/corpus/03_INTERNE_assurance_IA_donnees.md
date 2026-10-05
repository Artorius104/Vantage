---
document_id: VAS-PRO-AI-014
titre: Procédure d'assurance IA, données et validation
entreprise: Vantage Aerospace Systems SAS
version: 4.0
statut: applicable
proprietaire: Direction Ingénierie IA
approbateur: Responsable Sécurité aérienne
date_effet: 2026-06-01
prochaine_revue: 2027-03-01
niveau_acces: interne
portee: politique_interne
langue: fr
faits_canaris: [CANARI-KEPLER-19]
---

# Procédure d'assurance IA, données et validation

> **Document entièrement fictif — corpus de démonstration RAG.** Marque de contrôle : **CANARI-KEPLER-19**.

## Page 1/7 — Entrées du cycle d’ingénierie

Le cycle démarre par une fiche de finalité prévue et un concept d’opérations. Ils décrivent l’utilisateur, l’environnement, la décision influencée, les interfaces, le niveau d’autonomie, les conséquences d’une erreur et le comportement sûr. Les exigences système sont formulées avant le choix du modèle.

Chaque exigence est identifiable, testable et reliée à une preuve. Les exigences couvrent performances, robustesse, disponibilité, explicabilité utile, supervision, cybersécurité, données, journalisation et maintenance. Les formulations telles que « suffisamment fiable » sont refusées sans métrique, population et seuil.

L’équipe délimite le domaine de conception opérationnelle : plateformes, capteurs, altitudes, vitesses, météo, éclairage, géographies et scénarios. Toute condition non couverte est déclarée hors domaine. Le système doit détecter autant que possible son entrée hors domaine et adopter un état sûr.

Un plan d’assurance précise les activités indépendantes. La personne qui définit les seuils peut participer au développement, mais la validation finale A3 est réalisée par une équipe qui n’a pas entraîné le modèle. Les outils critiques sont qualifiés ou contrôlés par des vérifications indépendantes.

Les hypothèses sur les données et l’humain sont enregistrées comme exigences. Par exemple, si une caméra doit être nettoyée avant vol ou si l’opérateur doit confirmer une zone d’atterrissage, ces conditions figurent dans les instructions et les essais. Marque de contrôle : **CANARI-KEPLER-19**.

<div style="page-break-after: always;"></div>

## Page 2/7 — Acquisition et traçabilité des données

Toute source de données reçoit un identifiant, un propriétaire et une justification. Le dossier précise si les données sont collectées par Vantage, achetées, ouvertes, générées ou fournies par un client. Il conserve la licence, les restrictions de transfert, les consentements éventuels et les caractéristiques techniques des capteurs.

La chaîne de traçabilité relie chaque exemple brut aux transformations appliquées : correction, recadrage, anonymisation, annotation, augmentation et exclusion. Les scripts sont versionnés. Une transformation manuelle non reproductible est documentée avec l’auteur, la date et le motif.

Les données personnelles non nécessaires sont supprimées ou masquées le plus tôt possible. Pour les images aériennes, l’équipe recherche visages, plaques, domiciles et trajectoires pouvant identifier une personne. L’accès au brut est limité aux personnes autorisées. Les exports de jeux de données sont chiffrés et journalisés.

Les données synthétiques sont signalées. Elles peuvent compléter des cas rares mais ne remplacent pas une validation sur des données représentatives réelles lorsque l’usage est opérationnel. Le générateur, ses paramètres et les écarts connus sont conservés.

Une revue d’admission vérifie intégrité, format, provenance, droits, qualité et adéquation. Les lots non conformes sont mis en quarantaine. Aucun lot ne rejoint le dépôt approuvé sur la seule base de son volume ou de sa disponibilité. Marque de contrôle : **CANARI-KEPLER-19**.

<div style="page-break-after: always;"></div>

## Page 3/7 — Annotation, qualité et séparation

Le guide d’annotation définit les classes, les cas limites, les exemples positifs et négatifs et le traitement des incertitudes. Les annotateurs sont formés puis évalués sur un lot de calibration. Les divergences sont arbitrées sans modifier silencieusement la consigne après les résultats.

La qualité est mesurée par échantillonnage et accord entre annotateurs. Pour les classes critiques, une seconde lecture indépendante est obligatoire. Les erreurs sont corrigées dans le jeu source et propagées par une nouvelle version ; les fichiers ne sont pas remplacés sans historique.

La séparation entraînement-validation-test se fait au niveau qui évite la contamination. Des images consécutives d’un même vol, d’un même site ou d’un même objet ne sont pas réparties arbitrairement entre ensembles. Le jeu final est gelé avant le choix du modèle final.

Un registre d’exclusion décrit les données retirées et le motif : corruption, ambiguïté, doublon, licence, information personnelle, scénario hors finalité ou défaut de capteur. Retirer un cas difficile uniquement parce qu’il réduit le score est interdit.

Les versions sont décrites par une fiche de données. Celle-ci indique distributions, lacunes, biais, populations absentes, transformations et usages interdits. L’utilisateur de la fiche doit pouvoir comprendre ce que le jeu ne permet pas de conclure. Marque de contrôle : **CANARI-KEPLER-19**.

<div style="page-break-after: always;"></div>

## Page 4/7 — Développement, reproductibilité et sélection

Chaque expérience conserve le code, la configuration, les données, la graine, l’environnement, le matériel, les métriques et les artefacts. Une expérience non reproductible peut servir à explorer, mais pas à justifier la libération d’une version.

La sélection ne repose pas sur une seule métrique. L’équipe choisit une combinaison adaptée au danger : rappel pour les événements à ne pas manquer, précision pour limiter les fausses alertes, calibration pour interpréter la confiance, latence pour respecter le temps de réaction et robustesse pour les conditions dégradées.

Le modèle de référence simple est conservé. Une architecture plus complexe doit démontrer un bénéfice pertinent, pas seulement un meilleur score moyen. Les coûts en explicabilité, calcul, énergie, maintenance et dépendance fournisseur sont évalués.

Les hyperparamètres sont choisis sur l’ensemble de validation, jamais sur le test final. Les essais répétés sur le test sont enregistrés comme une contamination potentielle et peuvent imposer la constitution d’un nouveau jeu indépendant.

Les bibliothèques, poids préentraînés et conteneurs sont analysés. Les licences et vulnérabilités sont examinées avant intégration. Les modèles provenant d’un dépôt non vérifié restent en quarantaine jusqu’à validation de leur origine et de leur empreinte. Marque de contrôle : **CANARI-KEPLER-19**.

<div style="page-break-after: always;"></div>

## Page 5/7 — Validation et scénarios dégradés

Le protocole de validation est approuvé avant exécution. Il contient les hypothèses, jeux, métriques, seuils, analyses par sous-groupe, cas limites, procédures d’échec et critères d’arrêt. Les résultats négatifs sont conservés avec les résultats positifs.

Les essais couvrent bruit capteur, perte partielle de données, luminosité extrême, météo, compression, vibration, latence réseau, changement de caméra et entrées malformées selon le domaine. Les attaques pertinentes incluent empoisonnement de données, exemples adversariaux, extraction, modification de configuration et dépendance compromise.

La robustesse n’est pas prouvée par une seule campagne. Les essais de laboratoire, simulation, rejeu et terrain ont des objectifs différents. Le passage au terrain nécessite une analyse préalable, un périmètre limité, un pilote habilité, un observateur sécurité et une capacité d’interruption.

Les faux positifs et faux négatifs sont analysés qualitativement. L’équipe recherche des motifs récurrents, des dépendances parasites et des catégories insuffisamment couvertes. Un score conforme peut être rejeté si les erreurs se concentrent sur un scénario critique.

Le rapport conclut exigence par exigence : satisfaite, partiellement satisfaite, non satisfaite ou non testée. Une exigence partielle ne devient pas satisfaite par une moyenne globale. Marque de contrôle : **CANARI-KEPLER-19**.

<div style="page-break-after: always;"></div>

## Page 6/7 — Explicabilité, facteurs humains et journaux

L’explicabilité est définie par son destinataire et sa décision. L’ingénieur a besoin d’éléments de diagnostic ; l’opérateur a besoin d’une information brève et actionnable ; l’auditeur a besoin de traçabilité. Une visualisation séduisante sans fidélité démontrée n’est pas une preuve.

L’interface indique l’état du système, la qualité des entrées, la limite du domaine, la sortie, le niveau de confiance utile et l’action humaine attendue. Les essais vérifient que l’opérateur ne confond pas absence de détection et absence de danger.

Les journaux enregistrent version du modèle, configuration, horodatage, état capteur, entrées référencées ou empreintes, sorties, confiance, alertes, action humaine et changement d’état. Ils évitent les données personnelles non nécessaires et les secrets. L’horloge est synchronisée avec les autres systèmes d’essai.

L’opérateur peut ignorer ou annuler une recommandation sans procédure excessive. L’annulation et sa raison sont enregistrées pour l’analyse, mais ne sont pas automatiquement considérées comme une faute. La culture juste favorise le signalement des limites.

Les journaux sont testés comme une fonction. Une information supposée disponible mais absente lors d’un incident est traitée comme une défaillance d’assurance. Marque de contrôle : **CANARI-KEPLER-19**.

<div style="page-break-after: always;"></div>

## Page 7/7 — Libération, changement et surveillance

Le paquet de libération contient modèle, code, dépendances, paramètres, empreintes, données de calibration, rapport de validation, limites, manuel, plan de surveillance et stratégie de retour arrière. Les artefacts sont signés et stockés dans le référentiel approuvé.

Le comité de libération vérifie la couverture des exigences, les écarts ouverts et les conditions d’emploi. Une dérogation précise le risque, la durée, le périmètre, les compensations et l’autorité d’acceptation. Elle ne peut masquer une exigence réglementaire.

Après déploiement, les indicateurs couvrent taux d’erreur observé, hors-domaine, latence, disponibilité, overrides, dérive, incidents et modifications d’environnement. Les données de surveillance sont comparées aux hypothèses de validation.

Toute mise à jour suit une analyse d’impact. Un changement pré-approuvé peut utiliser une voie allégée si ses limites et critères ont été définis dans le dossier initial. Sinon, la version revient au cycle complet approprié à sa criticité.

Le retrait préserve les preuves nécessaires aux audits et incidents. Les clés, accès et endpoints sont révoqués. Le processus manuel ou la version antérieure sûre est restauré selon le plan de continuité. Marque de contrôle : **CANARI-KEPLER-19**.
