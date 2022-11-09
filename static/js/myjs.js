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

    $.ajax({
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
        }
    })
    console.log(url);

}


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
}