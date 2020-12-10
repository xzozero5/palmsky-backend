
from rest_framework import generics ,mixins
from backend.models import *
from .serializer import *
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly,UpdateOwnProfile
from rest_framework import viewsets,filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

class Token(models.Model):
    ...

    class Meta:
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS

class BookListAPIView(mixins.CreateModelMixin,generics.ListAPIView):
    lookup_field = 'pk' #id #url(?P<pk>\d+)
    serializer_class = BookSerializer
    def get_queryset(self) : #/?q = <text>
        qs = Book.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(author__icontains=query)|
                Q(publisher__icontains=query)
            ).distinct()
        return qs
    def post(self, request, *ards, **kwargs):
        return self.create(request, *ards, **kwargs)
    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}
    def upload(request):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()


class BookListRankAPIView(mixins.CreateModelMixin,generics.ListAPIView):
    lookup_field = 'pk' #id #url(?P<pk>\d+)
    serializer_class = BookSerializer
    def get_queryset(self) : #/?q = <text>
        qs = Book.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(author__icontains=query)|
                Q(publisher__icontains=query)
            ).distinct()
        qs = qs.order_by('-rank_score')
        return qs
    def post(self, request, *ards, **kwargs):
        return self.create(request, *ards, **kwargs)
    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}
    def upload(request):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()   
        """
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        """

class BookRudView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk' #id #url(?P<pk>\d+)
    serializer_class = BookSerializer
   # permission_classes = [IsOwnerOrReadOnly]
    def get_queryset(self) :
        return Book.objects.all()
    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}
    def upload(request):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()      
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT' or self.request.method == 'PATCH'  :
            serializer_class = BookSerializerWithoutFile
        return serializer_class
    
       
    """
    def get_object(self):
        pk = self.kwargs.get("pk")
        return Book.objects.get(pk=pk)
    """

class TagListAPIView(generics.ListAPIView):
    serializer_class = TagSerializer
    def get_queryset(self) : #/?q = <text>
       return Tag.objects.all()
       

class BookTagListAPIView(generics.ListAPIView):

    serializer_class = BookSerializer
    def get_queryset(self):
       qs = Book.objects.all()
       tag_qs = Tag.objects.all()
       query = self.request.GET.get("q")
       if query is not None:
           # print(query)
            s_tag = tag_qs.filter(word__iexact = query).values_list('id', flat=True)
            print(s_tag)
            qs = qs.filter(tags__in = s_tag).distinct()
       return qs


class UserAccountViewSet(viewsets.ModelViewSet):
    serializer_class = UserAccountSerializer
    queryset = UserAccount.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields =  ('=email',)

    def upload(request):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()     


class UserAccountRudViewSet(viewsets.ModelViewSet):
    serializer_class = UserAccountUrlSerializer
    queryset = UserAccount.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProfile,)

    def get_queryset(self):
        user = self.request.user
        return UserAccount.objects.filter(email = user.email)
    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
            
class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserAccountAddressViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserAccountAddressSerializer
    queryset = UserAccountAddress.objects.all()

    def perform_create(self, serializer):
        serializer.save(user_account=self.request.user)
    """
    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}
    def pre_save(self, obj):
        obj.owner = self.request.user
    def post(self, request):
        serializer = UserAccountAddressSerializer(data=request.data)
        serializer.save(user_account = self.request.user)
    """
    def get_queryset(self):
        user = self.request.user
        return UserAccountAddress.objects.filter(user_account = user)

class PromotionListAPIView(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = PromotionSerializer
    def get_queryset(self) : #/?q = <text>
       return Promotion.objects.all()


class PromotionBookListAPIView(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = PromotionBookSerializer
    def get_queryset(self) : #/?q = <text>
       return Promotion.objects.all()

