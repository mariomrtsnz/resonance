from rest_framework import serializers

class ProjectCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True)
    needed_skill_text = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        raise NotImplementedError("Serializers should not save directly in this architecture.")

    def update(self, instance, validated_data):
        raise NotImplementedError("Serializers should not update directly in this architecture.")

class ProjectSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    owner_id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    needed_skill_text = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True) 