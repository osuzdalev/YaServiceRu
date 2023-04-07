import asyncio
import pprint
from telegram.ext import PicklePersistence

persistence = PicklePersistence(filepath="yaserviceru_persistence")


async def check_data() -> None:
    data = await persistence.get_user_data()
    pprint.pp(data)

if __name__ == "__main__":
    asyncio.run(check_data())
