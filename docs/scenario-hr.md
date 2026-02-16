# Scénario HR - Gestion des Talents et Attrition

## 📊 Contexte Métier

Le département RH fait face à un taux d'attrition élevé (18% annualisé) et souhaite mettre en place des actions de rétention ciblées tout en optimisant le processus de recrutement.

## 🎯 Objectifs

1. Réduire le taux d'attrition volontaire à moins de 12%
2. Identifier les facteurs de risque de départ
3. Optimiser le temps et coût de recrutement
4. Améliorer l'engagement des employés

## 📋 Questions Métier Clés

### Analyse de l'Attrition
- Quel est notre taux d'attrition par département et par niveau ?
- Quels sont les profils d'employés les plus à risque de départ ?
- Quelle est la proportion de "regrettable losses" (talents clés) ?

### Recrutement
- Quel est notre time-to-fill moyen par poste ?
- Quel est le taux d'acceptation des offres ?
- Quels canaux de recrutement sont les plus efficaces ?

### Engagement
- Y a-t-il une corrélation entre satisfaction et attrition ?
- Quels managers ont les meilleurs taux de rétention ?
- Quel est l'impact des formations sur la rétention ?

## 📊 Données Disponibles

**Tables de Faits:**
- `gold_factattrition` - Départs d'employés
- `gold_facthiring` - Recrutements
- `gold_factactivities` - Activités RH (formations, évaluations)

**Dimensions:**
- `gold_dimemployee` - Profils employés (département, niveau, ancienneté)
- `gold_dimdate` - Calendrier

## 🔍 Analyse Détaillée

### Scénario 1: Réduction de l'Attrition dans l'IT

**Situation:** Le département IT a un taux d'attrition de 25%, bien au-dessus de la moyenne entreprise (18%)

**Analyse:**
```
- Profil des départs : seniors (5+ ans) partent pour la concurrence
- Motifs : rémunération non compétitive, manque d'évolution
- 70% des départs sont volontaires et regrettables
```

**Questions Data Agent:**
- "Montre-moi l'évolution de l'attrition IT sur les 12 derniers mois"
- "Quel est le profil type des employés IT qui partent ?"
- "Compare les salaires IT de notre entreprise vs le marché"

**Actions Recommandées:**
- Augmenter la grille salariale IT de 8-12%
- Créer un plan de carrière clair avec jalons tous les 18 mois
- Mettre en place des stock options pour les seniors
- Renforcer la formation continue (certifications cloud, AI)

### Scénario 2: Optimisation du Recrutement Sales

**Situation:** Time-to-fill de 75 jours pour les postes commerciaux, objectif 45 jours

**Analyse:**
```
- Étape la plus longue : validation des candidatures (30 jours)
- Taux d'acceptation des offres : 65% (objectif 80%)
- Coût par recrutement : €12,000
```

**Questions Data Agent:**
- "Quel est le time-to-fill par type de poste commercial ?"
- "Quels recruteurs ont les meilleurs taux de conversion ?"
- "Quel est le ROI des différents canaux de sourcing ?"

**Actions Recommandées:**
- Automatiser le screening initial avec l'IA
- Standardiser les entretiens avec des grilles d'évaluation
- Augmenter les salaires proposés pour améliorer l'acceptation
- Développer le vivier de candidats via LinkedIn

### Scénario 3: Prédiction des Départs à Risque

**Situation:** Anticiper les départs pour agir de manière proactive

**Analyse:**
```
Facteurs de risque identifiés :
- Ancienneté 2-4 ans (période critique)
- Pas de promotion depuis 3+ ans
- Manager avec fort taux d'attrition dans son équipe
- Scores d'engagement < 6/10
```

**Questions Data Agent:**
- "Identifie les employés avec 3+ facteurs de risque de départ"
- "Montre-moi les équipes avec le plus fort turnover"
- "Quel est le lien entre engagement et attrition ?"

**Actions Recommandées:**
- Créer une liste watch des employés à risque
- Organiser des one-on-ones avec le DRH
- Proposer des plans de développement personnalisés
- Améliorer la reconnaissance et les avantages

## 📈 KPIs à Suivre

| KPI | Formule DAX | Cible | Actuel |
|-----|-------------|-------|--------|
| Taux d'Attrition Total | `[Attrition Rate]` | 12% | 18% |
| Attrition Volontaire | `[Voluntary Attrition] / [Total Attrition]` | 60% | 78% |
| Regrettable Losses % | `[Regrettable Loss %]` | <30% | 45% |
| Time-to-Fill | `[Average Time to Fill (Days)]` | 45j | 62j |
| Taux Acceptation Offres | `[Offer Acceptance Rate]` | 80% | 68% |
| Coût par Recrutement | Moyenne des coûts de recrutement | €8K | €11K |

## 🎬 Démonstration

**Étape 1:** Ouvrir le rapport HR Dashboard
**Étape 2:** Visualiser la heatmap d'attrition par département
**Étape 3:** Interroger: "Quels sont les facteurs communs aux employés partis en 2025 ?"
**Étape 4:** Drill-down sur le département IT
**Étape 5:** Générer la liste des employés à risque avec recommandations

## 💡 Insights Attendus

- Identification des départements/managers à risque
- Profils d'employés susceptibles de partir dans les 6 prochains mois
- ROI des actions de rétention vs coût de remplacement
- Optimisation du budget recrutement par canal
- Plan d'action de rétention priorisé par impact
