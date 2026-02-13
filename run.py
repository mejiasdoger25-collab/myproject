from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
app = Flask(__name__)   #name, palabra reservada para que flask sepa donde encointrar las plantilla en nuestra app
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'   #añadido para el fichero signup_forms.html y para el forms.py, generamos el token para los ataques CSFR(falsificación de solicitudes)

posts = [4, 4, 4, 4, 4, 4, 4]

@app.route("/")
def index():
    page = request.args.get('page', 1)  #recopilamos los datos del user para paginar el listado, en este ej, estamos pidiendo la 1ªpg y los 10 primeros posts
    list = request.args.get('list', 20) #todo esto se hace mediante el uso del atb args del objeto request, como se puede ver en esta line  (IMPORTAR OBJT REQUEST DE FLASK, LINE 3)
    return render_template("index.html", posts = posts)


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



#ACTUALIZACIÓN DE LA ÚLTIMA VISTA, la del método get de ruta /signup/
from forms import SignupForm

@app.route("/signup/V2/", methods=["GET", "POST"])
def show_signup_form():
    form = SignupForm()     #esta es la diff, hacemos instancia de un objt de clase SignupForm(), al hacerlo pueden ocurrir 2 cosas en función de si la petición es GET o POST. Si el user simplemente acdcede a la pg que muestra el formulario de registro, se crea un objt con los campos vacíos.  
    if form.validate_on_submit():       #+(cont) || Por el contario, si el user ha hecho petición POST, se crea un objt con los campos inicializados (el valor de estos campos es el que se envía al cuerpo de la petición [que están en request.html])
        name = form.name.data   #ref: línea de arriba:: una vez isntaciado el formulario, se llama al method validate_on_submit para que compruebe por nosotros que se ha enviado el formulario y que los campos son válidos
        email = form.email.data
        password = form.password.data

        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('index'))
    return render_template("signup_form.html", form=form)


#ACTUALIZACIÓN DE LA VISTA CON RUTA /ADMIN/POST/
from forms import SignupForm, PostForm

@app.route("/admin/post/V2/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        title_slug = form.title_slug.data
        content = form.content.data

        post = {'title': title, 'title_slug': title_slug, 'content': content}   #en caso de que no haya error, aprovechamos para crear 
        posts.append(post)  #y guardar un post en esta variable, en la varialbe posts

        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)