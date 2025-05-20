from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Foydalanuvchi profili"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon raqami")
    address = models.TextField(blank=True, null=True, verbose_name="Manzil")
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="Lavozim")
    image = models.ImageField(upload_to='profiles/', default='profiles/default.png', verbose_name="Profil rasmi")

    def __str__(self):
        return f"{self.user.username} profili"

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Yangi foydalanuvchi yaratilganda profil yaratish"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Foydalanuvchi saqlanganda profilni saqlash"""
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Ehtiyot chorasiga profilni yaratamiz
        Profile.objects.create(user=instance)
