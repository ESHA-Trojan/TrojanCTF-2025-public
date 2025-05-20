FROM python:slim AS app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY keys keys
COPY protocol.py ./run


FROM eshatrojan/jail
COPY --from=app / /srv
# ENV JAIL_MEM=20M 