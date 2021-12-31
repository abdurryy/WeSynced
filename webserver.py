from flask import Flask, render_template, url_for, url_for, request, redirect
from flask_socketio import join_room, leave_room, SocketIO, emit
import random, json, os

app = Flask(__name__)
socketio = SocketIO(app)

syncgroups = {}
syncowners = {}

@app.route("/room/join/<code>")
def join(code):
    return render_template("room/room.html", room=code)

@app.route("/")
def index():
    return render_template("pages/index.html")


def random_username():
    r = random.randint(1, 5000)
    n = "Annonymous"+str(r)
    return n



@socketio.on("connect")
def connect():
    print("Connection established.")



@socketio.on("join")
def join(x):
    try:
        syncgroups[x["room"]]
        syncgroups[x["room"]].update({x["user"]})
    except:
        syncgroups[x["room"]] = {x["user"]}
        syncowners[x["room"]] = {x["user"]}

    print(f"{x['user']} is joining: ",x["room"])
    join_room(x["room"])
    print(f"{x['user']} has joined: ", x["room"])

    owner = ""
    for rx in syncowners[x["room"]]:
        owner = rx

    emit("client_connected", {"data": f"{x['user']} has connected", "owner": f"{owner}"}, room=x["room"])


@socketio.on("update_list")
def update(x):
    u = []
    d = []
    for sx in syncgroups[x["room"]]:
        try:
            xr = sx[0] + sx[1]
        except:
            xr = sx[0]
        
        d.append(sx.lower())

            
        xr = xr.upper()
        u.append(xr)

    
    emit("list_updated", {"list": u, "usernames": d }, room=x["room"])

@socketio.on('disconnects')
def disconnects(x):
    syncgroups[x["room"]].remove(x["user"])
    print(syncgroups)

    leave_room(x["room"])

    socketio.emit("removUser", {"user": x["user"]}, room=x["room"])

@socketio.on('paused')
def paused(x):
    emit("pause_request", {"user": x["user"]}, room=x["room"])

@socketio.on('played')
def played(x):
    emit("play_request", {"user": x["user"]}, room=x["room"])

@socketio.on('currentPlay')
def currentPlay(x):
    emit("clients_update", {"time": x["time"], "state": x["state"]}, room=x["room"])

@socketio.on("updateVideo")
def updateVideo(x): 
    emit("videoUpdated", {'url': x['url']} , room=x["room"])

    

    





socketio.run(app, debug=True, host="0.0.0.0", port=80)