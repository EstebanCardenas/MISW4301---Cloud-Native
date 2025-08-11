package port

import (
	"context"
	"time"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
)

type CreateUserRequest struct {
	Username    string
	Password    string
	Email       string
	Dni         *string
	FullName    *string
	PhoneNumber *string
}

func (req *CreateUserRequest) ToDomainModel() *domain.User {
	return &domain.User{
		Username:    req.Username,
		Email:       req.Email,
		PhoneNumber: req.PhoneNumber,
		Dni:         req.Dni,
		FullName:    req.FullName,
		Password:    req.Password,
		Status:      domain.NotVerified,
	}
}

type CreateUserResponse struct {
	Id        uint
	CreatedAt time.Time
}

type UpdateUserRequest struct {
	FullName    string
	PhoneNumber string
	Dni         string
	Status      *domain.UserStatus
}

type UserService interface {
	CreateUser(ctx context.Context, request *CreateUserRequest) (*CreateUserResponse, error)
	UpdateUser(ctx context.Context, userId int, request *UpdateUserRequest) error
}

type UserRepository interface {
	CreateUser(ctx context.Context, user *domain.User) error
	UpdateUser(ctx context.Context, userId int, user *UpdateUserRequest) error
	GetUserByUsername(ctx context.Context, username string) (*domain.User, error)
	SaveUserToken(ctx context.Context, id uint, tokenResponse *CreateTokenResponse) error
}
