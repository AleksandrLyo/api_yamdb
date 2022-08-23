from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, Comment, Review
from users.models import ROLES

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   allow_blank=False,
                                   validators=[
                                       UniqueValidator(
                                           queryset=User.objects.all(),
                                           message='Пользователь с таким '
                                                   'email уже существует!')])
    role = serializers.ChoiceField(choices=ROLES, read_only=True)

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError("Не может быть 'me'.")
        return value

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


class AdminUserSerializer(UserSerializer):
    role = serializers.ChoiceField(choices=ROLES, read_only=False,
                                   required=False)


class AuthUserSerializer(UserSerializer):
    confirmation_code = serializers.CharField

    class Meta:
        fields = ('username', 'confirmation_code')
        read_only_fields = ['confirmation_code']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    description = serializers.CharField(required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'category',
                  'genre', 'year', 'rating')

    def get_rating(self, ob):
        return ob.reviews.all().aggregate(Avg('score'))['score__avg']


class TitleEditSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class ReviewsSerializer(serializers.ModelSerializer):
    """Отзывы на произведения"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        fields = ('id', 'title', 'author', 'pub_date', 'text', 'score',)
        model = Review
        read_only_fields = ['title']

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request'].parser_context['kwargs']['title_id']
            )
            user = self.context['request'].user
            if user.reviews.filter(title_id=title_id).exists():
                raise serializers.ValidationError(
                    'Нельзя оставить отзыв на одно произведение дважды'
                )
        return data

    def validate_score(self, value):
        if 0 >= value >= 10:
            raise serializers.ValidationError('Проверьте оценку')
        return value


class CommentsSerializer(serializers.ModelSerializer):
    """Комментарии на отзывы"""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
