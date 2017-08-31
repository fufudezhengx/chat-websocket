from flask import session
from flask_socketio import (
    emit,
    join_room,
    leave_room,
    SocketIO
)

socketio = SocketIO()

"""
socketio 是对 websocket 的封装
在 socketio 中, 客户端连接的时候可以指定一个 namespace (我们这个例子中是 /chat)
如果不指定, 就是默认的 namespace (也就是 /)

有相同的 namespace 才能互相广播发送数据

除了 namespace 还有 room 的概念
用 join_room 来加入一个 room
用 leave_room 来退出一个 room

emit 发送数据可以让相同的 room 里面的连接收到信息
"""


@socketio.on('join', namespace='/chat')
def join(data):
    print('join', data)
    room = data['room']
    join_room(room)
    session['room'] = room
    name = session.get('name')
    message = '用户:({}) 进入了房间'.format(name)
    d = dict(
        message=message,
    )
    emit('status', d, room=room)


@socketio.on('send', namespace='/chat')
def send(data):
    room = session.get('room')
    name = session.get('name')
    message = data.get('message')
    formatted = '{} : {}'.format(name, message)
    print('send', formatted)
    d = dict(
        message=formatted
    )
    emit('message', d, room=room)


@socketio.on('leave', namespace='/chat')
def leave(data):
    room = session.get('room')
    leave_room(room)
    name = session.get('name')
    d = dict(
        message='{} 离开了房间'.format(name),
    )
    emit('status', d, room=room)
