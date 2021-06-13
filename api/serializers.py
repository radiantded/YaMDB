from rest_framework import serializers, validators

from .models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField(
        max_value=10,
        min_value=1
    )

    class Meta:
        model = Review
        fields = '__all__'
        required_fields = ('text', 'score',)
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('user', 'author',)
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        required_fields = ('text',)
        read_only_fields = ('title',)
