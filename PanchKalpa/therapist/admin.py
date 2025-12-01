from django.contrib import admin
from .models import Therapist, Therapy, Center, AvailableSlot


class AvailableSlotInline(admin.TabularInline):
    model = AvailableSlot
    extra = 1


@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "center", "experience")
    search_fields = ("name", "email")

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "email", "dob", "password")
        }),
        ("Professional Info", {
            "fields": ("center", "location", "experience")
        }),
        ("Expertise", {
            "fields": ("expertise",),
        }),
    )

    inlines = [AvailableSlotInline]


admin.site.register(Therapy)
admin.site.register(Center)
