from django.contrib.auth.models import User
from futbol.models import Equip

# Crear un usuario con un nombre único
user = User.objects.create_user(username="entrenador_FC_Cáceres_01", password="passw123")

# Obtener el equipo
equip = Equip.objects.get(nom="FC Cáceres")

# Asignar el usuario como entrenador del equipo
equip.usuari = user
equip.save()

# Confirmar la asignación
print(f"Entrenador {user.username} asignado al equipo {equip.nom}")
