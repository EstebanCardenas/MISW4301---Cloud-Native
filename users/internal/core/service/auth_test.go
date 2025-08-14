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
)

func TestAuthService_Login_Success(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		GetUserByUsernameFunc: func(ctx context.Context, user string) (*domain.User, error) {
			return &domain.User{
				Id:       1,
				Password: "testpasshash",
			}, nil
		},
		SaveUserTokenFunc: func(ctx context.Context, id uint, tokenResponse *port.CreateTokenResponse) error {
			return nil
		},
	}
	mockToken := &mockAuth.MockPasetoToken{
		CreateTokenFunc: func(user *domain.User) (*port.CreateTokenResponse, error) {
			return &port.CreateTokenResponse{
				Token:    "mytoken",
				ExpireAt: time.Now().Add(time.Hour * 4),
			}, nil
		},
	}
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
	res, err := authService.Login(t.Context(), req)
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if res.Token == "" {
		t.Fatalf("expected a token, got empty string")
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
				Id:       1,
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

func TestAuthService_Login_TokenCreationError(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		GetUserByUsernameFunc: func(ctx context.Context, user string) (*domain.User, error) {
			return &domain.User{
				Id:       1,
				Password: "testpasshash",
			}, nil
		},
	}
	mockToken := &mockAuth.MockPasetoToken{
		CreateTokenFunc: func(user *domain.User) (*port.CreateTokenResponse, error) {
			return nil, context.DeadlineExceeded
		},
	}
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
	if err != context.DeadlineExceeded {
		t.Fatalf("expected token creation error, got %v", err)
	}
}

func TestAuthService_Login_SaveTokenError(t *testing.T) {
	mockRepo := &repository.MockUserRepository{
		GetUserByUsernameFunc: func(ctx context.Context, user string) (*domain.User, error) {
			return &domain.User{
				Id:       1,
				Password: "testpasshash",
			}, nil
		},
		SaveUserTokenFunc: func(ctx context.Context, id uint, tokenResponse *port.CreateTokenResponse) error {
			return context.Canceled
		},
	}
	mockToken := &mockAuth.MockPasetoToken{
		CreateTokenFunc: func(user *domain.User) (*port.CreateTokenResponse, error) {
			return &port.CreateTokenResponse{
				Token:    "mytoken",
				ExpireAt: time.Now().Add(time.Hour * 4),
			}, nil
		},
	}
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
