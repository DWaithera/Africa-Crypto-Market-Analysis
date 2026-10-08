import pandas as pd
from pathlib import Path


# =========================================================
# Paths
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "market_analysis_base.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "demand_adoption_analysis.csv"


# =========================================================
# Load analytical base
# =========================================================

df = pd.read_csv(INPUT_FILE)


# =========================================================
# Validate input
# =========================================================

expected_countries = {"GHA", "KEN", "NGA", "ZAF"}

assert set(df["country_code"]) == expected_countries
assert len(df) == 4
assert df["country_code"].is_unique

assert df["crypto_search_interest"].notna().all()
assert df["crypto_adoption_rank"].notna().all()


# =========================================================
# Demand analysis
# =========================================================

market_average = df["crypto_search_interest"].mean()

df["demand_vs_market_average"] = (
    df["crypto_search_interest"] / market_average
)

df["demand_gap_vs_market_average"] = (
    df["crypto_search_interest"] - market_average
)

df["demand_rank"] = (
    df["crypto_search_interest"]
    .rank(method="min", ascending=False)
    .astype(int)
)


# =========================================================
# Adoption position
#
# Chainalysis gives a global rank:
# lower number = stronger position.
#
# We convert this into a simple position among
# these four markets for comparison.
# =========================================================

df["adoption_position_among_markets"] = (
    df["crypto_adoption_rank"]
    .rank(method="min", ascending=True)
    .astype(int)
)


# =========================================================
# Compare demand position with adoption position
# =========================================================

df["demand_adoption_rank_gap"] = (
    df["demand_rank"]
    - df["adoption_position_among_markets"]
)


# =========================================================
# Classification
#
# This is NOT a market recommendation.
# It simply describes the relationship between
# the two observed signals.
# =========================================================

def classify_relationship(row):

    if (
        row["demand_rank"] == row["adoption_position_among_markets"]
    ):
        return "Aligned demand and adoption position"

    if row["demand_rank"] < row["adoption_position_among_markets"]:
        return "Demand position stronger than adoption position"

    return "Adoption position stronger than demand position"


df["demand_adoption_relationship"] = df.apply(
    classify_relationship,
    axis=1
)


# =========================================================
# Select analytical output columns
# =========================================================

analysis = df[
    [
        "country_code",
        "country",

        "crypto_search_interest",
        "crypto_search_interest_year",

        "demand_vs_market_average",
        "demand_gap_vs_market_average",
        "demand_rank",

        "crypto_adoption_rank",
        "crypto_adoption_year",
        "adoption_position_among_markets",

        "demand_adoption_rank_gap",
        "demand_adoption_relationship",
    ]
].sort_values(
    by="crypto_search_interest",
    ascending=False
).reset_index(drop=True)


# =========================================================
# Analytical QA
# =========================================================

assert len(analysis) == 4
assert analysis["country_code"].is_unique

assert abs(
    analysis["demand_vs_market_average"].mean() - 1
) < 0.000001

assert (
    analysis["demand_rank"].min() == 1
    and analysis["demand_rank"].max() == 4
)

assert (
    analysis["adoption_position_among_markets"].min() == 1
    and analysis["adoption_position_among_markets"].max() == 4
)


# =========================================================
# Display results
# =========================================================

print("\n" + "=" * 80)
print("DEMAND & ADOPTION ANALYSIS")
print("=" * 80)

print(
    f"\nFour-market average crypto search interest: "
    f"{market_average:.2f}"
)

print("\nMarket comparison:")
print(
    analysis[
        [
            "country",
            "crypto_search_interest",
            "demand_vs_market_average",
            "demand_rank",
            "crypto_adoption_rank",
            "adoption_position_among_markets",
            "demand_adoption_relationship",
        ]
    ].to_string(index=False)
)

print("\nDetailed analytical output:")
print(analysis.to_string(index=False))


# =========================================================
# Save
# =========================================================

analysis.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved: {OUTPUT_FILE}")
