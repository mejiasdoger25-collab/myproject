from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
#importante importar todas las clases para que funcione al hacerles la "llamada"

class SignupForm(FlaskForm):    #creamos una clase pues los campos del formulario serán las variables de esta clase || Esta clase hereda de FlaskForm
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])   #estas variables son los campos del formulario
    password = PasswordField('Password', validators=[DataRequired()])   #para ver todos los tipos de campos, se pueden ver todos en el módulo wtforms
    email = StringField('Email', validators=[DataRequired(), Email()])  #podemos ver que las variables, en primer lugar le pasamos el name con el que el user las va a ver, después le pasamos validadores, como de longitud, obligatoriedad, etc, etc
    submit = SubmitField('Registrar')


#creamos la clase PostForm, que hereda de FlaskForm y rellenamos las variables como en la clase anterior
class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    title_slug = StringField('Título slug', validators=[Length(max=128)])
    content = TextAreaField('Contenido')
    submit = SubmitField('Enviar')