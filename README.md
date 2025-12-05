## BeanThere — Coffee Shop CLI Management System

BeanThere is a Python + SQLAlchemy + Click based CLI application built to manage coffee inventory, log drink sales, track tasting notes, generate business reports, and export daily records.

This project completes Phase 3 by demonstrating database modeling, ORM relationships, CLI tooling, CSV exports, and practical application architecture.

## Core Purpose
Business Need	BeanThere's Solution
Track coffee inventory	View, add and restock beans
Record daily drinks	Log sales, grams used, bean notes
Determine profitability	Automatic daily cost vs revenue reports
Save tasting notes	Flavor tags stored and queryable
Export drink history	CSV file generation for review
Quick demo setup	Seed script populates sample records
## Key Features
1.Inventory Management

2.Add new coffee beans

3.Restock existing beans

4.Tracks origin, cost per kilogram, roast details, stock in grams

5.Low stock notification below 250g

6.Drink Logging

7.Logs grams used, price, rating and tasting notes

8.Automatically deducts stock from inventory

9.Supports multiple flavor tags per drink (many-to-many)

10.Reporting

## Daily report calculates:

Metric	Example Output
Total drinks served	7
Total revenue	24.50
Bean cost used	7.10
Profit	17.40
Average drink rating	4.6
Most used bean	Kenya AA
CSV Export

## Exports drink history for the day including:

Time | Bean | Origin | Grams Used | Price | Rating | Notes | Flavor Tags

Useful for analytics, finance reports, supervisors and backups.

seed.py — Purpose and Use

seed.py ensures the application is testable immediately by populating the database with starter beans, flavors and sample drink logs.

Run seeding:

python3 -m beanthere.seed


It inserts:

Data Type	Examples
Beans	Colombia, Ethiopia, Brazil, Kenya
Flavors	Chocolate, Citrus, Floral, Caramel
Drinks	Pre-logged drinks with ratings and grams used

This script eliminates empty-database setup time and is ideal for demonstrations, testing and grading.

## Project Structure
beanthere/
├── cli.py          # CLI commands: add, restock, log, inventory, report, export
├── engine.py       # SQLite engine + SessionLocal
├── models.py       # Beans, Drinks, Flavors, drink_flavor association table
├── reports.py      # Business logic and CSV export functions
├── seed.py         # Fills DB with starter sample data
└── __init__.py

beanthere.db        # SQLite persistent database
README.md           # Project documentation

## How to Run the Program

Install dependencies:

pip install click sqlalchemy rich


Create the database:

from beanthere.models import Base
from beanthere.engine import engine
Base.metadata.create_all(engine)


Seed sample data (optional but recommended):

python3 -m beanthere.seed


Run commands:

python3 -m beanthere.cli inventory
python3 -m beanthere.cli addbean "Kenya AA" Kenya 500
python3 -m beanthere.cli log "Kenya AA" 18 4.5 --rating 5 --notes "Sweet and bright" --flavors "Berry,Lemon"
python3 -m beanthere.cli report
python3 -m beanthere.cli export

## Final Summary

BeanThere is a complete command-line management system designed for a coffee business. It provides inventory control, sales logging, tasting notes management, profitability reporting, and CSV exporting. The included seeding script allows quick demonstration without manual data entry.

This project successfully demonstrates:

Python modular programming

SQLAlchemy ORM with multiple table relationships

CLI design and user interaction logic

CSV reporting and business analytics

Practical real-world application workflow