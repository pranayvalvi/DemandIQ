# DemandIQ - Feature Engineering Documentation

This document explains every feature used in the DemandIQ machine learning pipeline.

## 1. Target Variable
* `Units Sold`: The actual historical demand (number of items sold).

## 2. Temporal Features
Generated from the `Date` column to capture seasonality and time-based patterns.
* `year`: The calendar year (e.g., 2021). Captures long-term trend.
* `month`: The month (1-12). Captures monthly seasonality.
* `week`: The ISO week number (1-52).
* `day`: Day of the month (1-31). Captures start/end of month effects.
* `day_of_week`: Day of the week (0=Monday, 6=Sunday). Captures weekly patterns.
* `is_weekend`: Binary indicator (1 if Saturday/Sunday, else 0). Captures weekend demand spikes.
* `quarter`: The quarter of the year (1-4).

## 3. Lag Features
Historical demand shifted forward to predict the future. All lag features are grouped by `Store` and `Product`.
* `lag_1`: The demand exactly 1 day prior.
* `lag_7`: The demand exactly 1 week (7 days) prior. Captures same-day-of-week trends.
* `lag_14`: The demand exactly 2 weeks prior.
* `lag_28`: The demand exactly 4 weeks prior.

## 4. Rolling Aggregation Features
Moving averages of historical demand to smooth out noise and capture recent momentum. Shifted by 1 day to strictly prevent data leakage.
* `rolling_mean_7`: The average demand over the last 7 days.
* `rolling_mean_14`: The average demand over the last 14 days.
* `rolling_mean_28`: The average demand over the last 28 days.

## 5. Business and Contextual Features
External factors directly impacting demand.
* `Price`: The selling price of the item.
* `Promotion`: Binary indicator (1 if on promotion, 0 if regular price).
* `Holiday`: Binary indicator (1 if the date is a holiday, 0 otherwise).
* `Inventory`: The available stock level.
* `Store`: An encoded identifier for the grocery store branch.
* `Product`: An encoded identifier for the specific product.
* `Category`: An encoded identifier for the product's category (e.g., Produce, Dairy).

## Data Leakage Prevention
To prevent data leakage during time-series forecasting:
1. `lag` and `rolling` features are strictly calculated using past data. For example, `rolling_mean_7` uses days `t-7` to `t-1`.
2. Any rows at the beginning of the dataset with missing historical lag values (the first 28 days) are dropped.
3. The Train/Validation/Test split is strictly **chronological** (70%/15%/15%). The data is never shuffled prior to splitting.
