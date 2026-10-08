import pandas as pd
from pathlib import Path


# =========================================================
# FINANCIAL & DIGITAL ACCESS ANALYSIS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "market_analysis_base.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "financial_digital_access_analysis.csv"
)


# =========================================================
# Load analytical base
# =========================================================

df = pd.read_csv(INPUT_FILE)


# =========================================================
# Validate input
# =========================================================

assert len(df) == 4
assert df["country_code"].is_unique

required_columns = [
    "account_ownership",
    "digital_payment_usage",
    "smartphone_adoption",
    "internet_penetration",
]

for column in required_columns:
    assert df[column].notna().all(), (
        f"Missing values found in {column}"
    )


# =========================================================
# Convert Findex proportions to percentages
# =========================================================

df["account_ownership_pct"] = (
    df["account_ownership"] * 100
)

df["digital_payment_usage_pct"] = (
    df["digital_payment_usage"] * 100
)

df["smartphone_adoption_pct"] = (
    df["smartphone_adoption"] * 100
)

# World Bank internet penetration is already a percentage.
df["internet_penetration_pct"] = (
    df["internet_penetration"]
)


# =========================================================
# Four-market averages
# =========================================================

account_avg = df["account_ownership_pct"].mean()
payment_avg = df["digital_payment_usage_pct"].mean()
smartphone_avg = df["smartphone_adoption_pct"].mean()
internet_avg = df["internet_penetration_pct"].mean()


# =========================================================
# Difference from four-market average
# =========================================================

df["account_ownership_gap"] = (
    df["account_ownership_pct"] - account_avg
)

df["digital_payment_gap"] = (
    df["digital_payment_usage_pct"] - payment_avg
)

df["smartphone_adoption_gap"] = (
    df["smartphone_adoption_pct"] - smartphone_avg
)

df["internet_penetration_gap"] = (
    df["internet_penetration_pct"] - internet_avg
)


# =========================================================
# Market rankings
# =========================================================

df["account_ownership_rank"] = (
    df["account_ownership_pct"]
    .rank(method="min", ascending=False)
    .astype(int)
)

df["digital_payment_rank"] = (
    df["digital_payment_usage_pct"]
    .rank(method="min", ascending=False)
    .astype(int)
)

df["smartphone_adoption_rank"] = (
    df["smartphone_adoption_pct"]
    .rank(method="min", ascending=False)
    .astype(int)
)

df["internet_penetration_rank"] = (
    df["internet_penetration_pct"]
    .rank(method="min", ascending=False)
    .astype(int)
)


# =========================================================
# Analytical output
# =========================================================

analysis = df[
    [
        "country_code",
        "country",

        "account_ownership_pct",
        "digital_payment_usage_pct",
        "smartphone_adoption_pct",
        "internet_penetration_pct",

        "findex_year",
        "internet_penetration_year",

        "account_ownership_gap",
        "digital_payment_gap",
        "smartphone_adoption_gap",
        "internet_penetration_gap",

        "account_ownership_rank",
        "digital_payment_rank",
        "smartphone_adoption_rank",
        "internet_penetration_rank",
    ]
].copy()


# =========================================================
# Quality checks
# =========================================================

assert len(analysis) == 4
assert analysis["country_code"].is_unique

percentage_columns = [
    "account_ownership_pct",
    "digital_payment_usage_pct",
    "smartphone_adoption_pct",
    "internet_penetration_pct",
]

for column in percentage_columns:
    assert (
        (analysis[column] >= 0)
        & (analysis[column] <= 100)
    ).all(), f"Invalid percentage in {column}"


# =========================================================
# Display
# =========================================================

print("\n" + "=" * 80)
print("FINANCIAL & DIGITAL ACCESS ANALYSIS")
print("=" * 80)

print("\nFour-market averages:")

print(
    f"Account ownership:       {account_avg:.2f}%"
)

print(
    f"Digital payment usage:   {payment_avg:.2f}%"
)

print(
    f"Smartphone adoption:     {smartphone_avg:.2f}%"
)

print(
    f"Internet penetration:    {internet_avg:.2f}%"
)

print("\nMarket comparison:")

print(
    analysis[
        [
            "country",
            "account_ownership_pct",
            "digital_payment_usage_pct",
            "smartphone_adoption_pct",
            "internet_penetration_pct",
        ]
    ]
    .sort_values(
        "account_ownership_pct",
        ascending=False
    )
    .to_string(index=False)
)

print("\nMarket rankings:")

print(
    analysis[
        [
            "country",
            "account_ownership_rank",
            "digital_payment_rank",
            "smartphone_adoption_rank",
            "internet_penetration_rank",
        ]
    ]
    .sort_values(
        "account_ownership_rank"
    )
    .to_string(index=False)
)


# =========================================================
# Save
# =========================================================

analysis.to_csv(
    OUTPUT_FILE,
    index=False
)

print(f"\nSaved: {OUTPUT_FILE}")
