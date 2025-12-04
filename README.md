# ☕ BeanThere — Coffee Shop CLI Management System

**BeanThere** is a Python + SQLAlchemy + Click powered CLI application designed to help baristas manage coffee inventory, log drinks, record tasting notes, generate sales reports, and export data for business insights.

This project represents the culmination of **Phase 3** (Python + SQL + ORM), demonstrating object-oriented programming, database relationships, command-line tooling, and real-world application design.

---

##  Core Purpose

A coffee shop must track essential business metrics. Here's how BeanThere solves each challenge:

| Question | BeanThere's Solution |
|----------|----------------------|
| How much coffee is in stock? | View, add, and restock beans |
| What drinks were made today? | Log drinks with bean usage + flavors |
| How profitable were sales? | Auto-generated daily sales report |
| Can I review tasting notes later? | Flavor profiles saved as many-to-many data |
| Can I export today's sales? | Yes — CSV export included |

---

##  Key Features

### ☕ **Inventory Management**
- Add new beans or restock existing ones
- Tracks origin, cost, grams remaining
- Low stock warnings at <250g

###  **Drink Logging**
- Deducts grams used from bean stock automatically
- Supports tasting notes + multiple flavors
- Stores drink rating + price paid

###  **Reporting**
Daily report includes:
- Number of drinks served
- Revenue + bean cost + profit
- Average rating → "vibe indicator"
- Top-selling bean of the day

###  **CSV Export**
- Saves timestamp, beans used, grams, price, rating, notes & flavors
- Ready for Excel / analytics / email to management

---

##  Technologies Used

| Tool | Role |
|------|------|
| **Python** | Core language |
| **SQLAlchemy ORM** | Database + model relationships |
| **SQLite** | Local persistent database |
| **Click** | CLI command system |
| **CSV Module** | Exporting drink history |
| **Rich** | Terminal formatting & colors |

---

##  Database Schema

### Tables

| Table | Description |
|-------|-------------|
| `beans` | Sources of coffee, inventory, cost, origin |
| `drinks` | Logged sales + grams used + ratings |
| `flavors` | Individual notes like Chocolate, Berry, Citrus |
| `drink_flavor` | Many-to-many join for tasting profiles |

### Relationships

- **Bean** 1 → many **Drinks**
- **Drink** many ↔ many **Flavors**

 **Satisfies requirement:** 3+ interrelated tables

---

##  Project Structure

```
beanthere/
├── cli.py          # CLI entrypoint (Click-based commands)
├── engine.py       # Database connection + session factory
├── models.py       # SQLAlchemy ORM models (3+ tables)
├── reports.py      # Sales metrics + CSV export
└── __init__.py

beanthere.db        # Generated SQLite database
README.md           # Project documentation
```

 **Matches Phase 3 best practices:**
- ✔ Separate modules
- ✔ ORM database modeling
- ✔ CLI-driven operations
- ✔ Clear app layout

---

##  How to Run The App

### 1. Install Dependencies

```bash
pip install click sqlalchemy rich
```

### 2. Create Database Tables

```bash
python3
```

```python
from beanthere.engine import engine
from beanthere.models import Base
Base.metadata.create_all(bind=engine)
quit()
```

### 3. Run the CLI

From project root:

```bash
python3 -m beanthere.cli
```

---

##  Example Usage

| Action | Command |
|--------|---------|
| Add new bean | `python3 -m beanthere.cli addbean "Kenya AA" Kenya 500` |
| View inventory | `python3 -m beanthere.cli inventory` |
| Log a drink | `python3 -m beanthere.cli log "Kenya AA" 18 4.5 --rating 5 --notes "Citrus" --flavors "Berry, Lemon"` |
| Generate report | `python3 -m beanthere.cli report` |
| Export CSV | `python3 -m beanthere.cli export` |

---

##  How This Project Fulfills Phase 3 Requirements

| Requirement | Delivered |
|-------------|-----------|
| CLI App solving real-world problem | ✔ Coffee shop management system |
| SQLAlchemy ORM + 3+ tables | ✔ Beans / Drinks / Flavors / Join table |
| Proper package structure | ✔ Separate CLI, models, engine, reports |
| Uses lists/tuples/dicts | ✔ Flavor lists, Counter tuples, vibe dict |
| Real business application | ✔ Inventory + sales + profit analysis |

---

##  Final Summary

**BeanThere** is a fully functional command-line application built to manage coffee inventory, track drinks, generate daily business insights, and export sales history.

It showcases:
- Python fundamentals & OOP structure
- Database modeling & ORM relationships
- Practical CLI design with Click
- Real-world application patterns

 **Satisfies all Phase 3 milestone expectations**
