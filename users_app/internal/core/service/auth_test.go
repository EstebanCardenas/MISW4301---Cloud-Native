package service

import (
	"context"
	"testing"
	"time"

	mockAuth "github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/auth/mock"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/data/mock/repository"
	mockHash "github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/hash/mock"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/google/uuid"
)

func TestAuthService_Login_Success(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		GetUserByUsernameFunc: func(ctx context.Context, user string) (*domain.User, error) {
			return &domain.User{
				Id:       uuid.New(),
				Password: "testpasshash",
			}, nil
		},
		SaveUserTokenFunc: func(ctx context.Context, id uuid.UUID) (time.Time, error) {
			return time.Now().Add(time.Hour * 4), nil
		},
	}
	mockToken := &mockAuth.MockTokenService{}
	mockHash := &mockHash.MockHashService{
		ComparePasswordFunc: func(password string, hashedPassword string) error {
			return nil
		},
	}
	authService := NewAuthService(mockRepo, mockToken, mockHash)
	req := &port.LoginRequest{
		Username: "testuser",
		Password: "testpass",
	}
	_, err := authService.Login(t.Context(), req)
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
}

func TestAuthService_Login_InvalidPayload(t *testing.T) {
	authService := NewAuthService(nil, nil, nil)
	req := &port.LoginRequest{
		Username: "",
		Password: "",
	}
	_, err := authService.Login(context.Background(), req)
	if err != domain.ErrInvalidLoginPayload {
		t.Fatalf("expected ErrInvalidLoginPayload, got %v", err)
	}
}

func TestAuthService_Login_UserNotFound(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		GetUserByUsernameFunc: func(ctx context.Context, user string) (*domain.User, error) {
			return nil, domain.ErrUserDoesNotExist
		},
	}
	authService := NewAuthService(mockRepo, nil, nil)
	req := &port.LoginRequest{
		Username: "notfound",
		Password: "irrelevant",
	}
	_, err := authService.Login(context.Background(), req)
	if err != domain.ErrUserDoesNotExist {
		t.Fatalf("expected ErrUserDoesNotExist, got %v", err)
	}
}

func TestAuthService_Login_PasswordMismatch(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		GetUserByUsernameFunc: func(ctx context.Context, user string) (*domain.User, error) {
			return &domain.User{
				Id:       uuid.New(),
				Password: "hashedpass",
			}, nil
		},
	}
	mockHash := &mockHash.MockHashService{
		ComparePasswordFunc: func(password string, hashedPassword string) error {
			return domain.ErrUserDoesNotExist
		},
	}
	authService := NewAuthService(mockRepo, nil, mockHash)
	req := &port.LoginRequest{
		Username: "testuser",
		Password: "wrongpass",
	}
	_, err := authService.Login(context.Background(), req)
	if err != domain.ErrUserDoesNotExist {
		t.Fatalf("expected ErrUserDoesNotExist, got %v", err)
	}
}

func TestAuthService_Login_SaveTokenError(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		GetUserByUsernameFunc: func(ctx context.Context, user string) (*domain.User, error) {
			return &domain.User{
				Id:       uuid.New(),
				Password: "testpasshash",
			}, nil
		},
		SaveUserTokenFunc: func(ctx context.Context, id uuid.UUID) (time.Time, error) {
			return time.Time{}, context.Canceled
		},
	}
	mockToken := &mockAuth.MockTokenService{}
	mockHash := &mockHash.MockHashService{
		ComparePasswordFunc: func(password string, hashedPassword string) error {
			return nil
		},
	}
	authService := NewAuthService(mockRepo, mockToken, mockHash)
	req := &port.LoginRequest{
		Username: "testuser",
		Password: "testpass",
	}
	_, err := authService.Login(context.Background(), req)
	if err != context.Canceled {
		t.Fatalf("expected SaveUserToken error, got %v", err)
	}
}
