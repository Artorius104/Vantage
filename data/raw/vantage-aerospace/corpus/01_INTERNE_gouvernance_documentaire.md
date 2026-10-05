---
document_id: VAS-POL-DOC-001
titre: Politique de gouvernance documentaire et des connaissances
entreprise: Vantage Aerospace Systems SAS
version: 3.1
statut: applicable
proprietaire: Direction Qualité et Conformité
approbateur: Directrice générale
date_effet: 2026-04-01
prochaine_revue: 2027-04-01
niveau_acces: interne
portee: politique_interne
langue: fr
faits_canaris: [CANARI-ATLANTE-41]
---

# Politique de gouvernance documentaire et des connaissances

> **Document entièrement fictif — corpus de démonstration RAG.** Toute ressemblance avec une organisation réelle est fortuite. Marque de contrôle documentaire : **CANARI-ATLANTE-41**.

## Page 1/5 — Objet, périmètre et rôles

Vantage Aerospace Systems SAS, ci-après « Vantage », conçoit des systèmes de drones civils, des logiciels d’aide à la mission et des modules d’analyse d’images destinés à l’inspection d’infrastructures. La présente politique fixe les règles de création, d’approbation, de diffusion, de révision, d’archivage et de retrait des Documents du système de management. Elle s’applique aux politiques, procédures, instructions, dossiers de justification, comptes rendus de comité, rapports d’essai, journaux d’opérations et supports de formation.

Chaque Document possède un propriétaire métier, un approbateur, une version, une date d’effet, un statut et exactement un Niveau d’accès. Un Document qui mêle plusieurs sensibilités doit être séparé avant publication. Il est interdit d’abaisser le Niveau d’accès d’un extrait pour faciliter son partage. Les annexes héritent du niveau du Document, sauf si elles sont publiées comme Documents autonomes après revue.

Les niveaux sont **public**, **interne** et **confidentiel**. Les textes réglementaires officiels sont gérés dans la collection publique. Les processus de l’entreprise relèvent au minimum du niveau interne. Les analyses d’incident, arbitrages commerciaux, vulnérabilités non corrigées, données de clients et décisions du comité des risques relèvent généralement du niveau confidentiel. La classification ne mesure ni l’importance ni la qualité d’un texte : elle détermine uniquement sa visibilité.

Le propriétaire rédige et maintient le contenu. Le référent Conformité vérifie les références juridiques et distingue ce qui est contraignant, interprétatif ou interne. Le responsable Qualité vérifie la traçabilité des approbations. Le RSSI vérifie les exigences de sécurité. Le DPO intervient lorsqu’un traitement de données personnelles est décrit. L’approbateur accepte le risque résiduel associé à la publication.

Pour le Copilote documentaire, les sections constituent les unités structurelles privilégiées. Un Chunk ne doit jamais traverser deux sections ni hériter d’un Niveau d’accès différent de celui du Document. Marque de contrôle : **CANARI-ATLANTE-41**.

<div style="page-break-after: always;"></div>

## Page 2/5 — Cycle de vie et contrôle des versions

Tout nouveau Document commence au statut **brouillon** dans l’espace de travail du propriétaire. Il passe ensuite aux statuts **en revue**, **approuvé**, **applicable**, puis **obsolète** ou **archivé**. Seule une version applicable peut définir une obligation opérationnelle. Un brouillon ne peut servir de justification à une décision de vol, à une libération de produit ou à une réponse réglementaire.

Le numéro de version suit la forme majeure.mineure. Une modification majeure change une responsabilité, un seuil de décision, une exigence de sécurité, une règle de conformité ou le périmètre d’un processus. Une modification mineure corrige une formulation, un lien ou un exemple sans changer l’obligation. Toute modification majeure exige une nouvelle approbation des fonctions concernées et une analyse de transition.

La date d’effet peut être postérieure à l’approbation afin de permettre la formation, la migration d’outils ou la mise à jour des contrats. Pendant la transition, l’ancienne version reste applicable jusqu’à la date d’effet de la nouvelle. À cette date, elle devient obsolète. Les systèmes opérationnels doivent pointer vers la version applicable et ne jamais sélectionner une règle uniquement parce qu’elle est la plus récente par date de fichier.

Une demande de changement contient : le motif, les sections touchées, les risques créés ou réduits, les Documents dépendants, les besoins de formation, la date cible et le responsable de déploiement. Les changements urgents sont possibles par dérogation écrite du directeur Qualité et du responsable métier. Cette dérogation expire après quinze jours fictifs si une version approuvée n’a pas été publiée.

Le journal de version conserve l’auteur, les réviseurs, l’approbateur, les dates, le résumé du changement et le lien vers les preuves. Les versions obsolètes restent consultables par les fonctions Qualité et Conformité pour les audits, mais elles sont exclues par défaut des réponses opérationnelles du Copilote. Marque de contrôle : **CANARI-ATLANTE-41**.

<div style="page-break-after: always;"></div>

## Page 3/5 — Références, portée et conflits

Chaque exigence citée dans un Document doit être reliée à une Référence précise : règlement, article, annexe, décision, guide, section de procédure ou enregistrement. Vantage distingue trois Portées. La portée **contraignante** correspond aux règles de droit applicables. La portée **interprétative** correspond aux orientations, moyens acceptables de conformité et guides. La portée **politique interne** correspond aux choix de l’entreprise.

