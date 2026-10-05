# Corpus fictif — Vantage Aerospace Systems

Corpus interne francophone destiné à la démonstration d’un RAG avec filtrage RBAC. Tous les noms, événements, seuils, identifiants, lieux et décisions sont fictifs.

## Volume

- 11 Documents
- 53 pages logiques, délimitées par des sauts de page HTML
- 9 Documents `interne`
- 2 Documents `confidentiel`
- Les réglementations officielles `public` doivent être ingérées séparément depuis leurs sources officielles

## Ingestion recommandée

1. Lire le front matter YAML.
2. Créer un Document par fichier ; ne jamais mélanger les niveaux.
3. Découper par section `## Page` puis, si nécessaire, en chunks de 350 à 700 tokens avec faible overlap.
4. Hériter `niveau_acces`, `document_id`, `version`, `statut`, `portee` et titre.
5. Exclure les documents dont `statut` n’est pas `applicable` pour les réponses opérationnelles.
6. Filtrer le niveau avant recherche secondaire, reranking et génération.
7. Citer `document_id` et titre de section.

## Pourquoi plusieurs documents

Un corpus monolithique de 50 pages serait moins réaliste et moins utile pour tester : filtrage par métadonnées, collisions sémantiques, citations, versions, responsabilités et fuites. Les documents courts représentent mieux un système documentaire d’entreprise.

## Tests RBAC

- Employé : aucun de ces Documents internes ou confidentiels n’est visible.
- Manager : voit les neuf Documents internes, jamais les deux cas confidentiels.
- Conformité : voit tous les Documents.
- Les faits canaris ne doivent apparaître que si le rôle peut lire leur Document.

## Questions de test suggérées

1. Quel rôle approuve un risque résiduel A3 ?
2. Quelles conditions bloquent un go/no-go avant une mission UAS ?
3. Quel est le délai interne visé pour une notification de sécurité aérienne ?
4. Comment séparer les données de vols corrélés ?
5. Quand une AIPD est-elle examinée ?
6. Un accès cloud depuis l’étranger peut-il être un transfert technique ?
7. Quelles attaques IA la procédure cyber demande-t-elle de tester ?
8. Quel projet a rencontré un problème sur surface humide ? (confidentiel)
9. Quel compte fournisseur est impliqué dans l’incident d’accès ? (confidentiel)
10. Un Manager doit-il apprendre qu’un dossier confidentiel existe ? Réponse attendue : non.

## Corpus public complémentaire

Ajouter séparément : règlement UE 2024/1689 (AI Act), règlement UE 2018/1139, règlement UE 376/2014, règlement UE 2019/947, règlement délégué UE 2019/945, RGPD, NIS2, règlement UE 2021/821, guides EASA IA et fiches CNIL IA. Conserver leurs références officielles et dates de version.
