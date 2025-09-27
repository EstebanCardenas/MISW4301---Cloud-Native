package service

import (
	"context"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
)

type AuthService struct {
	userRepo     port.UserRepository
	tokenService port.TokenService
	hashService  port.HashService
}

func NewAuthService(
	repo port.UserRepository,
	tokenService port.TokenService,
	hashService port.HashService,
) *AuthService {
	return &AuthService{
		repo, tokenService, hashService,
	}
}

func (service *AuthService) Login(ctx context.Context, req *port.LoginRequest) (*port.LoginResponse, error) {
	if req.Username == "" || req.Password == "" {
		return nil, domain.ErrInvalidLoginPayload
	}

	user, err := service.userRepo.GetUserByUsername(ctx, req.Username)
	if err != nil {
		return nil, err
	}

	err = service.hashService.ComparePassword(req.Password, user.Password)
	if err != nil {
		return nil, domain.ErrUserDoesNotExist
	}

	if user.Status == domain.PendingVerify { // Check if user has verification pending
		return nil, domain.ErrUserPendingVerify
	}
	if user.Status == domain.NotVerified {
		return nil, domain.ErrUserNotVerified
	}

	expireAt, err := service.userRepo.SaveUserToken(ctx, user.Id)
	if err != nil {
		return nil, err
	}

	return &port.LoginResponse{
		Id:       user.Id,
		Token:    user.Id,
		ExpireAt: &expireAt,
	}, nil
}
