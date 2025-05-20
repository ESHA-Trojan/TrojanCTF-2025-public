FROM python:3.12-bookworm AS prod

RUN apt-get -y update && apt-get -y upgrade

WORKDIR /app/
RUN useradd --system runner

COPY --chown=runner:runner requirements.txt requirements.txt
RUN pip install -r requirements.txt

USER runner

COPY --chown=runner:runner app.py app.py
COPY --chown=runner:runner templates/ templates/
COPY --chown=runner:runner static/ static/
COPY --chown=runner:runner instructions.txt instructions.txt
COPY --chown=runner:runner instructions_supervisor.txt instructions_supervisor.txt

EXPOSE 8080
CMD ["waitress-serve", "--threads=8", "--host=0.0.0.0", "app:app"]
