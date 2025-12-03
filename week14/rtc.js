"use strict";

let localVideo = document.getElementById("localVideo");
let remoteVideo = document.getElementById("remoteVideo");
let recordedVideo = document.getElementById("recordedVideo");

let isInitiator = false;
let isStarted = false;
let pc;  // RTCPeerConnection
let isVideoOff = false;       // 비디오 끄기
let isScreenSharing = false;  // 화면 공유
let originalVideoTrack;                 // 원본 카메라 트랙 저장
let mediaRecorder;                      // 녹화
let recordedChunks = [];        // 녹화 데이터 저장
let isRecording = false;      // 녹화 상태
let localStream;                      // 로컬 스트림

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
  const currentStream = localVideo.srcObject || localStream;
  if (!currentStream) return;
  const videoTrack = currentStream.getVideoTracks()[0];
  if (!videoTrack) return;
  isVideoOff = !isVideoOff;
  videoTrack.enabled = !isVideoOff;
  const videoBtn = document.querySelector('button[onclick="toggleVideo()"]');
  if (videoBtn) videoBtn.textContent = isVideoOff ? '비디오 켜기' : '비디오 끄기';
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
      const screenTrack = stream.getVideoTracks()[0];
      if (!screenTrack) return;
      originalVideoTrack = localStream ? localStream.getVideoTracks()[0] : null;
      const sender = pc && pc.getSenders ? pc.getSenders().find(s => s.track && s.track.kind === 'video') : null;
      if (sender) sender.replaceTrack(screenTrack);
      localVideo.srcObject = stream;
      isScreenSharing = true;
      const shareBtn = document.querySelector('button[onclick="toggleScreenShare()"]');
      if (shareBtn) shareBtn.textContent = '화면 공유 중지';
      screenTrack.onended = stopScreenShare;
    });
}

function stopScreenShare() {
  if (!isScreenSharing) return;
  const currentStream = localVideo.srcObject;
  if (currentStream) currentStream.getTracks().forEach(track => track.stop());
  const sender = pc && pc.getSenders ? pc.getSenders().find(s => s.track && s.track.kind === 'video') : null;
  if (sender && originalVideoTrack) sender.replaceTrack(originalVideoTrack);
  if (localStream) localVideo.srcObject = localStream;
  isScreenSharing = false;
  const shareBtn = document.querySelector('button[onclick="toggleScreenShare()"]');
  if (shareBtn) shareBtn.textContent = '화면 공유';
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
  a.download = 'recording_' + new Date().toISOString().replace(/:/g,'-') + '.webm';

  a.click();
  URL.revokeObjectURL(url);
}

function startRecording() {
  let stream = localVideo.srcObject;  // 1. 녹화할 스트림
  if (!stream) return;
  recordedChunks = [];  // 2. 데이터 저장 배열 초기화
  mediaRecorder = new MediaRecorder(stream);  // mediaRecorder 생성
  mediaRecorder.ondataavailable = function(e) {
    if (e.data && e.data.size > 0) recordedChunks.push(e.data);
  };
  mediaRecorder.onstop = function() {
    let blob = new Blob(recordedChunks, { type: 'video/webm' }); // Blob 생성
    let url = URL.createObjectURL(blob); // URL 변환
    recordedVideo.src = url;  // 비디오에서 재생
  };
  mediaRecorder.start(); // 녹화 시작
  isRecording = true;
  const recordBtn = document.querySelector('button[onclick="toggleRecording()"]');
  if (recordBtn) recordBtn.textContent = '녹화 중지';
}

function stopRecording() {
  if (!mediaRecorder || mediaRecorder.state === 'inactive') return;
  mediaRecorder.stop();  // 녹화 중지 
  isRecording = false;
  const recordBtn = document.querySelector('button[onclick="toggleRecording()"]');
  if (recordBtn) recordBtn.textContent = '녹화 시작';
}

window.toggleVideo = toggleVideo;
window.toggleScreenShare = toggleScreenShare;
window.toggleRecording = toggleRecording;
window.downloadRecording = downloadRecording;
