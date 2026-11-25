from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dbconn import *

app = Flask(__name__)
app.json.sort_keys = False
app.secret_key = "ASANDIAJKDAJSDJKANSDKJNAJSFNKKASNDJNASKDJASNDKJANJSNDAKDJJAKNDKJASDKJSJAKDJKASKJANSJKDNSJ"
app.config.update(SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

@app.route("/login")
def login():
    return render_template("login.html", gobackto=request.values["next"])

@app.route("/api/login", methods=['POST'])
def apilogin():
    matri, password = request.form.get('matricula', 0), request.form.get('password', 0)
    user, loggedin=get_user_login(matri, password)
    print(user)
    if loggedin:
        print("logged in")
        session["matri"] = user["matricula"]
        session["password"] = user["psswrd"]
        print("session get: ", session.get(matri))
        return {"loggedin": "logged in"}
    return {"loggedin": "not logged in"}

@app.route("/api/logout")
def logout():
    session["matri"] = 0
    session["password"] = ""
    return redirect(url_for("index"))

@app.route('/post/new')
def make_post():
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    if loggedin:
        return render_template("makepost.html", user=user)
    else:
        return redirect(url_for("index"))

@app.route('/reply/new/<int:id>')
def make_reply(id):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    if loggedin:
        post=get_post(id, user["matricula"], user["adminuser"])
        return render_template("makecomment.html", user=user, post=post)
    else:
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

@app.route("/post/<int:id>")
def post(id):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    responded, responses = get_responses(id)
    post=get_post(id, user["matricula"], user["adminuser"])
    if post is None:
        return redirect(url_for("index"))
    return render_template("post.html", title=('NERDWORKING ー ' + post["titulo"]), user=user, loggedin=loggedin, id=id, post=post, responded=responded, responses=responses, likes=get_likes(id))

@app.route("/noticia/<int:id>")
def noticia(id):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    noticia=get_noticia(id)
    if noticia is None:
        return redirect(url_for("index"))
    return render_template("noticia.html", title=('NERDWORKING ー ' + noticia["titulo"]), user=user, loggedin=loggedin, noticia=noticia, news=get_noticias())

@app.route("/userpage/<int:id>")
def userpage(id):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    profile=get_profile(id)
    if profile is None:
        return redirect(url_for("index"))
    return render_template("userpage.html", title=('NERDWORKING ー ' + profile["nombre"]), user=user, loggedin=loggedin, profile=profile, posts=get_posts_by_user(id, user["matricula"], user["adminuser"]), news=get_noticias())

@app.route("/search/<search>")
def search(search):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    return render_template("index.html", title="NERDWORKING", user=user, loggedin=loggedin, posts=get_posts_search(search, user["matricula"], user["adminuser"]), news=get_noticias_search(search))

@app.route("/search/tags/<search>")
def search_tags(search):
    print(search)
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    return render_template("index.html", title="NERDWORKING", user=user, loggedin=loggedin, posts=get_posts_search_tags(search, user["matricula"], user["adminuser"]), news=get_noticias_search_tags(search))

@app.route("/")
def index():
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    return render_template("index.html", title="NERDWORKING", user=user, loggedin=loggedin, posts=get_posts(user["matricula"], user["adminuser"]), news=get_noticias())

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

if __name__ == "__main__":
    app.run(debug=True)