# Gallstone Risk Prediction for Private Clinic Checkups

## Project Overview
This project focuses on building a **non-imaging gallstone risk prediction model** using routine clinical checkup variables. The primary objective is to provide an early triage tool for private clinics, where gallbladder imaging (e.g., ultrasound) is often not immediately available at the first visit.

The model outputs a risk probability to prioritize patients for screening, serving as a support tool rather than a diagnostic replacement.

## Dataset & Clinical Scope
The dataset includes clinical data for 319 individuals, with a balanced distribution of the target variable (`Gallstone Status`). Features are categorized into three groups:
1.  **Demographics**: Age, sex, height, weight, BMI.
2.  **Body Composition**: TBW, ECW, ICW, VFA, HFA, etc.
3.  **Laboratory Markers**: Glucose, Lipids (TC, LDL, HDL, TG), Creatinine, Hemoglobin, Vitamin D.

### Leakage Control
To ensure real-world applicability, "leakage" variables (features typically measured *after* diagnosis or directly related to symptomatic presentation like CRP, AST, ALT, ALP) were strictly excluded from the predictive pool. Only routine checkup variables are used.

## Methodology
The analysis follows a rigorous clinical data science pipeline:

1.  **Data Quality & Integrity**: Verification of target availability, missing values, and duplicates.
2.  **Clinical Feature Engineering**: Creation of metabolically informative ratios (e.g., LDL/HDL, TG/HDL, Age × BMI interaction).
3.  **Collinearity Diagnostics**: Analysis of multicollinearity among body composition variables using Variance Inflation Factor (VIF).
4.  **Feature Selection**: Recursive Feature Elimination (RFECV) and Mutual Information to select the most predictive subset.
5.  **Model Benchmarking**: Comparison of several architectures:
    *   Logistic Regression (Linear baseline)
    *   Random Forest
    *   XGBoost
    *   LightGBM (HistGradientBoosting)
6.  **Calibration & Diagnostics**: Probability calibration (Brier Score), subgroup analysis, and uncertainty estimation via bootstrapping.
7.  **Interpretation**: Global and local feature importance via SHAP (SHapley Additive exPlanations) to provide clinical transparency.

## Key Findings
- **Predictive Power**: The model achieves significant separation using non-imaging markers alone.
- **Top Predictors**: SHAP analysis highlights metabolic markers and age-related interactions as key drivers of gallstone risk.
- **Calibration**: The model is well-calibrated, ensuring predicted probabilities align with actual observed frequencies.

## Technologies Used
- **Language**: Python 3.x
- **Libraries**:
    - Machine Learning: `scikit-learn`, `xgboost`, `lightgbm`
    - Interpretation: `shap`
    - Analysis: `pandas`, `numpy`, `scipy`
    - Visualization: `matplotlib`, `seaborn`

## Usage
To reproduce the results, ensure you have the `gallstone.csv` dataset in the project root and run the `gallstone_project_new.ipynb` notebook.
