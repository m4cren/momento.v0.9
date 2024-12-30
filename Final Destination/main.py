from momento import create_website, socketio

app = create_website()


if __name__ == "__main__":
 
     socketio.run(app, debug = True, host="192.168.1.23")