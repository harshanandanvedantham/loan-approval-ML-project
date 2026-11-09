
import joblib
import pandas as pd

# Load trained model
model = joblib.load("models/loan_approval_model.pkl")

# Test applicant profiles
test_cases = [

    {
        "name": "Test 01 - Excellent Applicant",
        "no_of_dependents": 1,
        "education": "graduate",
        "self_employed": "no",
        "income_annum": 2500000,
        "loan_amount": 1500000,
        "loan_term": 10,
        "cibil_score": 850,
        "residential_assets_value": 5000000,
        "commercial_assets_value": 3000000,
        "luxury_assets_value": 2000000,
        "bank_asset_value": 2500000
    },

    {
        "name": "Test 02 - Poor Credit Score",
        "no_of_dependents": 2,
        "education": "graduate",
        "self_employed": "no",
        "income_annum": 1200000,
        "loan_amount": 1000000,
        "loan_term": 10,
        "cibil_score": 450,
        "residential_assets_value": 2000000,
        "commercial_assets_value": 500000,
        "luxury_assets_value": 300000,
        "bank_asset_value": 400000
    },

    {
        "name": "Test 03 - High Income, High Loan",
        "no_of_dependents": 2,
        "education": "graduate",
        "self_employed": "yes",
        "income_annum": 5000000,
        "loan_amount": 4000000,
        "loan_term": 15,
        "cibil_score": 780,
        "residential_assets_value": 6000000,
        "commercial_assets_value": 2000000,
        "luxury_assets_value": 1500000,
        "bank_asset_value": 2000000
    },

    {
        "name": "Test 04 - Low Income Applicant",
        "no_of_dependents": 3,
        "education": "not graduate",
        "self_employed": "no",
        "income_annum": 300000,
        "loan_amount": 2500000,
        "loan_term": 20,
        "cibil_score": 650,
        "residential_assets_value": 500000,
        "commercial_assets_value": 0,
        "luxury_assets_value": 0,
        "bank_asset_value": 100000
    },

    {
        "name": "Test 05 - High Assets, Average Income",
        "no_of_dependents": 2,
        "education": "graduate",
        "self_employed": "yes",
        "income_annum": 1000000,
        "loan_amount": 800000,
        "loan_term": 10,
        "cibil_score": 720,
        "residential_assets_value": 8000000,
        "commercial_assets_value": 4000000,
        "luxury_assets_value": 3000000,
        "bank_asset_value": 1500000
    },

    {
        "name": "Test 06 - No Declared Assets",
        "no_of_dependents": 1,
        "education": "graduate",
        "self_employed": "no",
        "income_annum": 1500000,
        "loan_amount": 1000000,
        "loan_term": 10,
        "cibil_score": 750,
        "residential_assets_value": 0,
        "commercial_assets_value": 0,
        "luxury_assets_value": 0,
        "bank_asset_value": 0
    },

    {
        "name": "Test 07 - Many Dependents",
        "no_of_dependents": 8,
        "education": "not graduate",
        "self_employed": "yes",
        "income_annum": 1200000,
        "loan_amount": 1500000,
        "loan_term": 15,
        "cibil_score": 700,
        "residential_assets_value": 1000000,
        "commercial_assets_value": 500000,
        "luxury_assets_value": 200000,
        "bank_asset_value": 300000
    },

    {
        "name": "Test 08 - Low Loan, Strong Credit",
        "no_of_dependents": 0,
        "education": "graduate",
        "self_employed": "no",
        "income_annum": 2000000,
        "loan_amount": 300000,
        "loan_term": 5,
        "cibil_score": 820,
        "residential_assets_value": 3000000,
        "commercial_assets_value": 1000000,
        "luxury_assets_value": 1000000,
        "bank_asset_value": 1500000
    },

    {
        "name": "Test 09 - High Loan, Poor Credit",
        "no_of_dependents": 4,
        "education": "not graduate",
        "self_employed": "yes",
        "income_annum": 800000,
        "loan_amount": 5000000,
        "loan_term": 20,
        "cibil_score": 500,
        "residential_assets_value": 1000000,
        "commercial_assets_value": 200000,
        "luxury_assets_value": 100000,
        "bank_asset_value": 50000
    },

    {
        "name": "Test 10 - Self Employed Applicant",
        "no_of_dependents": 2,
        "education": "graduate",
        "self_employed": "yes",
        "income_annum": 1800000,
        "loan_amount": 1200000,
        "loan_term": 10,
        "cibil_score": 760,
        "residential_assets_value": 2500000,
        "commercial_assets_value": 1000000,
        "luxury_assets_value": 500000,
        "bank_asset_value": 800000
    },

    {
        "name": "Test 11 - Borderline Credit Score",
        "no_of_dependents": 2,
        "education": "graduate",
        "self_employed": "no",
        "income_annum": 1000000,
        "loan_amount": 900000,
        "loan_term": 10,
        "cibil_score": 650,
        "residential_assets_value": 1500000,
        "commercial_assets_value": 500000,
        "luxury_assets_value": 300000,
        "bank_asset_value": 400000
    },

    {
        "name": "Test 12 - Very High Loan Amount",
        "no_of_dependents": 1,
        "education": "graduate",
        "self_employed": "no",
        "income_annum": 3000000,
        "loan_amount": 10000000,
        "loan_term": 20,
        "cibil_score": 800,
        "residential_assets_value": 5000000,
        "commercial_assets_value": 2000000,
        "luxury_assets_value": 1000000,
        "bank_asset_value": 2000000
    },

    {
        "name": "Test 13 - Non Graduate Applicant",
        "no_of_dependents": 1,
        "education": "not graduate",
        "self_employed": "no",
        "income_annum": 1500000,
        "loan_amount": 1000000,
        "loan_term": 10,
        "cibil_score": 780,
        "residential_assets_value": 2000000,
        "commercial_assets_value": 1000000,
        "luxury_assets_value": 500000,
        "bank_asset_value": 800000
    },

    {
        "name": "Test 14 - Very Long Loan Term",
        "no_of_dependents": 2,
        "education": "graduate",
        "self_employed": "no",
        "income_annum": 2000000,
        "loan_amount": 1500000,
        "loan_term": 30,
        "cibil_score": 750,
        "residential_assets_value": 3000000,
        "commercial_assets_value": 1000000,
        "luxury_assets_value": 500000,
        "bank_asset_value": 1000000
    },

    {
        "name": "Test 15 - Your Previous Sample",
        "no_of_dependents": 2,
        "education": "graduate",
        "self_employed": "no",
        "income_annum": 1200000,
        "loan_amount": 2000000,
        "loan_term": 10,
        "cibil_score": 820,
        "residential_assets_value": 4000000,
        "commercial_assets_value": 1000000,
        "luxury_assets_value": 500000,
        "bank_asset_value": 800000
    }
]


