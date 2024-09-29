import pytest
from adit.core.models import DicomServer
from pytest_mock import MockerFixture

from adit_client.client import AditClient


@pytest.mark.django_db
def test_store_study(live_server, mocker: MockerFixture, admin_with_group_and_token):
    mocker.patch("adit.dicom_web.views.stow_store", return_value=DicomServer(name="ORTHANC1"))
    mocker.patch("adit.dicom_web.views.WebDicomAPIView._get_dicom_server", return_value=[])

    _, _, token = admin_with_group_and_token

    client = AditClient(live_server, token)

    result = client.store_instances("ORTHANC1", [])
    assert len(result.FailedSOPSequence) == 0
