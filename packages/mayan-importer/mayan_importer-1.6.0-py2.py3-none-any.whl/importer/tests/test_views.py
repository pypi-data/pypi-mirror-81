from mayan.apps.common.tests.base import GenericViewTestCase
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.tests.mixins import DocumentTestMixin

from credentials.tests.mixins import CredentialTestMixin

from ..models import ImportSetup, ImportSetupItem
from ..permissions import (
    permission_import_setup_create, permission_import_setup_delete,
    permission_import_setup_edit, permission_import_setup_process,
    permission_import_setup_view
)

from .mixins import (
    ImportSetupTestMixin, ImportSetupItemTestMixin, ImportSetupViewTestMixin,
    ImportSetupItemViewTestMixin
)


class ImportSetupViewTestCase(
    CredentialTestMixin, DocumentTestMixin, ImportSetupTestMixin,
    ImportSetupViewTestMixin, GenericViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_credential()

    def test_import_setup_backend_selection_view_no_permissions(self):
        import_setup_count = ImportSetup.objects.count()

        response = self._request_test_import_setup_backend_selection_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(ImportSetup.objects.count(), import_setup_count)

    def test_import_setup_backend_selection_view_with_permissions(self):
        self.grant_permission(permission=permission_import_setup_create)

        import_setup_count = ImportSetup.objects.count()

        response = self._request_test_import_setup_backend_selection_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(ImportSetup.objects.count(), import_setup_count)

    def test_import_setup_create_view_no_permissions(self):
        import_setup_count = ImportSetup.objects.count()

        response = self._request_test_import_setup_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(ImportSetup.objects.count(), import_setup_count)

    def test_import_setup_create_view_with_permissions(self):
        self.grant_permission(permission=permission_import_setup_create)

        import_setup_count = ImportSetup.objects.count()

        response = self._request_test_import_setup_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            ImportSetup.objects.count(), import_setup_count + 1
        )

    def test_import_setup_delete_view_no_permissions(self):
        self._create_test_import_setup()

        import_setup_count = ImportSetup.objects.count()

        response = self._request_test_import_setup_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(ImportSetup.objects.count(), import_setup_count)

    def test_import_setup_delete_view_with_access(self):
        self._create_test_import_setup()

        self.grant_access(
            obj=self.test_import_setup, permission=permission_import_setup_delete
        )

        import_setup_count = ImportSetup.objects.count()

        response = self._request_test_import_setup_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            ImportSetup.objects.count(), import_setup_count - 1
        )

    def test_import_setup_edit_view_no_permissions(self):
        self._create_test_import_setup()

        import_setup_label = self.test_import_setup.label

        response = self._request_test_import_setup_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_import_setup.refresh_from_db()
        self.assertEqual(self.test_import_setup.label, import_setup_label)

    def test_import_setup_edit_view_with_access(self):
        self._create_test_import_setup()

        self.grant_access(
            obj=self.test_import_setup, permission=permission_import_setup_edit
        )

        import_setup_label = self.test_import_setup.label

        response = self._request_test_import_setup_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_import_setup.refresh_from_db()
        self.assertNotEqual(self.test_import_setup.label, import_setup_label)

    def test_import_setup_list_view_with_no_permission(self):
        self._create_test_import_setup()

        response = self._request_test_import_setup_list_view()
        self.assertNotContains(
            response=response, text=self.test_import_setup.label,
            status_code=200
        )

    def test_import_setup_list_view_with_access(self):
        self._create_test_import_setup()

        self.grant_access(
            obj=self.test_import_setup, permission=permission_import_setup_view
        )

        response = self._request_test_import_setup_list_view()
        self.assertContains(
            response=response, text=self.test_import_setup.label,
            status_code=200
        )


class ImportSetupItemViewTestCase(
    CredentialTestMixin, DocumentTestMixin, ImportSetupTestMixin,
    ImportSetupItemTestMixin, ImportSetupItemViewTestMixin,
    GenericViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_credential()
        self._create_test_import_setup()

    def test_import_setup_clear_view_no_permission(self):
        self._create_test_import_setup_item()

        import_setup_item_count = ImportSetupItem.objects.count()

        response = self._request_test_import_setup_clear_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            ImportSetupItem.objects.count(), import_setup_item_count
        )

    def test_import_setup_clear_view_with_access(self):
        self._create_test_import_setup_item()

        self.grant_access(
            obj=self.test_import_setup, permission=permission_import_setup_process
        )

        import_setup_item_count = ImportSetupItem.objects.count()

        response = self._request_test_import_setup_clear_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            ImportSetupItem.objects.count(), import_setup_item_count - 1
        )

    def test_import_setup_populate_view_no_permission(self):
        import_setup_item_count = ImportSetupItem.objects.count()

        response = self._request_test_import_setup_populate_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            ImportSetupItem.objects.count(), import_setup_item_count
        )

    def test_import_setup_populate_view_with_access(self):
        self.grant_access(
            obj=self.test_import_setup, permission=permission_import_setup_process
        )

        import_setup_item_count = ImportSetupItem.objects.count()

        response = self._request_test_import_setup_populate_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            ImportSetupItem.objects.count(), import_setup_item_count + 1
        )

    def test_import_setup_process_view_no_permission(self):
        self._create_test_import_setup_item()

        document_count = Document.objects.count()

        response = self._request_test_import_setup_process_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            Document.objects.count(), document_count
        )

    def test_import_setup_process_view_with_access(self):
        self._create_test_import_setup_item()

        self.grant_access(
            obj=self.test_import_setup, permission=permission_import_setup_process
        )
        document_count = Document.objects.count()

        response = self._request_test_import_setup_process_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Document.objects.count(), document_count + 1
        )
