import asyncio
from uuid import uuid4

from tracardi.domain.flow import FlowRecord
from tracardi.service.storage.driver import storage


def test_should_store_and_load_data():
    async def main():
        id = str(uuid4())

        try:
            record = await storage.driver.flow.load_record(id)
            assert record is None
            result = await storage.driver.flow.save(FlowRecord(
                id=id,
                name="test",
                type='collection'
            ))
            await storage.driver.flow.refresh()
            assert result.saved == 1
            assert result.ids[0] == id

            record = await storage.driver.flow.load_record(id)
            assert record.id == id
        finally:
            await storage.driver.flow.delete_by_id(id)

    asyncio.run(main())