# Run tests
print("\n========== LOAN MODEL TESTING ==========\n")

results = []

for case in test_cases:

    name = case["name"]

    # Remove test name before prediction
    applicant = {
        key: value
        for key, value in case.items()
        if key != "name"
    }

    # Convert applicant into DataFrame
    input_df = pd.DataFrame([applicant])

    # Predict
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    # Match probability to predicted class
    class_index = list(model.classes_).index(prediction)
    probability = probabilities[class_index] * 100

    print("-" * 55)
    print(name)
    print("Prediction:", str(prediction).upper())
    print(f"Model Probability: {probability:.2f}%")

    results.append({
        "Test Case": name,
        "Prediction": prediction,
        "Model Probability": round(probability, 2)
    })


# Summary
results_df = pd.DataFrame(results)

print("\n========== TEST SUMMARY ==========\n")
print(results_df.to_string(index=False))

print("\nTotal Test Cases:", len(results))
print("Testing completed successfully!")


from sklearn.model_selection import train_test_split

print("\n========== MODEL CONFIDENCE DIAGNOSTICS ==========\n")

# Get the fitted components
preprocessor = model.named_steps["preprocessor"]
classifier = model.named_steps["classifier"]

print("Tree depth:", classifier.get_depth())
print("Number of leaves:", classifier.get_n_leaves())

print("\n--- Individual applicant leaf analysis ---")

for case in test_cases:

    applicant = {
        key: value
        for key, value in case.items()
        if key != "name"
    }

    input_df = pd.DataFrame([applicant])
    transformed = preprocessor.transform(input_df)

    leaf_id = classifier.apply(transformed)[0]
    probabilities = model.predict_proba(input_df)[0]

    leaf_samples = classifier.tree_.n_node_samples[leaf_id]

    print("\n", case["name"])
    print("Leaf ID:", leaf_id)
    print("Training samples in leaf:", leaf_samples)
    print("Class probabilities:")

    for label, probability in zip(model.classes_, probabilities):
        print(f"  {label}: {probability * 100:.2f}%")


# Recheck the original held-out test dataset
print("\n--- Original held-out test set ---")

df = pd.read_csv("dataset/cleaned_loan_dataset.csv")

df.columns = df.columns.str.strip().str.lower()

for column in df.select_dtypes(include="object").columns:
    df[column] = df[column].str.strip().str.lower()

X = df.drop(columns=["loan_status", "loan_id"])
y = df["loan_status"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

test_probabilities = model.predict_proba(X_test)

max_probabilities = test_probabilities.max(axis=1)

print("Total held-out samples:", len(X_test))
print(
    "Samples with exactly 100% probability:",
    (max_probabilities >= 0.999999).sum()
)
print(
    "Average maximum probability:",
    round(max_probabilities.mean() * 100, 2), "%"
)
print(
    "Minimum maximum probability:",
    round(max_probabilities.min() * 100, 2), "%"
)
