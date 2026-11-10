#!/usr/bin/env python3
from aiohttp import web

async def handle(request):
    return web.Response(text="Kitty Corp Enterprise Test OK", status=200)

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/index.html', handle)

if __name__ == '__main__':
    print("Kitty Corp Local Test Server running on http://127.0.0.1:8080")
    web.run_app(app, host='127.0.0.1', port=8080, access_log=None)
