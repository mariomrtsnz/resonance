from rest_framework import serializers
from ...application.dtos import SkillDTO, SkillCreateDTO, SkillUpdateDTO

class SkillSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True, max_length=100)

class SkillCreateSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True, 
        max_length=100,
        error_messages={
            'blank': "Skill name cannot be empty",
            'required': "Skill name is required"
        }
    )
    
    def validate_name(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("Skill name cannot be empty")
        return value
    
    def create(self, validated_data) -> SkillCreateDTO:
        return SkillCreateDTO(**validated_data)

class SkillUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True, 
        max_length=50,
        error_messages={
            'blank': "Skill name cannot be empty",
            'required': "Skill name is required"
        }
    )

    def validate_name(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("Skill name cannot be empty")
        return value

    def to_dto(self) -> SkillUpdateDTO:
        if not hasattr(self, '_validated_data'):
            raise RuntimeError('You must call `.is_valid()` before calling `.to_dto()`.')
        return SkillUpdateDTO(**self.validated_data)
