FROM golang:1.24

WORKDIR /app
COPY . .
RUN go mod download
RUN go build -o bin/app cmd/http/main.go

EXPOSE 3000

CMD ["/app/bin/app"]
