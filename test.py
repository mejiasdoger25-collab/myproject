from flask import Flask
app = Flask(__name__)    

@app.route('/')     #cuando ejecutamos esta ruta, se hace lo posterior, la funicón definida con helloworld
def hello_world():
    return 'test2'  #esto no devuelve una cadena de caracteres, devuelve una respuesta http

if __name__ == '__main__':
       app.run('0.0.0.0', debug=True)