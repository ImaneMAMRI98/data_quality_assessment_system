from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings

# Create your models here.





class Services(models.Model):
    nom = models.CharField(max_length = 10000, null = True)
    domaine = models.CharField(max_length = 10000, null = True)
    nblignes = models.IntegerField(null=True,blank=True)
    nbcolonnes = models.IntegerField(null=True,blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null = True)
    fichier=models.FileField(upload_to='photos')
    def __str__(self):
        return str(self.id)


class MetaData(models.Model):
    nom_attribut=models.CharField(max_length=200,null = True)
    type_attribut=models.CharField(max_length=200,null = True)
    poids = models.IntegerField(null=True,blank=True)
    Fichier_source= models.ForeignKey(Services, on_delete=models.CASCADE,null = True)
    def __str__(self):
       return str(self.id)

class Int(models.Model):
    IVal_Min=models.IntegerField(null=True,blank=True)
    IVal_Max=models.IntegerField(null=True,blank=True)
    MetaData= models.ForeignKey(MetaData, on_delete=models.CASCADE,null = True,blank=True)
    def __str__(self):
        return str(self.id)

class Float(models.Model):
    FVal_Min=models.FloatField(null=True,blank=True)
    FVal_Max=models.FloatField(null=True,blank=True)
    MetaData= models.ForeignKey(MetaData, on_delete=models.CASCADE,null = True,blank=True)
    def __str__(self):
        return str(self.id)

class String(models.Model):
    Expression_Reguliere=models.CharField(max_length = 200,null=True,blank=True)
    longeur_min=models.IntegerField(null=True,blank=True)
    longeur_max=models.IntegerField(null=True,blank=True)
    MetaData= models.ForeignKey(MetaData, on_delete=models.CASCADE,null = True,blank=True)
    def __str__(self):
        return str(self.id)

class Date(models.Model):
    format = models.CharField(max_length = 200,null=True,blank=True)
    date_min = models.DateField()
    date_max = models.DateField()
    MetaData= models.ForeignKey(MetaData, on_delete=models.CASCADE,null = True,blank=True)
    def __str__(self):
        return str(self.id)

class semantic_rules(models.Model):
    rule = models.CharField(max_length = 200)
    attribut1 = models.ForeignKey(MetaData, on_delete=models.CASCADE, related_name='attribut1',null = True,blank=True)
    attribut2 = models.ForeignKey(MetaData, on_delete=models.CASCADE, related_name='attribut2',null = True,blank=True)
    def __str__(self):
        return str(self.id)

