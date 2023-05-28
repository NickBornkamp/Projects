const video = document.getElementById('webcam');                     // video element, renders the video stream of webcam
const liveView = document.getElementById('liveView');                // button and video div container
const demosSection = document.getElementById('demos');               // section element with id of demos
const enableWebcamButton = document.getElementById('webcamButton');  // reference to button
//const canvas = document.getElementById('canvas');                     // video element, renders the video stream of webcam

var model = 1;
var confThreshold = 0.66;
var currentEmotes = [];
var classShown = [];

const MODEL_URL = '/Final%20Presentation/models';
console.log(faceapi.nets);
faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
  faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL);
  faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL);
  faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL);
console.log("egg");
// Check if browser allows accessing the webcam stream via getUserMedia  
function getUserMediaSupported() {
    return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia); // !! cast to boolean value
}

  // Add an event listener so that the web camera can be enabled when the button is pushed.
  // Once the button is pushed the method enableCam will be invoked
  if (getUserMediaSupported()) {
    enableWebcamButton.addEventListener('click', enableCam);
  } else {
    console.warn('getUserMedia() is not supported by your browser');
  }


    // Show demo section now model is ready to use.
    demosSection.classList.remove('invisible');
 
    document.getElementById("confThreshold").oninput = function () {
      confThreshold = event.srcElement.value / 100.0;
    };

function enableCam(event) {
    // Only continue if the COCO-SSD has finished loading.
    if (!model) {
      return;          // return if model is not loaded
    }
    
    // Hide the button once clicked.
    event.target.classList.add('removed');  
    
    // getUsermedia parameters to force video but not audio.
    const constraints = {
      video: true                   // only want video stream
    };
  
    // Activate the webcam stream with asynchronous call, thus the use of then. Then we use an anonymous inline function takes stream as argument
    navigator.mediaDevices.getUserMedia(constraints, stream => video.srcObject = stream,).then(function(stream) {
      video.srcObject = stream;
      video.addEventListener('play', detectWebcam);   // Register method predictWebcam
    });
  }


  function detectWebcam(){
    const canvas = faceapi.createCanvasFromMedia(video)
    console.log(video.width);
    document.body.append(canvas)
    const displaySize = { width: video.width, height: video.height }
    faceapi.matchDimensions(canvas, displaySize)
    classShown.splice(0);
    setInterval(async () =>{
      classShown.splice(0);
      currentEmotes.splice(0);
      const fullFaceDescriptions =  await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions();
    const resizedFaceDescriptions = faceapi.resizeResults(fullFaceDescriptions, displaySize);
    var emotions = {};
    try {
      emotions = resizedFaceDescriptions[0]['expressions'];
    } catch (error) {
      emotions = {'No Faces': 1.0005};
    }
    
    for (const [emotion, confidence] of Object.entries(emotions)) {
      if(confidence >= confThreshold && !currentEmotes.includes(emotion)){
        currentEmotes.push(emotion);
          classShown.push([emotion, confidence.toFixed(2)]);
      }
    }
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    faceapi.draw.drawDetections(canvas, resizedFaceDescriptions)
    faceapi.draw.drawFaceLandmarks(canvas, resizedFaceDescriptions)
    faceapi.draw.drawFaceExpressions(canvas, resizedFaceDescriptions)

    document.getElementById('arrayMessage').innerHTML = classShown;
    }
    , 30);
  }