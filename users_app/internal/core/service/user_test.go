package service

import (
	"context"
	"errors"
	"testing"
	"time"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/data/mock/client"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/data/mock/repository"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/hash/mock"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/google/uuid"
)

func TestUserService_CreateUser_Success(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		CreateUserFunc: func(ctx context.Context, user *domain.User) error {
			user.Id = uuid.New()
			user.CreatedAt = time.Now()
			return nil
		},
		CreateVerificationRequestFunc: func(ctx context.Context, payload *port.VerificationRequestPayload) error {
			return nil
		},
	}
	mockHash := &mock.MockHashService{
		HashPasswordFunc: func(password string) (string, string, error) {
			return "hashed", "salt", nil
		},
	}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)
	req := &port.CreateUserRequest{
		Username: "testuser",
		Password: "password",
		Email:    "test@example.com",
	}
	resp, err := service.CreateUser(context.Background(), req)
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if resp == nil {
		t.Fatalf("expected valid response, got %v", resp)
	}
}

func TestUserService_CreateUser_InvalidPayload(t *testing.T) {
	mockRepo := &repository.MockUserRepository{}
	mockHash := &mock.MockHashService{}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)
	req := &port.CreateUserRequest{
		Username: "",
		Password: "",
		Email:    "",
	}
	resp, err := service.CreateUser(context.Background(), req)
	if err == nil {
		t.Fatalf("expected error, got nil")
	}
	if err != domain.ErrInvalidCreateUserPayload {
		t.Fatalf("expected ErrInvalidCreateUserPayload, got %v", err.Error())
	}
	if resp != nil {
		t.Fatalf("expected nil response, got %v", resp)
	}
}

func TestUserService_CreateUser_RepoError(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		CreateUserFunc: func(ctx context.Context, user *domain.User) error {
			return errors.New("repo error")
		},
	}
	mockHash := &mock.MockHashService{
		HashPasswordFunc: func(password string) (string, string, error) {
			return "hashed", "salt", nil
		},
	}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)
	req := &port.CreateUserRequest{
		Username: "testuser",
		Password: "password",
		Email:    "test@example.com",
	}
	resp, err := service.CreateUser(context.Background(), req)
	if err == nil {
		t.Fatalf("expected error, got nil")
	}
	if resp != nil {
		t.Fatalf("expected nil response, got %v", resp)
	}
}

func TestUserService_CreateUser_UserExists(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		CreateUserFunc: func(ctx context.Context, user *domain.User) error {
			return domain.ErrUsernameOrEmailExists
		},
	}
	mockHash := &mock.MockHashService{
		HashPasswordFunc: func(password string) (string, string, error) {
			return "hashed", "salt", nil
		},
	}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)
	req := &port.CreateUserRequest{
		Username: "testuser",
		Password: "password",
		Email:    "test@example.com",
	}
	resp, err := service.CreateUser(context.Background(), req)
	if err == nil {
		t.Fatalf("expected error, got nil")
	}
	if err != domain.ErrUsernameOrEmailExists {
		t.Fatalf("expected ErrUsernameOrEmailExists, got %v", err.Error())
	}
	if resp != nil {
		t.Fatalf("expected nil response, got %v", resp)
	}
}

func TestUserService_UpdateUser_Success(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		UpdateUserFunc: func(ctx context.Context, userId uuid.UUID, req *port.UpdateUserRequest) error {
			return nil
		},
	}
	mockHash := &mock.MockHashService{}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)
	req := &port.UpdateUserRequest{
		FullName:    "Test User",
		PhoneNumber: "123456789",
		Dni:         "123456",
	}
	err := service.UpdateUser(context.Background(), uuid.New(), req)
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
}

func TestUserService_UpdateUser_InvalidPayload(t *testing.T) {
	mockRepo := &repository.MockUserRepository{}
	mockHash := &mock.MockHashService{}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)
	req := &port.UpdateUserRequest{}
	err := service.UpdateUser(context.Background(), uuid.New(), req)
	if err == nil {
		t.Fatalf("expected error, got nil")
	}
	if err != domain.ErrInvalidUpdateUserPayload {
		t.Fatalf("expected ErrInvalidUpdateUserPayload, got %v", err.Error())
	}
}

func TestUserService_UpdateUser_InvalidStatus(t *testing.T) {
	mockRepo := &repository.MockUserRepository{}
	mockHash := &mock.MockHashService{}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)
	status := domain.UserStatus("Unknown Status")
	req := &port.UpdateUserRequest{
		Status: &status,
	}
	err := service.UpdateUser(context.Background(), uuid.New(), req)
	if err == nil {
		t.Fatalf("expected error, got nil")
	}
	if err != domain.ErrInvalidUserStatus {
		t.Fatalf("expected ErrInvalidUserStatus, got %v", err.Error())
	}
}

func TestUserService_UpdateUser_UserNotFound(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		UpdateUserFunc: func(ctx context.Context, userId uuid.UUID, req *port.UpdateUserRequest) error {
			return domain.ErrUserDoesNotExist
		},
	}
	mockHash := &mock.MockHashService{}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)
	req := &port.UpdateUserRequest{
		FullName: "Nonexistent User",
	}
	err := service.UpdateUser(context.Background(), uuid.New(), req)
	if err == nil {
		t.Fatalf("expected error, got nil")
	}
	if err != domain.ErrUserDoesNotExist {
		t.Fatalf("expected ErrUserNotFound, got %v", err)
	}
}

