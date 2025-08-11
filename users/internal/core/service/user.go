package service

import (
	"context"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/service/util"
	"github.com/hashicorp/go-set/v3"
)

type UserService struct {
	userRepo port.UserRepository
}

func NewUserService(
	repo port.UserRepository,
) *UserService {
	return &UserService{
		userRepo: repo,
	}
}

func (userService *UserService) CreateUser(ctx context.Context, request *port.CreateUserRequest) (*port.CreateUserResponse, error) {
	if request.Username == "" || request.Password == "" || request.Email == "" {
		return nil, domain.ErrInvalidCreateUserPayload
	}

	user := request.ToDomainModel()

	hasedPwd, salt, err := util.HashPassword(user.Password)
	if err != nil {
		return nil, domain.ErrInternal
	}
	user.Password = hasedPwd
	user.Salt = salt

	err = userService.userRepo.CreateUser(ctx, user)
	if err != nil {
		return nil, err
	}

	res := &port.CreateUserResponse{
		Id:        user.Id,
		CreatedAt: user.CreatedAt,
	}

	return res, nil
}

func (userService *UserService) UpdateUser(ctx context.Context, userId int, request *port.UpdateUserRequest) error {
	if request.Dni == "" && request.FullName == "" && request.PhoneNumber == "" && request.Status == nil {
		return domain.ErrInvalidUpdateUserPayload
	}

	if request.Status != nil {
		status := *request.Status
		userStatusSet := set.From(domain.UserStatusValues)
		if !userStatusSet.Contains(status) {
			return domain.ErrInvalidUserStatus
		}
	}

	err := userService.userRepo.UpdateUser(ctx, userId, request)
	if err != nil {
		return err
	}

	return nil
}
