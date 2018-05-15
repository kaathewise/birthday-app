import datetime
from aiohttp import web

from .storage import MySqlStorage

routes = web.RouteTableDef()
storage = MySqlStorage()

@routes.get('/statusz')
async def statusz(request):
    return web.Response(text="OK")

@routes.put('/hello/{name}')
async def put_birthday(request):
    name = request.match_info['name']
    date = (await request.json())['dateOfBirth']
    await storage.save_birthday(name, date)
    raise web.HTTPCreated()

@routes.get('/hello/{name}')
async def get_greeting(request):
    name = request.match_info['name']
    date = await storage.get_birthday(name)
    return web.json_response({'message': get_message(name, date)})

def get_message(name, birth_date):
    delta = days_before_birthday(birth_date)
    if delta:
        return "Hello, %s! Your birthday is in %s days" % (name, delta)
    else:
        return "Hello, %s! Happy birthday!" % (name,)

def days_before_birthday(birth_date):
    today = datetime.date.today()
    next_date = datetime.date(today.year, birth_date.month, birth_date.day)
    if next_date < today:
        next_date = datetime.date(next_date.year + 1, next_date.month, next_date.day)
    return (next_date - today).days

def run(argv):
    app = web.Application()
    app.add_routes(routes)
    return app
