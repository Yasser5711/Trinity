import os
import tempfile
from unittest.mock import patch

import pytest
from PyPDF2 import PdfReader


@patch("services.report_service.os.path.exists", return_value=True)
def test_generate_report(mock_exists, client, admin_auth_header):
    response = client.get("/reports", headers=admin_auth_header)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    file_path = os.path.join(tempfile.gettempdir(), "report.pdf")

    assert os.path.exists(file_path), "PDF file was not generated"

    reader = PdfReader(file_path)
    assert len(reader.pages) >= 1

    text = reader.pages[0].extract_text()
    assert "Analytics Report" in text
    os.remove(file_path)


@patch("services.report_service.os.path.exists", return_value=False)
def test_generate_report_missing_font(mock_exists, client, admin_auth_header):
    with pytest.raises(FileNotFoundError, match="Font file not found"):
        client.get("/reports", headers=admin_auth_header)
