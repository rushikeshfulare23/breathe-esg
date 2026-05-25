from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DataSource(models.Model):
    SOURCE_TYPES = [
        ('SAP', 'SAP'),
        ('UTILITY', 'UTILITY'),
        ('TRAVEL', 'TRAVEL'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    source_type = models.CharField(
        max_length=20,
        choices=SOURCE_TYPES
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.source_type


class RawRecord(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('VALID', 'VALID'),
        ('FAILED', 'FAILED'),
    ]

    datasource = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE
    )

    raw_json = models.JSONField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    error_message = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)


class EmissionRecord(models.Model):

    STATUS_CHOICES = [
        ('PENDING_REVIEW', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('LOCKED', 'Locked'),
    ]

    SCOPE_CHOICES = [
        ('SCOPE1', 'Scope 1'),
        ('SCOPE2', 'Scope 2'),
        ('SCOPE3', 'Scope 3'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE
    )

    source_record = models.ForeignKey(
        RawRecord,
        on_delete=models.CASCADE
    )

    scope = models.CharField(
        max_length=20,
        choices=SCOPE_CHOICES
    )

    category = models.CharField(max_length=100)

    activity_value = models.FloatField()

    unit = models.CharField(max_length=50)

    normalized_value = models.FloatField()

    normalized_unit = models.CharField(max_length=50)

    suspicious = models.BooleanField(default=False)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='PENDING_REVIEW'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.scope}"


class AuditLog(models.Model):
    record = models.ForeignKey(
        EmissionRecord,
        on_delete=models.CASCADE
    )

    action = models.CharField(max_length=255)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action