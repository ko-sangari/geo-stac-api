import pytest

from sqlalchemy import select

from src.models.geo_models import GeoField


@pytest.mark.asyncio
async def test_satellite_image_create(postgres, satellite_image_instance):
    async with postgres.session_factory() as session:
        session.add(satellite_image_instance)
        await session.commit()

        query_all = (await session.execute(select(GeoField))).scalars().all()
        assert len(query_all) == 1


@pytest.mark.asyncio
async def test_create_tables(postgres):
    async with postgres.session_factory() as session:
        async with session.bind.connect() as connection:
            table_names = await connection.run_sync(
                session.bind.dialect.get_table_names
            )
            assert table_names == ["spatial_ref_sys", "geo_fields"]


@pytest.mark.asyncio
async def test_health_check(postgres):
    result = await postgres.health_check()
    assert result is True


@pytest.mark.asyncio
async def test_drop_tables(postgres):
    await postgres.drop_tables()

    async with postgres.session_factory() as session:
        async with session.bind.connect() as connection:
            table_names = await connection.run_sync(
                session.bind.dialect.get_table_names
            )
            assert table_names == ["spatial_ref_sys"]

    await postgres.create_tables()
