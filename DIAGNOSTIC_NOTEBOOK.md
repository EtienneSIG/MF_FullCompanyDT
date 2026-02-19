# Cellule de diagnostic à ajouter au début du notebook 02_transform_to_silver

## Option 1 : Cellule Python complète (à insérer après la cellule Configuration)

```python
# ============================================================================
# DIAGNOSTIC - Vérifier les prérequis
# ============================================================================

print("="*80)
print("DIAGNOSTIC - Checking Prerequisites")
print("="*80)

# 1. Vérifier les fichiers CSV dans Files/bronze
print("\n1️⃣ Checking CSV files in Lakehouse...")
try:
    bronze_files = mssparkutils.fs.ls("Files/bronze/")
    domains = [f for f in bronze_files if f.isDir]
    print(f"✅ Found {len(domains)} domain folders in Files/bronze/")
    
    total_csv = 0
    for domain in domains[:5]:  # Show first 5
        csv_files = [f for f in mssparkutils.fs.ls(domain.path) if f.name.endswith('.csv')]
        total_csv += len(csv_files)
        print(f"   📁 {domain.name}: {len(csv_files)} CSV files")
    
    if len(domains) > 5:
        print(f"   ... and {len(domains) - 5} more domains")
    
    if total_csv == 0:
        print("\n⚠️  WARNING: No CSV files found!")
        print("   Action: Upload CSV files to Files/bronze/ first")
        
except Exception as e:
    print(f"❌ Cannot access Files/bronze/: {str(e)}")
    print("   Action: Upload CSV files to Lakehouse Files/bronze/")

# 2. Vérifier les tables Bronze
print("\n2️⃣ Checking Bronze Delta tables...")
all_tables = spark.catalog.listTables()

if len(all_tables) == 0:
    print("❌ No tables found in lakehouse!")
    print("   Action: Run notebook 01_ingest_to_bronze.ipynb first")
else:
    bronze_tables = [t for t in all_tables 
                     if not t.name.startswith("silver_") 
                     and not t.name.startswith("gold_")]
    
    if len(bronze_tables) == 0:
        print("❌ No Bronze tables found!")
        print("   Action: Run notebook 01_ingest_to_bronze.ipynb first")
    else:
        dimensions = [t for t in bronze_tables if t.name.startswith("dim")]
        facts = [t for t in bronze_tables if t.name.startswith("fact")]
        
        print(f"✅ Found {len(bronze_tables)} Bronze tables")
        print(f"   📊 Dimensions: {len(dimensions)}")
        print(f"   📈 Facts: {len(facts)}")
        
        # Show sample
        if dimensions:
            print(f"\n   Sample dimensions: {', '.join([t.name for t in dimensions[:3]])}")
        if facts:
            print(f"   Sample facts: {', '.join([t.name for t in facts[:3]])}")

# 3. Vérifier les tables Silver (si déjà créées)
print("\n3️⃣ Checking Silver tables (if already created)...")
silver_tables = [t for t in all_tables if t.name.startswith("silver_")]

if len(silver_tables) == 0:
    print("⏭️  No Silver tables yet (this is normal on first run)")
else:
    print(f"ℹ️  Found {len(silver_tables)} existing Silver tables")
    print("   Note: These will be overwritten when you run this notebook")

# 4. Conclusion
print("\n" + "="*80)
print("DIAGNOSTIC SUMMARY")
print("="*80)

ready = True

if total_csv == 0:
    print("❌ STEP 1 INCOMPLETE: Upload CSV files to Files/bronze/")
    ready = False
elif len(bronze_tables) == 0:
    print("❌ STEP 2 INCOMPLETE: Run notebook 01_ingest_to_bronze.ipynb")
    ready = False
else:
    print("✅ Prerequisites met - Ready to transform Bronze → Silver")

print("="*80)
```

## Option 2 : Commandes de vérification rapide

Avant d'exécuter le notebook 02, exécutez ces commandes dans une cellule :

```python
# Vérification rapide
print("Bronze tables:", len([t for t in spark.catalog.listTables() 
                             if not t.name.startswith(("silver_", "gold_"))]))

print("Files in bronze:", len(mssparkutils.fs.ls("Files/bronze/")))
```

Si le résultat est `0` pour l'un ou l'autre, vous devez d'abord :
1. Uploader les CSV dans Files/bronze/
2. Exécuter le notebook 01_ingest_to_bronze.ipynb
