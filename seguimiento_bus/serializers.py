from rest_framework import serializers
from seguimiento_bus.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('username', 'nombres', 'apellidos', 'correo', 'paradero', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        usuario = Usuario(
            username=validated_data['username'],
            nombres=validated_data['nombres'],
            apellidos=validated_data['apellidos'],
            correo=validated_data['correo'],
            paradero=validated_data['paradero']
        )
        usuario.set_password(validated_data['password'])  # Encripta la contraseña aquí
        usuario.save()
        return usuario




