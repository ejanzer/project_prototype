function hasGetUserMedia() {
    // Returns true if browser supports HTML5 webcam API.
    return !!(navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);
}

function convertDataURLToBlob(dataURL) {
    // Decode from base64 everything that follows the mimetype string
    var decodedstring = atob(dataURL.split(',')[1]);
    var chars = [];
    for (var i = 0; i < decodedstring.length; i++) {
        // Convert to an array of characters.
        chars.push(decodedstring.charCodeAt(i));
    }

    // Convert to a Blob. Uint8Array is an array of 8-bit unsigned ints.
    return new Blob([new Uint8Array(array)], {type: 'image/png'});
}

function convertCanvasToImage(canvas, callback) {
    // Create a new image element.
    var image = new Image();
    image.onload = function() {
        // Set the source of the image to the data URL from the canvas.
        image.src = canvas.toDataURL("image/png");
        // In case it takes a second to load, call back instead of return.
        callback(image);
    }

}

var errorCallback = function(e) {
    console.log("Error!", e);
};


$(document).ready(function() {
    if (hasGetUserMedia()) {
        // If the browser supports HTML5, get the getUserMedia attribute.
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;

        // Grab the canvas and video elements from the DOM.
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
        // When the "Snap Photo" button is clicked, 
        // display the captured image in the image-display div.
        $("#image-display").removeClass('hidden');

        // Draw Image accepts a video HTML element as an argument
        // in which case it just grabs the current frame of the video 
        // and paints it onto the canvas.
        context.drawImage(video, 0, 0, 640, 480);

        // This just creates a new image element and assigns the canvas' 
        // data URL to its src attribute.
        convertCanvasToImage(canvas, function(image) {

            // When the "Upload" button is clicked, 
            // send an AJAX POST request to the server with the image.
            $("button#send").on("click", function() {

                // Convert the image to form data first
                // since that's what the route in Flask expects...?
                formData = new FormData();

                // Flask looks for something called 'file' on the request.
                formData.append('file', image.src);
                console.log(formData);

                // Send an AJAX POST request with the image file.
                $.ajax({
                    url: "/",
                    data: formData, // This doesn't work right now.
                    cache: false,
                    mimeType: "multipart/form-data",
                    contentType: false,
                    processData: false,
                    type: "POST",
                    success: function(data) {
                        // Fix this later.
                        $('body').html(data);
                    }, 
                    error: function(err) {
                        console.log(err);
                    }
                });
            });
        });
    });
});

