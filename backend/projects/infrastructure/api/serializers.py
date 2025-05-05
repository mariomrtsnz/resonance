from rest_framework import serializers
from ...application.dtos import ProjectCreateDTO

class ProjectCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    needed_skill_text = serializers.CharField(allow_blank=True, required=False, allow_null=True)

    def create(self, validated_data):
        return ProjectCreateDTO(**validated_data)

    def update(self, instance, validated_data):
        raise NotImplementedError


class ProjectSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    owner_id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True, allow_null=True)
    needed_skill_text = serializers.CharField(read_only=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
