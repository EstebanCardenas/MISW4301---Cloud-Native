package mock

import (
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
)

type MockPasetoToken struct {
	CreateTokenFunc func(user *domain.User) (*port.CreateTokenResponse, error)
	VerifyTokenFunc func(token string) (*port.TokenPayload, error)
}

func (m *MockPasetoToken) CreateToken(user *domain.User) (*port.CreateTokenResponse, error) {
	return m.CreateTokenFunc(user)
}

func (m *MockPasetoToken) VerifyToken(token string) (*port.TokenPayload, error) {
	return m.VerifyTokenFunc(token)
}
