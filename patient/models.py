from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

# Create your models here.

GENDER_TYPES = [('M', 'Male'), ('F', 'Female'),
                ('O', 'Other'), ('U', 'Unknown')]


class Patient(models.Model):
    insuaranceNo = models.CharField(max_length=20)
    creditcardNo = models.CharField(max_length=20)
    expiryDate = models.CharField(max_length=20)
    cvv = models.CharField(max_length=20)
    pcpId = models.CharField(max_length=20)
    ssn = models.CharField(max_length=20)


class User(AbstractUser):
    """
    Required Fields:
        -   username
        -   empi
        -   date_of_birth
        -   tenant_id
    """

    _type = models.CharField(max_length=3, null=False)
    doctor = models.ForeignKey('doctor.Doctor', on_delete=None, null=True)
    patient = models.ForeignKey(Patient, on_delete=None, null=True)
    gender = models.CharField(
        max_length=50, choices=GENDER_TYPES, default='Unknown', null=True)
    dob = models.DateField(null=True)
    zip5 = models.CharField(max_length=10, null=True)
    phoneNo = models.CharField(null=False, unique=True, max_length=10)
    status = models.IntegerField(default=0)
    otp = models.IntegerField(default=0)

    class Meta(object):
        db_table = 'auth_user'


class Visit(models.Model):
    """

    """
    patient = models.ForeignKey(User, on_delete=None)
    # default is pending, started, ended, rejected
    status = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    doctor = ArrayField(models.CharField(max_length=25, blank=True))
    create_date = models.DateTimeField(auto_now_add=True)
    endAt = models.DateTimeField(null=True)


class Rooms(models.Model):
    participants = ArrayField(models.CharField(max_length=25, blank=True))
    status = models.CharField(max_length=20)
    visit = models.ForeignKey(Visit, on_delete=None)


class Messages(models.Model):
    """
    Will store all the messages sent for each campaign,
     relations will be found in MessageRecipient model.
    """
    sentAt = models.DateTimeField(auto_now=True)
    messageType = models.CharField(max_length=200, null=True)
    messageBody = models.TextField()
    room = models.ForeignKey(Rooms, on_delete=None)
    creator = models.ForeignKey(User, on_delete=None, null=True)
    url = models.URLField(null=True)
    attachmentDisplayName = models.CharField(max_length=200, null=True)
    localName = models.CharField(max_length=200, null=True)
    visit = models.ForeignKey(Visit, on_delete=None)
    formId = models.CharField(max_length=30)

    def __str__(self):
        return "%s : %s" % (self.messageType, self.messageBody)


class Form(models.Model):
    """
    """
    formType = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='SUBMITTED')  # PENDING
    createdBy = models.ForeignKey(User, on_delete=None)
