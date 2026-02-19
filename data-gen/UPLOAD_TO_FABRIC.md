# Upload données vers Microsoft Fabric Lakehouse

## Contexte
Les fichiers CSV ont été générés localement dans `output/structured/` et doivent être uploadés vers le Lakehouse Fabric pour être ingérés dans la couche Bronze.

## Structure attendue dans Fabric

Dans votre Lakehouse Fabric, créez cette structure dans **Files** :

```
📁 Files
  └─ 📁 bronze
      ├─ 📁 dimensions
      │   ├─ DimDate.csv
      │   ├─ DimCustomer.csv
      │   ├─ DimProduct.csv
      │   ├─ DimEmployee.csv
      │   ├─ DimGeography.csv
      │   ├─ DimFacility.csv
      │   ├─ DimProject.csv
      │   └─ DimAccount.csv
      ├─ 📁 crm
      │   ├─ FactOpportunities.csv
      │   └─ FactActivities.csv
      ├─ 📁 sales
      │   ├─ FactSales.csv
      │   └─ FactReturns.csv
      ├─ 📁 hr
      │   ├─ FactAttrition.csv
      │   └─ FactHiring.csv
      ├─ 📁 supply_chain
      │   ├─ FactInventory.csv
      │   └─ FactPurchaseOrders.csv
      ├─ 📁 manufacturing
      │   ├─ FactProduction.csv
      │   └─ FactWorkOrders.csv
      ├─ 📁 finance
      │   ├─ FactGeneralLedger.csv
      │   └─ FactBudget.csv
      ├─ 📁 esg
      │   └─ FactEmissions.csv
      ├─ 📁 call_center
      │   └─ FactSupport.csv
      ├─ 📁 itops
      │   └─ FactIncidents.csv
      ├─ 📁 finops
      │   └─ FactCloudCosts.csv
      ├─ 📁 rd
      │   └─ FactExperiments.csv
      ├─ 📁 quality_security
      │   ├─ FactDefects.csv
      │   └─ FactSecurityEvents.csv
      ├─ 📁 risk_compliance
      │   ├─ FactRisks.csv
      │   ├─ FactAudits.csv
      │   └─ FactComplianceChecks.csv
      ├─ 📁 marketing
      │   └─ FactCampaigns.csv
      └─ 📁 product
          └─ DimProductBOM.csv
```

## Méthodes d'upload

### Option 1 : Via l'interface Fabric (recommandé pour les petits datasets)

1. Ouvrez votre Lakehouse dans Microsoft Fabric
2. Allez dans **Files** > **bronze**
3. Créez les sous-dossiers si nécessaire
4. Uploadez les fichiers CSV depuis `output/structured/` vers les dossiers correspondants

### Option 2 : Via OneLake File Explorer (recommandé pour les gros datasets)

1. Installez **OneLake File Explorer** si ce n'est pas déjà fait
2. Montez votre Lakehouse comme lecteur réseau
3. Copiez-collez tous les dossiers de `output/structured/` vers `[OneLake Drive]/YourLakehouse/Files/bronze/`

### Option 3 : Via script PowerShell (si OneLake est monté)

```powershell
# Exemple si OneLake est monté en tant que lecteur O:
$source = ".\output\structured\*"
$destination = "O:\YourWorkspace\YourLakehouse\Files\bronze\"

Copy-Item -Path $source -Destination $destination -Recurse -Force
```

### Option 4 : Via Azure Data Factory / Pipeline Fabric

Créez un pipeline pour copier les fichiers depuis Azure Blob Storage ou autre source vers le Lakehouse.

## Vérification

Après l'upload, vérifiez dans Fabric que vous avez :
- ✅ 8 fichiers dans `bronze/dimensions/`
- ✅ 2 fichiers dans `bronze/supply_chain/`
- ✅ 2 fichiers dans `bronze/manufacturing/`
- ✅ etc.

Une fois les fichiers uploadés, relancez le notebook **01_ingest_to_bronze** !

## Notes importantes

⚠️ **Noms de dossiers** : Utilisez les noms avec underscores (`supply_chain`, `call_center`, etc.)  
⚠️ **Taille** : Le fichier `FactInventory.csv` fait ~912K lignes et peut être volumineux  
⚠️ **Encodage** : Les fichiers sont en UTF-8
