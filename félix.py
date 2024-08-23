# -*- coding: utf-8 -*-
"""
This notebook where made in Google Colab.
You can find the original verion in:
https://colab.research.google.com/drive/1RfsVHZLf85nNse9gT8ZZyhgCwhRFovwg?usp=sharing
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta
from statsmodels.stats.proportion import proportions_ztest
import numpy as np
from decimal import Decimal

df = pd.read_csv('/files/risk_case_study_data_2024-03-13T16_57_16.669322Z.csv')

# @title Main KPIs

# Filter transactions with is_dispute = True
disputes_df = df[df['is_dispute'] == True]

# Group by dispute reason and count the number of occurrences
dispute_counts = disputes_df['dispute_reason'].value_counts()

# Create the bar chart
plt.figure(figsize=(12, 8))
dispute_counts.plot(kind='bar', color='skyblue')

# Add title and labels with increased font size
plt.title('Number of Occurrences by Dispute Reason', fontsize=19)
plt.xlabel('Dispute Reason', fontsize=16)
plt.ylabel('Number of Occurrences', fontsize=16)
plt.xticks(rotation=45, fontsize=16)
plt.yticks(fontsize=16)

# Show the chart
plt.tight_layout()
plt.show()

# Dispute rate
total_transactions = len(df)  # total number of transactions
total_disputes = len(df[df['is_dispute'] == True])  # total number of disputes
dispute_rate = (total_disputes / total_transactions) * 100
print(f"{dispute_rate:.2f}")

# Fraudulent rate for disputed transactions
total_fraudulent_disputes = len(df[(df['is_dispute'] == True) & (df['dispute_reason'] == 'fraudulent')])
fraud_dispute_rate = (total_fraudulent_disputes / total_disputes) * 100
print(f"{fraud_dispute_rate:.2f}")

# @title Top 3 patterns

# Convert date columns to datetime
df['signup_created_at'] = pd.to_datetime(df['signup_created_at'])
df['created_at'] = pd.to_datetime(df['created_at'])

# Calculate the time difference between signup_created_at and created_at
df['time_diff'] = (df['created_at'] - df['signup_created_at']).dt.total_seconds() / 3600  # difference in hours

# Separate transactions with is_dispute = True and is_dispute = False
disputed = df[df['is_dispute'] == True]
non_disputed = df[df['is_dispute'] == False]

# Analyze descriptive statistics for the time difference
disputed_stats = disputed['time_diff'].describe().round(2)
non_disputed_stats = non_disputed['time_diff'].describe().round(2)

# Display the results
print("Time Difference Statistics for Disputed Transactions:")
print(disputed_stats)
print("\nTime Difference Statistics for Non-Disputed Transactions:")
print(non_disputed_stats)

# Separate transactions with is_dispute = True and is_dispute = False
quartile_25 = disputed['time_diff'].quantile(0.25)
quartile_50 = disputed['time_diff'].quantile(0.50)

time_disputed_25 = len(disputed[disputed['time_diff'] <= quartile_25])
time_disputed_50 = len(disputed[disputed['time_diff'] <= quartile_50])
time_non_disputed_25 = len(non_disputed[non_disputed['time_diff'] <= quartile_25])
time_non_disputed_50 = len(non_disputed[non_disputed['time_diff'] <= quartile_50])

percent_time_dispute_true_25 = (time_disputed_25 / len(disputed['is_dispute'])) * 100
percent_time_dispute_true_50 = (time_disputed_50 / len(disputed['is_dispute'])) * 100
percent_time_non_dispute_true_25 = (time_non_disputed_25 / len(non_disputed['is_dispute'])) * 100
percent_time_non_dispute_true_50 = (time_non_disputed_50 / len(non_disputed['is_dispute'])) * 100

print(f"Percentage of transactions with time_diff <= 25% quartile in dispute_true: {percent_time_dispute_true_25:.2f}%")
print(f"Percentage of transactions with time_diff <= 50% quartile in dispute_true: {percent_time_dispute_true_50:.2f}%")
print(f"Percentage of transactions with time_diff <= 25% quartile in non_dispute_true: {percent_time_non_dispute_true_25:.2f}%")
print(f"Percentage of transactions with time_diff <= 50% quartile in non_dispute_true: {percent_time_non_dispute_true_50:.2f}%")

# Check the affected users
r = len(df[df['time_diff']<=quartile_50])/len(df)
print(r)

# Proportions
prop_disputed_25 = time_disputed_25 / len(disputed)
prop_non_disputed_25 = time_non_disputed_25 / len(non_disputed)

prop_disputed_50 = time_disputed_50 / len(disputed)
prop_non_disputed_50 = time_non_disputed_50 / len(non_disputed)

# Sample sizes
n_disputed = len(disputed)
n_non_disputed = len(non_disputed)

# Z-test for proportions
# Number of events (transactions with time_diff <= quartile)
successes_25 = [time_disputed_25, time_non_disputed_25]
successes_50 = [time_disputed_50, time_non_disputed_50]

# Sample sizes
nobs_25 = [n_disputed, n_non_disputed]
nobs_50 = [n_disputed, n_non_disputed]

# Z-test for proportions
z_stat_25, p_value_25 = proportions_ztest(successes_25, nobs_25)
z_stat_50, p_value_50 = proportions_ztest(successes_50, nobs_50)

print(f"Z-test for proportion <= 25% quartile: z-statistic = {z_stat_25:.2f}, p-value = {p_value_25:.4f}")
print(f"Z-test for proportion <= 50% quartile: z-statistic = {z_stat_50:.2f}, p-value = {p_value_50:.50f}")

disputed_25 = disputed[disputed['time_diff'] <= quartile_25]['amount'].sum()
disputed_50 = disputed[disputed['time_diff'] <= quartile_50]['amount'].sum()

non_disputed_25 = non_disputed[non_disputed['time_diff'] <= quartile_25]['amount'].sum()
non_disputed_50 = non_disputed[non_disputed['time_diff'] <= quartile_50]['amount'].sum()

print("Total amount of disputed transactions with time_diff <= 25% quartile:", disputed_25)
print("Total amount of disputed transactions with time_diff <= 50% quartile:", disputed_50)
print("Total amount of non-disputed transactions with time_diff <= 25% quartile:", non_disputed_25 * 0.027)
print("Total amount of non-disputed transactions with time_diff <= 50% quartile:", non_disputed_50 * 0.019)

# Count the total number of transactions for is_dispute = True and False
total_dispute_true = len(df[(df['is_dispute'] == True) & (df['dispute_reason'] == 'fraudulent')])
total_dispute_false = len(df[df['is_dispute'] == False])

# Count the number of transactions where ip_country is different from billing_address_country
diff_country_dispute_true = len(df[(df['ip_country'] != df['billing_address_country']) & (df['is_dispute'] == True)])
diff_country_dispute_false = len(df[(df['ip_country'] != df['billing_address_country']) & (df['is_dispute'] == False)])

# Calculate the percentages
percent_diff_country_dispute_true = (diff_country_dispute_true / total_dispute_true) * 100
percent_diff_country_dispute_false = (diff_country_dispute_false / total_dispute_false) * 100
percent_diff_country_dispute = ((diff_country_dispute_true + diff_country_dispute_false) / len(df['is_dispute'])) * 100

# Display the results
print(f"Percentage of transactions with ip_country different from billing_address_country and is_dispute = True: {percent_diff_country_dispute_true:.2f}%")
print(f"Percentage of transactions with ip_country different from billing_address_country and is_dispute = False: {percent_diff_country_dispute_false:.2f}%")
print(f"Total percentage of transactions with ip_country different from billing_address_country: {percent_diff_country_dispute:.2f}%")

diff_country_dispute_true = df[(df['ip_country'] != df['billing_address_country']) & (df['is_dispute'] == True)]['amount'].sum()
diff_country_dispute_false = df[(df['ip_country'] != df['billing_address_country']) & (df['is_dispute'] == False)]['amount'].sum()

print(f"Total amount of disputed transactions with ip_country different from billing_address_country: {diff_country_dispute_true:.2f}")
print(f"Total amount of non-disputed transactions with ip_country different from billing_address_country: {diff_country_dispute_false:.2f}")

# Number of transactions with ip_country != billing_address_country
success_a = int(diff_country_dispute_true)
success_b = int(diff_country_dispute_false)

# Total number of transactions for each group
nobs_a = int(total_dispute_true)
nobs_b = int(total_dispute_false)

# Apply the proportion z-test
stat, p_value = proportions_ztest([success_a, success_b], [nobs_a, nobs_b])

print(f"Z-statistic: {stat}")
print(f"P-value: {p_value}")

# Count the total number of transactions for is_dispute = True and False
total_dispute_true = len(df[(df['is_dispute'] == True) & (df['dispute_reason'] == 'fraudulent')])
total_dispute_false = len(df[df['is_dispute'] == False])

# Count the number of transactions where vpn is True
vpn_dispute_true = len(df[(df['vpn'] == True) & (df['is_dispute'] == True)])
vpn_dispute_false = len(df[(df['vpn'] == True) & (df['is_dispute'] == False)])

# Calculate the percentages for vpn
percent_vpn_dispute_true = (vpn_dispute_true / total_dispute_true) * 100
percent_vpn_dispute_false = (vpn_dispute_false / total_dispute_false) * 100

# Display the results for vpn
print(f"Percentage of transactions with vpn = True and is_dispute = True: {percent_vpn_dispute_true:.2f}%")
print(f"Percentage of transactions with vpn = True and is_dispute = False: {percent_vpn_dispute_false:.2f}%")


# Number of events (transactions with vpn = True)
successes = [vpn_dispute_true, vpn_dispute_false]

# Sample sizes
nobs = [total_dispute_true, total_dispute_false]

# Z-test for proportions
z_stat, p_value = proportions_ztest(successes, nobs)

print(f"Z-test for proportion with vpn = True: z-statistic = {z_stat:.2f}, p-value = {p_value:.10f}")

disputed_vpn = df[(df['is_dispute'] == True) &  (df['vpn'] == True)]['amount'].sum()
non_disputed_vpn = df[(df['is_dispute'] == False) & (df['vpn'] == True)]['amount'].sum()

# disputed_vpn = df[(df['is_dispute'] == True) & (df['dispute_reason'] == 'fraudulent') & (df['vpn'] == True)]['amount'].sum()
# non_disputed_vpn = df[(df['is_dispute'] == False) & (df['vpn'] == True)]['amount'].sum()

print(f"Total amount of disputed transactions with vpn = true: {disputed_vpn:.2f}")
print(f"Total amount of non-disputed transactions with vpn = false or NaN: {non_disputed_vpn:.2f}")
