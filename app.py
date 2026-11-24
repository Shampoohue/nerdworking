from flask import Flask, render_template, request, jsonify, session
from dbconn import *

app = Flask(__name__)
app.json.sort_keys = False
app.config.update(SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',)

#@app.route("/login", method=["POST", "GET"])
#def login(id):
#    pass

@app.route("/post/<int:id>")
def post(id):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    responded, responses = get_responses(id)
    post=get_post(id)
    return render_template("post.html", title=('NERDWORKING ー ' + post["titulo"]), user=user, loggedin=True, id=id, post=post, responded=responded, responses=responses, likes=get_likes(id))

@app.route("/noticia/<int:id>")
def noticia(id):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    noticia=get_noticia(id)
    return render_template("noticia.html", title=('NERDWORKING ー ' + noticia["titulo"]), user=user, loggedin=True, noticia=noticia, news=get_noticias())

@app.route("/userpage/<int:id>")
def userpage(id):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    profile=get_profile(id)
    return render_template("userpage.html", title=('NERDWORKING ー ' + profile["nombre"]), user=user, loggedin=True, profile=profile, posts=get_posts_by_user(id), news=get_noticias())

@app.route("/search/<search>")
def search(search):
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    return render_template("index.html", title="NERDWORKING", user=user, loggedin=True, posts=get_posts_search(search), news=get_noticias_search(search))

@app.route("/search/tags/<search>")
def search_tags(search):
    print(search)
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    return render_template("index.html", title="NERDWORKING", user=user, loggedin=True, posts=get_posts_search_tags(search), news=get_noticias_search_tags(search))

@app.route("/")
def index():
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    return render_template("index.html", title="NERDWORKING", user=user, loggedin=True, posts=get_posts(), news=get_noticias())

@app.route("/api/like")
def like():
    user, loggedin=get_user_login(session.get("matri", 0), session.get("password", ""))
    responded, responses = get_responses(id)
    post=get_post(id)
    return render_template("post.html", title=('NERDWORKING ー ' + post["titulo"]), user=user, loggedin=True, id=id, post=post, responded=responded, responses=responses, likes=get_likes(id))

@app.route("/api/unlike")
def unlike():
    pass

if __name__ == "__main__":
    app.run(debug=True)