\# Africa Crypto Market Analysis \& Business Intelligence



Market analysis and business intelligence for understanding crypto-market conditions across Ghana, Kenya, Nigeria, and South Africa.



\## Overview



This project analyzes four African markets using a validated public-data foundation developed in the companion project:



\[Africa Crypto Market Data Pipeline](https://github.com/DWaithera/africa-crypto-market-data-pipeline)



The analysis examines:



\- Crypto search interest

\- Crypto adoption

\- Financial access

\- Digital payment usage

\- Smartphone adoption

\- Internet penetration

\- Population

\- GDP per capita

\- Remittances



The objective is to turn fragmented market data into evidence that can support Growth, Product, and Market Expansion teams in understanding differences across markets and identifying questions that require deeper investigation.



\## Business Problem



A centralized crypto exchange is evaluating African markets for potential growth and product expansion.



Before making expansion or investment decisions, the business needs to understand:



\- Where crypto interest is strongest

\- Whether observed interest corresponds with adoption

\- What financial and digital conditions exist in each market

\- How market scale and economic context differ

\- What additional evidence is required before making a market-level decision



This project focuses on \*\*market analysis and business intelligence\*\*, rather than producing a definitive market-entry recommendation.



\## Markets Analyzed



| Country | Code |

|---|---|

| Ghana | GHA |

| Kenya | KEN |

| Nigeria | NGA |

| South Africa | ZAF |



\## Analytical Questions



\### 1. Is there evidence of market demand?



Google Trends crypto search interest is used to compare observed search behaviour across the four markets.



\### 2. How does observed interest compare with crypto adoption?



Crypto search interest is compared with Chainalysis adoption rankings to identify areas of alignment and divergence.



\### 3. What financial and digital conditions surround participation?



The analysis examines:



\- Account ownership

\- Digital payment usage

\- Smartphone adoption

\- Internet penetration



\### 4. What does the broader market context look like?



The analysis considers:



\- Population

\- GDP per capita

\- Remittances as a percentage of GDP



\### 5. What does the combined evidence suggest?



The final analysis synthesizes the evidence into market profiles and identifies questions that Growth and Product teams would need to investigate before making expansion decisions.



\## Key Findings



\### Crypto interest and adoption do not always move together



Nigeria records the highest observed crypto search interest among the four markets at \*\*77\*\* and the strongest adoption position among the four.



Ghana and South Africa show greater divergence between observed interest and adoption position.



\### Similar interest can represent different market conditions



Ghana and Kenya both record \*\*31\*\* search interest, while their Chainalysis global adoption ranks are \*\*#46\*\* and \*\*#28\*\*, respectively.



This illustrates why search interest should not be treated as a standalone proxy for market maturity.



\### Financial and digital readiness varies materially



Kenya records the highest account ownership (\*\*90.1%\*\*) and digital payment usage (\*\*89.3%\*\*) among the four markets.



South Africa has the strongest combination of smartphone adoption (\*\*67.5%\*\*) and internet penetration (\*\*78.4%\*\*).



Nigeria has the largest population (\*\*237.5M\*\*) but lower financial and digital access indicators than the other markets.



\## Dashboard



The Power BI analysis is structured around four analytical pages:



1\. \*\*Market Landscape\*\*  

&#x20;  Market scale, economic context, and crypto interest.



2\. \*\*Crypto Interest vs Adoption\*\*  

&#x20;  Comparison of observed crypto interest and adoption position.



3\. \*\*Digital \& Financial Readiness\*\*  

&#x20;  Financial access, digital connectivity, and economic context.



4\. \*\*From Market Signals to Business Questions\*\*  

&#x20;  Cross-market synthesis, implications, and additional evidence required for deeper decision-making.



\## Analytical Approach



The project follows:



\*\*Business Question → Data → Metric → Comparison → Observation → Interpretation → Business Implication → Limitation → Next Question\*\*



The analysis is intentionally descriptive and comparative.



It does not attempt to estimate:



\- Exchange market share

\- Active crypto users

\- Transaction volume

\- Customer acquisition cost

\- Conversion

\- Retention

\- Revenue

\- Competitor market share

\- Regulatory impact



These areas represent additional evidence required for a more complete market-entry assessment.



\## Data Sources



| Source | Data Used |

|---|---|

| World Bank | Population, GDP per capita, internet penetration, remittances |

| Global Findex | Account ownership, digital payments, smartphone adoption |

| Google Trends | Crypto search interest |

| Chainalysis | Crypto adoption ranking |



\## Project Structure



```text

meps-market-analysis/

├── analysis/

│   ├── 01\_demand\_analysis.py

│   ├── 02\_financial\_digital\_access.py

│   ├── 03\_market\_context.py

│   └── build\_market\_analysis\_base.py

├── data/

│   └── processed/

│       ├── demand\_adoption\_analysis.csv

│       ├── financial\_digital\_access\_analysis.csv

│       ├── market\_analysis\_base.csv

│       └── market\_context\_analysis.csv

└── README.md



## Technology

- Python
- Pandas
- SQL
- Power BI
- Git
- GitHub

## Portfolio Context

This project is the analytical layer of a two-stage portfolio project.

### Stage 1 — Data Foundation

Public data was collected, validated, standardized, and prepared using Python, DuckDB, and dbt.

### Stage 2 — Market Analysis

The validated data was transformed into comparative market analysis and business intelligence using Python and Power BI.

## Limitations

The analysis uses public data from different sources and reporting periods.

Google Trends measures relative search interest rather than users, transactions, or revenue.

Chainalysis rankings represent an adoption index position rather than exchange market share or transaction volume.

The findings should therefore be treated as market signals and hypotheses for further investigation, rather than definitive market-entry recommendations.

## Author

**Damaris Waithera**

Data Analyst | FinTech & Web3 | Emerging Markets
