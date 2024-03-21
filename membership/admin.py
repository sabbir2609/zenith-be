from django.contrib import admin
from .models import (
    Membership,
    MembershipPlan,
    MembershipTier,
    Benefit,
    MembershipTierMapping,
)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "plan", "start_date", "end_date"]
    search_fields = ["user__username", "plan__name"]
    list_filter = ["plan"]


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "price_monthly", "price_annually"]
    search_fields = ["name"]


@admin.register(MembershipTier)
class MembershipTierAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(MembershipTierMapping)
class MembershipTierMappingAdmin(admin.ModelAdmin):
    list_display = ["plan", "tier"]
    search_fields = ["tier__name"]
    list_filter = ["tier"]
