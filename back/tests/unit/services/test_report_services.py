import os
from unittest.mock import MagicMock, patch

from services import report_service


@patch("services.report_service.os.path.exists", return_value=True)
@patch("services.report_service.FPDF")
def test_generate_report_success(mock_fpdf_class, mock_exists, db_session):
    mock_fpdf = MagicMock()
    mock_fpdf.output.return_value = "/tmp/report.pdf"  # noqa: S108
    mock_fpdf_class.return_value = mock_fpdf

    response = report_service.generate_report(db_session)

    assert response.status_code == 200
    assert response.media_type == "application/pdf"
    assert response.filename == "report.pdf"
    mock_fpdf.output.assert_called_once()


def test_generate_report_actual_output(db_session):
    with (
        patch("services.report_service.os.path.exists", return_value=True),
        patch("services.report_service.FPDF") as MockPDF,  # noqa: N806
    ):
        pdf_instance = MockPDF.return_value
        pdf_instance.output.side_effect = lambda path, _: open(path, "wb").write(
            b"%PDF dummy content"
        )

        response = report_service.generate_report(db_session)
        assert isinstance(response, report_service.FileResponse)
        assert os.path.exists(response.path)
        os.remove(response.path)


def test_generate_report_missing_fonts(db_session):
    with patch("services.report_service.os.path.exists", return_value=False):
        try:
            report_service.generate_report(db_session)
        except FileNotFoundError as e:
            assert "Font file not found" in str(e)
