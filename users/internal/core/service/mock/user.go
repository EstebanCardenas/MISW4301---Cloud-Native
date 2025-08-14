package mock

import (
	"context"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
)

type MockUserService struct {
	CreateUserFunc   func(ctx context.Context, request *port.CreateUserRequest) (*port.CreateUserResponse, error)
	UpdateUserFunc   func(ctx context.Context, userId int, request *port.UpdateUserRequest) error
	QueryMyselfFunc  func(ctx context.Context, userId uint) (*domain.User, error)
	GetUserCountFunc func(ctx context.Context) (uint, error)
	ResetUsersFunc   func(ctx context.Context) error
}

func (m *MockUserService) CreateUser(ctx context.Context, request *port.CreateUserRequest) (*port.CreateUserResponse, error) {
	return m.CreateUserFunc(ctx, request)
}
func (m *MockUserService) UpdateUser(ctx context.Context, userId int, request *port.UpdateUserRequest) error {
	return m.UpdateUserFunc(ctx, userId, request)
}
func (m *MockUserService) QueryMyself(ctx context.Context, userId uint) (*domain.User, error) {
	return m.QueryMyselfFunc(ctx, userId)
}
func (m *MockUserService) GetUserCount(ctx context.Context) (uint, error) {
	return m.GetUserCountFunc(ctx)
}
func (m *MockUserService) ResetUsers(ctx context.Context) error {
	return m.ResetUsersFunc(ctx)
}
