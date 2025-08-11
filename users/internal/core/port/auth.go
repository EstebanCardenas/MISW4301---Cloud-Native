package port

import (
	"context"
	"time"
)

type LoginRequest struct {
	Username string
	Password string
}

type LoginResponse struct {
	Id       uint
	Token    string
	ExpireAt *time.Time
}

type AuthService interface {
	Login(ctx context.Context, req *LoginRequest) (*LoginResponse, error)
}
