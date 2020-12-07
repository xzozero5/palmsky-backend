from rest_framework import serializers
from backend.models import *

class BookSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(read_only=True, slug_field='word', many=True) 
    url = serializers.SerializerMethodField(read_only=True)
    cover_Image = serializers.ImageField(max_length=None, use_url=True, required=False)
    pdf_file = serializers.FileField(max_length=None, use_url=True, required=False)
    class Meta:
        model = Book
        fields = [
            'url',
            'pk',
            'title',
            'author',
            'publisher',
            'desription',
            'publish_date',
            'price',
            'stock',
            'pages',
            'width',
            'height',
            'rank_score',
            'pdf_file',
            'cover_Image',
            'tags'
        ]
        read_only_fields = ['pk']
        
        
    def get_url(self,objects):
        request = self.context.get("request")
        return objects.get_api_url(request=request)

    def Validate_title(self,value):
        qs = Book.objects.filter(title_iexact = value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists() :
            raise serializers.ValidationError("This title has been used")
        return value


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'word',
            'slug',
            'created_at',
        ]



class BookSerializerWithoutFile(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(read_only=True, slug_field='word', many=True) 
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Book
        fields = [
            'url',
            'pk',
            'title',
            'author',
            'publisher',
            'desription',
            'publish_date',
            'price',
            'stock',
            'pages',
            'width',
            'height',
            'rank_score',
            'tags'
        ]
        read_only_fields = ['pk']
        
        
    def get_url(self,objects):
        request = self.context.get("request")
        return objects.get_api_url(request=request)

    def Validate_title(self,value):
        qs = Book.objects.filter(title_iexact = value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists() :
            raise serializers.ValidationError("This title has been used")
        return value


class UserAccountSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    picture = serializers.ImageField(max_length=None, use_url=True, required=False)
    class Meta:
        model = UserAccount
        fields = [
            'url',
            'id',
            'email',
            'mailingAllow',
            'password',
            'firstName',
            'lastName',
            'picture',
            'phone',
            'dateOfBirth',
            'gender',
            'addressName',
            'street',
            'subDistrict',
            'district',
            'province',
            'zipcode'
        ]
        extra_kwargs = {'password' : {'write_only' : True}}
        
    def get_url(self,objects):
        request = self.context.get("request")
        return objects.get_api_url(request=request)

    def create(self,validated_data):
        user = UserAccount(
            email = validated_data['email'],
            mailingAllow = validated_data['mailingAllow'],
            firstName = validated_data['firstName'],
            lastName = validated_data['lastName'],
            phone = validated_data['phone'],
            dateOfBirth = validated_data['dateOfBirth'],
            gender = validated_data['gender'],
            addressName = validated_data['addressName'],
            street= validated_data['street'],
            subDistrict = validated_data['subDistrict'],
            district = validated_data['district'],
            province = validated_data['province'],
            zipcode = validated_data['zipcode']
        )
        if 'picture' in validated_data:
            user.picture = validated_data.pop('picture')
        user.set_password(validated_data['password'])
        user.save()
        return user 

