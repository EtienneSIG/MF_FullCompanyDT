# Scénario Finance - Pilotage Budgétaire et Cash Flow

## 📊 Contexte Métier

La direction financière doit piloter la performance P&L, gérer le budget vs actuals, et optimiser le cash flow dans un contexte de croissance rapide et d'investissements importants.

## 🎯 Objectifs

1. Maintenir une marge EBITDA > 15%
2. Réduire les écarts budget vs actuals à moins de 5%
3. Améliorer le DSO (Days Sales Outstanding) à 45 jours
4. Optimiser l'allocation budgétaire par département

## 📋 Questions Métier Clés

### Performance Financière
- Quel est notre EBITDA actuel vs budget vs année précédente ?
- Quels départements dépassent leur budget et pourquoi ?
- Quelle est notre burn rate mensuel ?

### Gestion du Cash
- Quel est notre DSO actuel et par segment client ?
- Combien avons-nous de créances de plus de 60 jours ?
- Quel est notre working capital requirement ?

### Analyse des Coûts
- Quels sont les postes de coûts ayant le plus augmenté ?
- Quelle est la répartition des coûts fixes vs variables ?
- Y a-t-il des opportunités d'économies ?

## 📊 Données Disponibles

**Tables de Faits:**
- `gold_factgeneralledger` - Grand livre comptable
- `gold_factbudget` - Budget par département/compte (non disponible - à créer)
- `gold_factsales` - Pour analyse du CA
- `gold_factcloudcosts` - Coûts cloud (FinOps)

**Dimensions:**
- `gold_dimdate` - Calendrier fiscal
- Comptes (à créer dans DimAccount)
- Centres de coûts (départements)

## 🔍 Analyse Détaillée

### Scénario 1: Dépassement Budgétaire R&D

**Situation:** Le département R&D a dépassé son budget Q4 de 18%, mettant en péril l'objectif EBITDA

**Analyse:**
```
Budget R&D Q4 : €2.5M
Actuel Q4 : €2.95M
Variance : +€450K (+18%)

Causes identifiées :
- Recrutements non budgétés : +€180K
- Cloud computing : +€120K
- Équipements lab : +€150K
```

**Questions Data Agent:**
- "Montre-moi l'évolution mensuelle des dépenses R&D vs budget"
- "Quels sont les postes de coûts R&D ayant le plus dérivé ?"
- "Compare les dépenses R&D avec les autres départements"

**Actions Recommandées:**
- Geler les recrutements R&D jusqu'à Q2 2026
- Optimiser l'utilisation du cloud (right-sizing, reserved instances)
- Reporter les achats d'équipements non critiques
- Réviser le budget 2026 avec une marge de sécurité

### Scénario 2: Amélioration du Cash Flow

**Situation:** DSO de 68 jours, objectif 45 jours, impactant la trésorerie

**Analyse:**
```
Créances totales : €8.5M
Dont > 60 jours : €2.8M (33%)
DSO actuel : 68 jours
Objectif DSO : 45 jours
Manque à gagner trésorerie : ~€3.2M
```

**Questions Data Agent:**
- "Quels clients ont des factures impayées depuis plus de 60 jours ?"
- "Quel est le DSO par segment client (SMB, Mid, Enterprise) ?"
- "Montre-moi l'évolution du DSO sur les 12 derniers mois"

**Actions Recommandées:**
- Relancer agressivement les top 20 créances anciennes
- Mettre en place des pénalités de retard automatiques
- Offrir 2% d'escompte pour paiement à 15 jours
- Demander 50% d'acompte pour les nouveaux clients
- Externaliser le recouvrement pour créances > 90j

### Scénario 3: Optimisation des Coûts Cloud (FinOps)

**Situation:** Coûts cloud ont augmenté de 45% sans croissance proportionnelle du business

**Analyse:**
```
Coûts cloud 2024 : €1.2M
Coûts cloud 2025 : €1.74M (+45%)
Croissance revenus : +22%

Gaspillage identifié :
- Instances EC2 oversized : €180K/an
- Storage non utilisé : €95K/an
- Environnements dev/test non éteints : €120K/an
```

**Questions Data Agent:**
- "Montre-moi les coûts cloud par service et par environnement"
- "Identifie les ressources cloud non utilisées depuis 30+ jours"
- "Compare notre coût cloud par utilisateur vs benchmark industry"

**Actions Recommandées:**
- Automatiser l'arrêt des environnements dev/test hors heures
- Migrer vers instances spot pour les workloads non critiques
- Acheter des reserved instances pour réduire de 40% les coûts stables
- Nettoyer le stockage obsolète et archiver en Glacier
- Mettre en place des budgets alerts par équipe

## 📈 KPIs à Suivre

| KPI | Formule DAX | Cible | Actuel |
|-----|-------------|-------|--------|
| EBITDA % | (EBITDA / Revenus) | 15% | - |
| Variance Budget | `[Variance %]` | <5% | - |
| DSO | (Créances / CA) * 365 | 45j | 68j |
| Burn Rate | Dépenses mensuelles moyennes | €4.2M | - |
| Operating Ratio | (OpEx / Revenus) | <75% | - |
| Cloud Cost per User | Coûts cloud / nb employés | €1,200 | €1,680 |

## 🎬 Démonstration

**Étape 1:** Ouvrir le rapport Finance Executive Dashboard
**Étape 2:** Visualiser le P&L actuel vs budget vs N-1
**Étape 3:** Interroger: "Quels départements ont le plus grand écart budget ?"
**Étape 4:** Drill-down sur R&D pour analyser les drivers de variance
**Étape 5:** Analyser le bridge de l'EBITDA

## 💡 Insights Attendus

- Identification précise des variances budgétaires par nature de coûts
- Prédiction du cash flow sur 3 mois
- Opportunités d'optimisation des coûts (€500K+ identifiés)
- Recommandations de réallocation budgétaire inter-départements
- Simulations de scénarios What-If pour 2026
