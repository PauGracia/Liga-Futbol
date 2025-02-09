
from django.db import models


class Lliga(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    pais = models.CharField(max_length=50)

    def __str__(self):
        return self.nom

class Equip(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    lliga = models.ForeignKey(Lliga, on_delete=models.CASCADE, related_name="equips")
    any_fundacio = models.IntegerField()
    estadi = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Jugador(models.Model):
    nom = models.CharField(max_length=100)
    equip = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name="jugadors")
    posicio = models.CharField(max_length=50, choices=[
        ('PT', 'Porter'),
        ('DF', 'Defensa'),
        ('MC', 'Migcampista'),
        ('DL', 'Davanter')
    ])
    dorsal = models.IntegerField()
    nacionalitat = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nom} ({self.equip.nom})"

class Partit(models.Model):
    lliga = models.ForeignKey(Lliga, on_delete=models.CASCADE, related_name="partits")
    equip_local = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name="partits_locals")
    equip_visitant = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name="partits_visitants")
    data = models.DateTimeField(null=True,blank=True)
    
    
    def gols_local(self):
        return self.event_set.filter(ugador__equip=self.equip_local).count()
    
    def gols_visitant(self):
        return self.event_set.filter(ugador__equip=self.equip_visitant).count()

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
         return f"{self.jugador.nom} - {self.tipus_esdeveniment} ({self.minut}’)"

