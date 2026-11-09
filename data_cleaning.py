
import pandas as pd

df = pd.read_csv("cleaned_loan_dataset.csv")

print(df.shape)
print(df.isnull().sum())
print(df["loan_status"].value_counts())
print(df.dtypes)

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("dataset\loan_approval_dataset.csv")

print("INITIAL DATASET SHAPE:", df.shape)

# ==========================================
# 2. BASIC DATA CLEANING
# ==========================================

df.columns = df.columns.str.strip().str.lower()

for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip().str.lower()

df.drop_duplicates(inplace=True)

# ==========================================
# 3. HANDLE NEGATIVE ASSET VALUES
# ==========================================

asset_cols = [
    "residential_assets_value",
    "commercial_assets_value",
    "luxury_assets_value",
    "bank_asset_value"
]

for col in asset_cols:
    df[col] = df[col].clip(lower=0)

# ==========================================
# 4. OUTLIER DETECTION USING IQR
# ==========================================

outlier_cols = [
    "residential_assets_value",
    "commercial_assets_value",
    "bank_asset_value"
]

outlier_indices = set()

print("\nOUTLIER ANALYSIS")
print("=" * 45)

for col in outlier_cols:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = df[
        (df[col] < lower_limit) |
        (df[col] > upper_limit)
    ]

    print(f"\nColumn: {col}")
    print("Q1:", Q1)
    print("Q3:", Q3)
    print("IQR:", IQR)
    print("Lower limit:", lower_limit)
    print("Upper limit:", upper_limit)
    print("Outliers detected:", len(outliers))

    outlier_indices.update(outliers.index)

# ==========================================
# 5. REMOVE OUTLIER ROWS
# ==========================================

print("\n" + "=" * 45)

print("Total unique outlier rows:", len(outlier_indices))

original_rows = len(df)

df_cleaned = df.drop(index=list(outlier_indices))

removed_rows = original_rows - len(df_cleaned)

# ==========================================
# 6. FINAL DATASET ANALYSIS
# ==========================================

print("\nFINAL DATASET ANALYSIS")
print("=" * 45)

print("Original rows:", original_rows)
print("Removed outlier rows:", removed_rows)
print("Remaining rows:", len(df_cleaned))

print("Data retention:",
      round((len(df_cleaned) / original_rows) * 100, 2), "%")

# ==========================================
# 7. VERIFY REMAINING OUTLIERS
# ==========================================

print("\nREMAINING OUTLIER CHECK")

for col in outlier_cols:

    Q1 = df_cleaned[col].quantile(0.25)
    Q3 = df_cleaned[col].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    remaining = df_cleaned[
        (df_cleaned[col] < lower) |
        (df_cleaned[col] > upper)
    ]

    print(f"{col}: {len(remaining)}")

# ==========================================
# 8. EXPORT FINAL CLEANED DATASET
# ==========================================

df_cleaned.to_csv(
    "cleaned_loan_dataset.csv",
    index=False
)

print("\n" + "=" * 45)
print("DATA CLEANING COMPLETED SUCCESSFULLY!")
print("Final file: cleaned_loan_dataset.csv")
print("Final shape:", df_cleaned.shape)
print("=" * 45)
