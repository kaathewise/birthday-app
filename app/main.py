from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/statusz')
async def statusz(request):
    return web.Response(text="OK")

def run(argv):
    app = web.Application()
    app.add_routes(routes)
    return app
