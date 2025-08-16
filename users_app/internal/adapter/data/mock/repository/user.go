package repository

import (
	"context"
	"time"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/google/uuid"
)

type MockUserRepository struct {
	CreateUserFunc        func(ctx context.Context, user *domain.User) error
	UpdateUserFunc        func(ctx context.Context, userId uuid.UUID, user *port.UpdateUserRequest) error
	GetUserByUsernameFunc func(ctx context.Context, username string) (*domain.User, error)
	GetUserByIdFunc       func(ctx context.Context, userId uuid.UUID) (*domain.User, error)
	SaveUserTokenFunc     func(ctx context.Context, id uuid.UUID) (time.Time, error)
	GetUserCountFunc      func(ctx context.Context) (uint, error)
	ResetUsersFunc        func(ctx context.Context) error
}

func (m *MockUserRepository) CreateUser(ctx context.Context, user *domain.User) error {
	return m.CreateUserFunc(ctx, user)
}

func (m *MockUserRepository) UpdateUser(ctx context.Context, userId uuid.UUID, user *port.UpdateUserRequest) error {
	return m.UpdateUserFunc(ctx, userId, user)
}

func (m *MockUserRepository) GetUserByUsername(ctx context.Context, username string) (*domain.User, error) {
	return m.GetUserByUsernameFunc(ctx, username)
}

func (m *MockUserRepository) GetUserById(ctx context.Context, userId uuid.UUID) (*domain.User, error) {
	return m.GetUserByIdFunc(ctx, userId)
}

func (m *MockUserRepository) SaveUserToken(ctx context.Context, id uuid.UUID) (time.Time, error) {
	return m.SaveUserTokenFunc(ctx, id)
}

func (m *MockUserRepository) GetUserCount(ctx context.Context) (uint, error) {
	return m.GetUserCountFunc(ctx)
}

func (m *MockUserRepository) ResetUsers(ctx context.Context) error {
	return m.ResetUsersFunc(ctx)
}
