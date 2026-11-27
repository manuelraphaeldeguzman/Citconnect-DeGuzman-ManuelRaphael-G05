from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import StaffProfile, StudentProfile
from .models import Voucher, VoucherAssignment


User = get_user_model()


class VoucherManagementTests(TestCase):

    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staff_test",
            password="testpass123",
            role="STAFF"
        )
        self.staff_profile = StaffProfile.objects.create(
            user=self.staff_user,
            institutional_id="STAFF-TEST-001"
        )

        self.student_user = User.objects.create_user(
            username="student_test",
            password="testpass123",
            role="STUDENT"
        )
        self.student_profile = StudentProfile.objects.create(
            user=self.student_user,
            institutional_id="STUDENT-TEST-001"
        )

        self.other_student_user = User.objects.create_user(
            username="other_student",
            password="testpass123",
            role="STUDENT"
        )
        self.other_student_profile = StudentProfile.objects.create(
            user=self.other_student_user,
            institutional_id="STUDENT-TEST-002"
        )

        self.voucher = Voucher.objects.create(
            voucher_code="TEST-VOUCHER-001",
            created_by=self.staff_profile
        )

    def create_assignment(self, voucher, student):
        return VoucherAssignment.objects.create(
            voucher=voucher,
            student=student,
            assigned_by=self.staff_profile,
            expiration_date=timezone.localdate() + timedelta(days=7)
        )

    # 1. Staff can view the voucher list.
    def test_staff_can_view_voucher_list(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(reverse("voucher-list"))

        self.assertEqual(response.status_code, 200)

    # 2. Unauthenticated users cannot view the voucher list.
    def test_voucher_list_requires_login(self):
        response = self.client.get(reverse("voucher-list"))

        self.assertEqual(response.status_code, 302)

    # 3. Students cannot access staff voucher management.
    def test_student_cannot_view_voucher_list(self):
        self.client.force_login(self.student_user)

        response = self.client.get(reverse("voucher-list"))

        self.assertEqual(response.status_code, 403)

    # 4. Staff can create a voucher.
    def test_staff_can_create_voucher(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(
            reverse("voucher-create"),
            {"voucher_code": "TEST-VOUCHER-002"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Voucher.objects.filter(
                voucher_code="TEST-VOUCHER-002"
            ).exists()
        )

    # 5. Blank voucher codes are rejected.
    def test_blank_voucher_code_is_rejected(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(
            reverse("voucher-create"),
            {"voucher_code": ""}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Voucher.objects.count(), 1)

    # 6. Staff can assign a voucher to a student.
    def test_staff_can_assign_voucher(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(
            reverse("assignment-create"),
            {
                "voucher": self.voucher.pk,
                "student": self.student_profile.pk,
                "expiration_date": (
                    timezone.localdate() + timedelta(days=7)
                ).isoformat()
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            VoucherAssignment.objects.filter(
                voucher=self.voucher,
                student=self.student_profile
            ).exists()
        )

    # 7. A voucher cannot be assigned twice.
    def test_already_assigned_voucher_is_rejected(self):
        self.create_assignment(
            self.voucher,
            self.student_profile
        )

        self.client.force_login(self.staff_user)

        response = self.client.post(
            reverse("assignment-create"),
            {
                "voucher": self.voucher.pk,
                "student": self.other_student_profile.pk,
                "expiration_date": (
                    timezone.localdate() + timedelta(days=7)
                ).isoformat()
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(VoucherAssignment.objects.count(), 1)

    # 8. Expiration dates in the past are rejected.
    def test_past_expiration_date_is_rejected(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(
            reverse("assignment-create"),
            {
                "voucher": self.voucher.pk,
                "student": self.student_profile.pk,
                "expiration_date": (
                    timezone.localdate() - timedelta(days=1)
                ).isoformat()
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(VoucherAssignment.objects.count(), 0)

    # 9. Students can only see their own voucher assignments.
    def test_student_only_sees_own_vouchers(self):
        self.create_assignment(
            self.voucher,
            self.student_profile
        )

        other_voucher = Voucher.objects.create(
            voucher_code="OTHER-STUDENT-VOUCHER",
            created_by=self.staff_profile
        )
        self.create_assignment(
            other_voucher,
            self.other_student_profile
        )

        self.client.force_login(self.student_user)

        response = self.client.get(reverse("student-vouchers"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TEST-VOUCHER-001")
        self.assertNotContains(response, "OTHER-STUDENT-VOUCHER")

    # 10. Staff cannot access the student voucher page.
    def test_staff_cannot_view_student_vouchers(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(reverse("student-vouchers"))

        self.assertEqual(response.status_code, 403)