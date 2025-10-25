import asyncio

import aiofiles

import json


async def write_json():
    new_dict = {
        "Name": "File",
        "Age": 18,
        "Country": 'Russia'
    }
    async with aiofiles.open("config.json", "w") as f:
        await f.write(json.dumps(new_dict))


async def read_file():
    async with aiofiles.open("config.json", "r") as f:
        content = await f.read()
        json_dict = json.loads(content)
        print(json_dict)


async def main():
    await write_json()
    await read_file()


if __name__ == "__main__":
    asyncio.run(main())
