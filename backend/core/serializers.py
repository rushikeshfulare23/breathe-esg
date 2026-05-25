from rest_framework import serializers
from .models import (
    Tenant,
    DataSource,
    RawRecord,
    EmissionRecord,
    AuditLog
)


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = '__all__'


class RawRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawRecord
        fields = '__all__'


class EmissionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionRecord
        fields = '__all__'


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'