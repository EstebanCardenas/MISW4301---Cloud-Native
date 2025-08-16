# HTTP handlers test
go test -cover ./internal/adapter/handler/http/
# Service test (business logic)
go test -cover ./internal/core/service/
# Repository test (data layer)
go test -cover ./internal/adapter/data/postgres/repository/
