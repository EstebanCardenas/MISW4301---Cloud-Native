package mock

import (
	"context"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
)

type MockAuthService struct {
	LoginFunc func(ctx context.Context, req *port.LoginRequest) (*port.LoginResponse, error)
}

func (m *MockAuthService) Login(ctx context.Context, req *port.LoginRequest) (*port.LoginResponse, error) {
	return m.LoginFunc(ctx, req)
}
