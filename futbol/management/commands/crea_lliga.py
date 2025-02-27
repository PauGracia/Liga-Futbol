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

        # Usamos get() en lugar de filter()
        try:
            lliga = Lliga.objects.get(nom=titol_lliga)
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return
        except Lliga.DoesNotExist:
            lliga = Lliga(nom=titol_lliga)
            lliga.save()
            print(f"Creem la nova lliga: {titol_lliga}")

        print("Creem equips")
        prefix_list = ["RCD", "Athletic", "Deportivo", "Unión Deportiva", "FC"]
        for i in range(20):
            ciutat = faker.city()
            prefix = choice(prefix_list)  # Selección aleatoria de un prefijo
            nom = f"{prefix} {ciutat} {randint(1, 10000)}" if prefix else ciutat
            any_fundacio = randint(1898, 1999)
            equip = Equip(ciutat=ciutat, nom=nom, lliga=lliga, any_fundacio=any_fundacio)
            if Equip.objects.filter(nom=nom).exists():
                print(f"L'equip {nom} ja existeix, se saltarà la creació.")
                continue  # Salta este equipo y pasa al siguiente

            equip.save()
            lliga.equips.add(equip)

            print(f"Creem jugadors de l'equip {nom}")
            for j in range(25):  # 25 jugadores por equipo
                nom_jugador = faker.name()
                posicio = "jugador"
                dorsal = randint(1, 99)
                jugador = Jugador(nom=nom_jugador, posicio=posicio, equip=equip, dorsal=dorsal)
                jugador.save()

        print("Creem partits de la lliga")
        for local in lliga.equips.all():
            for visitant in lliga.equips.all():
                if local != visitant:  # Evitar que un equipo juegue contra sí mismo
                    partit = Partit(equip_local=local, equip_visitant=visitant, lliga=lliga)
                    partit.save()
                    # Crear eventos (goles) para el partido
                    self.generar_goles(partit, local, visitant)

    def generar_goles(self, partit, local, visitant):
        # Definir el número máximo de goles por partido
        max_goles = randint(0, 10)  # Número aleatorio de goles, por ejemplo entre 0 y 10

        for _ in range(max_goles):
            # Seleccionar aleatoriamente un equipo para marcar el gol
            equip_goleador = choice([local, visitant])
            # Obtener un jugador aleatorio de ese equipo
            jugador = choice(equip_goleador.jugadors.all())
            # Generar el minuto aleatorio para el gol (entre 1 y 90)
            minut = randint(1, 90)
            # Crear el evento de gol
            evento = Event(tipus_esdeveniment='gol', jugador=jugador, partit=partit, minut=minut)
            evento.save()

            print(f"Gol de {jugador.nom} ({equip_goleador.nom}) en el minut {minut}")
