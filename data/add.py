import os
import django
import sys

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram_backend.settings')

django.setup()

from ingredients.models import Ingredient
import csv


def load_ingredients_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            name, measurement_unit = row
            Ingredient.objects.get_or_create(
                name=name,
                measurement_unit=measurement_unit
            )
    print("Данные успешно загружены.")


if __name__ == '__main__':
    csv_file = '../data/ingredients.csv'
    load_ingredients_from_csv(csv_file)
