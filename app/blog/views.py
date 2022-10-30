from rest_framework import viewsets
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema

from .models import Blog
from .serializers import BlogSerializer
from .tasks import send_message


class BlogViewSet(viewsets.ModelViewSet):
    '''
    Blog API endpoint to create, retrieve, update and delete blogs
    '''
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogListCreateView(generics.ListCreateAPIView):
    '''
    Blog API endpoint to get list of blogs and create blogs
    '''
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    '''
     Blog API endpoint to retrieve, update and delete blogs
     '''
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogViewListCreate(views.APIView):

    @swagger_auto_schema(responses={200: BlogSerializer(many=True)}, operation_description="Get list of blogs")
    def get(self, request, *args, **kwargs):
        queryset = Blog.objects.all()
        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BlogSerializer)
    def post(self, request, *args, **kwargs):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogViewDetail(views.APIView):
    def get_object(self, pk):
        return get_object_or_404(Blog, pk=pk)

    @swagger_auto_schema(responses={200: BlogSerializer})
    def get(self, request, pk, *args, **kwargs):
        serializer = BlogSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BlogSerializer)
    def put(self, request, pk, *args, **kwargs):
        serializer = BlogSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "Blog successfully deleted"})
    def delete(self, request, pk, *args, **kwargs):
        object = self.get_object(pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='post', request_body=BlogSerializer)
@swagger_auto_schema(method='get', responses={200:BlogSerializer(many=True)})
@api_view(['GET', 'POST'])
def blog_list_create(request):
    if request.method == 'GET':
        queryset = Blog.objects.all()
        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_message.delay("Блог создан успешно!")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: BlogSerializer})
@swagger_auto_schema(method='put', request_body=BlogSerializer)
@swagger_auto_schema(method='delete', responses={204: "Blog successfully deleted"})
@api_view(['GET', 'PUT', "DELETE"])
def blog_detail(request, pk):
    if request.method == "GET":
        serializer = BlogSerializer(get_object_or_404(Blog, pk=pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = BlogSerializer(get_object_or_404(Blog, pk=pk))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        object = (get_object_or_404(Blog, pk=pk))
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)