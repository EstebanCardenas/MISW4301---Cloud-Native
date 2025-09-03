# --- Stage 1: Build the Go application ---
FROM golang:1.24-alpine AS builder

WORKDIR /app

# Copy the go.mod and go.sum files first to cache dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy the rest of the application source code
COPY . .

# Build the Go application
# CGO_ENABLED=0 is important for creating a statically linked binary
# that can run in the minimal Alpine image
RUN CGO_ENABLED=0 go build -o /app/bin/app ./main.go

# --- Stage 2: Create a minimal runtime image ---
FROM alpine:3.19

# Set the working directory
WORKDIR /app

# Copy the binary from the 'builder' stage
COPY --from=builder /app/bin/app ./bin/app

# Expose the port
EXPOSE 3000

# Run the binary
CMD ["/app/bin/app"]
