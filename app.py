from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dbconn import *

app = Flask(__name__)
app.json.sort_keys = False
app.secret_key = "ASANDIAJKDAJSDJKANSDKJNAJSFNKKASNDJNASKDJASNDKJANJSNDAKDJJAKNDKJASDKJSJAKDJKASKJANSJKDNSJ"
app.config.update(SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

CARRERAS = ('Arquitectura', 'Ing. Agrónomo', 'Ing. Biomédica', 'Ing. Civil', 'Ing. en Ciencias Ambientales', 'Ing. en Energías Renovables', 'Ing. en Materiales', 'Ing. en Semiconductores', 'Ing. en Sistemas de Información', 'Ing. en Tecnología Electrónica', 'Ing. Industrial y de Sistemas', 'Ing. Mecatrónica', 'Ing. Metalúrgica', 'Ing. Minero', 'Ing. Químico', 'Lic. de Químico en Alimentos', 'Lic. en Administración', 'Lic. en Administración Pública', 'Lic. en Antropología', 'Lic. en Artes Escénicas', 'Lic. en Artes Plásticas', 'Lic. en Biología', 'Lic. en Ciencias de la Computación', 'Lic. en Ciencias de la Comunicación', 'Lic. en Ciencias Genómicas', 'Lic. en Ciencias Nutricionales', 'Lic. en Contaduría Pública', 'Lic. en Cultura Física y Deporte', 'Lic. en Derecho', 'Lic. en Diseño Gráfico', 'Lic. en Economía', 'Lic. en Educación', 'Lic. en Enfermería', 'Lic. en Enseñanza del Inglés', 'Lic. en Finanzas', 'Lic. en Física', 'Lic. en Física Médica', 'Lic. en Fisioterapia', 'Lic. en Geología', 'Lic. en Historia', 'Lic. en Lingüística', 'Lic. en Literaturas Hispánicas', 'Lic. en Logística', 'Lic. en Matemáticas', 'Lic. en Mercadotecnia', 'Lic. en Música', 'Lic. en Negocios y Comercio Internacionales', 'Lic. en Odontología', 'Lic. en Psicología', 'Lic. en Química', 'Lic. en Seguridad Pública', 'Lic. en Sociología', 'Lic. en Sustentabilidad', 'Lic. en Trabajo Social', 'Lic. en Turismo', 'Medicina', 'Médico Veterinario Zootecnista', 'Químico Biólogo Clínico')

@app.route("/api/login", methods=['POST'])
def apilogin():
    matri, password = request.form.get('matricula', 0), request.form.get('password', 0)
    user, loggedin=get_user_login(matri, password)
    if loggedin:
        session["matri"] = user["matricula"]
        session["password"] = user["psswrd"]
        return {"loggedin": "logged in"}
    return {"loggedin": "not logged in"}

@app.route("/api/signin", methods=['POST'])
def apisignin():
    newuser = {
        "matricula": request.form.get('matricula', 0).strip(),
        "nombre": request.form.get('nombre', 0).strip(),
        "apepaterno": request.form.get('apepaterno', 0).strip(),
        "apematerno": request.form.get('apematerno', 0).strip(),
        "carrera": request.form.get('carrera', 0).strip(),
        "semestre": request.form.get('semestre', 0).strip(),
        "password": request.form.get('password', 0).strip(),
        "passwordconfirm": request.form.get('passwordconfirm', 0).strip()
        }
    if newuser["password"] == newuser["passwordconfirm"] and newuser["carrera"] in CARRERAS:
        userdata = (int(newuser["matricula"]), newuser["nombre"], newuser["apepaterno"], newuser["apematerno"], newuser["carrera"], int(newuser["semestre"]), newuser["password"])
        make_user(userdata)
        user, loggedin=get_user_login(int(newuser["matricula"]), newuser["password"])
        if loggedin:
            session["matri"] = user["matricula"]
            session["password"] = user["psswrd"]
            return {"signin":"signed + logged in"}
        return {"signin":"signed in"}
    return {"signin":"ERROR: cuenta no se pudo crear"}

@app.route("/logout")
def logout():
    session["matri"] = 0
    session["password"] = ""
    return redirect(url_for("index"))

@app.route('/api/posts/new', methods=['POST'])
def create_post():
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    if loggedin:
        title = request.form.get('titulo', '').strip()
        if not title:
            return jsonify(error='Las publicaciones requieren un titulo'), 400
        body = request.form.get('body', '').strip()
        tags = request.form.getlist('tags')
        image = request.files.get('image')

        newid = add_post(user["matricula"], title, body, tags, image)

        return {"newpost":newid}
    else:
        return jsonify(error='No tiene un usuario.'), 400

@app.route('/api/posts/edit', methods=['POST'])
def editing_post():
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    if loggedin and int(user["matricula"]) == int(request.form.get('creador', 0)):
        id = request.form.get('id', 0)
        title = request.form.get('titulo', '').strip()
        if not title:
            return jsonify(error='Las publicaciones requieren un titulo'), 400
        body = request.form.get('body', '').strip()
        tags = request.form.getlist('tags')
        image = request.form.get('image')
        if image != "keepimage":
            image = request.files.get('image')

        newid = update_post(id, title, body, tags, image)

        return {"newpost":newid}
    else:
        return jsonify(error='No tiene un usuario.'), 400

@app.route('/api/posts/delete', methods=['POST'])
def delete_post():
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    if loggedin and int(user["matricula"]) == int(request.form.get('creador', 0)):
        id = request.form.get('id', 0)

        remove_everyman(id)

        return {"deletedpost":"it was deleted"}
    else:
        return jsonify(error='No tiene un usuario.'), 400

@app.route('/api/reply/new/<int:id>', methods=['POST'])
def create_reply(id):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    if loggedin:
        body = request.form.get('body', '').strip()
        image = request.files.get('image')
        newid = add_reply(user["matricula"], body, image)
        add_reply_link(id, newid)
        return {"newreply":"success!"}
    else:
        return jsonify(error='No tiene un usuario.'), 400

@app.route('/api/user/edit', methods=['POST'])
def editing_profile():
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    if loggedin:
        title = request.form.get('titulo', '').strip()
        semester = int(request.form.get('semestre', '').strip())
        career = request.form.get('carrera', '').strip()
        if not semester:
            return jsonify(error='Es imposible ser un estudiante sin un semestre.'), 400
        if not career or not career in CARRERAS:
            return jsonify(error='Carrera no disponible.'), 400
        body = request.form.get('body', '').strip()
        tags = request.form.getlist('tags')
        image = request.form.get('image')
        if image != "keepimage":
            image = request.files.get('image')

        update_profile(user["matricula"], title, body, tags, image)
        update_user(user["matricula"], career, semester)

        return {"update":"perfil actualizado!"}
    else:
        return jsonify(error='No tiene un usuario.'), 400

@app.route("/api/like/<int:user>/<int:post>")
def like(user, post):
    user2, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    if loggedin and user == user2["matricula"]:
        like_post(user, post)
        make_notif(user, post, "A " + user2["nombres"] + " " + user2["apepaterno"] + " " + user2["apematerno"] + " le intereso tu proyecto!")
    return {"like":"te interesa!"}

@app.route("/api/unlike/<int:user>/<int:post>")
def unlike(user, post):
    print("unliking now")
    user2, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    if loggedin and user == user2["matricula"]:
        unlike_post(user, post)
    return {"unlike":"no te interesa..."}

@app.route("/signin")
def signin():
    return render_template("signin.html", title="NERDWORKING ー registrarse", carreras=CARRERAS)

@app.route("/login")
def login():
    return render_template("login.html", title="NERDWORKING ー iniciar sesión", gobackto=request.values["next"])

@app.route('/post/new')
def make_post():
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    if loggedin:
        return render_template("makepost.html", title="NERDWORKING ー publicar", user=user, post={}, edited=False)
    return redirect(url_for("index"))

@app.route('/post/edit/<int:id>')
def edit_post(id):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    if loggedin:
        post = get_post(id, user["matricula"], user["adminuser"])
        if post:
            return render_template("makepost.html", title=("NERDWORKING ー editar '" + post["titulo"] + "'"), user=user, post=post, edited=True)
    return redirect(url_for("index"))

@app.route('/reply/new/<int:id>')
def make_reply(id):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    if loggedin:
        post=get_post(id, user["matricula"], user["adminuser"])
        return render_template("makecomment.html", title=("NERDWORKING ー responder a '" + post["titulo"] + "'"), user=user, post=post)
    return redirect(url_for("index"))

@app.route("/post/<int:id>")
def post(id):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    responded, responses = get_responses(id)
    post=get_post(id, user["matricula"], user["adminuser"])
    if post is None:
        return redirect(url_for("index"))
    return render_template("post.html", title=('NERDWORKING ー ' + post["titulo"]), notifs=get_notif_count(user["matricula"]), user=user, loggedin=loggedin, id=id, post=post, responded=responded, responses=responses, likes=get_likes(id))

@app.route("/noticia/<int:id>")
def noticia(id):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    noticia=get_noticia(id)
    if noticia is None:
        return redirect(url_for("index"))
    return render_template("noticia.html", title=('NERDWORKING ー ' + noticia["titulo"]), notifs=get_notif_count(user["matricula"]), user=user, loggedin=loggedin, noticia=noticia, news=get_noticias())

@app.route("/userpage/<int:id>")
def userpage(id):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    profile=get_profile(id)
    if profile is None:
        return redirect(url_for("index"))
    return render_template("userpage.html", title=('NERDWORKING ー ' + profile["nombre"]), notifs=get_notif_count(user["matricula"]), user=user, loggedin=loggedin, profile=profile, posts=get_posts_by_user(id, user["matricula"], user["adminuser"]), news=get_noticias())

@app.route("/search/<search>")
def search(search):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    return render_template("index.html", title=("NERDWORKING ー buscando: " + search), notifs=get_notif_count(user["matricula"]), user=user, loggedin=loggedin, posts=get_posts_search(search, user["matricula"], user["adminuser"]), news=get_noticias_search(search))

@app.route("/search/tags/<search>")
def search_tags(search):
    print(search)
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    return render_template("index.html", title="NERDWORKING ー buscando categorias: " + search, notifs=get_notif_count(user["matricula"]), user=user, loggedin=loggedin, posts=get_posts_search_tags(search, user["matricula"], user["adminuser"]), news=get_noticias_search_tags(search))

@app.route("/notif")
def notif():
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    if loggedin:
        return render_template("notif.html", title="NERDWORKING ー notificaciones", user=user, loggedin=loggedin, notif=get_notif(user["matricula"]), notifs=get_notif_count(user["matricula"]))
    else:
        return redirect(url_for("index"))

@app.route("/notif/<int:id>")
def go_to_notif(id):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    notif = notif_check(id, loggedin, user)
    if notif == "index":
        return redirect(url_for(notif))
    return redirect(url_for(notif, id=id))

@app.route("/userconfig")
def userconfig():
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    if loggedin:
        return render_template("userconfig.html", title=("NERDWORKING ー Configuración de usuario"), loggedin=loggedin, user=user, profile=get_profile(user["matricula"]), notifs=get_notif_count(user["matricula"]), carreras=CARRERAS)

@app.route("/")
def index():
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    return render_template("index.html", title="NERDWORKING", notifs=get_notif_count(user["matricula"]), user=user, loggedin=loggedin, posts=get_posts(user["matricula"], user["adminuser"]), news=get_noticias())

if __name__ == "__main__":
    app.run(debug=True)