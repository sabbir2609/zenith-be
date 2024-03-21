from django.db import models
from django.conf import settings


class MembershipPlan(models.Model):
    name = models.CharField(
        max_length=100, help_text="The name of the membership plan."
    )
    description = models.TextField(help_text="A description of the membership plan.")
    price_monthly = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The monthly price of the membership plan.",
    )
    price_annually = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The annual price of the membership plan.",
    )

    class Meta:
        verbose_name = "Membership Plan"
        verbose_name_plural = "Membership Plans"

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships"
    )
    plan = models.ForeignKey(
        MembershipPlan, on_delete=models.CASCADE, related_name="memberships"
    )
    start_date = models.DateField(help_text="The start date of the membership.")
    end_date = models.DateField(help_text="The end date of the membership.")

    class Meta:
        verbose_name = "Membership"
        verbose_name_plural = "Memberships"

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"


class MembershipTier(models.Model):
    name = models.CharField(
        max_length=100, help_text="The name of the membership tier."
    )
    description = models.TextField(help_text="A description of the membership tier.")
    benefits = models.ManyToManyField(
        "Benefit", help_text="The benefits included in the membership tier."
    )

    class Meta:
        verbose_name = "Membership Tier"
        verbose_name_plural = "Membership Tiers"

    def __str__(self):
        return self.name


class Benefit(models.Model):
    name = models.CharField(max_length=100, help_text="The name of the benefit.")
    description = models.TextField(help_text="A description of the benefit.")

    class Meta:
        verbose_name = "Benefit"
        verbose_name_plural = "Benefits"

    def __str__(self):
        return self.name


class MembershipTierMapping(models.Model):
    plan = models.ForeignKey(
        MembershipPlan, on_delete=models.CASCADE, related_name="tier_mappings"
    )
    tier = models.ForeignKey(
        MembershipTier, on_delete=models.CASCADE, related_name="tier_mappings"
    )

    class Meta:
        verbose_name = "Membership Tier Mapping"
        verbose_name_plural = "Membership Tier Mappings"

    def __str__(self):
        return f"{self.plan.name} - {self.tier.name}"
