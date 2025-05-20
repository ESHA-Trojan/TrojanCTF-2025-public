FROM golang:latest@sha256:39d9e7d9c5d9c9e4baf0d8fff579f06d5032c0f4425cdec9e86732e8e4e374dc AS app
WORKDIR /app
COPY ./go.mod ./typed_proto.go flag.txt ./
RUN CGO_ENABLED=0 GOOS=linux go build -o run

FROM eshatrojan/jail
COPY --from=app / /srv
ENV JAIL_MEM=20M