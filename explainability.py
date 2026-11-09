import os
import joblib
import shap
import pandas as pd
import numpy as np

# ==========================================
# 1. LOAD TRAINED MODEL
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "loan_approval_model.pkl"
)

model = joblib.load(MODEL_PATH)

preprocessor = model.named_steps["preprocessor"]
classifier = model.named_steps["classifier"]

explainer = shap.TreeExplainer(classifier)

feature_names = preprocessor.get_feature_names_out()
classes = list(classifier.classes_)


# ==========================================
# 2. FEATURE NAME FORMATTING
# ==========================================

def format_feature_name(name):

    name = name.replace("numeric__", "")
    name = name.replace("categorical__", "")
    name = name.replace("_", " ").strip()

    return name.title()


# ==========================================
# 3. SHAP EXPLANATION ENGINE
# ==========================================

def generate_shap_explanation(input_data):

    input_df = pd.DataFrame([input_data])

    # Preserve training feature order
    expected_columns = list(preprocessor.feature_names_in_)
    input_df = input_df.reindex(columns=expected_columns)

    # Apply trained preprocessing
    transformed_data = preprocessor.transform(input_df)

    if hasattr(transformed_data, "toarray"):
        transformed_data = transformed_data.toarray()

    # Prediction
    prediction = model.predict(input_df)[0]

    probabilities = model.predict_proba(input_df)[0]

    predicted_index = classes.index(prediction)

    confidence = probabilities[predicted_index]

    # Generate SHAP values
    shap_values = explainer.shap_values(transformed_data)

    # Handle different SHAP versions and output shapes
    if isinstance(shap_values, list):

        values = np.asarray(
            shap_values[predicted_index]
        )[0]

    else:

        shap_values = np.asarray(shap_values)

        if shap_values.ndim == 3:

            values = shap_values[0, :, predicted_index]

        elif shap_values.ndim == 2:

            values = shap_values[0]

        else:

            raise ValueError(
                f"Unexpected SHAP output format: {shap_values.shape}"
            )

    if len(values) != len(feature_names):
        raise ValueError(
            "SHAP feature count does not match transformed feature count."
        )

    contributions = []

    for name, value in zip(feature_names, values):

        contributions.append({
            "feature": format_feature_name(name),
            "impact": float(value),
            "direction": (
                "positive" if value > 0 else "negative"
            )
        })

    # Sort by absolute contribution
    contributions.sort(
        key=lambda x: abs(x["impact"]),
        reverse=True
    )

    positive_factors = [
        item for item in contributions
        if item["impact"] > 0
    ][:5]

    negative_factors = [
        item for item in contributions
        if item["impact"] < 0
    ][:5]

    return {
        "prediction": str(prediction),
        "confidence": round(float(confidence) * 100, 2),
        "positive_factors": positive_factors,
        "negative_factors": negative_factors,
        "all_factors": contributions
    }


# ==========================================
# 4. RULE-BASED EXPLANATION ENGINE
# ==========================================

def generate_rule_explanation(data):

    positive_reasons = []
    negative_reasons = []

    cibil = float(data["cibil_score"])
    income = float(data["income_annum"])
    loan = float(data["loan_amount"])

    bank_assets = float(data["bank_asset_value"])

    total_assets = sum([
        float(data["residential_assets_value"]),
        float(data["commercial_assets_value"]),
        float(data["luxury_assets_value"]),
        bank_assets
    ])

    dependents = int(data["no_of_dependents"])

    # CIBIL SCORE
    if cibil >= 750:

        positive_reasons.append(
            "Strong CIBIL score indicates a favourable credit history."
        )

    elif cibil < 650:

        negative_reasons.append(
            "Low CIBIL score may indicate higher credit risk."
        )

    else:

        positive_reasons.append(
            "CIBIL score is within a moderate credit range."
        )

    # INCOME AND LOAN RELATIONSHIP
    if loan > 0:

        loan_income_ratio = loan / max(income, 1)

        if loan_income_ratio <= 2:

            positive_reasons.append(
                "Requested loan amount is relatively low compared "
                "to annual income."
            )

        elif loan_income_ratio > 5:

            negative_reasons.append(
                "Requested loan amount is high compared to annual income."
            )

        else:

            positive_reasons.append(
                "Loan-to-income ratio is within the middle range "
                "of this illustrative assessment."
            )

    # ASSET POSITION
    if loan > 0:

        asset_ratio = total_assets / loan

        if asset_ratio >= 2:

            positive_reasons.append(
                "Declared assets are substantial relative "
                "to the requested loan."
            )

        elif asset_ratio < 0.5:

            negative_reasons.append(
                "Declared assets are relatively low compared "
                "to the requested loan."
            )

    # BANK ASSETS
    if bank_assets > 0:

        positive_reasons.append(
            "Applicant has recorded bank assets."
        )

    else:

        negative_reasons.append(
            "No bank assets are recorded in the application."
        )

    # DEPENDENTS
    if dependents >= 4:

        negative_reasons.append(
            "A higher number of dependents may increase "
            "household financial commitments."
        )

    return {
        "positive_reasons": positive_reasons,
        "negative_reasons": negative_reasons
    }


# ==========================================
# 5. COMBINED EXPLANATION FUNCTION
# ==========================================

def explain_application(input_data):

    shap_result = generate_shap_explanation(input_data)

    rule_result = generate_rule_explanation(input_data)

    return {
        "prediction": shap_result["prediction"],
        "confidence": shap_result["confidence"],

        "shap": {
            "positive_factors": shap_result["positive_factors"],
            "negative_factors": shap_result["negative_factors"],
            "all_factors": shap_result["all_factors"]
        },

        "rules": rule_result
    }


# ==========================================
# 6. TESTING
# ==========================================

if __name__ == "__main__":

    sample_applicant = {
        "no_of_dependents": 2,
        "education": "Graduate",
        "self_employed": "No",
        "income_annum": 1200000,
        "loan_amount": 2000000,
        "loan_term": 10,
        "cibil_score": 820,
        "residential_assets_value": 4000000,
        "commercial_assets_value": 1000000,
        "luxury_assets_value": 500000,
        "bank_asset_value": 800000
    }

    result = explain_application(sample_applicant)

    print("\n========== LOAN ASSESSMENT ==========")

    print("Prediction:", result["prediction"])
    print("Model-predicted probability:", result["confidence"], "%")

    print("\n========== SHAP EXPLANATION ==========")

    print("\nFactors supporting the predicted class:")

    for item in result["shap"]["positive_factors"]:

        print(
            item["feature"],
            "Impact:",
            round(item["impact"], 5)
        )

    print("\nFactors opposing the predicted class:")

    for item in result["shap"]["negative_factors"]:

        print(
            item["feature"],
            "Impact:",
            round(item["impact"], 5)
        )

    print("\n========== RULE-BASED EXPLANATION ==========")

    print("\nPositive observations:")

    for reason in result["rules"]["positive_reasons"]:
        print("+", reason)

    print("\nNegative observations:")

    for reason in result["rules"]["negative_reasons"]:
        print("-", reason)