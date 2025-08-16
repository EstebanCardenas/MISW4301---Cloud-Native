package port

import (
	"context"
	"time"

	"github.com/google/uuid"
)

type LoginRequest struct {
	Username string
	Password string
}

type LoginResponse struct {
	Id       uuid.UUID
	Token    uuid.UUID
	ExpireAt *time.Time
}

type AuthService interface {
	Login(ctx context.Context, req *LoginRequest) (*LoginResponse, error)
}
