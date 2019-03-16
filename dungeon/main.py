import connexion
import rooms
import cherrypy


app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

if __name__ == "__main__":
    rooms.init_room()
    cherrypy.tree.graft(app, "/")
    cherrypy.server.unsubscribe()
    server = cherrypy._cpserver.Server()
    server.socket_host = "0.0.0.0"
    server.socket_port = 5000
    server.thread_pool = 1
    server.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()
