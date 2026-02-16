# Scénario Sales - Analyse des Performances Commerciales

## 📊 Contexte Métier

L'équipe commerciale souhaite optimiser ses performances de vente en analysant les tendances, la rentabilité par canal et par client, ainsi que l'efficacité de la force de vente.

## 🎯 Objectifs

1. Identifier les produits et clients les plus rentables
2. Analyser les tendances de vente par canal (Online, Retail, B2B)
3. Optimiser les marges en réduisant les retours
4. Améliorer le pipeline commercial et le taux de conversion

## 📋 Questions Métier Clés

### Performance Globale
- Quel est notre chiffre d'affaires total ce trimestre vs l'année dernière ?
- Quelle est notre marge brute moyenne par canal de vente ?
- Quels sont les 10 produits générant le plus de revenus ?

### Analyse Client
- Qui sont nos top 20 clients en termes de revenus ?
- Quel est le panier moyen par segment client (SMB, Mid-Market, Enterprise) ?
- Combien de nouveaux clients avons-nous acquis ce mois-ci ?

### Efficacité Commerciale
- Quel est le taux de conversion des opportunités par commercial ?
- Quelle est la valeur moyenne des deals fermés-gagnés ?
- Combien de temps en moyenne pour conclure une vente ?

### Analyse des Retours
- Quel est notre taux de retour par catégorie de produit ?
- Quels produits ont le plus fort taux de retour ?
- Quel est l'impact financier des retours sur notre marge nette ?

## 📊 Données Disponibles

**Tables de Faits:**
- `gold_factsales` - Transactions de vente détaillées
- `gold_factreturns` - Retours produits
- `gold_factopportunities` - Pipeline commercial CRM

**Dimensions:**
- `gold_dimcustomer` - Informations clients
- `gold_dimproduct` - Catalogue produits
- `gold_dimemployee` - Force de vente
- `gold_dimdate` - Calendrier fiscal

## 🔍 Analyse Détaillée

### Scénario 1: Optimisation des Marges

**Situation:** La marge brute a diminué de 3% au Q4 2025

**Analyse:**
```
- Identifier les produits à faible marge vendus en volume
- Comparer les marges par canal de distribution
- Analyser l'impact des promotions sur la rentabilité
```

**Questions Data Agent:**
- "Montre-moi les produits avec une marge inférieure à 30% qui représentent plus de 10% des ventes"
- "Compare la marge moyenne par canal entre Q3 et Q4 2025"
- "Quel est l'impact des remises sur notre marge globale ?"

**Actions Recommandées:**
- Augmenter les prix des produits à faible marge
- Réduire les promotions sur les produits déjà rentables
- Négocier les coûts d'achat avec les fournisseurs

### Scénario 2: Réduction du Taux de Retours

**Situation:** Le taux de retour atteint 8.5%, au-dessus de l'objectif de 5%

**Analyse:**
```
- Identifier les catégories de produits avec les plus forts retours
- Analyser les motifs de retour (défaut, insatisfaction, erreur commande)
- Corréler avec les avis clients et scores de qualité
```

**Questions Data Agent:**
- "Quels sont les 10 produits avec le plus haut taux de retour ?"
- "Montre-moi l'évolution du taux de retour par mois pour 2025"
- "Quel est le coût total des retours par catégorie de produit ?"

**Actions Recommandées:**
- Améliorer les descriptions produits pour réduire les erreurs
- Renforcer le contrôle qualité sur les produits à fort taux de retour
- Former les vendeurs sur les produits problématiques

### Scénario 3: Accélération du Pipeline Commercial

**Situation:** Le cycle de vente moyen est de 85 jours, objectif 60 jours

**Analyse:**
```
- Identifier les étapes du pipeline où les deals stagnent
- Analyser les taux de conversion par étape
- Comparer les performances par commercial
```

**Questions Data Agent:**
- "Quel est le taux de conversion à chaque étape du pipeline ?"
- "Quels commerciaux ont les cycles de vente les plus courts ?"
- "Combien d'opportunités sont bloquées depuis plus de 60 jours ?"

**Actions Recommandées:**
- Automatiser le suivi des opportunités dormantes
- Former les commerciaux sur les meilleures pratiques des top performers
- Simplifier le processus de validation des deals

## 📈 KPIs à Suivre

| KPI | Formule DAX | Cible | Actuel |
|-----|-------------|-------|--------|
| Revenus | `[Total Revenue]` | €50M | - |
| Marge Brute % | `[Gross Margin %]` | 40% | - |
| Panier Moyen | `[Average Order Value]` | €5,000 | - |
| Taux de Retour | `[Return Rate]` | 5% | - |
| Win Rate | `[Win Rate %]` | 30% | - |
| Cycle de Vente | Moyenne jours entre création et clôture | 60j | - |

## 🎬 Démonstration

**Étape 1:** Ouvrir le rapport Sales Dashboard
**Étape 2:** Filtrer sur Q4 2025
**Étape 3:** Interroger le Data Agent: "Montre-moi les tendances de revenus par canal"
**Étape 4:** Drill-down sur les produits à forte croissance
**Étape 5:** Analyser les opportunités en cours pour prédire Q1 2026

## 💡 Insights Attendus

- Identification des segments clients les plus rentables
- Opportunités de cross-sell/up-sell
- Prédiction des revenus futurs basée sur le pipeline
- Actions correctives pour réduire les retours
- Optimisation de l'allocation des ressources commerciales
