
# beanthere/cli.py
import click
from beanthere.engine import get_session
from beanthere.models import Bean, Drink, Flavor
from beanthere.reports import daily_report, export_csv

# -------------------------
# CLI group
# -------------------------
@click.group()
def cli():
    """BeanThere — Coffee Shop Management CLI"""
    pass

# -------------------------
# Inventory command
# -------------------------
@cli.command()
def inventory():
    """Show current bean inventory with low-stock warnings"""
    session = get_session()
    beans = session.query(Bean).all()
    if not beans:
        click.echo("No beans in inventory yet.")
        session.close()
        return

    click.echo(f"{'Bean':20} {'Origin':15} {'Stock(g)':10} Status")
    click.echo("-" * 60)
    for b in beans:
        status = "GOOD" if b.grams_in_stock > 250 else "LOW STOCK"
        click.echo(f"{b.name:20} {b.origin:15} {b.grams_in_stock:10.0f} {status}")
    session.close()

# -------------------------
# Add or restock bean
# -------------------------
@cli.command()
@click.argument("name")
@click.argument("origin")
@click.argument("grams", type=float)
def addbean(name, origin, grams):
    """Add a new bean or restock existing ones"""
    session = get_session()
    bean = session.query(Bean).filter_by(name=name).first()
    if bean:
        bean.grams_in_stock += grams
        click.echo(f"Restocked {name} +{grams}g")
    else:
        bean = Bean(name=name, origin=origin, grams_in_stock=grams)
        session.add(bean)
        click.echo(f"Added new bean: {name} from {origin}")
    session.commit()
    session.close()

# -------------------------
# Log a drink
# -------------------------
@cli.command()
@click.argument("bean_name")
@click.argument("grams", type=float)
@click.argument("price", type=float)
@click.option("--rating", type=click.IntRange(1, 5), prompt="Rating (1-5)")
@click.option("--notes", prompt="Tasting notes", default="")
@click.option("--flavors", prompt="Flavors (comma-separated)", default="")
def log(bean_name, grams, price, rating, notes, flavors):
    """Log a drink — automatically deducts from inventory"""
    session = get_session()
    bean = session.query(Bean).filter_by(name=bean_name).first()
    if not bean:
        click.echo(f"Bean '{bean_name}' not found.")
        session.close()
        return
    if bean.grams_in_stock < grams:
        click.echo(f"Not enough {bean_name}! Only {bean.grams_in_stock:.0f}g left.")
        session.close()
        return

    drink = Drink(bean=bean, grams_used=grams, price_paid=price, rating=rating, notes=notes)

    if flavors:
        for f_name in [x.strip() for x in flavors.split(",") if x.strip()]:
            flavor = session.query(Flavor).filter_by(name=f_name).first()
            if not flavor:
                flavor = Flavor(name=f_name)
                session.add(flavor)
            drink.flavors.append(flavor)

    bean.grams_in_stock -= grams
    session.add(drink)
    session.commit()
    session.close()
    click.echo(f"Logged {grams}g of {bean_name} — ${price} — {rating} stars")

# -------------------------
# Daily report command
# -------------------------
@cli.command()
def report():
    """Daily sales, profit, and vibe check"""
    daily_report()

# -------------------------
# Export CSV command
# -------------------------
@cli.command()
def export():
    """Export today’s drinks to CSV"""
    export_csv()

# -------------------------
# CLI entrypoint
# -------------------------
if __name__ == "__main__":
    cli()
