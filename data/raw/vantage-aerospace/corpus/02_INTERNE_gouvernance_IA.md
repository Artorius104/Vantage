---
document_id: VAS-POL-AI-002
titre: Politique de gouvernance des systèmes d'intelligence artificielle
entreprise: Vantage Aerospace Systems SAS
version: 2.4
statut: applicable
proprietaire: Responsable IA de confiance
approbateur: Comité exécutif
date_effet: 2026-05-15
prochaine_revue: 2027-05-15
niveau_acces: interne
portee: politique_interne
langue: fr
faits_canaris: [CANARI-CERES-82]
---

# Politique de gouvernance des systèmes d'intelligence artificielle

> **Document entièrement fictif — corpus de démonstration RAG.** Marque de contrôle : **CANARI-CERES-82**.

## Page 1/6 — Principes et classification interne

Vantage encadre tout système d’IA développé, acheté, intégré ou exploité par l’entreprise. La politique couvre les modèles embarqués, les outils d’aide à la conception, l’analyse d’images, la maintenance prédictive, les assistants documentaires et les modèles à usage général utilisés via une API. Elle s’applique de l’idéation au retrait.

Tout système est inscrit au registre IA avant d’accéder à des données non publiques. La fiche de registre décrit la finalité prévue, le propriétaire, les utilisateurs, les entrées, les sorties, les décisions influencées, le niveau d’autonomie, les personnes affectées, les produits concernés et les fournisseurs. Elle identifie séparément la qualification au titre de la sécurité aérienne, du règlement sur l’IA, du RGPD et des règles contractuelles.

La classification interne comporte quatre classes. **A0** désigne un prototype isolé sans donnée personnelle ni usage opérationnel. **A1** désigne une aide non décisionnelle dont la sortie doit être relue. **A2** désigne un système influençant une décision opérationnelle, humaine ou commerciale. **A3** désigne une fonction susceptible d’affecter directement la sécurité d’un aéronef, d’une personne ou d’une infrastructure critique. Cette classification interne ne remplace pas la qualification juridique.

Les systèmes A2 et A3 exigent une analyse de risques IA, un plan d’évaluation, une supervision humaine définie, une journalisation et un dossier de décision. Les systèmes A3 nécessitent en plus l’approbation du comité Sécurité-IA avant tout essai hors laboratoire. Une démonstration commerciale n’est pas un laboratoire si elle influence une opération réelle.

La finalité prévue constitue la limite centrale. Une réutilisation pour une autre population, un autre capteur, un autre domaine de vol ou une autre décision est un changement à évaluer, même si le code ne change pas. Marque de contrôle : **CANARI-CERES-82**.

<div style="page-break-after: always;"></div>

## Page 2/6 — Qualification réglementaire et responsabilités

Le propriétaire du système prépare une note de qualification. Il examine si le système est un composant de sécurité d’un produit aéronautique, s’il est lui-même un produit, s’il relève d’un cas à haut risque, s’il traite des données personnelles et si son usage est exclusivement civil, exclusivement défense ou mixte. La mention « expérimental » ne suffit pas à exclure un système utilisé en situation réelle.

Pour une fonction civile embarquée soumise à une évaluation de conformité tierce, l’équipe Conformité analyse l’application de l’article 6 du règlement européen sur l’IA en lien avec la réglementation aéronautique applicable. Les exigences IA sont intégrées au dossier de conformité sectoriel plutôt que traitées dans un dossier parallèle sans liaison.

Le fournisseur IA est responsable de la conception, du système de gestion de la qualité, de la documentation technique, de l’évaluation de conformité, du suivi après mise sur le marché et des actions correctives. Le déployeur est responsable de l’usage conforme aux instructions, des données d’entrée qu’il contrôle, de la supervision humaine, de la surveillance et du signalement. Vantage peut cumuler les deux rôles.

Le responsable IA de confiance maintient le registre et les modèles de preuve. Le responsable Sécurité aérienne accepte les arguments de sécurité. Le DPO décide si une AIPD est nécessaire et vérifie la base légale. Le RSSI évalue les menaces cyber et les dépendances. Le responsable Export contrôle le transfert de logiciels, modèles, poids, données techniques et assistance.

Aucune équipe ne peut déclarer seule qu’un système est « conforme ». La décision résulte d’un ensemble de preuves examinées par les fonctions compétentes. Les désaccords non résolus sont enregistrés et remontés au comité Sécurité-IA. Marque de contrôle : **CANARI-CERES-82**.

<div style="page-break-after: always;"></div>

## Page 3/6 — Gestion des risques et critères d’acceptation

Le processus de risque est continu et itératif. Il identifie les dangers issus de l’usage prévu et des mésusages raisonnablement prévisibles : erreur de perception, dérive des données, confiance excessive de l’opérateur, indisponibilité, attaque adversariale, confusion d’unités, sortie hors domaine et dépendance à un fournisseur.

Chaque risque comporte une cause, un événement redouté, des conséquences, une vraisemblance, une gravité, des barrières préventives, des barrières de détection et un risque résiduel. L’équipe relie les contrôles aux tests qui démontrent leur efficacité. Une simple affirmation de robustesse n’est pas une preuve.

Les métriques sont définies par cas d’usage. Une moyenne globale ne suffit pas lorsque certaines conditions rares sont critiques. L’évaluation est ventilée au minimum par capteur, météo, heure, géographie, configuration matérielle et catégorie de scène pertinentes. Les seuils d’acceptation sont fixés avant le test final pour éviter de les ajuster après observation des résultats.

