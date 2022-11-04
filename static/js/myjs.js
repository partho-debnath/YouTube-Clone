// ------------------------- Copy Video Url -------------------------
function getVideoUrl(){
    const domain = window.location.host + '/content/';
    const video_code = document.getElementById('video-unique-id').innerText;
    let video_url = domain + video_code + '/';
    
    navigator.clipboard.writeText(video_url);
};


// ------------------------- Copy Channel Url -------------------------
function getChannelUrl(){
    const domain = window.location.host + '/channel/';
    const channel_slug = document.getElementById('channel-url').innerText;
    let channel_url = domain + JSON.parse(channel_slug) + '/';
    
    navigator.clipboard.writeText(channel_url);
};


document.getElementById('btn-Subscribe').onclick = function (event){
    console.log("Ok");
    const channelID = document.getElementById('channel-id').textContent;
    const ws = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/ac/'
        + 'channel-subscribe/'
        + channelID
        + '/'
    );

    ws.onopen = function (event) {
        console.log("Connect");
    };
};