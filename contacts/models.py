from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator #for files uploaf

class User(AbstractUser):
    pass

class Contact(models.Model):#next we add this to admin.py
    name = models.CharField(max_length=100)
    # now we want to add files
    document= models.FileField(
        upload_to= 'contact_docs/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'txt'])],
        # coz we have contacts in the db with mo files we add, me g to formz.py
        blank= True,
        null= True
    )
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add= True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")

   

    
    class Meta:
        unique_together = ("user", "email")

    def __str__(self):
        return f"{self.name} <{self.email}>"
