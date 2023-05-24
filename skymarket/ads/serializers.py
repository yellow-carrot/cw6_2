from rest_framework import serializers
from phonenumber_field import serializerfields

from ads.models import Comment, Ad


class CommentSerializer(serializers.ModelSerializer):
    ad = serializers.SlugRelatedField(read_only=True, slug_field="title")
    author = serializers.CharField(read_only=True)
    author_first_name = serializers.CharField(read_only=True)
    author_last_name = serializers.CharField(read_only=True)
    author_id = serializers.IntegerField(read_only=True)
    author_image = serializers.ImageField(read_only=True)
    ad_id = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ("pk", "image", "title", "price", "description")


class AdDetailSerializer(serializers.ModelSerializer):
    author_first_name = serializers.ReadOnlyField(source="author.first_name")
    author_last_name = serializers.ReadOnlyField(source="author.last_name")
    phone = serializerfields.PhoneNumberField(source="author.phone", read_only=True)
    author_id = serializers.ReadOnlyField(source="author.id")

    class Meta:
        model = Ad
        fields = '__all__'
