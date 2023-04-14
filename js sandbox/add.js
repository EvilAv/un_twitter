const parent = document.querySelector('#tweet-list');
parent.addEventListener('change', likeTweet);

const tweetForm = document.querySelector('#tweet-sender');

tweetForm.addEventListener('input', function(event) {
    const inputField = event.target;
    if (!inputField) return;
    if (inputField.value.length >= 20){
        inputField.style.color = 'red';
    }
    else{
        inputField.style.color = 'black';
    }
})


tweetForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const tweetText = event.target.elements['tweet-input'];
    if (!tweetText || tweetText.value.length >= 20) return;
    else{
        createTweet(tweetText.value);
        tweetText.value = '';
    }
})

parent.addEventListener('click', function(event){
    const btn = event.target;
    if (!btn || btn.tagName != 'BUTTON') return;
    if (btn.value == 'delete'){
        btn.closest('li').remove();
    }
})

function createTweet(text){
    const elem = document.createElement('li');
    elem.innerHTML = '<p>' +text+' <span class="likes">'+getRandomInt(120)+'</span> <input type="checkbox" value="like"></p>'
                        +'<button value="delete">delete</button>';
    parent.prepend(elem);
}

function likeTweet(event){
    const curTweet = event.target;
    if (!curTweet) return;

    const likes = curTweet.parentNode.querySelector('.likes');
    if (curTweet.checked){
        likes.innerHTML++;
    }
    else{
        likes.innerHTML--;
    }
}

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}