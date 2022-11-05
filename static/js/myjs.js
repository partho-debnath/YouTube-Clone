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
        + '/ws/ac/'                  //   '/ws/ac/'   Asynchronous Connection
        + 'channel-subscribe/'
        + channelID
        + '/'
    );

    ws.onopen = function (event) {
        console.log("Connect", event);
        if (document.getElementById('btn-Subscribe').innerText == 'Subscribe'){
            document.getElementById('btn-Subscribe').innerText = 'Subscribed';
        }
        else {
            document.getElementById('btn-Subscribe').innerText = 'Subscribe';
        };
    };

    ws.onclose = function (event) {
        console.log('Connection Closed');
    };
};


//---------------------------For Like or Remove Like---------------------------

document.getElementById('like-video-btn').onclick = function(event) {
    console.log('Click Like Button.');

    let url = "http://" + window.location.host + "/content/like-or-remove-like-video/";
    const videoID = document.getElementById('videoID').innerText;

    $.ajax({
        type: 'GET',
        url: url,
        data: {'video_id': videoID},
        success: function (data) {
            if(data['message'] == "like-added"){
                console.log('Like Added......');
                document.getElementById('like-video-btn').style.backgroundColor="#4738cf";
            }
            else if(data['message'] == "like-removed"){
                console.log('Like Removed......');
                document.getElementById('like-video-btn').style.backgroundColor="white";
            }
        },
        error: function (error) {
            console.log(error);
        }
    })
};