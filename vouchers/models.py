from django.db import models
from accounts.models import StaffProfile, StudentProfile


class Voucher(models.Model):
    voucher_id = models.AutoField(primary_key=True)
    voucher_code = models.CharField(max_length=100, unique=True)

    created_by = models.ForeignKey(
        StaffProfile,
        on_delete=models.PROTECT,
        related_name="created_vouchers"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.voucher_code


class VoucherAssignment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        USED = "USED", "Used"
        EXPIRED = "EXPIRED", "Expired"
        REVOKED = "REVOKED", "Revoked"

    assignment_id = models.AutoField(primary_key=True)

    voucher = models.OneToOneField(
        Voucher,
        on_delete=models.CASCADE,
        related_name="assignment"
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="voucher_assignments"
    )

    assigned_by = models.ForeignKey(
        StaffProfile,
        on_delete=models.PROTECT,
        related_name="voucher_assignments"
    )

    assigned_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    def __str__(self):
        return f"{self.voucher.voucher_code} - {self.student}"


class VoucherHistory(models.Model):
    history_id = models.AutoField(primary_key=True)

    assignment = models.ForeignKey(
        VoucherAssignment,
        on_delete=models.CASCADE,
        related_name="history"
    )

    changed_by = models.ForeignKey(
        StaffProfile,
        on_delete=models.PROTECT,
        related_name="voucher_history"
    )

    action = models.CharField(max_length=255)
    previous_status = models.CharField(max_length=10, blank=True)
    new_status = models.CharField(max_length=10, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assignment} - {self.action}"
