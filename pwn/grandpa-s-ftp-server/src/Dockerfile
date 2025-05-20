FROM alpine:3.18 AS builder

RUN apk add --no-cache build-base

WORKDIR /src

COPY ./lftpd .

RUN make

FROM alpine:3.18

RUN apk add --no-cache tini

COPY --from=builder /src/lftpd /usr/local/bin/lftpd

EXPOSE 2121

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["lftpd"]
