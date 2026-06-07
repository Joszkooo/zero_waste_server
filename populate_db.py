import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from recipes.models import Product, Recipe, RecipeIngredient
from users.models import User

def populate():
    print("Czyszczenie bazy...")
    Product.objects.all().delete()
    Recipe.objects.all().delete()

    print("Dodawanie produktów...")
    products_data = [
        {'name': 'Jajko', 'category': 'Nabiał', 'default_unit': 'szt'},
        {'name': 'Masło', 'category': 'Nabiał', 'default_unit': 'g'},
        {'name': 'Sól', 'category': 'Przyprawy', 'default_unit': 'szczypta'},
        {'name': 'Makaron Spaghetti', 'category': 'Zbożowe', 'default_unit': 'g'},
        {'name': 'Mięso mielone', 'category': 'Mięso', 'default_unit': 'g'},
        {'name': 'Pomidory w puszce', 'category': 'Warzywa', 'default_unit': 'puszka'},
        {'name': 'Cebula', 'category': 'Warzywa', 'default_unit': 'szt'},
        {'name': 'Czosnek', 'category': 'Warzywa', 'default_unit': 'ząbek'},
        {'name': 'Chleb', 'category': 'Pieczywo', 'default_unit': 'kromka'},
        {'name': 'Szynka', 'category': 'Mięso', 'default_unit': 'plaster'},
        {'name': 'Pomidor', 'category': 'Warzywa', 'default_unit': 'szt'},
        {'name': 'Ser żółty', 'category': 'Nabiał', 'default_unit': 'plaster'}
    ]

    prods = {}
    for p_data in products_data:
        prod = Product.objects.create(**p_data)
        prods[p_data['name']] = prod

    print("Dodawanie przepisów...")
    
    # 1. Jajecznica
    r1 = Recipe.objects.create(
        title='Klasyczna Jajecznica',
        description='Szybka i smaczna jajecznica na maśle.',
        instructions='1. Rozgrzej masło na patelni.\n2. Wbij jajka.\n3. Posól i smaż mieszając aż zetną się według uznania.',
        prep_time_minutes=5,
        source_url='https://aniagotuje.pl/przepis/jajecznica'
    )
    RecipeIngredient.objects.create(recipe=r1, product=prods['Jajko'], quantity=3, unit='szt')
    RecipeIngredient.objects.create(recipe=r1, product=prods['Masło'], quantity=15, unit='g')
    RecipeIngredient.objects.create(recipe=r1, product=prods['Sól'], quantity=1, unit='szczypta')

    # 2. Spaghetti Bolognese
    r2 = Recipe.objects.create(
        title='Szybkie Spaghetti Bolognese',
        description='Tradycyjny włoski makaron w szybkim wydaniu.',
        instructions='1. Ugotuj makaron wg instrukcji.\n2. Podsmaż cebulę i czosnek.\n3. Dodaj mięso, smaż 5 minut.\n4. Zalej pomidorami i duś przez 10 minut.\n5. Podawaj z makaronem.',
        prep_time_minutes=25,
        source_url='https://www.kwestiasmaku.com/przepis/spaghetti-bolognese'
    )
    RecipeIngredient.objects.create(recipe=r2, product=prods['Makaron Spaghetti'], quantity=200, unit='g')
    RecipeIngredient.objects.create(recipe=r2, product=prods['Mięso mielone'], quantity=250, unit='g')
    RecipeIngredient.objects.create(recipe=r2, product=prods['Pomidory w puszce'], quantity=1, unit='puszka')
    RecipeIngredient.objects.create(recipe=r2, product=prods['Cebula'], quantity=1, unit='szt')
    RecipeIngredient.objects.create(recipe=r2, product=prods['Czosnek'], quantity=2, unit='ząbek')

    # 3. Wypasiona Kanapka
    r3 = Recipe.objects.create(
        title='Wypasiona Kanapka z Szynką',
        description='Najlepsze śniadanie na szybko.',
        instructions='1. Posmaruj chleb masłem.\n2. Połóż szynkę i ser.\n3. Na górę połóż pokrojonego pomidora.',
        prep_time_minutes=3,
        source_url='https://www.przepisy.pl/przepis/kanapka'
    )
    RecipeIngredient.objects.create(recipe=r3, product=prods['Chleb'], quantity=2, unit='kromka')
    RecipeIngredient.objects.create(recipe=r3, product=prods['Masło'], quantity=10, unit='g')
    RecipeIngredient.objects.create(recipe=r3, product=prods['Szynka'], quantity=2, unit='plaster')
    RecipeIngredient.objects.create(recipe=r3, product=prods['Ser żółty'], quantity=1, unit='plaster')
    RecipeIngredient.objects.create(recipe=r3, product=prods['Pomidor'], quantity=0.5, unit='szt')

    print("Gotowe! Baza została zasilona mockowymi danymi.")

if __name__ == '__main__':
    populate()
