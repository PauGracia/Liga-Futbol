from django.contrib.auth.models import User
from futbol.models import Equip



# Crear usuario
user = User.objects.create_user(username="entrenador_barca", password="password123")

# Asignarlo a un equipo
equip = Equip.objects.get(nom="Barcelona")
equip.usuari = user
equip.save()
