from rest_framework import serializers
from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    is_system = serializers.BooleanField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'user', 'is_system']
        read_only_fields = ['id', 'slug', 'user', 'is_system']

    def validate_name(self, value):
        user = self.context['request'].user

        qs = Category.objects.filter(name__iexact=value, user=user)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise serializers.ValidationError("Você já tem uma categoria com esse nome.")

        if Category.objects.filter(name__iexact=value, user=None).exists():
            raise serializers.ValidationError("Já existe uma categoria do sistema com esse nome")

        return value