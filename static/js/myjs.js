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


//---------------------------For Subscribe and Unsubscribe---------------------------
document.getElementById('btn-Subscribe').onclick = function (event){
    console.log("Ok");
    const channelID = document.getElementById('channel-id').textContent;
    const url = "http://" + window.location.host + '/content/' + 'channel-subscribe/' + JSON.parse(channelID) + '/';

    $.ajax(
        {
            type: 'GET',
            url : url,
            success: function (data) {
                if(data['message'] == "subscribed"){
                    console.log('Subscribe Added......');
                    document.getElementById('btn-Subscribe').innerText = 'Subscribed';
                    document.getElementById('btn-Subscribe').style.backgroundColor="#4738cf";
                }
                else if(data['message'] == "unsubscribed"){
                    console.log('Remove Subscribe......');
                    document.getElementById('btn-Subscribe').innerText = 'Subscribe';
                    document.getElementById('btn-Subscribe').style.backgroundColor="white";
                }

            },
            error: function (data) {
                console.log('-----------Error-----------');
                console.log(data);
            },
        }
    )
};


//---------------------------For Like or Remove Like---------------------------
document.getElementById('like-video-btn').onclick = function(event) {
    console.log('Click Like Button.');

    let url = "http://" + window.location.host + "/content/like-or-remove-like-video/";
    const video_unique_id = document.getElementById('video-unique-id').innerText;

    $.ajax(
        {
            type: 'GET',
            url: url,
            data: {'video_id': video_unique_id},
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
            },
        }
    )
};


//---------------------------For Add to Watch-Later or Remove From Watch-Later---------------------------
document.getElementById('add-to-watch-later').onclick = function(event) {
    console.log('Click Like Button.');

    let url = "http://" + window.location.host + "/content/add-to-watch-later/";
    const video_unique_id = document.getElementById('video-unique-id').innerText;

    $.ajax(
        {
            type: 'GET',
            url: url,
            data: {'video_id': video_unique_id},
            success: function(data) {
                if(data['message'] == "Add to Watch Later"){
                    console.log('Added to Watch Later......');
                    document.getElementById('add-to-watch-later').style.backgroundColor = "#4738cf";
                }
                else if(data['message'] == "Remove from Watch Later"){
                    console.log('Removed from Watch Later......');
                    document.getElementById('add-to-watch-later').style.backgroundColor = "white";
                }
            },
            error: function(error) {
                console.log('Error Occurs ......');
                console.log(error);
            },
        }
    )
};
