from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountFeatureTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="student1",
            password="StrongPass123!",
            email="student1@example.com",
            first_name="Test",
            last_name="Student",
        )

    def test_signup_page_loads(self):
        response = self.client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)

    def test_valid_registration_creates_account(self):
        response = self.client.post(reverse("signup"), {
            "username": "newstudent",
            "email": "newstudent@example.com",
            "first_name": "New",
            "last_name": "Student",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            User.objects.filter(username="newstudent").exists()
        )

    def test_registration_rejects_weak_password(self):
        response = self.client.post(reverse("signup"), {
            "username": "weakstudent",
            "email": "weak@example.com",
            "first_name": "Weak",
            "last_name": "Student",
            "password1": "123",
            "password2": "123",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="weakstudent").exists()
        )

    def test_new_registration_defaults_to_student(self):
        self.client.post(reverse("signup"), {
            "username": "defaultstudent",
            "email": "default@example.com",
            "first_name": "Default",
            "last_name": "Student",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })

        user = User.objects.get(username="defaultstudent")

        self.assertEqual(user.role, User.Role.STUDENT)

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)

    def test_student_login_redirects_to_dashboard(self):
        response = self.client.post(reverse("login"), {
            "username": "student1",
            "password": "StrongPass123!",
        })

        self.assertRedirects(
            response,
            reverse("dashboard"),
            fetch_redirect_response=False,
        )

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_authenticated_user_can_view_profile(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)

    def test_user_can_only_update_own_profile(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("profile"),
            {
                "first_name": "Updated",
                "last_name": "Name",
                "email": "updated@example.com",
                "course": "BSIT",
            },
        )

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.email, "updated@example.com")