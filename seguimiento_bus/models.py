from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UsuarioManager(BaseUserManager):
    def create_user(self, username, nombres, apellidos, correo, paradero,password = None):
        if not username or not nombres or not apellidos or not paradero :
            raise ValueError(' El usuario debe llenar los campos')
        correo = self.normalize_email(correo)
        usuario = self.model(
            username = username,
            nombres = nombres,
            correo=correo,
            apellidos = apellidos,
            paradero = paradero
        )
        usuario.set_password(password)
        usuario.save(using=self._db) 
        return usuario
    
    def create_superuser(self, correo,password = None):
        usuario = self.create_user(
            correo = self.normalize_email(correo),
        )
        usuario.set_password(password)
        usuario.usuario_admin = True
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser):
    username = models.CharField(max_length=30, unique= True)
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=50) 
    correo = models.EmailField(max_length =200, unique = True)
    paradero = models.CharField(max_length=100)
    usuario_activo = models.BooleanField(default = True)
    usuario_admin = models.BooleanField(default= False)

    objects= UsuarioManager()

    USERNAME_FIELD ='correo'
    REQUIRED_FIELDS = ['username', 'nombres', 'apellidos', 'paradero']

    def __str__(self):
        return self.correo
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        return self.usuario_admin