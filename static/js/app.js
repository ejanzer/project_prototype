function hasGetUserMedia() {
    return !!(navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);
}

if (hasGetUserMedia()) {
    alert("getUserMedia is supported in your browser! Yay!")
} else {
    alert("getUserMedia is not supported in your browser.")
}

var errorCallback = function(e) {
    console.log("Error!", e);
};

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;

var video = document.querySelector('video');

if (navigator.getUserMedia) {
    navigator.getUserMedia({audio: false, video: true}, function(stream) {
        video.src = window.URL.createObjectURL(stream);
        video.play();
    }, errorCallback);
} else {
    video.src = 'http://www.youtube.com/watch?v=ScMzIvxBSi4';
}