from django.db import models
from django.contrib.auth.models import User
# futbol/models.py


class Lliga(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    pais = models.CharField(max_length=50)

    def __str__(self):
        return self.nom


class Equip(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    lliga = models.ForeignKey(Lliga, on_delete=models.CASCADE, related_name="equips")
    any_fundacio = models.IntegerField()
    president = models.CharField(max_length=100, blank=True, null=True)
    estadi = models.CharField(max_length=100, blank=True, null=True)
    ciutat = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.nom


class Jugador(models.Model):
    POSICIONS = [
        ('PT', 'Porter'),
        ('DF', 'Defensa'),
        ('MC', 'Migcampista'),
        ('DL', 'Davanter')
    ]

    nom = models.CharField(max_length=100)
    equip = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name="jugadors")
    posicio = models.CharField(max_length=50, choices=POSICIONS)
    dorsal = models.IntegerField()
    nacionalitat = models.CharField(max_length=50)
    partits_jugats = models.IntegerField(default=0)
    gols_encaixats = models.IntegerField(default=0)
    foto = models.ImageField(upload_to='jugadors/', blank=True, null=True)

    def __str__(self):
        return f"{self.nom} ({self.equip.nom})"

    # Goles marcados
    def gols_marcats(self):
        return self.event_set.filter(tipus_esdeveniment="gol").count()

    # Goles encajados (solo si es portero)
    def gols_encajats(self):
        if self.posicio != 'PT':
            return 0

        # Buscar partidos donde jugó (por su equipo)
        partits = Partit.objects.filter(
            models.Q(equip_local=self.equip) | models.Q(equip_visitant=self.equip)
        )

        encajats = 0
        for partit in partits:
            if partit.equip_local == self.equip:
                encajats += partit.event_set.filter(
                    tipus_esdeveniment="gol",
                    jugador__equip=partit.equip_visitant
                ).count()
            else:
                encajats += partit.event_set.filter(
                    tipus_esdeveniment="gol",
                    jugador__equip=partit.equip_local
                ).count()
        return encajats


class Partit(models.Model):
    lliga = models.ForeignKey(Lliga, on_delete=models.CASCADE, related_name="partits")
    equip_local = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name="partits_locals")
    equip_visitant = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name="partits_visitants")
    data = models.DateTimeField(null=True, blank=True)

    def gols_local(self):
        return self.event_set.filter(
            jugador__equip=self.equip_local,
            tipus_esdeveniment="gol"
        ).count()

    def gols_visitant(self):
        return self.event_set.filter(
            jugador__equip=self.equip_visitant,
            tipus_esdeveniment="gol"
        ).count()

    def __str__(self):
        return f"{self.equip_local} vs {self.equip_visitant}"


class Event(models.Model):
    partit = models.ForeignKey(Partit, on_delete=models.CASCADE)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    tipus_esdeveniment = models.CharField(max_length=50, choices=[
        ('gol', 'Gol'),
        ('targeta_groga', 'Targeta Groga'),
        ('targeta_vermella', 'Targeta Vermella'),
        ('substitucio', 'Substitució')
    ])
    minut = models.IntegerField()

    def __str__(self):
        return f"{self.jugador.nom} - {self.tipus_esdeveniment} ({self.minut}')"
