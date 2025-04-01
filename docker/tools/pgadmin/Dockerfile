FROM dpage/pgadmin4

COPY pgpass /pgpass
COPY servers.json /pgadmin4/servers.json

USER root

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 80