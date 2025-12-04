# beanthere/reports.py
from rich.console import Console
from datetime import date
import csv
from collections import Counter

from beanthere.engine import get_session
from beanthere.models import Drink

console = Console()

VIBE_SCALE = {
    4.7: "[bold magenta]Transcendent[/]",
    4.2: "[bold green]Excellent[/]",
    3.5: "[yellow]Good[/]",
    0:   "[red]Needs work[/]"
}



def daily_report():
    with get_session() as session:
        drinks_today = session.query(Drink).filter(Drink.created_at >= date.today()).all()

    if not drinks_today:
        console.print("[yellow]No drinks logged today yet.[/]")
        return

    revenue = sum(d.price_paid for d in drinks_today)
    cost = sum((d.grams_used / 1000) * d.bean.cost_per_kg for d in drinks_today)
    profit = revenue - cost
    avg_rating = sum(d.rating for d in drinks_today) / len(drinks_today)

    vibe = (
        "[bold magenta]Transcendent[/]" if avg_rating >= 4.7 else
        "[bold green]Excellent[/]" if avg_rating >= 4.2 else
        "[yellow]Good[/]" if avg_rating >= 3.5 else
        "[red]Needs work[/]"
    )

    top_bean = Counter(d.bean.name for d in drinks_today).most_common(1)[0]

    console.print("\n[bold underline]BeanThere Daily Report[/]")
    console.print(f"Drinks served : {len(drinks_today)}")
    console.print(f"Revenue       : [green]${revenue:.2f}[/]")
    console.print(f"Bean cost     : [red]${cost:.2f}[/]")
    console.print(f"Profit        : [bold green]${profit:.2f}[/]")
    console.print(f"Vibe check    : {avg_rating:.2f}/5 → {vibe}")
    console.print(f"Top bean      : [cyan]{top_bean[0]}[/] ({top_bean[1]} drinks)")


def export_csv():
    with get_session() as session:
        drinks = session.query(Drink).filter(Drink.created_at >= date.today()).all()

    filename = f"beanthere_{date.today()}.csv"
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

    console.print(f"[green]Exported to {filename}[/]")
