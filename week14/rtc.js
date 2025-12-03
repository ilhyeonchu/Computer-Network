"use strict";

let localVideo = document.getElementById("localVideo");
let remoteVideo = document.getElementById("remoteVideo");

let isInitiator = false;
let isStarted = false;
let pc;  // RTCPeerConnection
let isVideoOff = false;       // 비디오 끄기
let isScreenSharing = false;  // 화면 공유
let originalVideoTrack;                 // 원본 카메라 트랙 저장
let mediaRecorder;                      // 녹화
let recordedChunks = [];        // 녹화 데이터 저장
let isRecording = false;      // 녹화 상태

// ICE 서버 설정 (Google STUN 서버 사용)
let pcConfig = {
    'iceServers': [{ 'urls': 'stun:stun.l.google.com:19302' }]
};

let room = 'test-room';
let socket = io.connect();

// 방 참가 요청
if (room !== '') {
    socket.emit('create or join', room);
}

// 방 생성됨 (첫 번째 접속자)
socket.on('created', (room, id) => {
    isInitiator = true;
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then(stream => {
            localVideo.srcObject = stream;
            localStream = stream;
        });
});

// 방 참가됨 (두 번째 접속자)
socket.on('joined', (room, id) => {
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then(stream => {
            localVideo.srcObject = stream;
            localStream = stream;
        });
});

// 연결 준비 완료
socket.on('ready', () => {
    if (isInitiator) maybeStart();
});

function maybeStart() {
    pc = new RTCPeerConnection(pcConfig);
    
    // 로컬 스트림 추가
    localStream.getTracks().forEach(track => pc.addTrack(track, localStream));
    
    // ICE candidate 전송
    pc.onicecandidate = e => {
        if (e.candidate) socket.emit('candidate', e.candidate);
    };
    
    // 원격 스트림 수신
    pc.ontrack = e => { remoteVideo.srcObject = e.streams[0]; };
    
    // Offer 생성 및 전송
    if (isInitiator) {
        pc.createOffer()
            .then(offer => pc.setLocalDescription(offer))
            .then(() => socket.emit('offer', pc.localDescription));
    }
}

function toggleVideo() {
  if (!localStream) return;
  let videoTrack = localStream.getVideoTracks()[0];
  videoTrack.enabled = false; // 끄기
  videoTrack.enabled = true;  // 켜기

  if (videoTrack) {
    isVideoOff = !isVideoOff;
    videoTrack.enabled = isVideoOff ? false : true;
    videoBtn.textContent = isVideoOff ? '비디오 켜기' : '비디오 끄기';
  }
}

function toggleScreenShare() {
  if (isScreenSharing) {
    stopScreenShare();
  } else {
    startScreenShare();
  }
}

function startScreenShare() {
  navigator.mediaDevices.getDisplayMedia({ video: true })
    .then(stream => {
      // 1. 화면 공유 트랙 가져오기
      // 2. 로컬 비디오에 표시
      // 3. 상태 변경
    });
}

function stopScreenShare() {
  // 원래 ㅁ카메라로 복원
  // localStream으로 복원
  isScreenSharing = false;
}

function toggleRecording() {
  if (isRecording) {
    stopRecording();
  } else {
    startRecording();
  }
}

function downloadRecording() {
  if (recordedChunks.length === 0) return;

  let blob = new Blob(recordedChunks, { type: 'video/webm' });
  let url = URL.createObjectURL(blob);
  
  let a = document.createElement('a');
  a.href = url;
  a.download = 'recording_' + new Data().tolSOString().replace(/:/g,'-') + '.webm'

  a.click();
}

function startRecording() {
  let stream = localVideo.srcObject;  // 1. 녹화할 스트림
  recordedChunks = [];  // 2. 데이터 저장 배열 초기화
  medialRecorder = ;  // mediaRecorder 생성
  mediaRecorder.ondataavailable = function(e) {
    // 4. 데이터 수집 + 녹화 완료
  };
  mediaRecorder.onstop = function() {
    let blob = ; // Blob 생성
    let url = ; // URL 변환
    recordedVideo.src = url;  // 비디오에서 재생
  };
    // add someting 녹화 시작
  isRecording = ture;
}

function stopRecording() {
  // add someting 녹화 중지 
  isRecording = false;
}

window.toggleVideo() = toggleVideo;
window.toggleScreenShare() = toggleScreenShare;
window.toggleRecording() = toggleRecording;
window.downloadRecording = downloadRecording;