func TestUserService_QueryMyself_Success(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		GetUserByIdFunc: func(ctx context.Context, userId uuid.UUID) (*domain.User, error) {
			return &domain.User{Id: userId, Username: "testuser"}, nil
		},
	}
	mockHash := &mock.MockHashService{}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)
	uuid := uuid.New()
	user, err := service.QueryMyself(context.Background(), uuid)
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if user == nil || user.Id != uuid {
		t.Fatalf("expected user with id 1, got %v", user)
	}
}

func TestUserService_QueryMyself_UserDoesNotExist(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		GetUserByIdFunc: func(ctx context.Context, userId uuid.UUID) (*domain.User, error) {
			return nil, domain.ErrUserDoesNotExist
		},
	}
	mockHash := &mock.MockHashService{}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)
	user, err := service.QueryMyself(context.Background(), uuid.New())
	if err == nil {
		t.Fatalf("expected error, got nil")
	}
	if err != domain.ErrUserDoesNotExist {
		t.Fatalf("expected ErrUserDoesNotExist, got %v", err.Error())
	}
	if user != nil {
		t.Fatalf("expected nil user, got %v", user)
	}
}

func TestUserService_GetUserCount_Success(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		GetUserCountFunc: func(ctx context.Context) (uint, error) {
			return 42, nil
		},
	}
	mockHash := &mock.MockHashService{}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)
	count, err := service.GetUserCount(context.Background())
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if count != 42 {
		t.Fatalf("expected count 42, got %d", count)
	}
}

func TestUserService_GetUserCount_RepoError(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		GetUserCountFunc: func(ctx context.Context) (uint, error) {
			return 0, errors.New("repo error")
		},
	}
	mockHash := &mock.MockHashService{}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)
	count, err := service.GetUserCount(context.Background())
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if count != 0 {
		t.Fatalf("expected count 0, got %d", count)
	}
}

func TestUserService_ResetUsers_Success(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		ResetUsersFunc: func(ctx context.Context) error {
			return nil
		},
	}
	mockHash := &mock.MockHashService{}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)
	err := service.ResetUsers(context.Background())
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
}

func TestUserService_ResetUsers_RepoError(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		ResetUsersFunc: func(ctx context.Context) error {
			return errors.New("repo error")
		},
	}
	mockHash := &mock.MockHashService{}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)
	err := service.ResetUsers(context.Background())
	if err == nil {
		t.Fatalf("expected error, got nil")
	}
}

func TestUserService_UpdateUserStatus_Success(t *testing.T) {
	// Setup
	mockRepo := &repository.MockUserRepository{
		UpdateUserFunc: func(context.Context, uuid.UUID, *port.UpdateUserRequest) error {
			return nil
		},
		CreateVerificationRequestFunc: func(ctx context.Context, payload *port.VerificationRequestPayload) error {
			return nil
		},
		GetUserByIdFunc: func(ctx context.Context, userId uuid.UUID) (*domain.User, error) {
			return &domain.User{
				Email: "myemail@test.com",
			}, nil
		},
	}
	mockHash := &mock.MockHashService{
		HashPasswordFunc: func(password string) (string, string, error) {
			return "hashed", "salt", nil
		},
		Hash256Func: func(string) string {
			return "myhash"
		},
	}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)

	// Act
	request := port.UpdateUserStatusRequest{
		Status:         string(domain.Verified),
		VerifyToken:    "myhash",
		UserIdentifier: uuid.NewString(),
	}
	err := service.UpdateUserStatus(
		t.Context(),
		"secret-token",
		&request,
	)
	if err != nil {
		t.Fatalf("expected nil, got %v", err)
	}
}

func TestUserService_UpdateUserStatus_InvalidToken(t *testing.T) {
	// Setup
	mockRepo := &repository.MockUserRepository{}
	mockHash := &mock.MockHashService{
		Hash256Func: func(string) string {
			return "myhash"
		},
	}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)

	// Act
	request := port.UpdateUserStatusRequest{
		Status:      string(domain.Verified),
		VerifyToken: "another-hash",
	}
	err := service.UpdateUserStatus(
		t.Context(),
		"secret-token",
		&request,
	)
	if err != domain.ErrInvalidVerifyToken {
		t.Fatalf("expected ErrInvalidVerifyToken, got %v", err)
	}
}

func TestUserService_UpdateUserStatus_UpdateUserFail(t *testing.T) {
	// Setup
	myErr := errors.New("update user error")
	mockRepo := &repository.MockUserRepository{
		UpdateUserFunc: func(context.Context, uuid.UUID, *port.UpdateUserRequest) error {
			return myErr
		},
	}
	mockHash := &mock.MockHashService{
		Hash256Func: func(string) string {
			return "myhash"
		},
	}
	notifsClient := client.MockNotificationsClient{}
	service := NewUserService(mockRepo, mockHash, &notifsClient)

	// Act
	request := port.UpdateUserStatusRequest{
		Status:      string(domain.Verified),
		VerifyToken: "myhash",
	}
	err := service.UpdateUserStatus(
		t.Context(),
		"secret-token",
		&request,
	)
	if err != myErr {
		t.Fatalf("expected %v, got %v", myErr, err)
	}
}
