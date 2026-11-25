import sqlite3
import datetime
from werkzeug.utils import secure_filename
import os, uuid

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    conn = sqlite3.connect("nerdworking.db")
    conn.row_factory = sqlite3.Row
    return conn

def monthconversion(mes):
    m = ""
    match mes:
        case 1:
            m = "ene"
        case 2:
            m = "feb"
        case 3:
            m = "mar"
        case 4:
            m = "abr"
        case 5:
            m = "may"
        case 6:
            m = "jun"
        case 7:
            m = "jul"
        case 8:
            m = "ago"
        case 9:
            m = "sep"
        case 10:
            m = "oct"
        case 11:
            m = "nov"
        case 12:
            m = "dic"
        case _:
            m = "???"
    return m

def maketimestr(dttiempo):
    timecom = datetime.datetime.now() - dttiempo
    tiempo = "Hace "
    if timecom.days > 15:
        tiempo = str(dttiempo.day) + "/" + monthconversion(dttiempo.month) + "/" + str(dttiempo.year)
    elif timecom.days > 1:
        tiempo += str(timecom.days) + " dias" 
    elif timecom.days == 1:
        tiempo += str(timecom.days) + " dia"
    elif timecom.seconds >= 7200:
        tiempo += str(int(timecom.seconds / 3600)) + " horas"
    elif timecom.seconds >= 3600:
        tiempo += str(int(timecom.seconds / 3600)) + " hora"
    elif timecom.seconds >= 120:
        tiempo += str(int(timecom.seconds / 60)) + " minutos"
    elif timecom.seconds >= 60:
        tiempo += str(int(timecom.seconds / 60)) + " minutos"
    elif timecom.seconds == 1:
        tiempo += str(timecom.seconds) + " segundo"
    else:
        tiempo += str(timecom.seconds) + " segundos"
    return tiempo


def get_everyman(instruct, categories, cutbody, hastime, hastags, likeid=0):
    conn = get_db() 
    cursor = conn.cursor()
    cursor.execute(instruct)
    datos = cursor.fetchall()
    if not datos:
        return []

    posts = []
    for fila in datos:
        everyman = {}
        i = 0
        for category in categories:
            everyman[category] = fila[i]
            if category == "body" and cutbody:
                everyman[category] = fila[i][0:170] + "..."
            i+=1

        if hastags:
            tagcursor = conn.cursor()
            taginstruct = "SELECT term FROM tags WHERE tsuku = ?;"
            tagcursor.execute(taginstruct, (fila[0],))
            tagdatos = tagcursor.fetchall()
            tags = []
            if tagdatos:
                for tag in tagdatos:
                    tags.append(tag[0])
            everyman["tags"] = tags
            tagcursor.close()

        if hastime:
            timecursor = conn.cursor()
            timeinstruct = "SELECT año, mes, dia, hora, min, seg FROM tiempo WHERE everyman = ?;"
            timecursor.execute(timeinstruct, (fila[0],))
            timedatos = timecursor.fetchone()
            dttiempo = datetime.datetime(timedatos[0], timedatos[1], timedatos[2], timedatos[3], timedatos[4], timedatos[5])
            everyman["tiempo"] = maketimestr(dttiempo)
            timecursor.close()

        if likeid > 0:
            likecursor = conn.cursor()
            likeinstruct = "SELECT interesado FROM interes WHERE user=? AND post=?;"
            likecursor.execute(likeinstruct, (likeid, fila[0],))
            likedatos = likecursor.fetchone()
            if likedatos is None:
                everyman["interes"] = 0
            else:
                everyman["interes"] = likedatos[0]
            timecursor.close()
        
        posts.append(everyman)
    cursor.close()
    conn.close()
    return posts

def get_posts(userid, admin):
    return get_everyman("""
        SELECT p.id, p.titulo, p.body, p.creator, p.imgfile, CONCAT(u.nombres, ' ', u.apepaterno, ' ', u.apematerno), u.carrera, img.imgfile, p.aceptable
        FROM everyman p
        LEFT JOIN usuario u ON u.matricula = p.creator
        JOIN tiempo t ON t.everyman = p.id
        JOIN everyman img ON img.creator = p.creator
        WHERE (p.aceptable = 1 OR 1 = """+ str(admin) +""" OR p.creator = """ + str(userid) +""") AND p.tipo = 'Post' AND img.tipo = 'Perfil'
        ORDER BY t.año DESC, t.mes DESC, t.dia DESC, t.hora DESC, t.min DESC, t.seg DESC;
    """, ["id", "titulo", "body", "creador", "imagen", "nombre", "carrera", "iconfile"], True, True, True, userid)

