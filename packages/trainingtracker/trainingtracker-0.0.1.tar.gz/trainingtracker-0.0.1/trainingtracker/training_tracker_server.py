import asyncio, websockets, socket, multiprocessing, copy, time

def run_server(queue):
    async def send_message(websocket, path):
        while True:
            try:
                incoming = await websocket.recv()

                # Get the latest internal state
                while not queue.empty(): server_state = queue.get_nowait()
                queue.put_nowait(server_state) # Pass the last server_state back into the pipe to get it next iteration
                outgoing = str(server_state)

                await websocket.send(outgoing)
            except: pass

    server_start = websockets.serve(send_message, port=15532)

    asyncio.get_event_loop().run_until_complete(server_start)
    asyncio.get_event_loop().run_forever()

def start_server():
    queue = multiprocessing.Queue()
    job = multiprocessing.Process(target=run_server, args=(queue,))
    job.start()
    return queue