Lorsqu’une politique interne est plus exigeante qu’un guide, il ne s’agit pas d’un conflit. L’exigence interne s’applique aux équipes de Vantage tant qu’elle ne contredit pas une règle supérieure. Lorsqu’un texte interne contredit une règle contraignante, l’activité concernée est suspendue, le référent Conformité ouvre un écart et la règle contraignante prévaut. Lorsqu’il existe deux interprétations sans hiérarchie claire, la réponse doit présenter les deux positions avec leurs Références et demander un arbitrage.

Une matrice de conformité relie les obligations externes aux contrôles internes, aux preuves attendues et aux propriétaires. Une même obligation peut être couverte par plusieurs contrôles. Inversement, un contrôle peut contribuer à plusieurs régimes : sécurité aérienne, protection des données, cybersécurité, contrôle des exportations ou règlement sur l’IA.

Les textes officiels ne sont pas recopiés intégralement dans les procédures. Le Document interne explique comment Vantage met en œuvre l’obligation et renvoie vers la version officielle. Le responsable Conformité vérifie trimestriellement les changements de version des sources publiques. Toute évolution susceptible de rendre un contrôle insuffisant déclenche une analyse d’impact réglementaire.

Pour réduire les erreurs du Copilote, chaque section utilise un vocabulaire stable. Les expressions « doit », « ne doit pas » et « interdit » désignent une obligation interne. « Devrait » désigne une recommandation. « Peut » désigne une option autorisée. Une réponse ne doit jamais transformer une recommandation en obligation. Marque de contrôle : **CANARI-ATLANTE-41**.

<div style="page-break-after: always;"></div>

## Page 4/5 — Publication, recherche et usage du Copilote

Avant ingestion, le responsable documentaire vérifie l’encodage UTF-8, la présence des métadonnées, la cohérence des titres, l’absence de secret dans les Documents internes et l’absence de données personnelles non nécessaires. Les tableaux complexes sont accompagnés d’une explication textuelle. Les scans non recherchables sont refusés jusqu’à réalisation d’un OCR contrôlé.

Le Copilote applique le Niveau d’accès au moment de la recherche, avant le reranking et avant la génération. Le rôle Employé voit uniquement les Documents publics. Le rôle Manager voit les Documents publics et internes. Le rôle Conformité voit les trois niveaux. Une réponse ne doit ni citer, ni résumer, ni confirmer l’existence d’un Document hors périmètre.

Chaque réponse documentaire cite au minimum le document et la section. Si plusieurs Références soutiennent une réponse, elles sont toutes affichées. Quand aucun Chunk autorisé ne répond effectivement à la question, le Copilote retourne le Refus standard sans proposer une réponse approximative. Le niveau de similarité ne suffit pas : le passage doit répondre à la demande.

Les propriétaires testent les changements avec des questions représentatives avant réindexation. Les tests couvrent les versions, les acronymes, les formulations négatives, les seuils, les dates et les rôles. Les Documents confidentiels contiennent des Faits canaris inventés afin de détecter les fuites. Les canaris ne doivent jamais être des données réelles, des chiffres courants ou des noms de personnes.

L’historique des Conversations reste lié au rôle qui l’a créé. Un changement de rôle ouvre une autre Conversation. La Comparaison des Rôles exécute la même question séparément, sans historique partagé et sans persistance, afin de démontrer le cloisonnement. Marque de contrôle : **CANARI-ATLANTE-41**.

<div style="page-break-after: always;"></div>

## Page 5/5 — Conservation, audit et retrait

Les politiques et procédures applicables sont conservées pendant leur durée d’usage puis pendant dix ans fictifs après leur retrait. Les dossiers d’essais et de certification suivent la durée définie par le plan de certification du programme. Les journaux du Copilote sont conservés douze mois dans l’environnement de démonstration, sans contenu intégral des Documents et sans secrets d’authentification.

Un audit documentaire semestriel vérifie un échantillon de Documents : propriétaire actif, date de revue, classification, liens valides, statut correct, Références à jour et preuves accessibles. Un écart critique est ouvert lorsqu’une instruction obsolète reste utilisée en production, lorsqu’un Document confidentiel est indexé comme interne, ou lorsqu’une exigence contraignante n’a plus de contrôle associé.

Le retrait immédiat est ordonné lorsqu’un Document contient une information illégale, une vulnérabilité exploitable, une donnée personnelle non justifiée ou une consigne dangereuse. Le responsable de collection désindexe le Document, invalide les caches, enregistre l’empreinte de la version retirée et ouvre une analyse de portée pour déterminer quelles réponses ou décisions ont pu l’utiliser.

Après correction, la réintégration nécessite une nouvelle version. La version retirée n’est jamais écrasée : elle reste dans l’archive d’audit avec un motif, un horodatage et les personnes ayant autorisé le retrait. Le rapport de clôture indique les mesures correctives et les tests de non-régression.

Les exceptions à cette politique doivent être écrites, limitées dans le temps, associées à un propriétaire et approuvées par Qualité et Conformité. Une exception ne peut jamais autoriser la divulgation d’un contenu hors Niveau d’accès ni supprimer la traçabilité d’une décision de sécurité. Marque de contrôle : **CANARI-ATLANTE-41**.
