FROM golang:1.24

WORKDIR /app
COPY . .
RUN go mod download
RUN go build -o bin/app cmd/http/main.go
CMD ["/app/bin/app"]
