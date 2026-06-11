# Structural Analysis of Swedish Bank Balance Sheets (2015–2025)

## Overview
This project provides a descriptive analysis of the balance sheets of the three major Swedish banks: SEB, Swedbank, and Handelsbanken over the period 2015–2025.

The analysis is based on financial market statistics from Statistics Sweden (SCB) and focuses on structural developments in assets, lending, and funding composition.

The objective is to describe how bank balance sheets evolve over time and how funding structures relate to lending activity in the Swedish banking system.

---

## Data
The dataset is sourced from Statistics Sweden (SCB) financial market statistics for monetary financial institutions (MFI).

It contains monthly balance sheet data and includes the following key variables:
- Total assets  
- Total lending  
- Deposits and other funding  
- Issued securities (including covered bonds)  
- Total liabilities and equity  

The data has been filtered to include:
- Skandinaviska Enskilda Banken (SEB)  
- Swedbank AB  
- Svenska Handelsbanken AB  

---

## Methodology
The analysis is based on time-series data at the bank level. The dataset is cleaned, reshaped, and standardized to ensure comparability across institutions and over time.

The study includes:
- Growth in total assets and lending  
- Funding structure decomposition  
- Lending-to-asset ratio  
- Lending relative to total funding base (deposit + wholesale funding)

The latter ratio is used as a simplified measure of structural funding dependency.

All results are descriptive and do not imply causal relationships or stability assessments.

---

## Key Findings (Visual Output)
The repository generates a set of visualizations illustrating:

- Development of total assets (2015–2025)  
- Development of total lending (2015–2025)  
- Funding structure over time  
- Funding composition in 2025  
- Lending-to-asset ratio  
- Lending relative to funding base  

All figures are included in the final report and stored in `/figures`.

---

## Limitations
- The analysis is purely descriptive  
- No econometric or causal inference is performed  
- Ratios are simplified representations of balance sheet structure  
- Data is aggregated at bank level and does not capture internal segmentation  

---

## Repository Structure
```
data/ Raw SCB dataset and processed data
figures/ Generated plots used in the report
report/ LaTeX source and compiled PDF
src/ Python scripts for data processing and analysis
```

---

## Tools Used
- Python (pandas, matplotlib, seaborn)
- LaTeX
- Statistics Sweden (SCB) financial market statistics

---

## Author
Tobias Bengtsson
