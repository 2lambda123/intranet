from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


def upload_to_name(instance, filename):
    return 'core/static/core/profile_pictures/' + filename  # A CHANGER EN 'static/core/profile_pictures/' EN PROD !!!

def upload_to_name_event(instance, filename):
    return 'core/static/core/event_pictures/' + filename  # A CHANGER EN 'static/core/event_pictures/' EN PROD !!!


# Create your models here.

class UserCategory(models.Model):
    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'

    name = models.CharField(unique=True, max_length=300, verbose_name='Nom')

    def __str__(self):
        return self.name


class UserStructure(models.Model):
    class Meta:
        verbose_name = 'Structure'
        verbose_name_plural = 'Structures'

    name = models.CharField(unique=True, max_length=300, verbose_name='Nom')

    def __str__(self):
        return self.name


class UserCotisationType(models.Model):
    class Meta:
        verbose_name = 'Cotisation utilisateur'
        verbose_name_plural = 'Types de cotisation utilisateurs'

    name = models.CharField(unique=True, max_length=300, verbose_name='Nom')
    cotisation_user = models.BooleanField()

    # company_cotisation = models.BooleanField(verbose_name='Pour les entreprises', blank=True)
    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=500)
    email = models.EmailField(unique=True)
    telephone = PhoneNumberField(blank=True, null=True)
    birthday = models.DateField('Date de naissance', blank=True, null=True)
    GENDER_CHOICES = (
        ('M', 'Homme'),
        ('F', 'Femme'),
        ('O', 'Autre / ne se prononce pas')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    photo = models.FileField(upload_to=upload_to_name,
                             blank=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(UserCategory, on_delete=models.CASCADE, default=1)
    structures = models.ManyToManyField(UserStructure, blank=True)
    is_enterprise = models.BooleanField()
    cotisation_type = models.ForeignKey(UserCotisationType, on_delete=models.CASCADE, default=1)
    twitter_link = models.CharField(max_length=200, blank=True, null=True)
    linkedin_link = models.CharField(max_length=200, blank=True, null=True)
    is_subscribed_newsletter = models.BooleanField(default=False)
    address = models.CharField(max_length=500, blank=True, null=True)
    address_complement = models.CharField(max_length=500, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    # Required fields to extend AbstractBaseUser
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        Not working for now
        """
        # send_mail(subject, message, from_email, [self.email], **kwargs)


class Event(models.Model):
    class Meta:
        verbose_name = 'Evénement'
        verbose_name_plural = 'Evénements'

    event_id = models.AutoField(primary_key=True)
    event_description = models.CharField(max_length=500)
    event_begin_date = models.DateTimeField("Date de début de l'événement")
    event_end_date = models.DateTimeField("Date de fin de l'évènement")
    event_title = models.CharField(max_length=100)
    event_address = models.CharField(max_length=300)
    event_price = models.FloatField()
    event_capacity = models.IntegerField()
    event_type = models.CharField(max_length=100)
    event_publication_date = models.DateTimeField(name="Date de création de l'évènement", auto_now_add=True)
    event_photo = models.FileField(upload_to=upload_to_name_event, blank=True)
    # event_is_private = models.BooleanField() # I don't know if it has to be here
    # event_is_valide = models.BooleanField() # I don't know if it has to be here

    def __str__(self):
        return self.event_title


class Yearbook:
    pass


class SelfDevelopmentProgram:
    pass
