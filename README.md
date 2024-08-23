# Félix Risk Case Study

This repository contains the analysis and visualization of transaction data for a risk case study. The goal is to identify patterns and KPIs (Key Performance Indicators) that can help detect fraudulent transactions and other risk factors.
The repository is not in a modular form due to it's analytical proposal only.

## Files in the Repository

- `félix.py`: The main Python script that performs the analysis on the dataset. It includes steps to calculate KPIs, perform statistical tests, and visualize the results.
- `risk_case_study_data_2024-03-13T16_57_16.669322Z.csv`: The dataset used for this analysis. It contains transaction details, dispute information, and other relevant data.

## Analysis Process

### 1. Data Loading
The dataset is loaded into a pandas DataFrame for processing.

### 2. Key Performance Indicators (KPIs)
The script calculates several KPIs, such as:
- **Dispute Rate:** The percentage of transactions that are disputed.
- **Fraudulent Dispute Rate:** The percentage of disputed transactions that are identified as fraudulent.

### 3. Time Difference Analysis
The time difference between the account signup and the transaction creation is calculated to find patterns. This analysis helps in understanding if transactions made shortly after signup are more likely to be disputed.

### 4. Country Comparison
Transactions where the IP country differs from the billing address country are analyzed to see if they are more likely to be disputed.

### 5. VPN Usage Analysis
The impact of VPN usage on the likelihood of a transaction being disputed is analyzed. A Z-test is conducted to compare the rates of VPN usage between disputed and non-disputed transactions.

### Z-Tests for Proportions
Z-tests are performed to determine if there is a statistically significant difference in the proportions of disputed and non-disputed transactions based on each risky parameter.

## How to Run the Script

1. Clone this repository to your local machine.
2. Ensure you have the required Python libraries installed (`pandas`, `matplotlib`, `statsmodels`).
3. Run the `félix.py` script to perform the analysis.

## Results
The results of the analysis, including visualizations and statistical tests, will be displayed in the console or as plots.

## Contact
For any questions or clarifications, please reach out to Julio Kravszenko, email juliockf@gmail.com.
