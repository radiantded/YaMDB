from django.core.exceptions import ValidationError
from rest_framework import serializers, validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Avg
from .models import Review, Comment, Title, Category, Genre
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    score = serializers.IntegerField(
        max_value=10,
        min_value=1
    )

    class Meta:
        model = Review
        fields = '__all__'
        required_fields = ('text', 'score',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        required_fields = ('text',)
        read_only_fields = ('review',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'username', 'bio', 'email', 'role')


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class TitleSerializerGet(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    genre = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name', many=True
    )

    rating = serializers.SerializerMethodField()

    def get_rating(self, title):
        return Review.objects.filter(title=title).aggregate(Avg('score'))['score__avg']

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating')
        model = Title


class TitleSerializerPost(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=False
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=False
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category
        lookup_field = 'slug'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirmation_code'] = serializers.CharField()
        del self.fields['password']

    def validate(self, attrs):
        try:
            user = User.objects.get(
                email=attrs['email'],
                confirmation_code=attrs['confirmation_code']
            )
        except User.DoesNotExist:
            raise ValidationError('Неверный email или confirmation_code')
        refresh = self.get_token(user)
        attrs = {}
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        return attrs
