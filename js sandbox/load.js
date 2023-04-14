const mainList = document.querySelector('#tweet-list');
let mainCounter = 0;

const pageHeight = document.documentElement.clientHeight;

window.addEventListener('scroll', isEnd);


loadTweets(mainCounter);
mainCounter++;

function isEnd(){
    const bottomLineOfHtml = document.documentElement.getBoundingClientRect().bottom;
    if (bottomLineOfHtml <= pageHeight + 50){
        // console.log(pageHeight);
        // console.log(document.documentElement.getBoundingClientRect().bottom);
        // console.log('-------------------------------------------')
        loadTweets(mainCounter);
        mainCounter++;
    }
}

function loadTweets(text){
    for (let i = 0; i < 70; i++){
        const listItem = document.createElement('li');
        listItem.classList.add('tweet');
        listItem.textContent = text + ' ' + i;
        mainList.append(listItem);
    }
}
