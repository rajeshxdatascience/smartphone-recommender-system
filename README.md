# SpecLens AI: A Data-Driven Smartphone Decision Support System

## Project Overview
**SpecLens AI** is a data-driven decision support system designed to help users choose smartphones through structured analysis of real-world specifications. Rather than relying on brand popularity or sponsored rankings, the system compares devices using measurable technical attributes such as price, performance, battery, display, and connectivity. The project emphasizes data quality, feature integrity, and system design to build a reliable foundation for recommendation and decision logic.

## Motivation
Smartphone data available online is often inconsistent in format, incomplete, or heavily influenced by marketing language. This project addresses these issues by:
* **Preserving raw data** as the source of truth.
* **Creating cleaned**, purpose-specific datasets.
* **Separating analytical logic** from UI-oriented information.

The objective is to facilitate informed and transparent decision-making by providing unbiased technical insights, moving beyond simple trend prediction.

## Dataset Summary
* **Scale:** 1,268 unique smartphone models.
* **Depth:** 65+ raw specification attributes.
* **Source:** Real-world smartphone specification pages.
* **Attributes:** Pricing, availability, hardware, software, display, and connectivity.

### Key Challenges Handled
* **Data Normalization:** Standardizing inconsistent price formats and currency across various sources.
* **Feature Extraction:** Parsing complex, unstructured strings into 19+ structured display attributes (HDR, Panel Technology, Protection levels).
* **Platform Mapping:** Handling platform-specific availability across Amazon, Flipkart, and official stores.
* **Deduplication & Naming:** Reducing variant-level noise in model naming to maintain a clean `model_id` hierarchy.
* **Nested Data Structures:** Breaking down multi-layered specification strings into atomic, ML-ready features.

## Project Structure and Design
The project follows a strict **Separation of Concerns** to ensure clarity and scalability:

1. **Raw Data:** Preserved without modification for traceability and auditing.
2. **Analytical / ML-Ready Data:** Cleaned and normalized features used for EDA and recommendation logic.
3. **UI-Oriented Metadata:** Links, images, and display-focused fields isolated from analytical features to prevent feature leakage.



## Development Stages

### Stage 1: Data Acquisition & Engineering (IN PROGRESS)
**Focus:** Building a reliable data foundation.
* [x] **Price Engineering:** Normalization of price-related fields and standardization of launch dates.
* [x] **Retail Mapping:** Binary availability flags for major retail platforms.
* [x] **Identifier Strategy:** Implementation of a stable `model_id` for relational integrity.
* [x] **Display Feature Engineering:** Extraction and normalization of panel family, refresh rate, HDR type, resolution, and protection (19+ attributes).
* [x] **Project Modularization:** Reorganization of repository into professional `scripts/` and `notebooks/` structure.
* [ ] **Next:** Processor (SoC) hierarchy, ranking strategy, and architecture-based performance scoring.

### Stage 2: Exploratory Data Analysis (EDA) (PLANNED)
* Price vs specification relationships and brand-wise feature distribution.

### Stage 3: Recommendation Logic (PLANNED)
* Similarity-based recommendation using distance and scoring metrics.

### Stage 4: Interface & Interaction Layer (PLANNED)
* Web-based interface with explainable recommendation outputs.

## Design Principles
* **Data integrity over forced completeness:** Missing values are treated as meaningful signals, not errors.
* **Decision support, not blind recommendation:** The system is designed to explain technical trade-offs.
* **Static but scalable design:** Supports future incremental updates.

## Tech Stack
* **Language:** Python
* **Libraries:** Pandas, NumPy, BeautifulSoup4
* **Environment:** Jupyter Notebook, Google Colab
* **Version Control:** Git & GitHub

---
*Project Status: Active Development. Current priority is building a correct and ML-ready data foundation.*
