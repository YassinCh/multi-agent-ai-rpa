from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Person

# Register your models here.


@admin.register(Person)
class PersonAdmin(ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "gender",
        "occupation",
        "created_at",
    )
    list_filter = ("gender", "created_at")
    search_fields = ("first_name", "last_name", "email", "occupation")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        (
            "Personal Information",
            {"fields": (("first_name", "last_name"), "gender", "birth_date")},
        ),
        ("Contact Details", {"fields": ("email", "phone", "address")}),
        ("Professional Information", {"fields": ("occupation",)}),
    )
