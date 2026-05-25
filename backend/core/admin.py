from django.contrib import admin
from .models import (
    Tenant,
    DataSource,
    RawRecord,
    EmissionRecord,
    AuditLog
)

admin.site.register(Tenant)
admin.site.register(DataSource)
admin.site.register(RawRecord)
admin.site.register(EmissionRecord)
admin.site.register(AuditLog)