function clicklike(button, user, post) {
    if (button.value == 1){
        if (button.classList.contains('clicked')){
            button.classList.remove('clicked');
        }
        fetch("/api/unlike/"+user+"/"+post)
        .then(response => response.json())  
        .then(json => {console.log(json)});
    } else{
        button.classList.add('clicked');
        fetch("/api/like/"+user+"/"+post)
        .then(response => response.json())  
        .then(json => {console.log(json)});
    }
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
    disableScroll();
}

function closepostmaker(){
    document.getElementById("postmaker").remove();
    enableScroll();
}

function openresponsemaker(responded){
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
                <div><div class="superweaktext weaktext">John Ingenieria</div>Respondiendo a ` + responded + `</div>
            </div></div>
            <div class="bodytext"><textarea id="answer" class="writer answerwrite newpostwriter bodytextwriter" type="text" placeholder="Texto" aria-label="Search"></textarea>
            <input id="answer" class="writer answerwrite newpostwriter" type="text" placeholder="Categorias" aria-label="Search"></div>
            <div class="buttons answer twoinone"><input type="file" id="file" name="file" multiple/><button onclick="closepostmaker()">Publicar</button></div>
        </div>
    </div>`;
    disableScroll();
}

function disableScroll() {
    scrollTop =
        window.pageYOffset ||
        document.documentElement.scrollTop;
    scrollLeft =
        window.pageXOffset ||
        document.documentElement.scrollLeft,
    window.onscroll = function () {
        window.scrollTo(scrollLeft, scrollTop);
    };
}

function enableScroll() {
    window.onscroll = function () { };
}

function open_response_maker(id){
    window.location.href = "/reply/new/" + id;
}