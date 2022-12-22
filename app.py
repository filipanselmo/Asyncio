import aiohttp
import asyncio
import asyncpg

from more_itertools import chunked


URL = 'https://swapi.dev/api/people/'

MAX = 10
PARTITION = 10



async def add(data):
    conn = await asyncpg.connect('postgresql://admin:admin@127.0.0.1:5002/swapi_db')
    query = f'INSERT INTO character  VALUES ({str(data.values())[13:-2]})'
    await conn.execute(query)



async def get_char(char_id, session):
    async with session.get(f'{URL}{char_id}') as response:
        char = await response.json()
        char['id'] = char_id
        print(char)
        return char



async def form(char_data):
    new_char = {
        'id': char_data['id'],
        'birth_year': char_data['birth_year'],
        'eye_color': char_data['eye_color'],
        'films': await list_to_string(char_data['films']),
        'gender': char_data['gender'],
        'hair_color': char_data['hair_color'],
        'height': char_data['height'],
        'homeworld': char_data['homeworld'],
        'mass': char_data['mass'],
        'name': char_data['name'],
        'skin_color': char_data['skin_color'],
        'species': await list_to_string(char_data['species']),
        'starships': await list_to_string(char_data['starships']),
        'vehicles': await list_to_string(char_data['vehicles'])}
    return new_char


async def list_to_string(data_list):
    result = ''
    for i in data_list:
        result += f'{i}, '
    return result[:-2]


async def main():
    all_ids = range(1, MAX+1)
    async with aiohttp.ClientSession() as session:
        for chunk_id in chunked(all_ids, PARTITION):
            coros = [get_char(char_id, session) for char_id in chunk_id]
            chars = await asyncio.gather(*coros)
            form_coros = [form(char) for char in chars]
            formed_chars = await asyncio.gather(*form_coros)
            db_coros = [add(char) for char in formed_chars]
            await asyncio.gather(*db_coros)
    return chars

asyncio.get_event_loop().run_until_complete(main())
