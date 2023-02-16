from .serializers import MyTokenObtainPairSerializer,ProfileSerializer,PostSerializer
from .models import Profile,Post
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
##############################################################################
# ---register--
@api_view(['POST'])
def register(request):
    user = User.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password']
    )
    user.is_active = True
    user.is_staff = True
    user.save()
    return Response("new user born")
# ---login--
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# ---full crud for login users--
@permission_classes([IsAuthenticated])
class crudView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request):
        """
        Handle GET requests to return a list of MyModel objects
        """
        user = request.user
        print(user)
        my_model = user.profile_set.all()
        # my_model = Profile.objects.all()
        serializer = ProfileSerializer(my_model, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handle POST requests to create a new Task object
        """
        serializer = ProfileSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        """
        Handle PUT requests to update an existing Task object
        """
        my_model = Profile.objects.get(id=id)
        serializer = ProfileSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        Handle DELETE requests to delete a Task object
        """
        my_model = Profile.objects.get(id=id)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# ---full crud for login users post--
@permission_classes([IsAuthenticated])
class postcrudView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request):
        """
        Handle GET requests to return a list of MyModel objects
        """
        user = request.user
        my_model = user.post_set.all()
        serializer = PostSerializer(my_model, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handle POST requests to create a new Task object
        """
        serializer = PostSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            tsk = serializer.save()
            if request.FILES.get('pic'):
                tsk.pic = request.FILES['pic']
                tsk.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        """
        Handle PUT requests to update an existing Task object
        """
        my_model = Post.objects.get(id=id)
        serializer = PostSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        Handle DELETE requests to delete a Task object
        """
        my_model = Post.objects.get(id=id)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
