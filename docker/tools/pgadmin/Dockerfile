FROM dpage/pgadmin4

COPY entrypoint.sh /entrypoint.sh
COPY servers.json.template /servers.json.template
COPY pgpass.template /pgpass.template

RUN chmod +x /entrypoint.sh

USER root
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 80
