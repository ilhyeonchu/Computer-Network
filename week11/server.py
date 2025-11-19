#!/usr/bin/env python3
"""
간단한 파일 업로드 웹서버
Flask를 사용하여 파일 업로드 및 다운로드 링크 제공
"""

from flask import Flask, request, send_file, render_template_string, url_for, redirect
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# 설정
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'mp4', 'mp3', 'avi', 'mov', 'pcap', 'pcapng'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# 업로드 폴더 생성
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """허용된 파일 확장자인지 확인"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# HTML 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>파일 업로드 서버</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        .content {
            padding: 30px;
        }
        .upload-section {
            background: #f8f9fa;
            border: 2px dashed #667eea;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
            margin-bottom: 30px;
            transition: all 0.3s;
        }
        .upload-section:hover {
            border-color: #764ba2;
            background: #f0f1f5;
        }
        .file-input-wrapper {
            position: relative;
            overflow: hidden;
            display: inline-block;
            margin-bottom: 15px;
        }
        .file-input-wrapper input[type=file] {
            position: absolute;
            left: -9999px;
        }
        .file-input-label {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s;
            display: inline-block;
        }
        .file-input-label:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .upload-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s;
            margin-top: 10px;
        }
        .upload-btn:hover {
            background: #218838;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(40, 167, 69, 0.4);
        }
        .upload-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        .file-name {
            margin-top: 15px;
            color: #666;
            font-style: italic;
        }
        .files-section {
            margin-top: 30px;
        }
        .files-section h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        .file-list {
            list-style: none;
        }
        .file-item {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s;
        }
        .file-item:hover {
            background: #e9ecef;
            transform: translateX(5px);
        }
        .file-info {
            flex: 1;
        }
        .file-name-text {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        .file-meta {
            font-size: 0.85em;
            color: #666;
        }
        .file-actions {
            display: flex;
            gap: 10px;
        }
        .download-btn, .copy-btn {
            padding: 8px 20px;
            border-radius: 20px;
            text-decoration: none;
            font-size: 14px;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
        }
        .download-btn {
            background: #007bff;
            color: white;
        }
        .download-btn:hover {
            background: #0056b3;
            transform: translateY(-2px);
        }
        .copy-btn {
            background: #6c757d;
            color: white;
        }
        .copy-btn:hover {
            background: #545b62;
        }
        .message {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        }
        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
        }
        .empty-state svg {
            width: 80px;
            height: 80px;
            margin-bottom: 20px;
            opacity: 0.5;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📁 파일 업로드 서버</h1>
            <p>파일을 업로드하고 다운로드 링크를 공유하세요</p>
        </div>
        
        <div class="content">
            {% if message %}
            <div class="message {{ message_type }}">
                {{ message }}
            </div>
            {% endif %}
            
            <div class="upload-section">
                <h2>📤 파일 업로드</h2>
                <form method="post" enctype="multipart/form-data" id="uploadForm">
                    <div class="file-input-wrapper">
                        <label for="file" class="file-input-label">파일 선택</label>
                        <input type="file" name="file" id="file" onchange="updateFileName(this)" required>
                    </div>
                    <div class="file-name" id="fileName">선택된 파일 없음</div>
                    <br>
                    <button type="submit" class="upload-btn">업로드</button>
                </form>
                <p style="margin-top: 15px; color: #666; font-size: 0.9em;">
                    최대 파일 크기: 100MB<br>
                    허용 확장자: txt, pdf, png, jpg, jpeg, gif, zip, doc, docx, xls, xlsx, ppt, pptx, mp4, mp3, avi, mov
                </p>
            </div>
            
            <div class="files-section">
                <h2>📋 업로드된 파일 ({{ files|length }}개)</h2>
                {% if files %}
                <ul class="file-list">
                    {% for file in files %}
                    <li class="file-item">
                        <div class="file-info">
                            <div class="file-name-text">📄 {{ file.name }}</div>
                            <div class="file-meta">
                                크기: {{ file.size }} | 업로드: {{ file.time }}
                            </div>
                        </div>
                        <div class="file-actions">
                            <a href="{{ url_for('download_file', filename=file.name) }}" class="download-btn">다운로드</a>
                            <button onclick="copyLink('{{ request.host_url }}download/{{ file.name }}')" class="copy-btn">링크 복사</button>
                        </div>
                    </li>
                    {% endfor %}
                </ul>
                {% else %}
                <div class="empty-state">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 13H15M9 17H15M9 9H10M20 21V7.8C20 6.11984 20 5.27976 19.673 4.63803C19.3854 4.07354 18.9265 3.6146 18.362 3.32698C17.7202 3 16.8802 3 15.2 3H8.8C7.11984 3 6.27976 3 5.63803 3.32698C5.07354 3.6146 4.6146 4.07354 4.32698 4.63803C4 5.27976 4 6.11984 4 7.8V21L6.75 19L9.25 21L12 19L14.75 21L17.25 19L20 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <p>아직 업로드된 파일이 없습니다</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
    
    <script>
        function updateFileName(input) {
            const fileName = document.getElementById('fileName');
            if (input.files && input.files[0]) {
                fileName.textContent = '선택된 파일: ' + input.files[0].name;
            } else {
                fileName.textContent = '선택된 파일 없음';
            }
        }
        
        function copyLink(link) {
            navigator.clipboard.writeText(link).then(function() {
                alert('링크가 클립보드에 복사되었습니다!\\n' + link);
            }, function(err) {
                alert('링크 복사 실패: ' + err);
            });
        }
    </script>
</body>
</html>
"""

def get_file_size(size_bytes):
    """파일 크기를 읽기 쉬운 형식으로 변환"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

@app.route('/', methods=['GET', 'POST'])
def index():
    """메인 페이지 - 파일 업로드 및 목록 표시"""
    message = None
    message_type = None
    
    # 업로드된 파일 목록 가져오기
    files = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({
                    'name': filename,
                    'size': get_file_size(stat.st_size),
                    'time': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
    
    # 최신 파일부터 표시
    files.sort(key=lambda x: x['time'], reverse=True)
    
    return render_template_string(HTML_TEMPLATE, files=files, message=message, message_type=message_type)

@app.route('/download/<filename>')
def download_file(filename):
    """파일 다운로드"""
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return f"파일을 찾을 수 없습니다: {str(e)}", 404

if __name__ == '__main__':
    print("=" * 60)
    print(f"업로드 폴더: {os.path.abspath(UPLOAD_FOLDER)}")
    print("=" * 60)
    print("서버 주소: http://localhost:5000")
    print("네트워크 접근: http://0.0.0.0:5000")
    print("다운로드 링크: http://localhost:5000/download/[파일명]")
    print("=" * 60)
    print("종료하려면 Ctrl+C를 누르세요")
    print("=" * 60)
    
    # 서버 실행 (모든 네트워크 인터페이스에서 접근 가능)
    app.run(host='0.0.0.0', port=5000, debug=True)