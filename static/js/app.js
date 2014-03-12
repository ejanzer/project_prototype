function hasGetUserMedia() {
    // Returns true if browser supports HTML5 webcam API.
    return !!(navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);
}


function convertCanvasToImage(canvas, callback) {
    var image = new Image();
    image.onload = function() {
        callback(image);
    }
    image.src = canvas.toDataURL("image/png");
}

var errorCallback = function(e) {
    console.log("Error!", e);
};


$(document).ready(function() {
    if (hasGetUserMedia()) {
        alert("getUserMedia is supported in your browser! Yay!")

        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;

        var canvas = document.getElementById("canvas");
        var context = canvas.getContext("2d");
        var video = document.getElementById("video");


        if (navigator.getUserMedia) {
            // Access the video stream from the webcam.
            navigator.getUserMedia({audio: false, video: true}, function(stream) {

                // Make the video div visible on detection of getUserMedia.
                $('#video-feed').removeClass('hidden');

                // Set the video element's source to that stream.
                video.src = window.URL.createObjectURL(stream);

                // Play the video.
                video.play();

            }, errorCallback);
        } else {
            // Default video source, just in case.
            video.src = 'http://www.youtube.com/watch?v=ScMzIvxBSi4';
        }

    } else {
        alert("getUserMedia is not supported in your browser.")
    }

    $("#snap").on("click", function() {
        $("#image-display").removeClass('hidden');
        context.drawImage(video, 0, 0, 640, 480);
        convertCanvasToImage(canvas, function(image) {
            console.log(image.src);
        });
    });

});

