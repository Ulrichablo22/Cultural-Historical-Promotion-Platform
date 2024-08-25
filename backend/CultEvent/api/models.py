from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class User(AbstractUser):
    ROLE_CHOICES = [
        ('visitor', 'Visiteur'),
        ('organizer', 'Organisateur'),
        ('admin', 'Administrateur')
    ]
    
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='visitor')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000)
    bio = models.CharField(max_length=100)
    image = models.ImageField(upload_to="user_images", default="default.jpg")
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Lieu(models.Model):
    CATEGORIE_CHOICES = [
        ('Histo', 'Historique'),
        ('Cult', 'Culturel'),
    ]
    nom = models.CharField(max_length=255)
    description = models.TextField()
    adresse = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=10, decimal_places=8)
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    utilisateur = models.ForeignKey(User, related_name='lieux', on_delete=models.CASCADE)
    is_approved = models.BooleanField(null=True, default=None)

    def __str__(self):
        return self.nom
    

class Evenement(models.Model):
    CATEGORIE_CHOICES = [
        ('Histo', 'Historique'),
        ('Cult', 'Culturel'),
    ]
    nom = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    lieu = models.ForeignKey(Lieu, related_name='evenement', on_delete=models.CASCADE)
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    utilisateur = models.ForeignKey(User, related_name='evenements', on_delete=models.CASCADE)
    is_approved = models.BooleanField(null=True, default=None)

    def __str__(self):
        return self.nom
    

def validate_file_type(value):
    if not value.name.endswith(('.jpg', '.jpeg', '.png', '.mp4')):
        raise ValidationError('Unsupported file type.')

class Media(models.Model):
    TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]
    
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    file = models.FileField(upload_to='media_files/', validators=[validate_file_type])
    evenement = models.ForeignKey('Evenement', related_name='medias', on_delete=models.CASCADE, null=True, blank=True)
    lieu = models.ForeignKey('Lieu', related_name='medias', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.file.name}"
    
class Avis(models.Model):
    utilisateur = models.ForeignKey(User, related_name='avis', on_delete=models.CASCADE)
    lieu = models.ForeignKey(Lieu, related_name='avis', on_delete=models.CASCADE, null=True, blank=True)
    evenement = models.ForeignKey(Evenement, related_name='avis', on_delete=models.CASCADE, null=True, blank=True)
    commentaire = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        target = self.lieu or self.evenement
        return f"Avis par {self.utilisateur.username} sur {target}" if target else f"Avis par {self.utilisateur.username}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('creation', 'Création'),
        ('approval', 'Approbation'),
        ('rejection', 'Rejet'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.user.email} - {self.get_type_display()}"
