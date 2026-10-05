# Conception d’un corpus RAG fictif pour une entreprise aérospatiale

## Réponse directe

Le meilleur corpus n’est pas un faux « manuel d’entreprise » unique, mais un ensemble de politiques, procédures, dossiers de décision et rapports d’incident. Cette structure produit des questions réalistes, des recouvrements contrôlés et des différences de Niveau d’accès utiles au test du retrieval et du RBAC.

Le corpus livré représente Vantage Aerospace Systems SAS, entreprise fictive de drones civils et d’IA embarquée. Il couvre 53 pages logiques. Il complète, sans les reproduire, les textes publics qui doivent être ingérés dans une collection `public`.

## Documents inclus

| ID | Document | Pages | Niveau | Finalité RAG |
|---|---|---:|---|---|
| VAS-POL-DOC-001 | Gouvernance documentaire | 5 | interne | Versions, portée, citations, retrait |
| VAS-POL-AI-002 | Gouvernance IA | 6 | interne | Qualification, risques, supervision, suivi |
| VAS-PRO-AI-014 | Assurance IA et données | 7 | interne | Data lineage, validation, robustesse, logs |
| VAS-PRO-OPS-021 | Opérations UAS | 6 | interne | Autorisation, SORA, go/no-go, urgence |
| VAS-PRO-SAF-030 | Événements | 5 | interne | Signalement, délais, enquête, CAPA |
| VAS-PRO-CYB-040 | Cybersécurité | 5 | interne | Accès, supply chain, vulnérabilités, NIS2 |
| VAS-PRO-DAT-050 | Données et RGPD | 5 | interne | Finalité, AIPD, droits, violation |
| VAS-PRO-EXP-060 | Contrôle export | 4 | interne | Double usage, transferts, licences |
| VAS-PRO-CFG-070 | Configuration | 4 | interne | Baseline, changement, libération, retrait |
| VAS-CAS-CONF-101 | Cas Asterion | 3 | confidentiel | Faiblesse IA et décision sensible |
| VAS-CAS-CONF-102 | Incident Solstice | 3 | confidentiel | Accès fournisseur et réponse cyber |

## Ancrage réglementaire

Le règlement UE 2018/1139 établit un cadre commun visant un niveau élevé et uniforme de sécurité de l’aviation civile ; Part-21 organise notamment la navigabilité initiale et la certification des produits et organisations[cite:19][cite:23]. Le corpus traduit cela en contrôles internes de configuration, preuves, approbations et événements, sans prétendre reproduire une organisation certifiée réelle.

Le règlement UE 376/2014 organise la notification, l’analyse et le suivi des événements de sécurité ; les événements concernés sont à notifier dans les 72 heures après prise de connaissance, sauf circonstances exceptionnelles[cite:22][cite:31]. La procédure interne reprend ce délai comme cible et distingue notification initiale, enquête et action corrective.

Les opérations UAS relèvent des catégories ouverte, spécifique ou certifiée ; pour une opération spécifique non couverte par un scénario standard, la SORA permet d’identifier risques, mesures et objectifs de sécurité[cite:68][cite:69]. Le corpus incorpore donc autorisations, dossier mission, risques au sol et en air, confinement et critères go/no-go.

L’AI Act classe comme potentiellement à haut risque les systèmes d’IA servant de composant de sécurité d’un produit couvert par une législation de l’Union et soumis à évaluation tierce ; l’aviation figure dans ce cadre[cite:4]. Les exigences associées couvrent gestion des risques, gouvernance des données, documentation, logs, transparence, supervision humaine, robustesse, cybersécurité, système qualité et évaluation de conformité[cite:4].

Le RGPD exige une analyse d’impact lorsque le traitement susceptible d’utiliser de nouvelles technologies présente un risque élevé, et encadre les décisions fondées exclusivement sur un traitement automatisé produisant des effets importants[cite:36]. La CNIL recommande en outre de présumer nécessaire l’examen d’une AIPD pour les systèmes IA à haut risque traitant des données personnelles et insiste sur les habilitations, la traçabilité et l’analyse des risques[cite:50][cite:52].

NIS2 prévoit une approche couvrant analyse des risques, incidents, continuité et sécurité de la chaîne d’approvisionnement ; son schéma de notification comporte notamment alerte précoce sous 24 heures, notification sous 72 heures et rapport final sous un mois[cite:35][cite:42]. Le corpus formule ces délais avec prudence, car leur application concrète dépend du périmètre de l’entité et du droit national transposé.

Le règlement UE 2021/821 contrôle exports, courtage, assistance, transit et transfert de biens à double usage, y compris logiciels et technologies pouvant servir à des usages civils et militaires[cite:43]. C’est pourquoi le corpus traite aussi les accès cloud, dépôts, assistance distante et modèles, plutôt que les seuls envois physiques.

## Choix RAG

Chaque fichier contient exactement un Niveau d’accès. Les cas sensibles recouvrent volontairement des thèmes présents dans les procédures internes : validation IA, accès fournisseur, incidents et changement. Ce recouvrement est essentiel pour produire des Paires exposées où un retriever sans filtre trouverait une réponse confidentielle plausible.

Les faits canaris sont des identifiants fictifs uniques. Ils permettent de mesurer une fuite de réponse, tandis que l’inspection des chunks passés au générateur mesure la fuite de contexte. Le filtrage doit donc intervenir avant reranking et génération, conformément au modèle fonctionnel fourni dans les documents de projet.

Le front matter fournit les métadonnées nécessaires. Pour l’ingestion, conserver `document_id`, `niveau_acces`, `version`, `statut`, `portee`, le titre de section et une empreinte du fichier. Le chunking par section est préférable ici au découpage aveugle : responsabilités, conditions et exceptions restent réunies.

## Alternative utile

Une variante encore plus exigeante consisterait à ajouter deux versions obsolètes contenant des règles anciennes et un document public de FAQ client. Le retriever devrait alors filtrer simultanément par Niveau d’accès et statut, puis gérer les questions temporelles. Cette extension est plus démonstrative qu’un simple ajout de pages.

## Limites

Les Documents internes sont fictifs et pédagogiques : ils ne constituent ni conseil juridique, ni manuel d’exploitation, ni moyen de conformité EASA. Les textes réglementaires et guides officiels doivent rester la source publique de référence et être versionnés séparément.
