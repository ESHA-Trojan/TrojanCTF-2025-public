FROM python:3.11-slim AS prod

WORKDIR /app/
RUN useradd --system runner

COPY --chown=runner:runner requirements.txt requirements.txt
RUN pip install -r requirements.txt && pip install waitress

USER runner

COPY --chown=runner:runner blockchain.py blockchain.py

EXPOSE 5000

CMD ["waitress-serve", "--host", "0.0.0.0", "--port=5000", "blockchain:app"]
