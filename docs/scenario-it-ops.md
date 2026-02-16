# Scénario IT Operations - Amélioration de la Disponibilité et Performance

## 📊 Contexte Métier

L'équipe IT Ops doit garantir une disponibilité de 99.9% des systèmes critiques tout en gérant 800+ incidents/mois et en optimisant les coûts d'infrastructure.

## 🎯 Objectifs

1. Atteindre 99.9% de disponibilité (actuellement 99.2%)
2. Réduire le MTTR (Mean Time To Repair) à moins de 2 heures
3. Diminuer de 30% les incidents P1/P2
4. Optimiser les coûts cloud de 25%

## 📋 Questions Métier Clés

### Disponibilité & Performance
- Quel est notre uptime actuel par service critique ?
- Combien d'heures de downtime avons-nous eu ce mois ?
- Quels systèmes ont les plus forts taux d'incidents ?

### Gestion des Incidents
- Quel est notre MTTR moyen par sévérité ?
- Combien d'incidents P1 avons-nous eu ce trimestre ?
- Quels sont les patterns d'incidents récurrents ?

### Optimisation des Coûts
- Quelle est notre dépense cloud mensuelle par service ?
- Quelles ressources cloud sont sous-utilisées ?
- Quel est notre ROI sur les investissements infrastructure ?

## 📊 Données Disponibles

**Tables de Faits:**
- `gold_factincidents` - Incidents IT
- `gold_factcloudcosts` - Coûts cloud par service
- `gold_factactivities` - Maintenance et interventions

**Dimensions:**
- `gold_dimemployee` - Équipe IT
- `gold_dimdate` - Calendrier

## 🔍 Analyse Détaillée

### Scénario 1: Réduction des Incidents Critiques

**Situation:** 48 incidents P1 en Q4 2025, causant 156 heures de downtime cumulé

**Analyse:**
```
Incidents P1 : 48 (objectif <20)
Downtime total : 156 heures
Impact business estimé : €2.4M

Top 3 causes :
1. Database slowdown : 18 incidents (38%)
2. Network issues : 12 incidents (25%)
3. App crashes : 10 incidents (21%)
```

**Questions Data Agent:**
- "Montre-moi l'évolution des incidents P1 sur les 6 derniers mois"
- "Quels sont les patterns communs aux incidents database ?"
- "Quel est le MTTR moyen par type d'incident ?"

**Actions Recommandées:**
- Migrer vers database managed service (RDS) pour réduire incidents DB
- Implémenter monitoring proactif avec alerting prédictif
- Mettre en place un runbook automatisé pour incidents fréquents
- Renforcer la redondance réseau avec multi-AZ

### Scénario 2: Amélioration du MTTR

**Situation:** MTTR moyen de 4.2 heures, objectif 2 heures

**Analyse:**
```
MTTR P1 : 6.8 heures (objectif 1h)
MTTR P2 : 4.2 heures (objectif 4h)
MTTR P3 : 2.1 heures (objectif 8h)

Causes de lenteur :
- Diagnostic : 42% du temps
- Escalade/Approbation : 28%
- Résolution technique : 22%
- Communication : 8%
```

**Questions Data Agent:**
- "Quel est le temps moyen de diagnostic par type d'incident ?"
- "Combien d'incidents nécessitent une escalade ?"
- "Quels incidents se répètent le plus souvent ?"

**Actions Recommandées:**
- Déployer un système d'observabilité (Datadog, New Relic)
- Créer des runbooks automatisés pour top 20 incidents
- Former les L1/L2 pour réduire les escalades de 40%
- Implémenter ChatOps pour collaboration rapide

### Scénario 3: Optimisation Coûts Cloud

**Situation:** €145K/mois de dépenses cloud avec 32% de gaspillage identifié

**Analyse:**
```
Coûts mensuels : €145K
Gaspillage identifié : €46K (32%)

Détail du gaspillage :
- Instances EC2 oversized : €18K
- Storage non utilisé : €12K
- Snapshots obsolètes : €8K
- Environnements dev/test : €8K
```

**Questions Data Agent:**
- "Montre-moi les coûts cloud par environnement et par service"
- "Identifie les ressources non utilisées depuis 30 jours"
- "Quel est le coût par transaction pour chaque service ?"

**Actions Recommandées:**
- Automatiser shutdown des environnements dev/test (économie €8K/mois)
- Right-sizing des instances avec AWS Compute Optimizer (€18K/mois)
- Nettoyer storage et snapshots obsolètes (€12K/mois)
- Acheter Reserved Instances pour workloads stables (€15K/mois)
- Total économies : €53K/mois (36%)

## 📈 KPIs à Suivre

| KPI | Formule DAX | Cible | Actuel |
|-----|-------------|-------|--------|
| Uptime % | `[Availability %]` | 99.9% | 99.2% |
| MTTR (heures) | `[MTTR (Minutes)] / 60` | 2h | 4.2h |
| Incidents P1 | `[P1 Incidents]` | <20/trim | 48/trim |
| Downtime (heures) | `[Total Downtime (Hours)]` | <10h | 38h |
| Cloud Cost | Dépenses cloud mensuelles | €100K | €145K |
| Incidents Récurrents % | Incidents déjà vus / Total | <15% | 28% |

## 🎬 Démonstration

**Étape 1:** Ouvrir le rapport IT Operations Dashboard
**Étape 2:** Visualiser la heatmap de disponibilité par service
**Étape 3:** Interroger: "Quels services ont causé le plus de downtime ?"
**Étape 4:** Analyser le trend MTTR sur 12 mois
**Étape 5:** Explorer les opportunités d'optimisation cloud

## 💡 Insights Attendus

- Identification des single points of failure
- Prédiction des incidents basée sur patterns historiques
- ROI des investissements en monitoring et automation
- Plan de réduction des coûts cloud prioritisé
- Recommandations d'architecture pour améliorer la résilience
