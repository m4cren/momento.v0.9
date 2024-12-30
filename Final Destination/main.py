from momento import create_website, socketio

app = create_website()


if __name__ == "__main__":
 
     socketio.run(app, debug = True, host="0.0.0.0")
