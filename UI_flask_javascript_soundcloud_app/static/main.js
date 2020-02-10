

/* 1. Search */

var UI = {};

UI.ClickIcon = function() {
    document.querySelector('.js-submit').addEventListener('click', function(){

        let songs = {{ songs|safe}};

        console.log(songs);

        songs.forEach(function(song){
               SoundCloudAPI.getTrack(song);
        });

        //let input = document.querySelector('.js-search').value;
        //SoundCloudAPI.getTrack(input);
    });
};

/*
UI.ClickEnter = function(e) {
    document.querySelector('.js-search').addEventListener('keyup', function(e){
        let input = document.querySelector('.js-search').value;
        if (e.which === 13) {
            SoundCloudAPI.getTrack(input);
        };
    });
};
 */

UI.ClickEnter();
UI.ClickIcon();

/* 2. Query Soundcloud API */

var SoundCloudAPI = {};

SoundCloudAPI.init = function() {
    SC.initialize({
        client_id: 'cd9be64eeb32d1741c17cb39e41d254d'
    });
};
SoundCloudAPI.init();

SoundCloudAPI.getTrack = function(inputValue) {
    SC.get('/tracks', {
        q: inputValue,
    }).then(function(tracks) {
        SoundCloudAPI.renderTracks(tracks[0]);
    });
};

/* 3. Display cards */
SoundCloudAPI.renderTracks = function(track) {

    // clean the page before inserting new cards
    // document.querySelector('.js-search-results').innerHTML='';

    //tracks.forEach(function(track){

    let card = document.createElement("div");
    card.classList.add("card");

    // image sub-div
    let imageDiv = document.createElement("div");
    imageDiv.classList.add("image");
    let image_img = document.createElement("img");
    image_img.classList.add("image");
    image_img.src = track.artwork_url || 'http://lorempixel.com/100/100/abstract';

    imageDiv.appendChild(image_img);

        // content
    let contentDiv = document.createElement("div");
    contentDiv.classList.add("content");

    let headerDiv = document.createElement("div");
    headerDiv.classList.add("header");
    headerDiv.innerHTML = '<a href=' + track.permalink_url + ' target = "_blank">' + track.title + '</a>';

    contentDiv.appendChild(headerDiv);

        // button
    let buttonDiv = document.createElement("div");
    buttonDiv.classList.add("ui", "bottom", "attached", "button", "js-button");

    let icon= document.createElement("i");
    icon.classList.add("add", "icon");

    let buttonText = document.createElement("span");
    buttonText.innerHTML = "Add to playlist";

    buttonDiv.appendChild(icon);
    buttonDiv.appendChild(buttonText);
    buttonDiv.addEventListener('click', function() {
        SoundCloudAPI.embed(track.permalink_url);
        });

        // adding all sub-divs
    card.appendChild(imageDiv);
    card.appendChild(contentDiv);
    card.appendChild(buttonDiv);


    let searchResults = document.querySelector(".js-search-results");
    searchResults.append(card);

};

/* 4. Add to playlist and play */
SoundCloudAPI.embed = function(link) {
    SC.oEmbed(link, {
        auto_play: true
    }).then(function (embed) {
        let sideBar = document.querySelector('.js-playlist');
        let box = document.createElement('div');

        box.innerHTML = embed.html;
        sideBar.insertBefore(box, sideBar.firstChild);
        localStorage.setItem('key', sideBar.innerHTML);
    })
};

let sideBar = document.querySelector('.js-playlist');
sideBar.innerHTML = localStorage.getItem('key');

