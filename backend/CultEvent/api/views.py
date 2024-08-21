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
    permission_classes = [IsAuthenticatedForCRUD]

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.role = request.data.get('role', user.role)  # Assuming 'role' is a field in your User model
        user.is_active = request.data.get('is_active', user.is_active)
        user.save()
        return Response(UserSerializer(user).data)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LieuViewSet(viewsets.ModelViewSet):
    queryset = Lieu.objects.all()
    serializer_class = LieuSerializer
    permission_classes = [IsAuthenticatedForCRUD]

    def perform_create(self, serializer):
        serializer.save()
        user = self.request.user
        if user.role == 'visiteur':
            user.role = 'organisateur'
            user.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user', None)
        if user_id:
            queryset = Lieu.objects.filter(utilisateur_id=user_id)
        else:
            queryset = Lieu.objects.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EvenementViewSet(viewsets.ModelViewSet):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    permission_classes = [IsAuthenticatedForCRUD]

    def perform_create(self, serializer):
        serializer.save()
        user = self.request.user
        if user.role == 'visiteur':
            user.role = 'organisateur'
            user.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user', None)
        if user_id:
            queryset = Evenement.objects.filter(utilisateur_id=user_id)
        else:
            queryset = Evenement.objects.all()

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

    # Filtrer par emplacement (si applicable)
    if location:
        lieux = lieux.filter(emplacement__icontains=location)

    # Formater les résultats
    results = {
        'lieux': lieux.values(),
        'evenements': evenements.values(),
    }

    return Response(results)
