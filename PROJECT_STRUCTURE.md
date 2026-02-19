# MF_FullCompanyDT - Structure du Projet

## 📁 Structure nettoyée (Février 2026)

```
MF_FullCompanyDT/
├── .git/                    # Repository Git
├── .gitignore              # Configuration Git
├── .gitattributes          # Configuration Git
│
├── README.md               # Documentation principale du projet
├── AGENTS.md               # Configuration et documentation des agents Fabric
├── requirements.txt        # Dépendances Python
│
├── data-gen/               # 🔧 Générateur de données synthétiques
│   ├── config.yml          # Configuration de génération (dates, volumes, etc.)
│   ├── generate_all.py     # Script principal de génération
│   ├── upload_to_fabric.py # Script d'upload vers Fabric Lakehouse
│   ├── generators/         # Générateurs par domaine (15+ domaines)
│   ├── utils/              # Utilitaires (dimensions, qualité, texte)
│   └── output/             # 📊 Données générées (CSV)
│       ├── structured/     # 1.6M+ enregistrements en CSV
│       │   ├── dimensions/ # DimDate, DimCustomer, DimProduct, etc.
│       │   ├── sales/
│       │   ├── crm/
│       │   ├── hr/
│       │   ├── supply_chain/
│       │   ├── manufacturing/
│       │   ├── finance/
│       │   ├── esg/
│       │   ├── call_center/
│       │   ├── itops/
│       │   ├── finops/
│       │   ├── rd/
│       │   ├── quality_security/
│       │   ├── risk_compliance/
│       │   └── marketing/
│       └── unstructured/   # Fichiers texte (5000+ documents)
│
├── fabric/                 # 📓 Notebooks Microsoft Fabric
│   ├── data-agent/         # Configuration Data Agent
│   │   ├── instructions.md
│   │   └── examples.md
│   └── notebooks/          # Notebooks de transformation (Medallion)
│       ├── 01_ingest_to_bronze.ipynb       # CSV → Bronze Delta
│       ├── 02_transform_to_silver.ipynb    # Qualité & conformité
│       ├── 03_build_gold_star_schema.ipynb # Star schema analytique
│       ├── 04_create_shortcuts.ipynb       # OneLake shortcuts
│       └── 05_ai_transformations.ipynb     # AI sur non-structuré
│
└── docs/                   # 📚 Documentation complète
    ├── data-catalog.md                 # Dictionnaire de données
    ├── demo-script.md                  # Script de démonstration
    ├── security-and-governance.md      # Sécurité et gouvernance
    ├── shortcuts-and-ai-transforms.md  # Guide AI shortcuts
    ├── scenario-sales.md               # Scénarios analytiques
    ├── scenario-finance.md
    ├── scenario-hr.md
    ├── scenario-esg.md
    ├── scenario-customer-service.md
    ├── scenario-it-ops.md
    ├── scenario-operations.md
    └── scenario-cross-domain.md
```

## 🗑️ Fichiers supprimés (nettoyage)

### Fichiers temporaires
- ✅ `DIAGNOSTIC_NOTEBOOK.md` - Guide diagnostic temporaire
- ✅ `WORKFLOW_COMPLETE.md` - Documentation workflow temporaire
- ✅ `DEMO_CHECKLIST.md` - Checklist temporaire
- ✅ `PROJECT_STATUS.md` - Status temporaire

### Fichiers data-gen/
- ✅ `cleanup_duplicate_folders.py` - Script de nettoyage (obsolète)
- ✅ `data_generation.log` - Log de génération
- ✅ `UPLOAD_TO_FABRIC.md` - Documentation upload temporaire

## 🚀 Quick Start

### 1. Générer les données
```bash
cd data-gen
python generate_all.py
```

### 2. Uploader vers Fabric
```bash
# Modifier le chemin OneLake dans upload_to_fabric.py
python upload_to_fabric.py
```

### 3. Exécuter les notebooks Fabric
1. `01_ingest_to_bronze.ipynb` - Ingestion CSV vers Delta
2. `02_transform_to_silver.ipynb` - Transformation et qualité
3. `03_build_gold_star_schema.ipynb` - Star schema
4. `04_create_shortcuts.ipynb` - OneLake shortcuts
5. `05_ai_transformations.ipynb` - AI sur texte

### 4. Créer le Semantic Model
- Direct Lake connection
- Configurer relations
- Ajouter mesures DAX (voir `docs/`)

### 5. Configurer Data Agent
- Utiliser `fabric/data-agent/instructions.md`
- Exemples dans `fabric/data-agent/examples.md`

## 📊 Données générées

- **1,622,192** enregistrements structurés
- **8** dimensions conformed
- **23+** tables de faits
- **15** domaines métier
- **5,000+** documents non-structurés

## 📖 Documentation

Voir le dossier [docs/](docs/) pour la documentation complète :
- Architecture Medallion (Bronze/Silver/Gold)
- Catalogue de données complet
- Scénarios d'analyse par domaine
- Guide de démonstration
- Configuration sécurité et gouvernance

## 🔍 Support

Pour plus d'informations, voir :
- [README.md](README.md) - Vue d'ensemble complète
- [AGENTS.md](AGENTS.md) - Configuration agents
- [docs/demo-script.md](docs/demo-script.md) - Script de démo

---

**Dernière mise à jour** : Février 2026  
**Status** : Production Ready ✅
