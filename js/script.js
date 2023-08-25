
let shouldStop = false;
let stopped = false;

let stopwatchInterval;
let seconds = 0;
let minutes = 0;

const videoElement = document.getElementsByTagName("video")[0];
const downloadLink = document.getElementById('download');
const stopButton = document.getElementById('stop');

function startRecord() {
    $('.btn-outline-info').prop('disabled', true);
    $('.btn-outline-warning').prop('disabled', true);
    $('.btn-outline-success').prop('disabled', true);
    $('.btn-outline-primary').prop('disabled', true);
    $('.btn-outline-danger').prop('disabled', true);
    $('#stop').prop('disabled', false).removeClass('d-none');
    $('#download').css('display', 'none');
    $('#downloadAlert').addClass('d-none');

    $('#stopwatch').removeClass('d-none');
    startStopwatch();
}

function stopRecord() {
    $('.btn-outline-info').prop('disabled', false);
    $('.btn-outline-warning').prop('disabled', false);
    $('.btn-outline-success').prop('disabled', false);
    $('.btn-outline-primary').prop('disabled', false);
    $('.btn-outline-danger').prop('disabled', false);
    $('#stop').prop('disabled', true).addClass('d-none');
    $('#download').css('display', 'block');

    $('#stopwatch').addClass('d-none');
    stopStopwatch();
}

stopButton.addEventListener('click', function () {
    shouldStop = true;
});

const audioConstraints = {
    echoCancellation: false,
    autoGainControl: false,
    noiseSuppression: false
};

const handleRecord = function ({stream, mimeType}) {
    startRecord()
    let recordedChunks = [];
    stopped = false;
    const mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = function (e) {
        if (e.data.size > 0) {
            recordedChunks.push(e.data);
        }

        if (shouldStop === true && stopped === false) {
            mediaRecorder.stop();
            stopped = true;
        }
    };

    mediaRecorder.onstop = function () {
        const blob = new Blob(recordedChunks, {
            type: mimeType
        });
        recordedChunks = [];
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `recording-${timestamp}`;
    
        downloadLink.href = URL.createObjectURL(blob);
        downloadLink.download = `${filename}.webm`;
        stopRecord();
        videoElement.srcObject = null;

       
    };    

    mediaRecorder.start(200);
};

document.getElementById('download').addEventListener('click', function () {
    $('#downloadAlert').removeClass('d-none');
});

/*async function recordAudioMic() {
    const mimeType = 'audio/webm';
    shouldStop = false;
    const stream = await navigator.mediaDevices.getUserMedia({audio: audioConstraints});
    handleRecord({stream, mimeType})
}*/

async function recordScreenWithAudioMicandDesk() {
    const mimeType = 'video/webm';
    shouldStop = false;
    const constraints = {
        video: {
            cursor: 'motion'
        },
        audio: audioConstraints,
    };
    if (!(navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia)) {
        return window.alert('Screen Record not supported in this device!')
    }
    let stream = null;
    const displayStream = await navigator.mediaDevices.getDisplayMedia(constraints);
    const audioContext = new AudioContext();

    const voiceStream = await navigator.mediaDevices.getUserMedia({
        audio: audioConstraints,
        video: false
    });
    
    const userAudio = audioContext.createMediaStreamSource(voiceStream);

    const audioDestination = audioContext.createMediaStreamDestination();
    userAudio.connect(audioDestination);

    if (displayStream.getAudioTracks().length > 0) {
        const displayAudio = audioContext.createMediaStreamSource(displayStream);
        displayAudio.connect(audioDestination);
    }

    const tracks = [...displayStream.getVideoTracks(), ...audioDestination.stream.getTracks()]
    stream = new MediaStream(tracks);
    handleRecord({ stream, mimeType });
    videoElement.srcObject = stream;
}

async function recordScreenWithAudioDesk() {
    const mimeType = 'video/webm';
    shouldStop = false;
    const constraints = {
        video: {
            cursor: 'motion'
        },
        audio: audioConstraints,
    };
    if (!(navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia)) {
        return window.alert('Screen Record not supported in this device!')
    }
    let stream = null;
    const displayStream = await navigator.mediaDevices.getDisplayMedia(constraints);
    const tracks = [...displayStream.getVideoTracks(), ...displayStream.getAudioTracks()]
    stream = new MediaStream(tracks);
    handleRecord({ stream, mimeType });
    videoElement.srcObject = stream;
}

function startStopwatch() {
    seconds = 0;
    minutes = 0;

    stopwatchInterval = setInterval(function () {
        seconds++;
        if (seconds === 60) {
            seconds = 0;
            minutes++;
        }
        updateStopwatchDisplay();
    }, 1000);
}

function stopStopwatch() {
    clearInterval(stopwatchInterval);
}

function updateStopwatchDisplay() {
    const secondsDisplay = seconds < 10 ? `0${seconds}` : seconds;
    const minutesDisplay = minutes < 10 ? `0${minutes}` : minutes;
    document.getElementById('seconds').textContent = secondsDisplay;
    document.getElementById('minutes').textContent = minutesDisplay;
}