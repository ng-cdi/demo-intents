FROM willfantom/mininet:ngcdi

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT /entrypoint.sh
