import socketio
from json import dumps

sio = socketio.Server(cors_allowed_origins=["https://webdisplay.onrender.com"])
app = socketio.WSGIApp(sio)

offers = {}

@sio.event
def connect(sid, environ):
    print(f"Cliente {sid} conectado")
    sio.emit("offers", dumps(offers))

@sio.event
def disconnect(sid):
    remove_sid(sid)
    print(f"Cliente {sid} desconectado")
    sio.emit('offers', dumps(offers))

@sio.event
def message(sid, data):
    print(f"Mensagem recebida de {sid}: {data}")
    sio.send(sid, f"Mensagem recebida: {data}")

@sio.event
def removesid(sid,):
    remove_sid(sid)
    sio.emit("offers", dumps(offers))


@sio.event
def offer(sid, data):
    print(f"\033[31moffer received from {sid}!\033[m")
    if sid not in offers.keys():
        offers[sid] = data
        sio.emit('offers', dumps(offers))

@sio.event
def answer(sid, sidsender, data):
    print(f"\033[32manswer received from {sid} to {sidsender}!\033[m")
    print("Sended")
    sio.emit("answer", data, to=sidsender)

@sio.event
def iceCandidate(sid, data):
    sio.emit("iceCandidate", data)

def remove_sid(sid):
    global offers
    try:
        offers.pop(sid)
    except:
        pass

if __name__ == '__main__':
    import eventlet
    import socketio

    # Usamos o Eventlet para suportar o gerenciamento assíncrono do WebSocket
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8090)), app)
