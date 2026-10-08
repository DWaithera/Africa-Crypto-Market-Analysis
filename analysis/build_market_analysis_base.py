import duckdb
import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REPO1_DB = (
    Path.home()
    / "Desktop"
    / "africa-crypto-market-data-pipeline"
    / "dev.duckdb"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "market_analysis_base.csv"


# ---------------------------------------------------------
# Connect to validated Repo 1 database
# ---------------------------------------------------------

con = duckdb.connect(str(REPO1_DB), read_only=True)


# ---------------------------------------------------------
# Build country-level analytical dataset
# ---------------------------------------------------------

query = """

WITH countries AS (

    SELECT DISTINCT
        country_code,
        country
    FROM stg_google_trends

),

demand AS (

    SELECT
        country_code,
        country,
        value AS crypto_search_interest,
        year AS crypto_search_interest_year
    FROM stg_google_trends
    WHERE indicator = 'crypto_search_interest'

),

adoption AS (

    SELECT
        country_code,
        crypto_adoption_rank,
        year AS crypto_adoption_year
    FROM stg_chainalysis
    WHERE indicator = 'crypto_adoption_rank'

),

findex AS (

    SELECT
        country_code,

        MAX(
            CASE
                WHEN indicator = 'account_ownership'
                THEN value
            END
        ) AS account_ownership,

        MAX(
            CASE
                WHEN indicator = 'digital_payment_usage'
                THEN value
            END
        ) AS digital_payment_usage,

        MAX(
            CASE
                WHEN indicator = 'smartphone_adoption'
                THEN value
            END
        ) AS smartphone_adoption,

        MAX(year) AS findex_year

    FROM stg_global_findex

    GROUP BY country_code

),

world_bank_ranked AS (

    SELECT
        country_code,
        country,
        indicator_code,
        indicator_name,
        year,
        value,

        ROW_NUMBER() OVER (
            PARTITION BY country_code, indicator_code
            ORDER BY
                CASE WHEN value IS NOT NULL THEN 0 ELSE 1 END,
                year DESC
        ) AS rn

    FROM stg_world_bank

),

world_bank_latest AS (

    SELECT
        country_code,

        MAX(
            CASE
                WHEN indicator_code = 'IT.NET.USER.ZS'
                THEN value
            END
        ) AS internet_penetration,

        MAX(
            CASE
                WHEN indicator_code = 'IT.NET.USER.ZS'
                THEN year
            END
        ) AS internet_penetration_year,

        MAX(
            CASE
                WHEN indicator_code = 'NY.GDP.PCAP.CD'
                THEN value
            END
        ) AS gdp_per_capita,

        MAX(
            CASE
                WHEN indicator_code = 'NY.GDP.PCAP.CD'
                THEN year
            END
        ) AS gdp_per_capita_year,

        MAX(
            CASE
                WHEN indicator_code = 'SP.POP.TOTL'
                THEN value
            END
        ) AS population,

        MAX(
            CASE
                WHEN indicator_code = 'SP.POP.TOTL'
                THEN year
            END
        ) AS population_year

    FROM world_bank_ranked

    WHERE rn = 1

    GROUP BY country_code

),

remittances_ranked AS (

    SELECT
        country_code,
        year,
        value,

        ROW_NUMBER() OVER (
            PARTITION BY country_code
            ORDER BY
                CASE WHEN value IS NOT NULL THEN 0 ELSE 1 END,
                year DESC
        ) AS rn

    FROM stg_world_bank_remittances

    WHERE indicator_code = 'BX.TRF.PWKR.DT.GD.ZS'

),

remittances_latest AS (

    SELECT
        country_code,
        value AS remittances_pct_gdp,
        year AS remittances_pct_gdp_year

    FROM remittances_ranked

    WHERE rn = 1

)

SELECT
    c.country_code,
    c.country,

    d.crypto_search_interest,
    d.crypto_search_interest_year,

    a.crypto_adoption_rank,
    a.crypto_adoption_year,

    f.account_ownership,
    f.digital_payment_usage,
    f.smartphone_adoption,
    f.findex_year,

    wb.internet_penetration,
    wb.internet_penetration_year,

    wb.gdp_per_capita,
    wb.gdp_per_capita_year,

    wb.population,
    wb.population_year,

    r.remittances_pct_gdp,
    r.remittances_pct_gdp_year

FROM countries c

LEFT JOIN demand d
    ON c.country_code = d.country_code

LEFT JOIN adoption a
    ON c.country_code = a.country_code

LEFT JOIN findex f
    ON c.country_code = f.country_code

LEFT JOIN world_bank_latest wb
    ON c.country_code = wb.country_code

LEFT JOIN remittances_latest r
    ON c.country_code = r.country_code

ORDER BY c.country_code

"""


df = con.sql(query).df()

con.close()


# ---------------------------------------------------------
# Basic analytical-layer checks
# ---------------------------------------------------------

expected_countries = {"GHA", "KEN", "NGA", "ZAF"}

actual_countries = set(df["country_code"])

assert actual_countries == expected_countries, (
    f"Unexpected countries: {actual_countries}"
)

assert len(df) == 4, (
    f"Expected 4 country rows, got {len(df)}"
)

assert df["country_code"].is_unique, (
    "Country grain is not unique."
)

assert df["crypto_search_interest"].notna().all()
assert df["crypto_adoption_rank"].notna().all()

assert df["account_ownership"].notna().all()
assert df["digital_payment_usage"].notna().all()
assert df["smartphone_adoption"].notna().all()

assert df["gdp_per_capita"].notna().all()
assert df["population"].notna().all()

assert df["remittances_pct_gdp"].notna().all()

assert (df["crypto_search_interest"] >= 0).all()
assert (df["crypto_adoption_rank"] > 0).all()

print("\nAnalytical base:")
print(df.to_string(index=False))

print("\nShape:", df.shape)
print("Country grain unique:", df["country_code"].is_unique)

print("\nObservation years:")
year_columns = [c for c in df.columns if c.endswith("_year")]
print(df[["country_code"] + year_columns].to_string(index=False))


# ---------------------------------------------------------
# Write controlled analytical dataset
# ---------------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved: {OUTPUT_FILE}")
