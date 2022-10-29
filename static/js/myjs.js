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


