FROM ubuntu:22.04

RUN apt-get update && apt-get install -y ffmpeg python3 curl vim && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

EXPOSE 8080

CMD ["/bin/bash"]
