# WebRTC Prac

## 요구사항
    1. 비디오 on/off 기능
    2. 화면 공유 기능
    3. 화면 녹화 기능

### 1. 비디오 on/off 기능
    - MediaStreamTrack의 enabled 속성으로 on/off 제어
    - enable = false이면 off, true이면 on
    - 버튼 클릭시 on/off 토글되는 함수 구현
    - 현태 상태를 기억하는 변수 선언 및 활용

### 2. 화면 공유 기능
    - getDisplayMedia() 로 화면/췬도우/탭 스트림 획득
    - 사용자가 공유 대상 선택
    - 화면 공유 시작 기능 구현
    - 카메라(비디오)로 복원 기능 구현
    - startCamera()에서 원본을 저장해두어야 복원가
### 3. 화면 녹화 기능
    - MediaRecorder API로 스트림을 녹화
    - ondataavailable: 녹화 데이터 수집
    - onstop: 녹화 완료 후 처리
    - Blob으로 변환하여 재생/다운로드
    - 녹화 시작/중지 기능 구현
    - 녹화된 영상 재생 + 다운로드 기능 구현
    - 화면 녹화 기능 구현 방식
        1. MediaRecorder 생성: new MediaRecorder(스트림)
        2. 녹화 시작/중지: .start(), .stop()
        3. Blob 생성: new Blob(배열, { type: 'video/webm' })
        4. URL 변환: URL.createObjectURL(blob)
        5. 데이터 수집: recordedChunks.push(e.data)

## 주의사항
함수들만 수정 가능
단 maybeStart() 함수는 수정 불가
