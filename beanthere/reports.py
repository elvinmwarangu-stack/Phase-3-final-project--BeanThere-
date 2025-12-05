# beanthere/reports.py
from sqlalchemy.orm import joinedload
from beanthere.engine import get_session
from beanthere.models import Drink
from datetime import date
import csv
from collections import Counter
import click

# -------------------------
# Vibe scale function
# -------------------------
def get_vibe(avg_rating):
    if avg_rating >= 4.7:
        return "Transcendent"
    elif avg_rating >= 4.2:
        return "Excellent"
    elif avg_rating >= 3.5:
        return "Good"
    else:
        return "Needs work"

# -------------------------
# Daily report
# -------------------------
def daily_report():
    session = get_session()
    today = date.today()
    drinks_today = (
        session.query(Drink)
        .options(joinedload(Drink.bean), joinedload(Drink.flavors))
        .filter(Drink.created_at >= today)
        .all()
    )

    if not drinks_today:
        click.echo("No drinks logged today yet.")
        session.close()
        return

    revenue = sum(d.price_paid for d in drinks_today)
    cost = sum((d.grams_used / 1000) * d.bean.cost_per_kg for d in drinks_today)
    profit = revenue - cost
    avg_rating = sum(d.rating for d in drinks_today) / len(drinks_today)
    vibe = get_vibe(avg_rating)

    top_bean = Counter(d.bean.name for d in drinks_today).most_common(1)[0]

    click.echo("\nBeanThere Daily Report")
    click.echo(f"Drinks served : {len(drinks_today)}")
    click.echo(f"Revenue       : ${revenue:.2f}")
    click.echo(f"Bean cost     : ${cost:.2f}")
    click.echo(f"Profit        : ${profit:.2f}")
    click.echo(f"Vibe check    : {avg_rating:.2f}/5 → {vibe}")
    click.echo(f"Top bean      : {top_bean[0]} ({top_bean[1]} drinks)")

    session.close()

# -------------------------
# Export CSV
# -------------------------
def export_csv():
    session = get_session()
    today = date.today()
    drinks = (
        session.query(Drink)
        .options(joinedload(Drink.bean), joinedload(Drink.flavors))
        .filter(Drink.created_at >= today)
        .all()
    )
    session.close()

    filename = f"beanthere_{today}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Bean", "Origin", "Grams", "Price", "Rating", "Notes", "Flavors"])
        for d in drinks:
            flavors = ", ".join(f.name for f in d.flavors)
            writer.writerow([
                d.created_at.strftime("%H:%M"),
                d.bean.name, d.bean.origin, d.grams_used,
                d.price_paid, d.rating, d.notes, flavors
            ])

    click.echo(f"Exported to {filename}")
