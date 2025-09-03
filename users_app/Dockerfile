# Stage 1: Build the Go application
FROM golang:1.24 AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/bin/app ./cmd/http/main.go

# Stage 2: Create a minimal production image
FROM alpine:3.20

WORKDIR /app

# Copy the built binary from the builder stage
COPY --from=builder /app/bin/app ./bin/app

EXPOSE 3000

CMD ["/app/bin/app"]