Tout risque résiduel A3 doit être accepté par le responsable Sécurité aérienne et le propriétaire produit. Un risque relatif aux droits fondamentaux ou aux données personnelles requiert aussi l’avis Conformité ou DPO. Un objectif commercial, un retard calendrier ou un coût déjà engagé ne constitue pas une justification suffisante.

Le plan traite également les personnes vulnérables lorsque le contexte le justifie. Pour les drones opérant près de zones habitées, l’analyse considère les personnes au sol qui ne participent pas à l’opération. Pour les outils RH, l’analyse considère les candidats et salariés affectés par la décision. Marque de contrôle : **CANARI-CERES-82**.

<div style="page-break-after: always;"></div>

## Page 4/6 — Supervision humaine et transparence

Chaque système A2 ou A3 dispose d’un concept de supervision humaine. Celui-ci précise qui supervise, quelles compétences sont requises, quelles informations sont visibles, combien de temps est disponible pour agir, et comment l’opérateur peut ignorer, corriger, annuler ou arrêter le système.

L’interface doit présenter la confiance et les limites sans donner une illusion de certitude. Une probabilité ne doit pas être affichée comme un verdict. Les alertes sont hiérarchisées afin d’éviter la fatigue. Lorsqu’une sortie est hors domaine ou que l’intégrité des entrées est insuffisante, le comportement sûr prévu est activé et clairement signalé.

Pour les fonctions de vol, la supervision n’est crédible que si l’opérateur dispose du temps, de la situation et de l’autorité nécessaires. Un bouton d’arrêt inaccessible ou une alerte apparaissant après l’action ne constitue pas une supervision effective. Les essais facteurs humains mesurent la compréhension, le temps de réaction, les erreurs d’interprétation et le biais d’automatisation.

Les instructions d’utilisation décrivent la finalité, les performances validées, les populations ou environnements couverts, les limitations, la maintenance, les journaux disponibles et les qualifications nécessaires. Elles distinguent les fonctions garanties des fonctions expérimentales.

Les utilisateurs sont informés qu’ils interagissent avec un système d’IA lorsque cela n’est pas évident. Les sorties générées pour un usage externe font l’objet d’une validation éditoriale et technique. Les citations d’un assistant documentaire doivent pointer vers des Références récupérées, jamais vers une mémoire supposée du modèle. Marque de contrôle : **CANARI-CERES-82**.

<div style="page-break-after: always;"></div>

## Page 5/6 — Données, modèles et fournisseurs

Chaque jeu de données possède une fiche décrivant origine, licence, finalité, période, population, capteurs, transformations, exclusions, qualité, biais connus et durée de conservation. Les données d’entraînement, validation et test sont séparées de façon à prévenir les fuites. Les doublons et séquences corrélées sont traités avant la séparation.

Les données doivent être pertinentes et suffisamment représentatives du domaine d’emploi. Pour un modèle de vision embarqué, l’équipe documente les conditions lumineuses, météorologiques, géographiques et matérielles. Un bon résultat sur des images de laboratoire ne justifie pas un usage en vol.

L’usage de données personnelles exige une base légale, une minimisation, une information adaptée et des contrôles d’accès. Les données sensibles ne sont utilisées qu’après validation du DPO et uniquement si la nécessité est démontrée. Les environnements de développement utilisent des données fictives ou anonymisées lorsque cela suffit.

Avant l’achat d’un modèle, Vantage obtient les limites d’usage, les conditions de licence, les versions, les dépendances, les localisations de traitement, les mécanismes de sécurité, les modalités d’incident et les conditions de sortie. L’impossibilité d’auditer un fournisseur augmente le risque et peut interdire un usage A3.

Les mises à jour de modèle sont gelées par version. Un modèle téléchargé à nouveau sous le même nom n’est pas réputé identique. Les empreintes, poids, configurations, bibliothèques et données de calibration sont conservés afin de reproduire les résultats. Marque de contrôle : **CANARI-CERES-82**.

<div style="page-break-after: always;"></div>

## Page 6/6 — Mise en service, surveillance et retrait

La mise en service exige : qualification approuvée, risques acceptés, tests réussis, documentation disponible, personnes formées, supervision opérationnelle, plan de retour arrière, journalisation active et responsabilités d’incident attribuées. Pour A3, une revue indépendante confirme que les preuves couvrent les exigences.

Le suivi mesure les performances, les erreurs, les changements de distribution, les interventions humaines, les incidents, les quasi-incidents et les plaintes. Les seuils d’alerte sont définis avant exploitation. Une alerte n’entraîne pas automatiquement le retrait, mais elle impose une analyse dans le délai prévu par la criticité.

Un changement substantiel comprend notamment une nouvelle finalité, une nouvelle autorité de décision, un nouveau capteur critique, une modification non prévue des performances, un apprentissage continu non évalué ou une nouvelle population exposée. Il déclenche une nouvelle qualification et, si nécessaire, une nouvelle évaluation de conformité.

Le système est suspendu si une défaillance crée un risque non maîtrisé, si les journaux essentiels sont indisponibles, si le modèle ne correspond plus à la version approuvée, ou si une obligation de signalement ne peut être respectée. Le plan de retrait prévoit la conservation des preuves, l’information des parties concernées et la restauration d’un processus manuel sûr.

La clôture documente les enseignements et met à jour le registre IA. Les modèles retirés sont archivés avec leurs restrictions ; ils ne peuvent pas être réutilisés comme prototypes sans nouvelle autorisation. Marque de contrôle : **CANARI-CERES-82**.
