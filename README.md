# Hotel Booking Data Quality Monitor

I built this to practice data validation using SQL and Python on a real dataset.

The idea was simple — instead of just analyzing hotel booking data, I wanted to check if the data itself is trustworthy. Bad data causes real problems: wrong pricing, incorrect invoicing, broken reports.

## What it checks

- Duplicate bookings
- Negative room prices
- Bookings with zero guests
- Room type mismatches (reserved vs assigned)
- Invalid lead times
- Null pricing values

## How it works

Loads the CSV into a SQLite database, runs SQL queries against it to catch quality issues, then outputs an HTML report with pass/fail results.

## Stack

Python, SQLite, Pandas

## Dataset

Hotel Booking Demand from Kaggle — 119,390 rows

## Results

Found 14,917 room type mismatches and 8,613 duplicate entries in the dataset.
