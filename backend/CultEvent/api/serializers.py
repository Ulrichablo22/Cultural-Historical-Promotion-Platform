from api.models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



# Serializer pour le modèle User
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'is_active')  # Inclure le champ role
    
    def update(self, instance, validated_data):

        # Mettre à jour les champs de l'utilisateur
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user_id', 'full_name', 'bio', 'image')  # Champs modifiables

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
    

class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'is_active', 'profile')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        # Mettre à jour l'utilisateur
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        # Mettre à jour le profil si des données de profil sont fournies
        if profile_data:
            profile_instance = instance.profile
            profile_instance.full_name = profile_data.get('full_name', profile_instance.full_name)
            profile_instance.bio = profile_data.get('bio', profile_instance.bio)
            profile_instance.image = profile_data.get('image', profile_instance.image)
            profile_instance.save()

        return instance
        

# Serializer personnalisé pour JWT
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Ajout de claims personnalisés
        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = user.profile.bio
        token['image'] = str(user.profile.image)
        token['verified'] = user.profile.verified
        token['role'] = user.role  # Inclure le rôle dans le token
        token['id'] = user.id
        token['is_active'] = user.is_active

        return token

# Serializer pour l'enregistrement des utilisateurs
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'confirm_password', 'role')  

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."})

        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', 'visitor')  # Attribuer un rôle par défaut si non spécifié
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    


class LieuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lieu
        fields = '__all__'

class EvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evenement
        fields = '__all__'

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

class AvisSerializer(serializers.ModelSerializer):
    utilisateur = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    lieu = serializers.PrimaryKeyRelatedField(queryset=Lieu.objects.all(), required=False, allow_null=True)
    evenement = serializers.PrimaryKeyRelatedField(queryset=Evenement.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Avis
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'type', 'is_read', 'created_at']