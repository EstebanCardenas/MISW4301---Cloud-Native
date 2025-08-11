package port

import (
	"time"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/google/uuid"
)

type TokenPayload struct {
	ID uuid.UUID
}

type CreateTokenResponse struct {
	Token    string
	ExpireAt time.Time
}

type TokenService interface {
	// CreateToken creates a new token for a given user
	CreateToken(user *domain.User) (*CreateTokenResponse, error)
	// VerifyToken verifies the token and returns the payload
	VerifyToken(token string) (*TokenPayload, error)
}
