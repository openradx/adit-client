import pytest
from pytest_mock import MockerFixture

from adit_client.client import AditClient


@pytest.mark.django_db
def test_store_study(
    live_server,
    settings,
    mocker: MockerFixture,
    admin_with_group_and_token,
):
    settings.STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    # Make sure it won't try to save created reports to any full text search database
    # as those are not available during test
    mocker.patch("adit.dicom_web.views.stow_store", return_value=[])

    _, _, token = admin_with_group_and_token

    client = AditClient(live_server, token)

    client.store_instances("ORTHANC1", [])