def get_posts_search(search, userid, admin):
    return get_everyman("""
        SELECT p.id, p.titulo, p.body, p.creator, p.imgfile, CONCAT(u.nombres, ' ', u.apepaterno, ' ', u.apematerno), u.carrera, img.imgfile
        FROM everyman p
        LEFT JOIN usuario u ON u.matricula = p.creator
        JOIN tiempo t ON t.everyman = p.id
        JOIN everyman img ON img.creator = p.creator
        WHERE (p.aceptable = 1 OR 1 = """+ str(admin) +""" OR p.creator = """ + str(userid) +""") AND p.tipo = 'Post' AND img.tipo = 'Perfil' AND (p.titulo LIKE '%""" + search + """%' OR p.body LIKE '%""" + search + """%')
        ORDER BY t.año DESC, t.mes DESC, t.dia DESC, t.hora DESC, t.min DESC, t.seg DESC;
    """, ["id", "titulo", "body", "creador", "imagen", "nombre", "carrera", "iconfile"], True, True, True, userid)

def get_posts_search_tags(search, userid, admin):
    return search_tags(get_posts(userid, admin), search)

def get_post(id, userid, admin):
    return get_everyman("""
        SELECT p.id, p.titulo, p.body, p.creator, p.imgfile, CONCAT(u.nombres, ' ', u.apepaterno, ' ', u.apematerno), u.carrera, img.imgfile
        FROM everyman p
        LEFT JOIN usuario u ON u.matricula = p.creator
        JOIN everyman img ON img.creator = p.creator
        WHERE (p.aceptable = 1 OR 1 = """+ str(admin) +""" OR p.creator = """ + str(userid) +""") AND img.tipo = 'Perfil' AND p.tipo = 'Post' AND p.id = """ + str(id) + """;
    """, ["id", "titulo", "body", "creador", "imagen", "nombre", "carrera", "iconfile"], False, True, True, userid)[0]

def get_responses(id):
    responses = get_everyman("""
        SELECT p.id, p.titulo, p.body, p.creator, p.imgfile, CONCAT(u.nombres, ' ', u.apepaterno, ' ', u.apematerno), u.carrera, img.imgfile
        FROM everyman p
        LEFT JOIN usuario u ON u.matricula = p.creator
        JOIN tiempo t ON t.everyman = p.id
        JOIN respuesta r ON r.response = p.id
        JOIN everyman img ON img.creator = p.creator
        WHERE p.tipo = 'Respuesta' AND img.tipo = 'Perfil' AND r.responded = """ + str(id) + """;
    """, ["id", "titulo", "body", "creador", "imagen", "nombre", "carrera", "iconfile"], False, True, False)
    return not not responses, responses

def get_likes(id):
    conn = get_db() 
    cursor = conn.cursor()
    cursor.execute("SELECT u.matricula AS matricula, CONCAT(u.nombres, ' ', u.apepaterno, ' ', u.apematerno) AS nombre FROM interes i JOIN usuario u ON u.matricula = i.user WHERE interesado = 1 AND post = " + str(id) + ";")
    fetchall = cursor.fetchall()
    cursor.close()
    conn.close()
    return fetchall

def get_noticias():
    return get_everyman("""
        SELECT n.id, n.titulo, n.body, n.imgfile
        FROM everyman n
        JOIN tiempo t ON t.everyman = n.id
        WHERE n.tipo = 'Anuncio'
        ORDER BY t.año DESC, t.mes DESC, t.dia DESC, t.hora DESC, t.min DESC, t.seg DESC;
    """, ["id", "titulo", "body", "imagen"], True, True, True)

def get_noticias_search(search):
    return get_everyman("""
        SELECT n.id, n.titulo, n.body, n.imgfile
        FROM everyman n
        JOIN tiempo t ON t.everyman = n.id
        WHERE n.tipo = 'Anuncio' AND (n.titulo LIKE '%""" + search + """%' OR n.body LIKE '%""" + search + """%')
        ORDER BY t.año DESC, t.mes DESC, t.dia DESC, t.hora DESC, t.min DESC, t.seg DESC;
    """, ["id", "titulo", "body", "imagen"], True, True, True)

def get_noticias_search_tags(search):
    return search_tags(get_noticias(), search)

def search_tags(searched, search):
    hastags = []
    for s in searched:
        for t in s["tags"]:
            if t.lower() == search.strip().lower():
                hastags.append(s)
    return hastags

def get_noticia(id):
    return get_everyman("""
        SELECT id, titulo, body, imgfile
        FROM everyman
        WHERE tipo = 'Anuncio' AND id=""" + str(id) + ";", ["id", "titulo", "body", "imagen"], False, True, True)[0]

def get_profile(id):
    return get_everyman("""
        SELECT p.id, p.titulo, p.body, p.creator, p.imgfile, CONCAT(u.nombres, ' ', u.apepaterno, ' ', u.apematerno), u.carrera, u.semestre
        FROM everyman p
        LEFT JOIN usuario u ON u.matricula = p.creator
        WHERE p.aceptable = 1 AND p.tipo = 'Perfil' AND p.creator = """ + str(id) + """;
    """, ["id", "titulo", "body", "creador", "imagen", "nombre", "carrera", "semestre"], False, False, True)[0]

