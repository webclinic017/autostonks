FROM golang:1.17-alpine AS builder
LABEL org.opencontainers.image.source=https://github.com/CasualCodersProjects/autostonks
WORKDIR /go/src/app
COPY . . 
RUN go get -d -v ./...
RUN go build -v -o autostonks

FROM alpine:latest
WORKDIR /app
COPY --from=builder /go/src/app/autostonks .
COPY entrypoint.sh .
CMD ["./autostonks"]