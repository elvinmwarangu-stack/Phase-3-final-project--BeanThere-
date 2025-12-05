# beanthere/seeds.py
from beanthere.engine import get_session, Base, engine
from beanthere.models import Bean, Drink, Flavor
from datetime import datetime

# 1️ Ensure tables exist
Base.metadata.create_all(engine)

# 2️ Open session
session = get_session()

# 3️ Create sample beans (expanded list)
beans = [
    Bean(name="Colombia Supremo", origin="Colombia", grams_in_stock=500),
    Bean(name="Ethiopia Sidamo", origin="Ethiopia", grams_in_stock=300),
    Bean(name="Kenya AA", origin="Kenya", grams_in_stock=400),
    Bean(name="Guatemala Antigua", origin="Guatemala", grams_in_stock=350),
    Bean(name="Sumatra Mandheling", origin="Indonesia", grams_in_stock=450),
    Bean(name="Brazil Santos", origin="Brazil", grams_in_stock=600),
    Bean(name="Costa Rica Tarrazu", origin="Costa Rica", grams_in_stock=320),
]

session.add_all(beans)
session.commit()  # Commit beans first

# 4️Create sample flavors
flavors = [
    Flavor(name="Chocolate"),
    Flavor(name="Berry"),
    Flavor(name="Citrus"),
    Flavor(name="Floral"),
    Flavor(name="Nutty"),
    Flavor(name="Caramel"),
]

session.add_all(flavors)
session.commit()  # Commit flavors first

# 5️ Log sample drinks
drink1 = Drink(
    bean=beans[0],  # Colombia Supremo
    grams_used=18,
    price_paid=4.5,
    rating=5,
    notes="Smooth & nutty",
    created_at=datetime.utcnow()
)
drink1.flavors.extend([flavors[0], flavors[1]])  # Chocolate, Berry

drink2 = Drink(
    bean=beans[1],  # Ethiopia Sidamo
    grams_used=20,
    price_paid=5.0,
    rating=4,
    notes="Bright acidity",
    created_at=datetime.utcnow()
)
drink2.flavors.extend([flavors[2], flavors[3]])  # Citrus, Floral

drink3 = Drink(
    bean=beans[3],  # Guatemala Antigua
    grams_used=22,
    price_paid=5.5,
    rating=5,
    notes="Rich and balanced",
    created_at=datetime.utcnow()
)
drink3.flavors.extend([flavors[4], flavors[5]])  # Nutty, Caramel

session.add_all([drink1, drink2, drink3])

# 6️ Deduct stock automatically
for drink in [drink1, drink2, drink3]:
    drink.bean.grams_in_stock -= drink.grams_used

session.commit()
session.close()

print(" Database seeded with expanded sample beans, drinks, and flavors!")
