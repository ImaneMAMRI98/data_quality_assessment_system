# Generated by Django 3.2.3 on 2021-07-03 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nom_application', models.CharField(max_length=200)),
                ('logo_application', models.CharField(max_length=200, null=True)),
                ('url', models.CharField(max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_categorie', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=10000, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('objet', models.CharField(max_length=10000, null=True)),
                ('message', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entité_commerciale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200, null=True)),
                ('prenom', models.CharField(max_length=200, null=True)),
                ('contact', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fonctionnalité',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fonctionnalité', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Langue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('langue', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MetaData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_attribut', models.CharField(max_length=200, null=True)),
                ('type_attribut', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Modele_prix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modele_prix', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plateforme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plateforme', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc_prix', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Période_essaie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('période_essaie', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=10000, null=True)),
                ('fichier', models.FileField(upload_to='photos')),
            ],
        ),
        migrations.CreateModel(
            name='Type_business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_business', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='String',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Expression_Reguliere', models.CharField(max_length=200, null=True)),
                ('longeur_min', models.IntegerField(null=True)),
                ('longeur_max', models.IntegerField(null=True)),
                ('MetaData', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.metadata')),
            ],
        ),
        migrations.CreateModel(
            name='Sous_categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_sous_categorie', models.CharField(max_length=200)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.categorie')),
            ],
        ),
        migrations.AddField(
            model_name='metadata',
            name='Fichier_source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.services'),
        ),
        migrations.CreateModel(
            name='Int',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Val_Min', models.IntegerField(null=True)),
                ('Val_Max', models.IntegerField(null=True)),
                ('MetaData', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.metadata')),
            ],
        ),
        migrations.CreateModel(
            name='formulaire_app',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_logiciel', models.CharField(max_length=200, null=True)),
                ('catégorie', models.CharField(choices=[('Logiciel de comptabilité pour consultants', 'Logiciel de comptabilité pour consultants'), ('Logiciel comptes clients', 'Logiciel comptes clients'), ('Logiciel de gestion des contras', 'Logiciel de gestion des contras'), ('Logiciel de gestion de documents', 'Logiciel de gestion de documents'), ("Logiciel d'enregistrement", "Logiciel d'enregistrement"), ('Logiciel de gestion de compte', 'Logiciel de gestion de compte'), ('Logiciel CRM de concession automobile', 'Logiciel CRM de concession automobile'), ('Outils de Business Intelligence', 'Outils de Business Intelligence'), ('Outils de cloud BI', 'Outils de cloud BI'), ('Logiciel ERP', 'Logiciel ERP'), ('Systèmes de gestion financière', 'Systèmes de gestion financière'), ("Logiciel de gestion de la chaîne d'approvisionnement", "Logiciel de gestion de la chaîne d'approvisionnement"), ('Logiciel de gestion du cycle de vie du contrat', 'Logiciel de gestion du cycle de vie du contrat'), ('Logiciel comptes payables', 'Logiciel comptes payables'), ('Logiciel de collaboration', 'Logiciel de collaboration'), ('Logiciel de gestion des actifs numériques', 'Logiciel de gestion des actifs numériques'), ("Logiciel de gestion de contenu d'entreprise", "Logiciel de gestion de contenu d'entreprise"), ('Logiciel CRM', 'Logiciel CRM'), ('Logiciel CRM Android', 'Logiciel CRM Android'), ('Logiciel CRM bancaire', 'Logiciel CRM bancaire'), ('Outils Big Data', 'Outils Big Data'), ('Logiciel de tableau de bord', 'Logiciel de tableau de bord'), ('Logiciel ERP Cloud', 'Logiciel ERP Cloud'), ("Systèmes ERP pour l'enseignement supérieur", "Systèmes ERP pour l'enseignement supérieur"), ('Logiciel 3PL', 'Logiciel 3PL'), ('Logiciel de planification de la demande', 'Logiciel de planification de la demande')], max_length=200, null=True)),
                ('url', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(null=True)),
                ('autre_fonctionnalité', models.TextField(null=True)),
                ('autre_langue', models.CharField(blank=True, max_length=200, null=True)),
                ('autre_modele_prix', models.CharField(blank=True, max_length=200, null=True)),
                ('période_essaie', models.CharField(blank=True, max_length=200, null=True)),
                ('fonctionnalité', models.ManyToManyField(to='app.Fonctionnalité')),
                ('fournisseur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.entité_commerciale')),
                ('langue', models.ManyToManyField(blank=True, to='app.Langue')),
                ('modele_prix', models.ManyToManyField(blank=True, to='app.Modele_prix')),
                ('plateforme', models.ManyToManyField(blank=True, to='app.Plateforme')),
                ('type_business', models.ManyToManyField(blank=True, to='app.Type_business')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Float',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Val_Min', models.FloatField(null=True)),
                ('Val_Max', models.FloatField(null=True)),
                ('MetaData', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.metadata')),
            ],
        ),
        migrations.CreateModel(
            name='Description_suplémentaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('langue', models.ManyToManyField(blank=True, to='app.Langue')),
                ('modele_prix', models.ManyToManyField(blank=True, to='app.Modele_prix')),
                ('plateforme', models.ManyToManyField(blank=True, to='app.Plateforme')),
                ('période_essaie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.période_essaie')),
                ('type_business', models.ManyToManyField(blank=True, to='app.Type_business')),
            ],
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(null=True)),
                ('description_suplémentaire', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.description_suplémentaire')),
                ('fonctionnalité', models.ManyToManyField(to='app.Fonctionnalité')),
                ('prix', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.prix')),
            ],
        ),
        migrations.CreateModel(
            name='Avis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentaire', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('application', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.application')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='Entité_commerciale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.entité_commerciale'),
        ),
        migrations.AddField(
            model_name='application',
            name='description',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.description'),
        ),
        migrations.AddField(
            model_name='application',
            name='sous_categorie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.sous_categorie'),
        ),
    ]
