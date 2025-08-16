package auth

import (
	"context"
	"time"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/google/uuid"
)

type TokenService struct {
	userRepo port.UserRepository
}

func NewTokenService(userRepo port.UserRepository) *TokenService {
	return &TokenService{userRepo: userRepo}
}

func (service *TokenService) VerifyToken(token string) (*uuid.UUID, error) {
	id, err := uuid.Parse(token)
	if err != nil {
		return nil, domain.ErrInvalidToken
	}

	user, err := service.userRepo.GetUserById(context.Background(), id)
	if err != nil {
		return nil, err
	}

	if user.ExpireAt != nil {
		expireAt := *user.ExpireAt
		if time.Now().After(expireAt) {
			return nil, domain.ErrExpiredToken
		}
	}

	return &id, nil
}
