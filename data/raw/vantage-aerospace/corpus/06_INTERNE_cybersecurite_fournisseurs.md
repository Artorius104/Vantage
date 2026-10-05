---
document_id: VAS-PRO-CYB-040
titre: Procédure cybersécurité produit, accès et chaîne d'approvisionnement
entreprise: Vantage Aerospace Systems SAS
version: 2.5
statut: applicable
proprietaire: RSSI
approbateur: Comité des risques
date_effet: 2026-04-20
prochaine_revue: 2027-04-20
niveau_acces: interne
portee: politique_interne
langue: fr
faits_canaris: [CANARI-NOVA-64]
---

# Procédure cybersécurité produit, accès et chaîne d’approvisionnement

> **Document entièrement fictif — corpus de démonstration RAG.** Marque de contrôle : **CANARI-NOVA-64**.

## Page 1/5 — Analyse de risques et architecture

Tout produit connecté, service cloud, pipeline IA ou outil d’exploitation fait l’objet d’une analyse de risques cyber fondée sur les actifs, menaces, vulnérabilités, impacts et dépendances. L’approche couvre les systèmes numériques et leur environnement physique.

L’architecture sépare développement, essai, production et environnements embarqués. Les flux sont inventoriés et limités. Les interfaces de maintenance, télémétrie et mise à jour sont authentifiées. Les secrets ne sont ni placés dans le code ni inclus dans les images de conteneurs.

Pour l’IA, le modèle et les données sont des actifs. Les menaces incluent empoisonnement, extraction, inversion, exemple adversarial, altération de poids, substitution de modèle et instruction malveillante pour les assistants génératifs.

Chaque contrôle possède un propriétaire et une preuve. Les risques résiduels élevés sont acceptés par le comité des risques. Le fait qu’un système soit isolé n’exclut pas le risque lié aux supports amovibles, fournisseurs ou opérations de maintenance.

Les exigences cyber sont intégrées dès la conception et revues lors des changements. Marque de contrôle : **CANARI-NOVA-64**.

<div style="page-break-after: always;"></div>

## Page 2/5 — Identités, habilitations et journalisation

Les accès suivent le moindre privilège, la séparation des tâches et une durée adaptée au besoin. Les comptes partagés sont interdits sauf dispositif technique exceptionnel approuvé et traçable. Les comptes à privilèges sont distincts des comptes usuels.

Une authentification multifacteur est requise pour les accès administratifs, distants et aux dépôts sensibles. Les habilitations sont revues trimestriellement et à chaque départ ou changement de fonction. Les accès temporaires expirent automatiquement.

Les dépôts de données et modèles appliquent des niveaux différenciés : lecture, contribution, approbation, déploiement et administration. Une personne ne peut pas seule modifier puis libérer un modèle A3.

Les journaux enregistrent connexions, échecs, modifications, téléchargements, suppressions, changements d’habilitation et déploiements. Ils sont protégés contre l’altération et surveillés selon le risque.

Les anomalies d’accès sont transmises au processus d’incident. Marque de contrôle : **CANARI-NOVA-64**.

<div style="page-break-after: always;"></div>

## Page 3/5 — Développement et vulnérabilités

Le développement suit revue de code, analyse de dépendances, gestion des secrets, tests et signatures d’artefacts. Une nomenclature logicielle est produite pour les composants critiques. Les images et paquets proviennent de sources approuvées.

Les vulnérabilités sont qualifiées selon exploitabilité, exposition et impact opérationnel. Les délais de correction dépendent du risque et non du seul score public. Une vulnérabilité sans correctif reçoit des compensations, un propriétaire et une date de réexamen.

Les modèles téléchargés sont vérifiés par empreinte, licence et provenance. Les formats capables d’exécuter du code sont traités avec précaution. Les environnements d’évaluation sont isolés des données et réseaux sensibles.

Les tests incluent abus d’API, injection, escalade, exfiltration et indisponibilité. Pour le RAG, ils incluent prompt injection documentaire, contournement du filtre de Niveau d’accès, fuite par citation et empoisonnement du corpus.

Le déploiement est automatisé lorsque possible et conserve la trace de l’artefact exact. Marque de contrôle : **CANARI-NOVA-64**.

<div style="page-break-after: always;"></div>

## Page 4/5 — Fournisseurs et continuité

Avant contrat, le propriétaire évalue criticité, accès aux données, localisation, sous-traitants, pratiques de sécurité, notification d’incident, réversibilité, mises à jour et fin de service. Les exigences sont proportionnées au risque fournisseur et au produit.

Les fournisseurs critiques communiquent les changements susceptibles d’affecter sécurité ou conformité. Les contrats prévoient coopération d’incident, conservation de preuves et délai d’information. L’absence de visibilité est un risque explicite.

La continuité prévoit sauvegardes, restauration testée, fournisseurs alternatifs lorsque justifié et fonctionnement dégradé. Pour une fonction de sécurité, la perte du service cloud doit conduire à un état sûr, non à un comportement indéfini.

Les dépendances uniques sont inscrites au registre. Le plan de sortie couvre données, modèles, clés, formats et compétences. Une sauvegarde qui n’a jamais été restaurée n’est pas considérée comme une preuve suffisante.

La revue annuelle vérifie les attestations et incidents des fournisseurs. Marque de contrôle : **CANARI-NOVA-64**.

<div style="page-break-after: always;"></div>

## Page 5/5 — Incident et notifications

Toute suspicion d’incident déclenche préservation, confinement, analyse et communication selon la procédure VAS-PRO-SAF-030. Le RSSI tient l’heure de prise de connaissance et évalue l’impact sur les services, clients, données et opérations.

Lorsqu’un incident significatif relève du cadre NIS2 applicable, l’équipe prépare une alerte précoce dans les 24 heures, une notification dans les 72 heures et un rapport final dans le mois, sous réserve de la transposition et des instructions de l’autorité compétente.

La correction urgente respecte une voie de changement contrôlée. Pour un système embarqué, la sécurité aérienne valide que le correctif cyber n’introduit pas un danger fonctionnel. Une mise à jour non testée peut être plus dangereuse que la vulnérabilité qu’elle corrige.

Les clients affectés reçoivent les mesures nécessaires à leur protection. Les informations publiques sont approuvées par Communication, Juridique et RSSI.

Après incident, les détections, exercices, contrats et plans sont mis à jour. Marque de contrôle : **CANARI-NOVA-64**.
