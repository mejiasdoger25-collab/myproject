from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
app = Flask(__name__)   #name, palabra reservada para que flask sepa donde encointrar las plantilla en nuestra app


posts = [4, 4, 4, 4, 4, 4, 4]

@app.route("/")
def index():
    page = request.args.get('page', 1)  #recopilamos los datos del user para paginar el listado, en este ej, estamos pidiendo la 1ªpg y los 10 primeros posts
    list = request.args.get('list', 20) #todo esto se hace mediante el uso del atb args del objeto request, como se puede ver en esta line  (IMPORTAR OBJT REQUEST DE FLASK, LINE 3)
    return render_template("index.html", num_posts=len(posts))


@app.route("/p/<string:slug>/")
def show_post(slug):
    return render_template("post_view.html", slug_title=slug)


@app.route("/admin/post/")
@app.route("/admin/post/<int:post_id>/")
def post_form(post_id=None):
    return render_template("admin/post_form.html", post_id=post_id)


#nueva vista añadida para mostrar el formulario, como se puede ver en la dirección de la ruta
@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if request.method == 'POST':    #aquí se accede al atb method del objeto request, para "filtrar" si el user ha usado post o get, en este caso post
        name = request.form['name'] #usando el diccionario form del objeto request, vamos rellenando los campos (atbs) [que son los indicados en el formulario.html, es decri, signup_form.html]
        email = request.form['email']
        password = request.form['password']
        next = request.args.get('next', None)
        if next:    #aquí comprobamos si se pasó por la URL el parámetro next, que se usará para redirigir al user a la pg que se indica, si no se especifica, se envía a la ppal mismamente
            return redirect(next)
        return redirect(url_for('index'))   #este último return se ejecutará en caso de que ninguno de los anteriores lo hagan, de forma que se le enviará al user a la página que muestra el registro, en este caso es index, como se puede ver en los paréntesis
    return render_template("signup_form.html")  #NO es necesario, se hace por buena práctica en caso de que el user recargue la pg o le de hacia atrás(puesto que este return se dará si no se cumple nada de la condición if anterior al mismo)


#DUDA--> ¿Y si el user pone un email que no existe? ¿Y si no introduce su name? -->SOL: usando la extensión WTForms se puede validar todo esto, sin necesidad
#de "ensuciar" el método/vista de la ruta signup