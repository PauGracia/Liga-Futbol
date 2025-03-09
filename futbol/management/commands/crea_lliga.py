from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from random import randint, choice

# Asegúrate de que tus modelos estén importados
from futbol.models import Lliga, Equip, Jugador, Partit, Event

faker = Faker(["es_CA", "es_ES"])

class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'

    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)

    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]

        # Comprovar si la lliga ja existeix
        if Lliga.objects.filter(nom=titol_lliga).exists():
            print(f"Aquesta lliga '{titol_lliga}' ja està creada. Posa un altre nom.")
            return

        lliga = Lliga(nom=titol_lliga)
        lliga.save()
        print(f"Creem la nova lliga: {titol_lliga}")

        print("Creem equips...")
        prefix_list = ["RCD", "Athletic", "Deportivo", "Unión Deportiva", "FC"]
        noms_usats = set(Equip.objects.values_list('nom', flat=True))  # Equipos ya en la BD

        for _ in range(20):  # 20 equips
            while True:
                ciutat = faker.city()
                prefix = choice(prefix_list)  # Seleccionamos un prefijo aleatorio
                nom = f"{prefix} {ciutat}" if prefix else ciutat
                
                if nom not in noms_usats:  # Si el nombre es único, lo usamos
                    noms_usats.add(nom)
                    break

            any_fundacio = randint(1898, 1999)
            equip = Equip(nom=nom, lliga=lliga, any_fundacio=any_fundacio, estadi=faker.company())
            equip.save()
            print(f"Equip creat: {nom}")

            print(f"   Creant jugadors per a {nom}...")
            for _ in range(25):  # 25 jugadores por equipo
                nom_jugador = faker.name()
                posicio = choice(['PT', 'DF', 'MC', 'DL'])
                dorsal = randint(1, 99)
                nacionalitat = faker.country()
                jugador = Jugador(nom=nom_jugador, posicio=posicio, equip=equip, dorsal=dorsal, nacionalitat=nacionalitat)
                jugador.save()

        print("Creem partits de la lliga...")
        for local in lliga.equips.all():
            for visitant in lliga.equips.all():
                if local != visitant:  # Evitar que un equipo juegue contra sí mismo
                    partit = Partit(equip_local=local, equip_visitant=visitant, lliga=lliga, data=timezone.now())
                    partit.save()
                    self.generar_goles(partit, local, visitant)

    def generar_goles(self, partit, local, visitant):
        max_goles = randint(0, 5)  # Número aleatorio de goles entre 0 y 5

        for _ in range(max_goles):
            equip_goleador = choice([local, visitant])
            jugador = equip_goleador.jugadors.order_by('?').first()  # Selecciona un jugador al azar
            if not jugador:
                continue  # Si no hay jugadores, pasamos

            minut = randint(1, 90)
            evento = Event(tipus_esdeveniment='gol', jugador=jugador, partit=partit, minut=minut)
            evento.save()
            print(f"Gol de {jugador.nom} ({equip_goleador.nom}) al minut {minut}")
