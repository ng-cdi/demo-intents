FROM willfantom/mininet:ngcdi

RUN   sed -i -e's/ main/ main contrib non-free/g' /etc/apt/sources.list && \
	apt-get  update && \
	apt-get -y dist-upgrade && \
    apt-get install -y --no-install-recommends curl dynamips dynagen \
	bridge-utils

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT /entrypoint.sh
