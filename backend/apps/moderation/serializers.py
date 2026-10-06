from rest_framework import serializers

from .models import Report


class ReportCreateSerializer(serializers.Serializer):
    target_type = serializers.ChoiceField(choices=Report.TargetType.choices)
    target_id = serializers.IntegerField(min_value=1)
    reason = serializers.ChoiceField(choices=Report.Reason.choices)
    text = serializers.CharField(max_length=1000, required=False, allow_blank=True, default="")


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "status", "created_at"]
        read_only_fields = fields


class BlockCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
