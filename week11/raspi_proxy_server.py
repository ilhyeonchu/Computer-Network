#!/usr/bin/env python3


import subprocess

from flask import Flask, jsonify

app = Flask(__name__)

# Raspberry Pi 설정
RASPI_HOST = "ilhyeonchu@100.87.116.106"
RASPI_PROJECT_DIR = "/home/ilhyeonchu/Documents/GitHub/Computer-Network/week11/"


def run_ssh_command(command, timeout=10):
    """SSH로 명령 실행"""
    try:
        result = subprocess.run(
            ["ssh", RASPI_HOST, command],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.route("/")
def index():
    """API 정보"""
    return jsonify(
        {
            "service": "Raspberry Pi Proxy Server",
            "endpoints": {
                "/status": "라즈베리파이 상태 확인",
                "/uptime": "가동 시간",
                "/memory": "메모리 사용량",
                "/disk": "디스크 사용량",
                "/files": "프로젝트 파일 목록",
            },
        }
    )


@app.route("/status")
def status():
    """전체 시스템 상태"""
    # 연결 테스트
    test = run_ssh_command("echo 'connected'")

    if not test["success"] or "connected" not in test["stdout"]:
        return jsonify(
            {"connected": False, "error": "Raspberry Pi에 연결할 수 없습니다."}
        )

    # 시스템 정보 수집
    info = {
        "connected": True,
        "hostname": run_ssh_command("hostname")["stdout"].strip(),
        "uptime": run_ssh_command("uptime -p")["stdout"].strip(),
        "memory": run_ssh_command("free -h | grep Mem | awk '{print $3\"/\"$2}'")[
            "stdout"
        ].strip(),
        "disk": run_ssh_command('df -h / | tail -1 | awk \'{print $3"/"$2" ("$5")"}\'')[
            "stdout"
        ].strip(),
        "python_version": run_ssh_command("python3 --version")["stdout"].strip(),
    }

    return jsonify(info)


@app.route("/uptime")
def uptime():
    """가동 시간"""
    result = run_ssh_command("uptime -p")
    return jsonify(result)


@app.route("/memory")
def memory():
    """메모리 사용량"""
    result = run_ssh_command("free -h")
    return jsonify(result)


@app.route("/disk")
def disk():
    """디스크 사용량"""
    result = run_ssh_command("df -h")
    return jsonify(result)


@app.route("/files")
def files():
    """프로젝트 디렉토리 파일 목록"""
    result = run_ssh_command(f"ls -lh {RASPI_PROJECT_DIR}")
    return jsonify(result)


@app.route("/command/<path:cmd>")
def custom_command(cmd):
    """커스텀 명령 실행 (주의: 보안 위험)"""
    result = run_ssh_command(cmd)
    return jsonify(result)


if __name__ == "__main__":
    print("=" * 60)
    print(" Raspberry Pi 로컬 프록시 서버 시작")
    print(f" 연결 대상: {RASPI_HOST}")
    print(" 서버 주소: http://localhost:5000")
    print("=" * 60)
    print("\n사용 가능한 엔드포인트:")
    print("  - http://localhost:5000/status   (전체 상태)")
    print("  - http://localhost:5000/uptime   (가동 시간)")
    print("  - http://localhost:5000/memory   (메모리)")
    print("  - http://localhost:5000/disk     (디스크)")
    print("  - http://localhost:5000/files    (파일 목록)")
    print("\n종료하려면 Ctrl+C를 누르세요.")
    print("=" * 60)

    app.run(host="localhost", port=5000, debug=False)
