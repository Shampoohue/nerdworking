import sqlite3
import datetime
import os

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


def get_everyman(instruct, categories, cutbody, hastime, hastags):
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
        
        posts.append(everyman)
    cursor.close()
    conn.close()
    return posts

def get_posts():
    return get_everyman("""
        SELECT p.id, p.titulo, p.body, p.creator, p.imgfile, CONCAT(u.nombres, ' ', u.apepaterno, ' ', u.apematerno), u.carrera, img.imgfile
        FROM everyman p
        LEFT JOIN usuario u ON u.matricula = p.creator
        JOIN tiempo t ON t.everyman = p.id
        JOIN everyman img ON img.creator = p.creator
        WHERE p.aceptable = 1 AND p.tipo = 'Post' AND img.tipo = 'Perfil'
        ORDER BY t.año DESC, t.mes DESC, t.dia DESC, t.hora DESC, t.min DESC, t.seg DESC;
    """, ["id", "titulo", "body", "creador", "imagen", "nombre", "carrera", "iconfile"], True, True, True)

def get_posts_search(search):
    return get_everyman("""
        SELECT p.id, p.titulo, p.body, p.creator, p.imgfile, CONCAT(u.nombres, ' ', u.apepaterno, ' ', u.apematerno), u.carrera, img.imgfile
        FROM everyman p
        LEFT JOIN usuario u ON u.matricula = p.creator
        JOIN tiempo t ON t.everyman = p.id
        JOIN everyman img ON img.creator = p.creator
        WHERE p.aceptable = 1 AND p.tipo = 'Post' AND img.tipo = 'Perfil' AND (p.titulo LIKE '%""" + search + """%' OR p.body LIKE '%""" + search + """%')
        ORDER BY t.año DESC, t.mes DESC, t.dia DESC, t.hora DESC, t.min DESC, t.seg DESC;
    """, ["id", "titulo", "body", "creador", "imagen", "nombre", "carrera", "iconfile"], True, True, True)

def get_posts_search_tags(search):
    return search_tags(get_posts(), search)

def get_post(id):
    return get_everyman("""
        SELECT p.id, p.titulo, p.body, p.creator, p.imgfile, CONCAT(u.nombres, ' ', u.apepaterno, ' ', u.apematerno), u.carrera, img.imgfile
        FROM everyman p
        LEFT JOIN usuario u ON u.matricula = p.creator
        JOIN everyman img ON img.creator = p.creator
        WHERE p.aceptable = 1 AND img.tipo = 'Perfil' AND p.tipo = 'Post' AND p.id = """ + str(id) + """;
    """, ["id", "titulo", "body", "creador", "imagen", "nombre", "carrera", "iconfile"], False, True, True)[0]

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
    return cursor.fetchall()

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
        SELECT p.id, p.titulo, p.body, p.creator, p.imgfile, CONCAT(u.nombres, ' ', u.apepaterno, ' ', u.apematerno), u.carrera
        FROM everyman p
        LEFT JOIN usuario u ON u.matricula = p.creator
        WHERE p.aceptable = 1 AND p.tipo = 'Perfil' AND p.creator = """ + str(id) + """;
    """, ["id", "titulo", "body", "creador", "imagen", "nombre", "carrera"], False, False, True)[0]

def get_posts_by_user(id):
    return get_everyman("""
        SELECT p.id, p.titulo, p.body, p.creator, p.imgfile, CONCAT(u.nombres, ' ', u.apepaterno, ' ', u.apematerno), u.carrera, img.imgfile
        FROM everyman p
        LEFT JOIN usuario u ON u.matricula = p.creator
        JOIN tiempo t ON t.everyman = p.id
        JOIN everyman img ON img.creator = p.creator
        WHERE p.aceptable = 1 AND p.tipo = 'Post' AND img.tipo = 'Perfil' AND p.creator = """ + str(id) + """
        ORDER BY t.año DESC, t.mes DESC, t.dia DESC, t.hora DESC, t.min DESC, t.seg DESC;
    """, ["id", "titulo", "body", "creador", "imagen", "nombre", "carrera", "iconfile"], True, True, True)

def add_edit_everyman(instruct, textinput, tags, edited):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(instruct, textinput)
    newid = cursor.lastrowid
    tags2 = []
    for tag in tags:
        tags2.append((newid, tag))
    cursor.executemany("INSERT INTO tags VALUES (tsuku, term) VALUES (?, ?)", tags)
    if edited:
        cursor.execute

def make_profile(tipo, titulo, body, creador, imgfile, tags):
    instruct = """
        INSERT INTO everyman VALUES (tipo, titulo, body, creador, imgfile) VALUES (?, ?, ?, ?, ?) 
    """
    words = (tipo, titulo, body, creador, imgfile)
    return add_edit_everyman(instruct, words, tags, False)

def get_user_login(matri, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario WHERE matricula = " + str(matri) + ";")
    usu = {"matricula":0, "nombres":"", "apepaterno":"", "apematerno":"", "carrera":"", "correo":"", "psswrd":""}
    if cursor.rowcount == 0:
        usu = cursor.fetchone()
    return usu, usu.get("psswrd", "") == password