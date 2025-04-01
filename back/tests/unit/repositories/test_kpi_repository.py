import repositories.kpi_repository as kpi_repository
from db.models.models import KPI


def test_create_kpi_repo(db_session):
    kpi = KPI(name="Repo KPI", value=42.0)
    saved = kpi_repository.create(db_session, kpi)
    assert saved.id


def test_get_by_id_repo(db_session):
    kpi = KPI(name="Find Me", value=11.0)
    db_session.add(kpi)
    db_session.commit()
    found = kpi_repository.get_by_id(db_session, kpi.id)
    assert found.name == "Find Me"


def test_update_kpi_repo(db_session):
    kpi = KPI(name="Will Change", value=5.0)
    db_session.add(kpi)
    db_session.commit()

    kpi.value = 10.0
    updated = kpi_repository.update(db_session, kpi)
    assert updated.value == 10.0


def test_delete_kpi_repo(db_session):
    kpi = KPI(name="Gone Soon", value=0.0)
    db_session.add(kpi)
    db_session.commit()

    kpi_repository.delete(db_session, kpi)
    assert kpi_repository.get_by_id(db_session, kpi.id) is None
