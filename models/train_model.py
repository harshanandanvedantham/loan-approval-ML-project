
import os
import json
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)

# ==========================================
# 1. LOAD DATASET
# ==========================================

DATA_PATH = "dataset\cleaned_loan_dataset.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 55)
print("       LOAN APPROVAL ML MODEL TRAINING")
print("=" * 55)

print("\nDataset shape:", df.shape)

# ==========================================
# 2. PREPARE DATA
# ==========================================

df.columns = df.columns.str.strip().str.lower()

# Normalize target labels
df["loan_status"] = (
    df["loan_status"].astype(str).str.strip().str.lower()
)

# Remove identifier column
df.drop(columns=["loan_id"], errors="ignore", inplace=True)

# Separate input features and target
X = df.drop(columns=["loan_status"])
y = df["loan_status"]

if y.isnull().any():
    raise ValueError("Target column contains missing values.")

if y.nunique() != 2:
    raise ValueError(
        f"Expected 2 loan_status classes, found: {y.unique()}"
    )

print("\nTarget distribution:")
print(y.value_counts())

# ==========================================
# 3. IDENTIFY COLUMN TYPES
# ==========================================

numerical_cols = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_cols = X.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()

print("\nNumerical features:", numerical_cols)
print("\nCategorical features:", categorical_cols)

# ==========================================
# 4. TRAIN-TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# ==========================================
# 5. PREPROCESSING PIPELINE
# ==========================================

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numerical_cols),
    ("categorical", categorical_pipeline, categorical_cols)
])

# ==========================================
# 6. DEFINE ML ALGORITHMS
# ==========================================

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=2000,
        random_state=42
    ),

    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )
}

# ==========================================
# 7. CROSS-VALIDATION MODEL COMPARISON
# ==========================================

results = {}

print("\n" + "=" * 55)
print("          MODEL CROSS-VALIDATION")
print("=" * 55)

for name, algorithm in models.items():

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", algorithm)
    ])

    scores = cross_val_score(
        pipeline,
        X_train,
        y_train,
        cv=5,
        scoring="f1_macro",
        n_jobs=-1
    )

    results[name] = {
        "pipeline": pipeline,
        "cv_score": scores.mean()
    }

    print(f"\n{name}")
    print("CV F1 scores:", scores.round(4))
    print("Mean CV F1:", round(scores.mean(), 4))

# ==========================================
# 8. SELECT BEST MODEL
# ==========================================

best_name = max(
    results,
    key=lambda name: results[name]["cv_score"]
)

best_model = results[best_name]["pipeline"]

print("\n" + "=" * 55)
print("BEST MODEL:", best_name)
print("=" * 55)

# ==========================================
# 9. TRAIN BEST MODEL
# ==========================================

best_model.fit(X_train, y_train)

# ==========================================
# 10. TEST MODEL PERFORMANCE
# ==========================================

y_pred = best_model.predict(X_test)

print("\nFINAL TEST RESULTS")
print("=" * 55)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(
    y_test, y_pred, pos_label="approved", zero_division=0
)
recall = recall_score(
    y_test, y_pred, pos_label="approved", zero_division=0
)
f1 = f1_score(
    y_test, y_pred, pos_label="approved", zero_division=0
)

print("Accuracy:", round(accuracy * 100, 2), "%")
print("Precision (Approved):", round(precision, 4))
print("Recall (Approved):", round(recall, 4))
print("F1 Score (Approved):", round(f1, 4))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix(
    y_test,
    y_pred,
    labels=best_model.classes_
))

# ==========================================
# 11. ROC-AUC SCORE
# ==========================================

approved_index = list(best_model.classes_).index("approved")

y_probability = best_model.predict_proba(X_test)[:, approved_index]

roc_auc = roc_auc_score(
    (y_test == "approved").astype(int),
    y_probability
)

print("\nROC-AUC Score:", round(roc_auc, 4))

# ==========================================
# 12. SAVE TRAINED MODEL
# ==========================================

os.makedirs("models", exist_ok=True)

joblib.dump(
    best_model,
    "models/loan_approval_model.pkl"
)

# Save model information
model_info = {
    "model_name": best_name,
    "accuracy": round(accuracy, 4),
    "precision_approved": round(precision, 4),
    "recall_approved": round(recall, 4),
    "f1_approved": round(f1, 4),
    "roc_auc": round(roc_auc, 4),
    "training_samples": len(X_train),
    "testing_samples": len(X_test),
    "features": X.columns.tolist(),
    "classes": best_model.classes_.tolist()
}

with open("models/model_info.json", "w") as file:
    json.dump(model_info, file, indent=4)

print("\n" + "=" * 55)
print("       MODEL TRAINING COMPLETED!")
print("=" * 55)

print("Selected model:", best_name)
print("Saved: models/loan_approval_model.pkl")
print("Saved: models/model_info.json")
