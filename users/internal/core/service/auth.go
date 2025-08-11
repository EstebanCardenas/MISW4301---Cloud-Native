package service

import (
	"context"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/service/util"
)

type AuthService struct {
	userRepo     port.UserRepository
	tokenService port.TokenService
}

func NewAuthService(repo port.UserRepository, tokenService port.TokenService) *AuthService {
	return &AuthService{repo, tokenService}
}

func (service *AuthService) Login(ctx context.Context, req *port.LoginRequest) (*port.LoginResponse, error) {
	if req.Username == "" || req.Password == "" {
		return nil, domain.ErrInvalidLoginPayload
	}

	user, err := service.userRepo.GetUserByUsername(ctx, req.Username)
	if err != nil {
		return nil, err
	}

	err = util.ComparePassword(req.Password, user.Password)
	if err != nil {
		return nil, domain.ErrUserDoesNotExist
	}

	tokenRes, err := service.tokenService.CreateToken(user)
	if err != nil {
		return nil, err
	}

	err = service.userRepo.SaveUserToken(ctx, user.Id, tokenRes)
	if err != nil {
		return nil, err
	}

	return &port.LoginResponse{
		Id:       user.Id,
		Token:    tokenRes.Token,
		ExpireAt: &tokenRes.ExpireAt,
	}, nil
}
