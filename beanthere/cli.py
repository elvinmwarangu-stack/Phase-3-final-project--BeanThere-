# beanthere/cli.py
import click
from rich.console import Console
from rich.table import Table
from beanthere.engine import get_session
from beanthere.models import Bean, Drink, Flavor
from beanthere.reports import daily_report, export_csv
from datetime import date

console = Console()

@click.group()
def cli():
    """BeanThere — Hipster Coffee Shop Management"""
    pass

@cli.command()
def inventory():
    """Show current bean inventory with low-stock warnings"""
    session = get_session()
    beans = session.query(Bean).all()
    table = Table(title="Bean Inventory")
    table.add_column("Bean", style="bold cyan")
    table.add_column("Origin", style="magenta")
    table.add_column("Stock", justify="right")
    table.add_column("Status")

    for b in beans:
        status = "[green]Good[/]" if b.grams_in_stock > 250 else "[red]LOW STOCK[/]"
        table.add_row(b.name, b.origin, f"{b.grams_in_stock:.0f}g", status)
    console.print(table)
    session.close()

@cli.command()
@click.argument("name")
@click.argument("origin")
@click.argument("grams", type=float)
def addbean(name: str, origin: str, grams: float):
    """Add or restock a bean"""
    session = get_session()
    bean = session.query(Bean).filter_by(name=name).first()
    if bean:
        bean.grams_in_stock += grams
        console.print(f"[green]Restocked {name} +{grams}g[/]")
    else:
        bean = Bean(name=name, origin=origin, grams_in_stock=grams)
        session.add(bean)
        console.print(f"[bold green]New bean added: {name} from {origin}[/]")
    session.commit()
    session.close()

@cli.command()
@click.argument("bean_name")
@click.argument("grams", type=float)
@click.argument("price", type=float)
@click.option("--rating", type=click.IntRange(1,5), prompt="Rating (1-5 stars)")
@click.option("--notes", prompt="Tasting notes", default="")
@click.option("--flavors", prompt="Flavors (comma-separated)", default="")
def log(bean_name, grams, price, rating, notes, flavors):
    """Log a drink — automatically deducts from inventory"""
    session = get_session()
    bean = session.query(Bean).filter_by(name=bean_name).first()
    if not bean:
        console.print(f"[red]Bean '{bean_name}' not found[/]")
        return
    if bean.grams_in_stock < grams:
        console.print(f"[red]Not enough {bean_name}! Only {bean.grams_in_stock:.0f}g left[/]")
        return

    drink = Drink(bean=bean, grams_used=grams, price_paid=price, rating=rating, notes=notes)
    if flavors:
        for f in [x.strip() for x in flavors.split(",") if x.strip()]:
            flavor = session.query(Flavor).filter_by(name=f).first()
            if not flavor:
                flavor = Flavor(name=f)
                session.add(flavor)
            drink.flavors.append(flavor)

    bean.grams_in_stock -= grams
    session.add(drink)
    session.commit()
    session.close()
    console.print(f"[bold green]Logged {grams}g of {bean_name} — ${price} — {rating} stars[/]")

@cli.command()
def report():
    """Daily sales, profit, and vibe check"""
    daily_report()

@cli.command()
def export():
    """Export today’s drinks to CSV"""
    export_csv()

# Register report/export as CLI commands
cli.add_command(report)
cli.add_command(export)

if __name__ == "__main__":
    cli()