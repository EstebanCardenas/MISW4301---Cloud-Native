package mock

import (
	"github.com/google/uuid"
)

type MockTokenService struct {
	VerifyTokenFunc func(token string) (*uuid.UUID, error)
}

func (m *MockTokenService) VerifyToken(token string) (*uuid.UUID, error) {
	return m.VerifyTokenFunc(token)
}
