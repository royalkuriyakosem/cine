from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import CustomUser
from finance.models import Contract
from productions.models import Production

class RolePermissionTests(APITestCase):
    def setUp(self):
        # Create a dummy production for foreign key relations
        self.production = Production.objects.create(title="Test Production", owner=self._create_user('admin_user', 'ADMIN'))

        # Create users with different roles
        self.admin_user = self._create_user('admin', 'ADMIN')
        self.producer_user = self._create_user('producer', 'PRODUCER')
        self.finance_user = self._create_user('finance', 'FINANCE_LEGAL')
        self.director_user = self._create_user('director', 'DIRECTOR')

        # Create a contract instance to test against
        self.contract = Contract.objects.create(
            production=self.production,
            party_name="Test Party",
            start_date="2025-01-01",
            end_date="2025-12-31",
        )
        self.contract_url = reverse('contract-detail', kwargs={'pk': self.contract.pk})

    def _create_user(self, username, role):
        user = CustomUser.objects.create_user(username, f'{username}@test.com', 'password123')
        user.role = role
        user.save()
        return user

    def test_admin_can_access_restricted_endpoint(self):
        """
        Admins should have access to any endpoint, regardless of required_roles.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.contract_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_allowed_role_can_access_endpoint(self):
        """
        Users with a role in required_roles (Producer, Finance) should get access.
        """
        # Test with Producer
        self.client.force_authenticate(user=self.producer_user)
        response = self.client.get(self.contract_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test with Finance/Legal
        self.client.force_authenticate(user=self.finance_user)
        response = self.client.get(self.contract_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_role_is_denied_access(self):
        """
        A user whose role is not in required_roles (Director) should get a 403 Forbidden.
        """
        self.client.force_authenticate(user=self.director_user)
        response = self.client.get(self.contract_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_is_denied_access(self):
        """
        Unauthenticated users should be handled by IsAuthenticated, resulting in a 401.
        Note: Our RolePermission allows unauthenticated users to pass through to the next check.
        """
        response = self.client.get(self.contract_url)
        # This will be 401 because IsAuthenticated runs first in the default DRF setup
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)