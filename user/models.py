from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profil(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE) 
	type_utilisateur = models.CharField(max_length = 200)
	def __str__(self):
		return str(self.user)

	