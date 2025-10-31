from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from faker import Faker
from random import randint, choice, sample
from futbol.models import Lliga, Equip, Jugador, Partit, Event
from django.core.files import File
import requests
from io import BytesIO
from collections import defaultdict

# Para lanzar y generar datos: python manage.py crea_lliga "nombre de liga"

faker = Faker(["es_ES", "es_CA"])


class Command(BaseCommand):

    help = 'Crea una lliga amb equips, jugadors i partits falsos (reseteja abans la base de dades).'

    def get_random_avatar(self):
        from django.core.files import File
        import requests
        from io import BytesIO
        from random import randint

        num = randint(1, 99)
        url = f"https://randomuser.me/api/portraits/men/{num}.jpg"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return File(BytesIO(response.content), name=f"avatar_{num}.jpg")
        except:
            pass
        return None


    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)

    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        foto = self.get_random_avatar()

        # 1. Borrar todos los datos previos
        print("🧹 Esborrant dades antigues...")
        Event.objects.all().delete()
        Partit.objects.all().delete()
        Jugador.objects.all().delete()
        Equip.objects.all().delete()
        Lliga.objects.all().delete()
        User.objects.all().delete()
        print("✅ Dades antigues esborrades.")

        # 2. Crear superuser admin
        print("👑 Creant superusuari...")
        admin_user = User.objects.create_superuser(username="admin", password="admin", email="admin@example.com")
        print("✅ Superusuari creat: admin / admin")

        # 3. Crear lliga
        lliga = Lliga.objects.create(nom=titol_lliga, pais=faker.country())
        print(f"🏆 Creada la lliga: {titol_lliga}")

        # 4. Crear equips
        print("🏟️ Creant equips...")
        prefix_list = ["RCD", "Athletic", "Deportivo", "Unión Deportiva", "FC", "Sporting", "Real"]
        noms_usats = set()

        for _ in range(20):  # 20 equips
            while True:
                ciutat = faker.city()
                prefix = choice(prefix_list)
                nom = f"{prefix} {ciutat}"
                if nom not in noms_usats:
                    noms_usats.add(nom)
                    break

            any_fundacio = randint(1890, 2005)
            estadi = f"Estadi {faker.last_name()}"
            president = faker.name()

            equip = Equip.objects.create(
                nom=nom,
                lliga=lliga,
                any_fundacio=any_fundacio,
                estadi=estadi,
                president=president,
                ciutat=ciutat
            )
            print(f"   🟢 Equip creat: {nom} ({president})")

            # Crear jugadors per equip
            
            for _ in range(25):
                # Contamos cuántos porteros tiene el equipo actualmente
                num_porters = equip.jugadors.filter(posicio='PT').count()

                # Elegimos la posición
                if num_porters < 2:
                    posicio = choice(['PT', 'DF', 'MC', 'DL'])  # PT permitido
                else:
                    posicio = choice(['DF', 'MC', 'DL'])  # Ya hay 2 porteros, no más

                # Crear el jugador
                jugador = Jugador.objects.create(
                    nom=f"{faker.first_name_male()} {faker.last_name()}",
                    equip=equip,
                    posicio=posicio,
                    dorsal=randint(1, 99),
                    nacionalitat=faker.country()
                )

                  # Agregar foto aleatoria
                foto = self.get_random_avatar()  # Función que descarga un avatar de randomuser.me
                if foto:
                    jugador.foto.save(f"jugador_{jugador.id}.jpg", foto, save=True)


  
        # 🏁 5. Crear partits
        print("📅 Creant partits i events (gols)...")
        equips = list(lliga.equips.all())
        count_partits = 0

        for local in equips:
            for visitant in equips:
                if local != visitant:
                    partit = Partit.objects.create(
                        equip_local=local,
                        equip_visitant=visitant,
                        lliga=lliga,
                        data=timezone.now()
                    )
                    count_partits += 1
                    self.generar_goles(partit, local, visitant)

        print(f"✅ Total partits creats: {count_partits}")
        print("🎉 Dades falses creades correctament!")


    

    def generar_goles(self, partit, local, visitant):
        porter_local = partit.equip_local.jugadors.filter(posicio='PT').first()
        porter_visitant = partit.equip_visitant.jugadors.filter(posicio='PT').first()

        # Titulares y suplentes
        jugadors_locals = list(partit.equip_local.jugadors.all())
        jugadors_visitants = list(partit.equip_visitant.jugadors.all())

        titulars_local = sample(jugadors_locals, min(11, len(jugadors_locals)))
        titulars_visitants = sample(jugadors_visitants, min(11, len(jugadors_visitants)))

        # Cambios
        num_canvis_local = randint(0, 3)
        num_canvis_visitant = randint(0, 3)
        suplents_local = [j for j in jugadors_locals if j not in titulars_local]
        suplents_visitants = [j for j in jugadors_visitants if j not in titulars_visitants]

        canvis_local = sample(suplents_local, min(num_canvis_local, len(suplents_local)))
        canvis_visitant = sample(suplents_visitants, min(num_canvis_visitant, len(suplents_visitants)))

        jugadors_participants = titulars_local + canvis_local + titulars_visitants + canvis_visitant

        # Incrementamos partidos jugados
        for jugador in jugadors_participants:
            jugador.partits_jugats += 1
            jugador.save()

        # Crear goles
        gols_partit = randint(0, 5)
        for _ in range(gols_partit):
            equip_golejador = choice([local, visitant])
            jugador = choice(jugadors_participants)
            Event.objects.create(
                tipus_esdeveniment='gol',
                jugador=jugador,
                partit=partit,
                minut=randint(1, 90)
            )

            if equip_golejador == local and porter_visitant:
                porter_visitant.gols_encaixats += 1
            elif equip_golejador == visitant and porter_local:
                porter_local.gols_encaixats += 1

        if porter_local:
            porter_local.save()
        if porter_visitant:
            porter_visitant.save()

        # -------------------
        # Crear tarjetas
        # Llevamos un conteo de amarillas por jugador
        amarillas = defaultdict(int)

        for jugador in jugadors_participants:
            # Tarjeta roja directa: 1 entre 20
            if randint(1, 20) == 1:
                Event.objects.create(
                    partit=partit,
                    jugador=jugador,
                    tipus_esdeveniment='targeta_vermella',
                    minut=randint(1, 90)
                )
            # Tarjeta amarilla: 1 entre 10
            if randint(1, 10) == 1:
                amarillas[jugador] += 1
                Event.objects.create(
                    partit=partit,
                    jugador=jugador,
                    tipus_esdeveniment='targeta_groga',
                    minut=randint(1, 90)
                )
                # Si ya tiene 2 amarillas → roja
                if amarillas[jugador] == 2:
                    Event.objects.create(
                        partit=partit,
                        jugador=jugador,
                        tipus_esdeveniment='targeta_vermella',
                        minut=randint(1, 90)
                    )
