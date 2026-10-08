import pandas as pd
from pathlib import Path


# =========================================================
# MARKET CONTEXT ANALYSIS
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
    / "market_context_analysis.csv"
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
    "population",
    "gdp_per_capita",
    "remittances_pct_gdp",
]

for column in required_columns:
    assert df[column].notna().all(), (
        f"Missing values found in {column}"
    )


# =========================================================
# Four-market averages
# =========================================================

population_avg = df["population"].mean()
gdp_avg = df["gdp_per_capita"].mean()
remittance_avg = df["remittances_pct_gdp"].mean()


# =========================================================
# Difference from four-market average
# =========================================================

df["population_vs_average"] = (
    df["population"] - population_avg
)

df["gdp_per_capita_vs_average"] = (
    df["gdp_per_capita"] - gdp_avg
)

df["remittances_vs_average"] = (
    df["remittances_pct_gdp"] - remittance_avg
)


# =========================================================
# Relative market positions
# =========================================================

df["population_rank"] = (
    df["population"]
    .rank(method="min", ascending=False)
    .astype(int)
)

df["gdp_per_capita_rank"] = (
    df["gdp_per_capita"]
    .rank(method="min", ascending=False)
    .astype(int)
)

df["remittances_rank"] = (
    df["remittances_pct_gdp"]
    .rank(method="min", ascending=False)
    .astype(int)
)


# =========================================================
# Output
# =========================================================

analysis = df[
    [
        "country_code",
        "country",

        "population",
        "population_year",
        "population_rank",
        "population_vs_average",

        "gdp_per_capita",
        "gdp_per_capita_year",
        "gdp_per_capita_rank",
        "gdp_per_capita_vs_average",

        "remittances_pct_gdp",
        "remittances_pct_gdp_year",
        "remittances_rank",
        "remittances_vs_average",
    ]
].copy()


# =========================================================
# Quality checks
# =========================================================

assert len(analysis) == 4
assert analysis["country_code"].is_unique

assert (analysis["population"] > 0).all()
assert (analysis["gdp_per_capita"] > 0).all()
assert (analysis["remittances_pct_gdp"] >= 0).all()


# =========================================================
# Display
# =========================================================

print("\n" + "=" * 80)
print("MARKET CONTEXT ANALYSIS")
print("=" * 80)

print("\nFour-market averages:")

print(
    f"Population:              {population_avg:,.0f}"
)

print(
    f"GDP per capita:          "
)

print(
    f"Remittances (% GDP):     {remittance_avg:.2f}%"
)

print("\nMarket comparison:")

print(
    analysis[
        [
            "country",
            "population",
            "gdp_per_capita",
            "remittances_pct_gdp",
        ]
    ]
    .sort_values(
        "population",
        ascending=False
    )
    .to_string(index=False)
)

print("\nMarket rankings:")

print(
    analysis[
        [
            "country",
            "population_rank",
            "gdp_per_capita_rank",
            "remittances_rank",
        ]
    ]
    .sort_values(
        "population_rank"
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
