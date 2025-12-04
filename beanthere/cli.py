# beanthere/cli.py  (CLICK-ONLY VERSION)
import click
from beanthere.engine import get_session
from beanthere.models import Bean, Drink, Flavor
from beanthere.reports import daily_report, export_csv


@click.group()
def cli():
    """BeanThere — Coffee Shop Management (Click Only)"""
    pass


@cli.command()
def inventory():
    """Show current bean inventory"""
    with get_session() as s:
        beans = s.query(Bean).all()

    click.echo("=== Bean Inventory ===")
    for b in beans:
        status = "OK" if b.grams_in_stock > 250 else "LOW"
        click.echo(f"{b.name:20} {b.origin:12} {b.grams_in_stock:5.0f}g  [{status}]")


@cli.command()
@click.argument("name")
@click.argument("origin")
@click.argument("grams", type=float)
def addbean(name, origin, grams):
    """Add or restock coffee beans"""
    with get_session() as s:
        bean = s.query(Bean).filter_by(name=name).first()

        if bean:
            bean.grams_in_stock += grams
            msg = f"Restocked {name} +{grams}g"
        else:
            bean = Bean(name=name, origin=origin, grams_in_stock=grams)
            s.add(bean)
            msg = f"Added NEW bean: {name} ({origin})"

        s.commit()

    click.echo(msg)


@cli.command()
@click.argument("bean_name")
@click.argument("grams", type=float)
@click.argument("price", type=float)
@click.option("--rating", prompt="Rating (1-5)", type=click.IntRange(1,5))
@click.option("--notes", default="", prompt="Notes")
@click.option("--flavors", default="", prompt="Flavors (comma-separated)")
def log(bean_name, grams, price, rating, notes, flavors):
    """Log a drink sale + deduct bean inventory"""
    with get_session() as s:
        bean = s.query(Bean).filter_by(name=bean_name).first()

        if not bean:
            click.echo(f"ERROR: Bean '{bean_name}' not found")
            return

        if bean.grams_in_stock < grams:
            click.echo(f"ERROR: Only {bean.grams_in_stock:.0f}g left")
            return

        drink = Drink(bean=bean, grams_used=grams, price_paid=price,
                      rating=rating, notes=notes)

        for f in [x.strip() for x in flavors.split(",") if x.strip()]:
            flavor = s.query(Flavor).filter_by(name=f).first() or Flavor(name=f)
            drink.flavors.append(flavor)
            s.add(flavor)

        bean.grams_in_stock -= grams
        s.add(drink)
        s.commit()

    click.echo(f"Logged {grams}g of {bean_name} for ${price} — {rating}★")


@cli.command()
def report():
    """Show daily summary"""
    daily_report()


@cli.command()
def export():
    """Save today's orders to CSV"""
    export_csv()


if __name__ == "__main__":
    cli()
