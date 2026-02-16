# Scénario ESG - Réduction de l'Empreinte Carbone

## 📊 Contexte Métier

L'entreprise s'est engagée à atteindre la neutralité carbone d'ici 2030. Il faut mesurer, réduire et compenser les émissions de CO2 sur les scopes 1, 2 et 3.

## 🎯 Objectifs

1. Réduire les émissions de 40% d'ici 2028 (vs baseline 2023)
2. Atteindre 100% d'énergie renouvelable d'ici 2027
3. Engager 80% des fournisseurs stratégiques dans la démarche
4. Publier un rapport ESG conforme CSRD

## 📋 Questions Métier Clés

### Mesure des Émissions
- Quelles sont nos émissions totales par scope ?
- Quelle est notre intensité carbone (CO2e/€ de CA) ?
- Quels sont les principaux contributeurs d'émissions ?

### Trajectoire de Réduction
- Sommes-nous alignés avec notre trajectoire 1.5°C ?
- Quelle est la tendance YoY de nos émissions ?
- Quelles actions ont le plus d'impact ?

### Reporting & Compliance
- Avons-nous les données nécessaires pour le rapport CSRD ?
- Quelle est la qualité de nos données carbone ?
- Quels scopes/catégories manquent de mesure ?

## 📊 Données Disponibles

**Tables de Faits:**
- `gold_factemissions` - Émissions CO2e par source
- `gold_factcloudcosts` - Pour calcul empreinte cloud
- `gold_factproduction` - Pour intensité carbone

**Dimensions:**
- `gold_dimdate` - Calendrier
- Scopes & Catégories GHG Protocol

## 🔍 Analyse Détaillée

### Scénario 1: Décarbonation des Opérations

**Situation:** Émissions 2025 de 12,500 tCO2e, objectif 2028 de 7,500 tCO2e

**Analyse:**
```
Émissions totales 2025 : 12,500 tCO2e
Objectif 2028 : 7,500 tCO2e
Réduction nécessaire : 5,000 tCO2e (40%)

Répartition par scope :
- Scope 1 (combustion directe) : 1,800 tCO2e (14%)
- Scope 2 (électricité) : 2,200 tCO2e (18%)
- Scope 3 (chaîne de valeur) : 8,500 tCO2e (68%)
```

**Questions Data Agent:**
- "Montre-moi l'évolution de mes émissions par scope depuis 2023"
- "Quels sont les top 10 sources d'émissions ?"
- "Sommes-nous alignés avec notre trajectoire de réduction ?"

**Actions Recommandées:**
- **Scope 1** : Convertir la flotte véhicules en électrique (économie 450 tCO2e/an)
- **Scope 2** : Souscrire à des PPAs renouvelables (économie 2,200 tCO2e/an)
- **Scope 3** : Optimiser la logistique et privilégier fournisseurs bas carbone

### Scénario 2: Décarbonation du Cloud (Scope 3)

**Situation:** Cloud représente 1,850 tCO2e/an (15% du total), en croissance de 32%

**Analyse:**
```
Émissions cloud 2024 : 1,400 tCO2e
Émissions cloud 2025 : 1,850 tCO2e (+32%)

Par région :
- US East (charbon) : 890 tCO2e (48%)
- EU West (mix) : 520 tCO2e (28%)
- EU North (hydro) : 440 tCO2e (24%)
```

**Questions Data Agent:**
- "Quelle est l'empreinte carbone de nos ressources cloud ?"
- "Compare les émissions par région cloud"
- "Quel est l'impact d'une migration vers EU North ?"

**Actions Recommandées:**
- Migrer workloads de US East vers EU North (économie 450 tCO2e/an)
- Optimiser utilisation pour réduire ressources de 25% (économie 460 tCO2e/an)
- Sélectionner des régions bas carbone pour nouveaux projets

### Scénario 3: Engagement Fournisseurs (Scope 3)

**Situation:** 68% des émissions proviennent de la chaîne de valeur (Scope 3)

**Analyse:**
```
Émissions Scope 3 : 8,500 tCO2e
Top catégories :
1. Biens et services achetés : 4,200 tCO2e (49%)
2. Transport amont : 1,800 tCO2e (21%)
3. Déchets : 850 tCO2e (10%)

Fournisseurs stratégiques :
- Total : 120 fournisseurs
- Ayant un plan climat : 28 (23%)
- Objectif : 96 (80%)
```

**Questions Data Agent:**
- "Quels fournisseurs contribuent le plus à nos émissions ?"
- "Combien de nos fournisseurs ont des objectifs SBTi ?"
- "Quel est le potentiel de réduction avec engagement fournisseurs ?"

**Actions Recommandées:**
- Inclure critères carbone dans appels d'offres (score 20%)
- Privilégier fournisseurs avec objectifs SBTi validés
- Organiser des ateliers décarbonation avec top 20 fournisseurs
- Objectif : Réduire de 30% les émissions fournisseurs d'ici 2028

## 📈 KPIs à Suivre

| KPI | Formule DAX | Cible 2028 | Actuel |
|-----|-------------|------------|--------|
| Émissions totales (tCO2e) | `[Total Emissions (CO2e)]` | 7,500 | 12,500 |
| Scope 1 | `[Scope 1 Emissions]` | 900 | 1,800 |
| Scope 2 | `[Scope 2 Emissions]` | 0 | 2,200 |
| Scope 3 | `[Scope 3 Emissions]` | 6,600 | 8,500 |
| Intensité carbone | `[Emissions Intensity]` (tCO2e/M€) | 120 | 200 |
| % Énergie renouvelable | Part renouvelable / Total énergie | 100% | 35% |

## 🎬 Démonstration

**Étape 1:** Ouvrir le rapport ESG Dashboard
**Étape 2:** Visualiser la trajectoire d'émissions vs objectif 2030
**Étape 3:** Interroger: "Quelles actions ont le plus grand impact carbone ?"
**Étape 4:** Drill-down sur Scope 3 par catégorie
**Étape 5:** Simuler l'impact de la migration cloud vers régions bas carbone

## 💡 Insights Attendus

- Trajectoire actuelle vs objectif neutralité carbone
- Plan d'action priorisé par impact et coût (€/tCO2e évitée)
- Identification des hot spots d'émissions
- ROI des investissements décarbonation
- Compliance au CSRD et autres réglementations
