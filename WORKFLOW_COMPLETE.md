# Workflow complet - De la génération de données à l'analyse

## Étape 1 : Générer les données (LOCAL) ✅ FAIT

```powershell
cd MF_FullCompanyDT\data-gen
python generate_all.py
```

**Résultat** : Fichiers CSV dans `output/structured/`
- 1,622,192 enregistrements
- 16 domaines (crm, sales, supply_chain, etc.)

---

## Étape 2 : Uploader vers Fabric Lakehouse ⚠️ À FAIRE

### Option A : Via OneLake File Explorer (Recommandé)

1. Installez **OneLake File Explorer** si nécessaire
2. Montez votre Lakehouse
3. Copiez le contenu de `output/structured/` vers :
   ```
   [OneLake Drive]\[Workspace]\[Lakehouse]\Files\bronze\
   ```

### Option B : Script automatique (si OneLake monté)

```python
# Dans upload_to_fabric.py, modifiez :
ONELAKE_PATH = r"O:\VotreWorkspace\VotreLakehouse\Files\bronze"

# Puis exécutez :
python upload_to_fabric.py
```

### Option C : Via l'interface Fabric (Pour petits volumes)

1. Ouvrez votre Lakehouse dans Fabric
2. Cliquez sur **Files** > **Upload** > **Upload folder**
3. Uploadez chaque dossier de domaine depuis `output/structured/`

**Vérification** : Dans Fabric, vous devriez voir :
```
📁 Files
  └─ 📁 bronze
      ├─ 📁 dimensions (8 fichiers CSV)
      ├─ 📁 crm (2 fichiers)
      ├─ 📁 sales (2 fichiers)
      ├─ 📁 supply_chain (2 fichiers)
      └─ ... (etc.)
```

---

## Étape 3 : Exécuter 01_ingest_to_bronze.ipynb (FABRIC) ⚠️ À FAIRE

**Objectif** : Ingérer les CSV en tables Delta Bronze

1. Ouvrez le notebook dans Fabric
2. Attachez votre Lakehouse
3. Exécutez toutes les cellules (Run All)

**Résultat attendu** :
```
✅ Dimensions ingested: 8/8
✅ Fact tables ingested: 23
⏭️  Skipped: 0
❌ Failed: 0
```

**Tables créées** :
- DimDate, DimCustomer, DimProduct, DimEmployee, etc.
- FactSales, FactInventory, FactSupport, etc.

---

## Étape 4 : Exécuter 02_transform_to_silver.ipynb (FABRIC) ⏳ VOUS ÊTES ICI

**Objectif** : Transformer Bronze → Silver avec data quality

1. Vérifiez que le notebook 01 a réussi
2. Exécutez le notebook 02

**Résultat attendu** :
```
STEP 1: Transforming Dimension Tables
✅ Silver_DimCustomer created: 50,000 → 50,000 rows

STEP 2: Transforming Fact Tables
✅ Silver_FactSales created: 201,221 → 201,221 rows

STEP 3: Data Quality Validation
✅ silver_dimcustomer: 0 nulls in customer_id
✅ Primary key uniqueness: OK
```

**Erreur actuelle** : Les tables Bronze n'existent pas encore, donc rien à transformer.

---

## Étape 5 : Exécuter 03_build_gold_star_schema.ipynb (FABRIC)

**Objectif** : Créer le schéma en étoile optimisé pour l'analyse

1. Fusionne les dimensions et faits
2. Crée les tables Gold dénormalisées
3. Optimise pour les requêtes analytiques

---

## Étape 6 : Créer le Semantic Model Power BI (FABRIC)

1. Créez un nouveau **Semantic Model** dans Fabric
2. Connectez-le au Lakehouse (mode Direct Lake)
3. Importez les tables Gold
4. Configurez les relations et mesures DAX

---

## Étape 7 : Configurer le Data Agent (FABRIC)

1. Créez un nouveau **Data Agent** dans Fabric
2. Connectez-le au Semantic Model
3. Testez avec des questions en langage naturel

---

## Checklist Rapide

- [x] 1️⃣ Données générées localement (1.6M records)
- [ ] 2️⃣ CSV uploadés dans Lakehouse Files/bronze/
- [ ] 3️⃣ Notebook 01 - Ingestion Bronze (CSV → Delta)
- [ ] 4️⃣ Notebook 02 - Transformation Silver (Qualité)
- [ ] 5️⃣ Notebook 03 - Gold Star Schema (Analytics)
- [ ] 6️⃣ Semantic Model Power BI créé
- [ ] 7️⃣ Data Agent configuré et testé

---

## Commandes de diagnostic

### Vérifier les fichiers uploadés (dans un notebook Fabric)
```python
files = mssparkutils.fs.ls("Files/bronze/")
for f in files:
    print(f.name, f.size)
```

### Vérifier les tables Bronze créées
```python
tables = spark.catalog.listTables()
bronze = [t for t in tables if not t.name.startswith(("silver_", "gold_"))]
print(f"Bronze tables: {len(bronze)}")
for t in bronze:
    print(f"  - {t.name}")
```

### Vérifier les tables Silver créées
```python
silver = [t for t in spark.catalog.listTables() if t.name.startswith("silver_")]
print(f"Silver tables: {len(silver)}")
```

---

## Prochaine action recommandée

🎯 **Uploadez d'abord les CSV vers le Lakehouse**, puis exécutez les notebooks dans l'ordre !
