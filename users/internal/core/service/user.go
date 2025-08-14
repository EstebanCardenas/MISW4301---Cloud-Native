package service

import (
	"context"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/hashicorp/go-set/v3"
)

type UserService struct {
	userRepo    port.UserRepository
	hashService port.HashService
}

func NewUserService(
	repo port.UserRepository,
	hashService port.HashService,
) *UserService {
	return &UserService{
		userRepo:    repo,
		hashService: hashService,
	}
}

func (userService *UserService) CreateUser(ctx context.Context, request *port.CreateUserRequest) (*port.CreateUserResponse, error) {
	if request.Username == "" || request.Password == "" || request.Email == "" {
		return nil, domain.ErrInvalidCreateUserPayload
	}

	user := request.ToDomainModel()

	hasedPwd, salt, err := userService.hashService.HashPassword(user.Password)
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

func (userServcie *UserService) QueryMyself(ctx context.Context, userId uint) (*domain.User, error) {
	user, err := userServcie.userRepo.GetUserById(ctx, userId)
	if err != nil {
		return nil, err
	}

	return user, nil
}

func (userService *UserService) GetUserCount(ctx context.Context) (uint, error) {
	count, err := userService.userRepo.GetUserCount(ctx)
	if err != nil {
		return 0, nil
	}

	return count, nil
}

func (userService *UserService) ResetUsers(ctx context.Context) error {
	err := userService.userRepo.ResetUsers(ctx)
	if err != nil {
		return err
	}

	return nil
}
