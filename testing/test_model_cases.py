
import pandas as pd
from explainability import model

# These feature names and categories match the LOANWISE model.
FEATURES = [
    "no_of_dependents",
    "education",
    "self_employed",
    "income_annum",
    "loan_amount",
    "loan_term",
    "cibil_score",
    "residential_assets_value",
    "commercial_assets_value",
    "luxury_assets_value",
    "bank_asset_value"
]

test_cases = [
    {
        "name": "High credit score",
        "values": [1, "Graduate", "No", 8000000, 10000000,
                   10, 800, 5000000, 2000000, 1000000, 3000000]
    },
    {
        "name": "Low credit score",
        "values": [2, "Not Graduate", "Yes", 2000000, 15000000,
                   15, 350, 0, 0, 0, 0]
    },
    {
        "name": "High income and low credit score",
        "values": [0, "Graduate", "No", 15000000, 5000000,
                   5, 400, 8000000, 3000000, 2000000, 5000000]
    },
    {
        "name": "Low income and high credit score",
        "values": [3, "Not Graduate", "Yes", 1500000, 10000000,
                   20, 850, 0, 0, 0, 100000]
    },
    {
        "name": "Zero assets",
        "values": [0, "Graduate", "No", 5000000, 3000000,
                   10, 700, 0, 0, 0, 0]
    },
    {
        "name": "Maximum dependents and CIBIL",
        "values": [10, "Graduate", "Yes", 10000000, 5000000,
                   10, 900, 10000000, 5000000, 3000000, 7000000]
    }
]

print("\n========== LOANWISE MODEL TESTING ==========\n")

passed = 0
failed = 0

for case in test_cases:
    try:
        row = pd.DataFrame([case["values"]], columns=FEATURES)

        prediction = model.predict(row)[0]
        probabilities = model.predict_proba(row)[0]

        assert prediction in model.classes_, "Invalid predicted class"
        assert len(probabilities) == len(model.classes_), "Invalid probability count"
        assert all(0 <= p <= 1 for p in probabilities), "Probability outside range"
        assert abs(sum(probabilities) - 1.0) < 1e-6, "Probabilities do not sum to 1"

        predicted_probability = max(probabilities) * 100

        print(f"TEST: {case['name']}")
        print(f"Prediction: {prediction}")
        print(f"Model probability: {predicted_probability:.2f}%")
        print("RESULT: PASS\n")

        passed += 1

    except Exception as error:
        print(f"TEST: {case['name']}")
        print(f"RESULT: FAIL")
        print(f"ERROR: {error}\n")

        failed += 1

print("========== TEST SUMMARY ==========")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Total:  {passed + failed}")
