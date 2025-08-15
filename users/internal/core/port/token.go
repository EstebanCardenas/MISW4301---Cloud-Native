package port

import "github.com/google/uuid"

type TokenService interface {
	// VerifyToken verifies the token and returns the payload
	VerifyToken(token string) (*uuid.UUID, error)
}
