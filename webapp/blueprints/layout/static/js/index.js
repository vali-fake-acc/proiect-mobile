

if('ondeviceproximity' in window) {
    // Fired when object is in the detection zone
    window.addEventListener('deviceproximity', function(event) {
        // Object distance in centimeters
        console.log(event.value + " centimeters");
    });
} else {
    console.log("deviceproximity not supported");
}

if('ondeviceproximity' in window){
    // Fired when object is in the detection zone
    window.addEventListener('userproximity', function(event) {
        if(event.near == true) {
            console.log("Object is near");
        } else {
            console.log("Object is far");
        }
    });
} else {
    console.log("userproximity not supported");
}



if('ondevicelight' in window) {
    window.addEventListener("devicelight", function(event) {
        //light level is returned in lux units
        alert(event.value + " lux");
    });
}

if('onlightlevel' in window){
    window.addEventListener("lightlevel", function(event) {
        //light value can be dim, normal or bright
        alert(event.value);
    });
}


//
//
//
// // Check that the browser supports getUserMedia.
// // If it doesn't show an alert, otherwise continue.
// if (navigator.getUserMedia) {
//   // Request the camera.
//   navigator.getUserMedia(
//     // Constraints
//     {
//       video: true
//     },

//     // Success Callback
//     function(localMediaStream) {

//     },

//     // Error Callback
//     function(err) {
//       // Log the error to the console.
//       alert('The following error occurred when trying to use getUserMedia: ' + err);
//     }
//   );

// } else {
//   alert('Sorry, your browser does not support getUserMedia');
// }