def get_posts_by_user(id, userid, admin):
    return get_everyman("""
        SELECT p.id, p.titulo, p.body, p.creator, p.imgfile, CONCAT(u.nombres, ' ', u.apepaterno, ' ', u.apematerno), u.carrera, img.imgfile
        FROM everyman p
        LEFT JOIN usuario u ON u.matricula = p.creator
        JOIN tiempo t ON t.everyman = p.id
        JOIN everyman img ON img.creator = p.creator
        WHERE (p.aceptable = 1 OR 1 = """+ str(admin) +""" OR p.creator = """ + str(userid) +""") AND p.tipo = 'Post' AND img.tipo = 'Perfil' AND p.creator = """ + str(id) + """
        ORDER BY t.año DESC, t.mes DESC, t.dia DESC, t.hora DESC, t.min DESC, t.seg DESC;
    """, ["id", "titulo", "body", "creador", "imagen", "nombre", "carrera", "iconfile"], True, True, True, userid)

def add_edit_everyman(instruct, textinput, tags, image, edited):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(instruct, textinput)
    conn.commit()
    newid = 0
    if edited:
        newid = textinput[-1]
    else:
        newid = cursor.lastrowid
    tags2 = []

    saved_image = None
    if image and image.filename:
        ext = os.path.splitext(image.filename)[1].lower()
        if ext in {'.jpg', '.jpeg', '.png', '.gif', '.webp'}:
            unique_name = f"{uuid.uuid4().hex}{ext}"
            image.save(os.path.join(UPLOAD_FOLDER, unique_name))
            saved_image = {
                'stored_as': unique_name,
                'original_name': secure_filename(image.filename)[:100],
                'url': f'uploads/{unique_name}',
            }
            cursor.execute("UPDATE everyman SET imgfile = ? WHERE id = ?", (saved_image["url"], newid))
            conn.commit()

    for tag in tags:
        tags2.append((newid, tag))
    if tags:
        if edited:
            cursor.execute("DELETE FROM tags WHERE tsuku = ?", (newid,))
        cursor.executemany("INSERT INTO tags (tsuku, term) VALUES (?, ?)", tags2)
        conn.commit()
    if edited:
        cursor.execute("UPDATE everyman SET edited = 1 WHERE id = " + newid + ";")
        conn.commit()
    else:
        now = datetime.datetime.now()
        cursor.execute("INSERT INTO tiempo (año, mes, dia, hora, min, seg, everyman) VALUES (?, ?, ?, ?, ?, ?, ?)", (now.year, now.month, now.day, now.hour, now.minute, now.second, newid,))
        conn.commit()
    cursor.close()
    conn.close()
    return newid

def add_post(creator, title, body, tags, image):
    instruct = "INSERT INTO everyman (tipo, titulo, body, creator) VALUES ('Post', ?, ?, ?)"
    values = (title, body, creator)
    
    return add_edit_everyman(instruct, values, tags, image, False)

def add_reply(creator, body, image):
    instruct = "INSERT INTO everyman (tipo, titulo, body, creator) VALUES ('Respuesta', '', ?, ?)"
    values = (body, creator)
    
    return add_edit_everyman(instruct, values, [], image, False)

def add_reply_link(responded, response):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO respuesta (responded, response) VALUES (?, ?)", (responded, response,))
    conn.commit()
    cursor.close()
    conn.close()

def make_profile(tipo, titulo, body, creador, imgfile, tags):
    instruct = """
        INSERT INTO everyman (tipo, titulo, body, creador, imgfile) VALUES (?, ?, ?, ?, ?) 
    """
    words = (tipo, titulo, body, creador, imgfile)
    return add_edit_everyman(instruct, words, tags, False)

def get_user_login(matri, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario WHERE matricula=?", (matri,))
    usu = {"matricula":0, "nombres":"", "apepaterno":"", "apematerno":"", "semestre":0, "carrera":"", "correo":"", "psswrd":"", "adminuser": 0}
    loggedin = False
    fetchone = cursor.fetchone()
    if not fetchone is None:
        i = 0
        a = ["matricula", "nombres", "apepaterno", "apematerno", "semestre", "carrera", "correo", "psswrd", "adminuser"]
        usu = {}
        for f in fetchone:
            usu[a[i]] = f
            i+=1
        if usu["psswrd"] == password:
            loggedin = True
    cursor.close()
    conn.close()
    return usu, loggedin

def like_post(user, post):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO interes (post, user) VALUES (?, ?)", (post, user,))
    conn.commit()
    cursor.close()
    conn.close()

def unlike_post(user, post):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM interes WHERE post=? AND user=?", (post, user,))
    conn.commit()
    cursor.close()
    conn.close()

def make_notif(user, post, text):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO interes (post, user, descr) VALUES (?, ?, ?)", (post, user, text))
    conn.commit()
    cursor.close()
    conn.close()