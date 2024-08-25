from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Evenement, Lieu, Notification, User

@receiver(post_save, sender=Evenement)
def notify_event_actions(sender, instance, created, **kwargs):
    if created:
        # Notification pour l'admin
        admins = User.objects.filter(role='admin')
        for admin in admins:
            Notification.objects.create(
                user=admin,
                message=f"Nouvel évènement '{instance.nom}' créé par {instance.utilisateur.email}. En attente d'approbation.",
                type='creation'
            )
    elif instance.is_approved:
        # Notification pour l'utilisateur qui a créé l'évènement
        Notification.objects.create(
            user=instance.utilisateur,
            message=f"Votre évènement '{instance.nom}' a été approuvé.",
            type='approval'
        )
    elif instance.is_approved is False:
        # Notification en cas de rejet
        Notification.objects.create(
            user=instance.utilisateur,
            message=f"Votre évènement '{instance.nom}' a été rejeté.",
            type='rejection'
        )

@receiver(post_save, sender=Lieu)
def notify_lieu_actions(sender, instance, created, **kwargs):
    if created:
        # Notification pour l'admin
        admins = User.objects.filter(role='admin')
        for admin in admins:
            Notification.objects.create(
                user=admin,
                message=f"Nouveau lieu '{instance.nom}' créé par {instance.utilisateur.email}. En attente d'approbation.",
                type='creation'
            )
    elif instance.is_approved:
        # Notification pour l'utilisateur qui a créé le lieu
        Notification.objects.create(
            user=instance.utilisateur,
            message=f"Votre lieu '{instance.nom}' a été approuvé.",
            type='approval'
        )
    elif instance.is_approved is False:
        # Notification en cas de rejet
        Notification.objects.create(
            user=instance.utilisateur,
            message=f"Votre lieu '{instance.nom}' a été rejeté.",
            type='rejection'
        )

