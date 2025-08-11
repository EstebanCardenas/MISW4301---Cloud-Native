package auth

import (
	"time"

	"aidanwoods.dev/go-paseto"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/google/uuid"
)

/**
 * PasetoToken implements port.TokenService interface
 * and provides an access to the paseto library
 */
type PasetoToken struct {
	token    *paseto.Token
	key      *paseto.V4SymmetricKey
	parser   *paseto.Parser
	duration time.Duration
}

// New creates a new paseto instance
func NewTokenService() port.TokenService {
	duration := 48 * time.Hour

	token := paseto.NewToken()
	key := paseto.NewV4SymmetricKey()
	parser := paseto.NewParser()

	return &PasetoToken{
		&token,
		&key,
		&parser,
		duration,
	}
}

// CreateToken creates a new paseto token
func (pt *PasetoToken) CreateToken(user *domain.User) (*port.CreateTokenResponse, error) {
	id, err := uuid.NewRandom()
	if err != nil {
		return nil, domain.ErrTokenCreation
	}

	payload := &port.TokenPayload{
		ID: id,
	}

	err = pt.token.Set("payload", payload)
	if err != nil {
		return nil, domain.ErrTokenCreation
	}

	issuedAt := time.Now()
	expiredAt := issuedAt.Add(pt.duration)

	pt.token.SetIssuedAt(issuedAt)
	pt.token.SetNotBefore(issuedAt)
	pt.token.SetExpiration(expiredAt)

	token := pt.token.V4Encrypt(*pt.key, nil)

	return &port.CreateTokenResponse{
		Token:    token,
		ExpireAt: expiredAt,
	}, nil
}

// VerifyToken verifies the paseto token
func (pt *PasetoToken) VerifyToken(token string) (*port.TokenPayload, error) {
	var payload *port.TokenPayload

	parsedToken, err := pt.parser.ParseV4Local(*pt.key, token, nil)
	if err != nil {
		if err.Error() == "this token has expired" {
			return nil, domain.ErrExpiredToken
		}
		return nil, domain.ErrInvalidToken
	}

	err = parsedToken.Get("payload", &payload)
	if err != nil {
		return nil, domain.ErrInvalidToken
	}

	return payload, nil
}
