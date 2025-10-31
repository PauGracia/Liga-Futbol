from django.core.management.base import BaseCommand
from futbol.models import Lliga


# Para borrar la bbdd en consola: python manage.py delete_lliga "nombre_liga" --force

class Command(BaseCommand):
    help = "Borra una lliga i tots els seus equips, jugadors i partits."

    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', type=str, help="Nom de la lliga a esborrar")

    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga']

        try:
            lliga = Lliga.objects.get(nom=titol_lliga)
        except Lliga.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"La lliga '{titol_lliga}' no existeix."))
            return

        confirmacio = input(f"Segur que vols esborrar '{titol_lliga}'? Aquesta acció és irreversible! (si/no): ").strip().lower()

        if confirmacio == "si":
            lliga.delete()
            self.stdout.write(self.style.SUCCESS(f"La lliga '{titol_lliga}' i tot el seu contingut s'ha esborrat correctament."))
        else:
            self.stdout.write(self.style.WARNING("Operació cancel·lada."))
