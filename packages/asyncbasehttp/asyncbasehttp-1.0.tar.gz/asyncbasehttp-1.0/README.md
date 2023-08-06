# Async Http Server

The simplest async python http server library.

# Example

    import asyncio
    from asyncbasehttp import request_handler, Request, Response

    @request_handler
    async def handle_request(req: Request):
        return Response.create_ok_response(f'You requested path: {req.path}'.encode())


    async def main():
        server = await asyncio.start_server(handle_request, port=8000)
        print("http://localhost:8000")
        await server.serve_forever()

    asyncio.run(main())

