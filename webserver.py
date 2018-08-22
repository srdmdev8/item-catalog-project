from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from database_setup import Base, Console, ConsoleGame
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Create session and connect to DB
engine = create_engine('sqlite:///consolegames.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/delete"):
                consoleID = self.path.split("/")[2]
                myConsoleQuery = session.query(Console).filter_by(
                    id=consoleID).one()
                if myConsoleQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output = "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?</h1>" % myConsoleQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action = '/consoles/%s/delete' >" % consoleID
                    output += "<input type = 'submit' value = 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)
            
            if self.path.endswith("/edit"):
                consoleID = self.path.split("/")[2]
                myConsoleQuery = session.query(Console).filter_by(
                    id=consoleID).one()
                if myConsoleQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myConsoleQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/consoles/%s/edit' >" % consoleID
                    output += "<input name = 'newConsoleName' type='text' placeholder = '%s' >" % myRestaurantQuery
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)
                    
            #Get console page and display all consoles. Also have options for
            #adding a new console and editing/deleting any existing ones
            if self.path.endswith("/consoles") or self.path.endswith("/consoles/"):
                consoles = session.query(Console).all()
                output = ""
                output += "<h1>Shawn's Console and Game Catalog</h1>"
                output += "<a href = '/consoles/new' > Add a New Console Here </a></br></br>"
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output += "<html><body>"
                for console in consoles:
                    output += console.name
                    output += "</br>"
                    output += "<a href = '/consoles/%s/games'>View Games</a>" % console.id
                    output += "</br>"
                    output += "<a href = '/consoles/%s/edit'>Edit</a>" % console.id
                    output += "</br>"
                    output += "<a href = '/consoles/%s/delete'>Delete</a>" % console.id
                    output += "</br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            #Get add new console page and allow user to add a new console
            if self.path.endswith("/consoles/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Add a New Console</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/consoles/new'>\
                            <input name="newConsoleName" type="text" placeholder='New Console Name'>\
                            <input type="submit" value="Add"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                    consoleID = self.path.split("/")[2]
                    myConsoleQuery = session.query(Console).filter_by(
                        id=consoleID).one()
                    if myConsoleQuery:
                        session.delete(myConsoleQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/consoles')
                        self.end_headers()
            
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newConsoleName')
                    consoleID = self.path.split("/")[2]
                    
                    myConsoleQuery = session.query(Console).filter_by(
                        id=consoleID).one()
                    if myConsoleQuery != []:
                        myConsoleQuery.name = messagecontent[0]
                        session.add(myConsoleQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/consoles')
                        self.end_headers()
                        
            if self.path.endswith("/consoles/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newConsoleName')
                    
                    # Create new Console Object
                    newConsole = Console(name=messagecontent[0])
                    session.add(newConsole)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/consoles')
                    self.end_headers()
            
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
