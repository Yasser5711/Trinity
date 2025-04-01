import services.kpi_service as kpi_service
from db.schemas.kpis_schemas import KPICreate, KPIUpdate
import pytest


def test_create_kpi_service(db_session):
    data = KPICreate(name="Test KPI", value=99.9)
    kpi = kpi_service.create_kpi(db_session, data)
    assert kpi.name == "Test KPI"
    assert kpi.value == 99.9


def test_get_kpi_by_id_service(db_session):
    kpi = kpi_service.create_kpi(
        db_session, KPICreate(name="Fetch KPI", value=77.7))
    fetched = kpi_service.get_kpi_by_id(db_session, kpi.id)
    assert fetched.id == kpi.id


def test_update_kpi_service(db_session):
    kpi = kpi_service.create_kpi(
        db_session, KPICreate(name="Old KPI", value=5.0))
    update_data = KPIUpdate(value=10.0)
    updated = kpi_service.update_kpi(db_session, kpi.id, update_data)
    assert updated.value == 10.0


def test_delete_kpi_service(db_session):
    kpi = kpi_service.create_kpi(
        db_session, KPICreate(name="Delete Me", value=1.0))
    kpi_service.delete_kpi(db_session, kpi.id)

    with pytest.raises(ValueError):
        kpi_service.get_kpi_by_id(db_session, kpi.id)
