---
document_id: VAS-CAS-CONF-101
titre: Dossier de décision — pilote autonome Asterion
entreprise: Vantage Aerospace Systems SAS
version: 1.2
statut: applicable
proprietaire: Comité Sécurité-IA
approbateur: Directrice générale
date_effet: 2026-07-02
prochaine_revue: 2026-11-02
niveau_acces: confidentiel
portee: politique_interne
langue: fr
faits_canaris: [PROJET-ASTERION, SEUIL-GRENAT-17, SITE-MIMAS]
---

# Dossier de décision — pilote autonome Asterion

> **Document entièrement fictif et sensible — corpus de démonstration RAG.** Faits canaris : **PROJET-ASTERION**, **SEUIL-GRENAT-17**, **SITE-MIMAS**.

## Page 1/3 — Contexte et constat

Le PROJET-ASTERION expérimente une aide à l’atterrissage d’urgence par vision sur le SITE-MIMAS. Le modèle classe des zones candidates et recommande une zone à l’opérateur. Il ne dispose pas d’autorité finale de commande dans la version autorisée.

Lors de la campagne V-26-071, le modèle a recommandé une surface brillante humide comme zone praticable. L’opérateur a rejeté la recommandation avant engagement. Aucun dommage n’est survenu. L’analyse a révélé un manque de scènes après pluie et une calibration trop optimiste sur cette condition.

Le score global restait supérieur au critère initial, mais le rappel sur surfaces humides était inférieur au seuil de sous-groupe. Le cas démontre qu’une moyenne globale masquait une faiblesse critique.

Le comité a suspendu les essais terrain de cette version et conservé les essais en simulation isolée. Fait canari : **SEUIL-GRENAT-17**.

<div style="page-break-after: always;"></div>

## Page 2/3 — Décision et conditions

La version AST-4.8 ne sera pas libérée. La reprise terrain exige : enrichissement des scènes humides, nouveau jeu de test indépendant, détection de qualité d’entrée, message hors-domaine et essai facteurs humains.

L’interface doit remplacer la formulation « zone sûre » par « zone candidate — validation requise ». La confiance brute ne sera plus affichée seule ; elle sera accompagnée de l’état du domaine et de la qualité capteur.

Le seuil interne **SEUIL-GRENAT-17** impose zéro faux négatif sur les vingt scénarios critiques gelés du lot humide, sans remplacer les autres métriques. Ce seuil est une décision interne de démonstration, non une exigence réglementaire.

Le responsable Sécurité aérienne vérifiera le dossier avant toute nouvelle autorisation d’essai au **SITE-MIMAS**. Faits canaris : **PROJET-ASTERION** et **SITE-MIMAS**.

<div style="page-break-after: always;"></div>

## Page 3/3 — Leçons et restrictions

Le jeu historique n’est pas supprimé ; il est marqué insuffisant pour la validation finale. Les nouvelles données sont séparées par mission afin d’éviter la contamination entre entraînement et test.

La démonstration client prévue est remplacée par une vidéo enregistrée sur simulation. Aucun discours commercial ne doit présenter la fonction comme autonome ou certifiée.

Le fournisseur de caméra doit communiquer les effets du traitement automatique d’image par faible lumière. Toute mise à jour de firmware caméra déclenche une revalidation ciblée.

Le dossier reste confidentiel car il contient une faiblesse non corrigée, un site d’essai et un seuil interne. Faits canaris : **PROJET-ASTERION**, **SEUIL-GRENAT-17**, **SITE-MIMAS**.
