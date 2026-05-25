import pandas as pd

from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    Tenant,
    DataSource,
    RawRecord,
    EmissionRecord,
    AuditLog
)

from .serializers import (
    EmissionRecordSerializer,
    AuditLogSerializer
)

from .normalizer import (
    normalize_sap,
    normalize_utility,
    normalize_travel,
    validate_record
)


def home(request):
    return JsonResponse({
        "message": "Breathe ESG API Running"
    })


@api_view(['POST'])
def upload_data(request):

    file = request.FILES.get("file")
    source_type = request.data.get("source_type")

    if not file:
        return Response(
            {"error": "No file uploaded"},
            status=400
        )

    df = pd.read_csv(file)

    tenant, _ = Tenant.objects.get_or_create(
        name="Demo Company"
    )

    datasource = DataSource.objects.create(
        tenant=tenant,
        source_type=source_type
    )

    for _, row in df.iterrows():

        raw_record = RawRecord.objects.create(
            datasource=datasource,
            raw_json=row.to_dict(),
            status="VALID"
        )

        if source_type == "SAP":
            normalized = normalize_sap(row)

        elif source_type == "UTILITY":
            normalized = normalize_utility(row)

        elif source_type == "TRAVEL":
            normalized = normalize_travel(row)

        else:
            continue

        errors = validate_record(
            normalized["value"]
        )

        suspicious = len(errors) > 0

        EmissionRecord.objects.create(
            tenant=tenant,
            source_record=raw_record,
            scope=normalized["scope"],
            category=normalized["category"],
            activity_value=normalized["value"],
            unit=normalized["unit"],
            normalized_value=normalized["value"],
            normalized_unit=normalized["unit"],
            suspicious=suspicious,
            status="PENDING_REVIEW"
        )

    return Response({
        "message": "File uploaded successfully"
    })


@api_view(['GET'])
def list_records(request):

    records = EmissionRecord.objects.all().order_by("-id")

    serializer = EmissionRecordSerializer(
        records,
        many=True
    )

    return Response(serializer.data)


@api_view(['PATCH'])
def approve_record(request, pk):

    try:
        record = EmissionRecord.objects.get(id=pk)

    except EmissionRecord.DoesNotExist:
        return Response(
            {"error": "Record not found"},
            status=404
        )

    new_status = request.data.get("status")

    if new_status not in [
        "APPROVED",
        "REJECTED",
        "LOCKED"
    ]:
        return Response(
            {"error": "Invalid status"},
            status=400
        )

    record.status = new_status
    record.save()

    AuditLog.objects.create(
        record=record,
        action=new_status
    )

    return Response({
        "message": "Record updated"
    })


@api_view(['GET'])
def audit_logs(request):

    logs = AuditLog.objects.all().order_by(
        "-timestamp"
    )

    serializer = AuditLogSerializer(
        logs,
        many=True
    )

    return Response(serializer.data)