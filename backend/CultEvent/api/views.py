from django.shortcuts import render
from api.models import *
from api.serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsAuthenticatedForCRUD
from django.db.models import Q
from django.utils import timezone

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

# Get All Routes

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "Hello buddy"
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.role = request.data.get('role', user.role)
        user.is_active = request.data.get('is_active', user.is_active)
        user.save()
        return Response(UserSerializer(user).data)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserProfileSerializer  # Définir le serializer par défaut

    def get_object(self):
        # Récupérer l'utilisateur associé au profil
        return super().get_object()

    def update(self, request, *args, **kwargs):
        user = self.get_object()  # Récupérer l'utilisateur

        user_profile_serializer = self.get_serializer(user, data=request.data, partial=True)
        user_profile_serializer.is_valid(raise_exception=True)
        user_profile_serializer.save()  # Met à jour à la fois l'utilisateur et le profil

        return Response(user_profile_serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LieuViewSet(viewsets.ModelViewSet):
    queryset = Lieu.objects.all()
    serializer_class = LieuSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)
        user = self.request.user
        if user.role == 'visitor':
            user.role = 'organizer'
            user.save()

        # Notification pour l'admin
        Notification.objects.create(
            user=User.objects.get(role='admin'),
            message=f"Nouveau lieu '{serializer.instance.nom}' créé par {user.email}. En attente d'approbation.",
            type='creation'
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.is_approved:
            Notification.objects.create(
                user=instance.utilisateur,
                message=f"Votre lieu '{instance.nom}' a été approuvé.",
                type='approval'
            )
        elif instance.is_approved is False:
            Notification.objects.create(
                user=instance.utilisateur,
                message=f"Votre lieu '{instance.nom}' a été rejeté.",
                type='rejection'
            )

    def perform_destroy(self, instance):
        instance.delete()

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user', None)
        is_approved = request.query_params.get('is_approved', None)
        
        queryset = Lieu.objects.all()

        if user_id:
            queryset = queryset.filter(utilisateur_id=user_id)

        if is_approved is not None:
            if is_approved == 'null':
                queryset = queryset.filter(is_approved__isnull=True)
            else:
                queryset = queryset.filter(is_approved=is_approved)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class EvenementViewSet(viewsets.ModelViewSet):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)
        user = self.request.user
        if user.role == 'visitor':
            user.role = 'organizer'
            user.save()

        # Notification pour l'admin
        Notification.objects.create(
            user=User.objects.get(role='admin'),
            message=f"Nouvel évènement '{serializer.instance.nom}' créé par {user.email}. En attente d'approbation.",
            type='creation'
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.is_approved:
            Notification.objects.create(
                user=instance.utilisateur,
                message=f"Votre évènement '{instance.nom}' a été approuvé.",
                type='approval'
            )
        elif instance.is_approved is False:
            Notification.objects.create(
                user=instance.utilisateur,
                message=f"Votre évènement '{instance.nom}' a été rejeté.",
                type='rejection'
            )

    def perform_destroy(self, instance):
        instance.delete()

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user', None)
        is_approved = request.query_params.get('is_approved', None)
        queryset = Evenement.objects.all()

        if user_id:
            queryset = queryset.filter(utilisateur_id=user_id)

        if is_approved is not None:
            if is_approved.lower() == 'null':
                queryset = queryset.filter(is_approved__isnull=True)
            else:
                queryset = queryset.filter(is_approved=is_approved)
        
        # Filtrer les événements dont la date est supérieure ou égale à aujourd'hui
        today = timezone.now().date()
        queryset = queryset.filter(date__gte=today)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticatedForCRUD]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def list(self, request, *args, **kwargs):
        evenement_id = request.query_params.get('evenement', None)
        lieu_id = request.query_params.get('lieu', None)

        if evenement_id:
            queryset = Media.objects.filter(evenement_id=evenement_id)
        elif lieu_id:
            queryset = Media.objects.filter(lieu_id=lieu_id)
        else:
            queryset = Media.objects.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class AvisViewSet(viewsets.ModelViewSet):
    queryset = Avis.objects.all()
    serializer_class = AvisSerializer
    permission_classes = [IsAuthenticatedForCRUD]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user', None)
        if user_id:
            queryset = Avis.objects.filter(utilisateur_id=user_id)
        else:
            queryset = Avis.objects.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    category = request.data.get('category', '')
    date = request.data.get('date', '')
    location = request.data.get('location', '')

    lieux = Lieu.objects.all()
    evenements = Evenement.objects.all()

    # Filtrer par catégorie
    if category:
        lieux = lieux.filter(categorie=category)
        evenements = evenements.filter(categorie=category)

    # Filtrer par date
    if date:
        evenements = evenements.filter(date=date)

    # Filtrer par emplacement (en utilisant 'adresse')
    if location:
        lieux = lieux.filter(adresse__icontains=location)

    # Filtrage par query générale (nom ou description)
    if query:
        lieux = lieux.filter(Q(nom__icontains=query) | Q(description__icontains=query))
        evenements = evenements.filter(Q(nom__icontains=query) | Q(description__icontains=query))

    # Formater les résultats
    results = {
        'lieux': lieux.values(),
        'evenements': evenements.values(),
    }

    return Response(results)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user', None)
        if user_id:
            queryset = Notification.objects.filter(user_id=user_id)
        else:
            queryset = Notification.objects.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
