import aiosqlite
import datetime
import random
from colorama import init as colorama_init, Fore
from .enums import ConsoleTheme

def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

async def evalsql(database, sql, vals:tuple=(), fetch=None):
    conn = await aiosqlite.connect(database)
    conn.row_factory = _dict_factory
    cursor = await conn.cursor()
    cursor = await cursor.execute(sql, vals)

    data = None
    if fetch == 'one':
        data = await cursor.fetchone()
    elif fetch == 'all':
        data = await cursor.fetchall()
    
    if fetch:
        pass
    else:
        await conn.commit()
    
    await cursor.close()
    await conn.close()
    return data

def createhelp(text, permissions=None):
    if not permissions:
        return text
    
    return '{} || {}'.format(text, permissions)

def generate_uid():
    '''
    Generates a unique ID

    1624662067 61835490
    |----v---| |---v--|
       epoch    random
    '''
    timestamp = datetime.datetime.utcnow().timestamp()
    key = random.randint(10000000, 99999999)
    return str(round(timestamp)) + str(key)

def format_time(time: datetime.datetime):
    return time.strftime('%c')

def log(text, theme='info'):
    colorama_init()
    print(ConsoleTheme[theme].value+text+Fore.RESET)