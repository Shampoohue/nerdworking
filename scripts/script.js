function create(param = 1) {

    document.body.innerHTML = `<header>
                                    <div class="logo" style="justify-self: start;" onclick="focusindex()">NERDWORKING</div>
                                    <input id="search" class="writer" type="text" placeholder="🔍︎ Busqueda" aria-label="Search">
                                    <div class="buttons"><button id="notif">🔔︎</button><button id="signup">Registrate</button><button id="signin">Inicia Session</button></div>
                                </header>` + document.body.innerHTML;

    document.getElementById("other").innerHTML = `<div class="card others" onclick="focususer()"><div class="usersets">🏘 Mis Publicaciones</div></div>
                                                <div class="card others"><div class="usersets">🔔︎ Notificaciones</div></div>
                                                <div class="card others"><div class="usersets">🗨︎ Mensajes</div></div>
                                                <div class="card others"><div class="usersets">⚙︎ Configuración</div></div>`;

    if(param === 2){
        document.getElementById("posts").innerHTML = makemainpost("John Ingenieria", "Ayudenme con mi proyecto", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.", ["HTML", "CSS", "JavaScript", "PHP", "MySQL"], "") + document.getElementById("posts").innerHTML
        for (let i = 0; i < 5; i++) {
            document.getElementById("posts").innerHTML += makecomment("Jane Ingenieria", "Pregunta sobre el proyecto", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.");
        }
    }
    else if(param === 3){
        document.getElementById("posts").innerHTML = makemainnew("NASA Spaceapps blah blah blah", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.", ["HTML", "CSS", "JavaScript", "PHP", "MySQL"], "") + document.getElementById("posts").innerHTML
    }
    else {
        for (let i = 0; i < 5; i++) {
            document.getElementById("posts").innerHTML += makepost("John Ingenieria", "Ayudenme con mi proyecto", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.", ["HTML", "CSS", "JavaScript", "PHP", "MySQL"], "");
        }
    }
    for (let i = 0; i < 5; i++) {
        document.getElementById("news").innerHTML += makenews("NASA Spaceapps blah blah blah", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...", ["HTML", "CSS", "JavaScript", "PHP", "MySQL"], "");
    }
}

function makepost(user, title, text, tags, multm) {
    var tags2 = "";
    for (let i = 0; i < tags.length; i++) {
        tags2 += `<button>` + tags[i] + `</button>`;
    }
    return `<div class="card post" onclick="focuspost(this)">
                <div class="title"><div class="twoinone">
                    <div class="usericon" onclick="event.stopPropagation(); focususer(this)"></div>
                    <div><div class="weaktext superweaktext" onclick="event.stopPropagation(); focususer(this)">` + user + `</div>` + title + `</div>
                </div></div>
                <div class="bodytext">` + text + `</div>
                <div onclick="event.stopPropagation();"><div class="tags">` + tags2 + `</div>
                <div class="answer"><button class="like" onclick="clicklike(this)">♥ <div class="meinteresa">Me interesa!</div></button><input id="answer" class="writer answerwrite" onclick="openresponsemaker()" type="text" placeholder="Responde a esta publicación" aria-label="Search"></div></div>
            </div>`;
}

function makenews(title, text, tags, multm) {
    var tags2 = "";
    for (let i = 0; i < tags.length; i++) {
        tags2 += `<button>` + tags[i] + `</button>`;
    }
    return `<div class="bodytext anuncio" onclick="focusanuncio(this)">
                <div class="title">` + title +`</div>
                ` + text + ` 
                <div onclick="event.stopPropagation();"><div class="tags">` + tags2 + `</div>
                <div class="bar"></div></div>
            </div>`;
}

function makecomment(user, title, text) {
    return `<div class="card post" onclick="focuspost(this)">
                <div class="title"><div class="twoinone">
                    <div class="usericon" onclick="event.stopPropagation(); focususer(this)"></div>
                    <div><div class="weaktext superweaktext" onclick="event.stopPropagation(); focususer(this)">` + user + `</div>` + title + `</div>
                </div></div>
                <div class="bodytext">` + text + `</div>
                <div class="answer"></button><input id="answer" class="writer answerwrite answercomment" onclick="openresponsemaker()" type="text" placeholder="Responde a esta publicación" aria-label="Search"></div></div>
            </div>`;
}

function makemainpost(user, title, text, tags, multm) {
    var tags2 = "";
    for (let i = 0; i < tags.length; i++) {
        tags2 += `<button>` + tags[i] + `</button>`;
    }
    return `<div class="card post mainpost">
                <div class="title"><div class="twoinone">
                    <div class="usericon" onclick="event.stopPropagation(); focususer(this)"></div>
                    <div><div class="weaktext superweaktext" onclick="event.stopPropagation(); focususer(this)">` + user + `</div>` + title + `</div>
                </div></div>
                <div class="bodytext">` + text + `</div>
                <div onclick="event.stopPropagation();"><div class="tags">` + tags2 + `</div>
                <div class="answer"><button class="like" onclick="clicklike(this)">♥ <div class="meinteresa">Me interesa!</div></button><input id="answer" onclick="openresponsemaker()" class="writer answerwrite" type="text" placeholder="Responde a esta publicación" aria-label="Search"></div></div>
            </div>`;
}

function makemainnew(title, text, tags, multm){
    var tags2 = "";
    for (let i = 0; i < tags.length; i++) {
        tags2 += `<button>` + tags[i] + `</button>`;
    }
    return `<div class="card post mainpost">
                <div class="title">` + title + `</div>
                <div class="bodytext">` + text + `</div>
                <div onclick="event.stopPropagation();"><div class="tags">` + tags2 + `</div>
            </div>`;
}

function focusindex(){
    window.location.href = "index.html";
}

function clicklike(event) {
    event.classList.toggle('clicked');
}

function focuspost(event){
    window.location.href = "post.html";
}

function focusanuncio(event){
    window.location.href = "noticia.html";
}

function focususer(event){
    window.location.href = "userpage.html";
}

function openpostmaker(){
    document.body.innerHTML += 
    `<div id="postmaker" class="blockage">
        <div class="card iteminblockage">
            <div class="title">
            <button class="cancelbutton" onclick="closepostmaker()">X</button>
            <div class="twoinone">
                <div class="usericon"></div>
                <div class="weaktext superweaktext">John Ingenieria<input id="answer" class="writer answerwrite newpostwriter" type="text" placeholder="Titulo" aria-label="Search"></div>
            </div></div>
            <div class="bodytext"><textarea id="answer" class="writer answerwrite newpostwriter bodytextwriter" type="text" placeholder="Texto" aria-label="Search"></textarea>
            <input id="answer" class="writer answerwrite newpostwriter" type="text" placeholder="Categorias" aria-label="Search"></div>
            <div class="buttons answer twoinone"><input type="file" id="file" name="file" multiple/><button onclick="closepostmaker()">Publicar</button></div>
        </div>
    </div>`;
}

function closepostmaker(){
    document.getElementById("postmaker").remove();
}

function openresponsemaker(){
    document.body.innerHTML +=     
    `<div id="postmaker" class="blockage">
        <div class="card iteminblockage">
                <div class="title"><div class="twoinone">
                    <div class="usericon"></div>
                    <div><div class="weaktext superweaktext">John Ingenieria</div>Ayudenme con mi proyecto</div>
                </div></div>
                <div class="bodytext">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</div>
            <div class="title">
                <button class="cancelbutton" onclick="closepostmaker()">X</button>
                <div class="twoinone">
                <div class="usericon"></div>
                <div class="weaktext superweaktext">John Ingenieria<input id="answer" class="writer answerwrite newpostwriter" type="text" placeholder="Titulo" aria-label="Search"></div>
            </div></div>
            <div class="bodytext"><textarea id="answer" class="writer answerwrite newpostwriter bodytextwriter" type="text" placeholder="Texto" aria-label="Search"></textarea>
            <input id="answer" class="writer answerwrite newpostwriter" type="text" placeholder="Categorias" aria-label="Search"></div>
            <div class="buttons answer twoinone"><input type="file" id="file" name="file" multiple/><button onclick="closepostmaker()">Publicar</button></div>
        </div>
    </div>`;
}