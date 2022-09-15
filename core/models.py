from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4



# Create your models here.
class User(AbstractUser):
    """Represents the adverage user who will log in with a gmail account and a NHI number"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    is_patient = models.BooleanField(null=False, default=False)
    is_pharmacist = models.BooleanField(null=False, default=False)
    pharmacy = models.ForeignKey('Pharmacy', on_delete=models.PROTECT, null=True, blank=True)
    
    def __str__(self):
        return 
    

class Pharmacy(models.Model):
    pass




class Medication(models.Model):
    pass



class Prescription(models.Model):
    pass


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nhi = models.TextField(max_length=7, unique=True, null=False, blank=False)


