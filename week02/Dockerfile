FROM python:3.10-slim

RUN apt-get update && apt-get install -y curl wget net-tools ssh telnet tcpdump && rm -rf /var/lib/apt/lists/*


WORKDIR /app

RUN echo '#!/bin/sh' > /entrypoint.sh && echo 'tcpdump -i eth0 -U -w /app/out.pcap -c 10 tcp &' >> /entrypoint.sh && echo 'curl --max-time 5 http://www.google.com' >> /entrypoint.sh && echo 'wait' >> /entrypoint.sh && chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
