package service

import (
	"context"
	"fmt"
	"log/slog"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/google/uuid"
	"github.com/hashicorp/go-set/v3"
)

type UserService struct {
	userRepo            port.UserRepository
	hashService         port.HashService
	notificationsClient port.NotificationsClient
}

func NewUserService(
	repo port.UserRepository,
	hashService port.HashService,
	notificationsClient port.NotificationsClient,
) *UserService {
	return &UserService{
		userRepo:            repo,
		hashService:         hashService,
		notificationsClient: notificationsClient,
	}
}

func (userService *UserService) CreateUser(ctx context.Context, request *port.CreateUserRequest) (*port.CreateUserResponse, error) {
	if request.Username == "" || request.Password == "" || request.Email == "" {
		return nil, domain.ErrInvalidCreateUserPayload
	}

	user := request.ToDomainModel()
	user.Status = domain.PendingVerify

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

	// Create verification request
	payload := port.VerificationRequestPayload{
		User: struct {
			Email    string
			Dni      *string
			FullName *string
			Phone    *string
		}{
			Email:    user.Email,
			Dni:      user.Dni,
			FullName: user.FullName,
			Phone:    user.PhoneNumber,
		},
		TransactionIdentifier: uuid.NewString(),
		UserIdentifier:        user.Id.String(),
		UserWebHook:           request.UpdateUserWebhookUrl,
	}
	err = userService.userRepo.CreateVerificationRequest(ctx, &payload)
	if err != nil {
		return nil, err
	}

	res := &port.CreateUserResponse{
		Id:        user.Id,
		CreatedAt: user.CreatedAt,
	}

	return res, nil
}

func (userService *UserService) UpdateUser(ctx context.Context, userId uuid.UUID, request *port.UpdateUserRequest) error {
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

func (userService *UserService) UpdateUserStatus(
	ctx context.Context,
	secretToken string,
	request *port.UpdateUserStatusRequest,
) error {
	// Verify token
	token := fmt.Sprintf(
		"%s:%s:%v",
		secretToken, request.RUV, request.Score,
	)
	sha_token := userService.hashService.Hash256(token)
	if sha_token != request.VerifyToken {
		return domain.ErrInvalidVerifyToken
	}

	// Perform update
	updateUserRequest := port.UpdateUserRequest{
		Status: (*domain.UserStatus)(&request.Status),
	}
	userId, _ := uuid.Parse(request.UserIdentifier)
	err := userService.UpdateUser(ctx, userId, &updateUserRequest)
	if err != nil {
		return err
	}

	// Send result email
	userUuid, _ := uuid.Parse(request.UserIdentifier)
	user, err := userService.QueryMyself(ctx, userUuid)
	if err != nil {
		return err
	}

	var fullName string
	if user.FullName != nil {
		fullName = *user.FullName
	}
	var dni string
	if user.Dni != nil {
		dni = *user.Dni
	}
	var phone string
	if user.PhoneNumber != nil {
		phone = *user.PhoneNumber
	}
	notifRequest := port.SendNotificationRequest{
		Template: "rf-007",
		To:       user.Email,
		Subject:  "Resultado del proceso de verificación",
		Data: port.NotificationRequestData{
			FinalState:  domain.UserStatus(request.Status),
			RUV:         request.RUV,
			FullName:    fullName,
			DNI:         dni,
			PhoneNumber: phone,
		},
	}
	err = userService.notificationsClient.SendNotification(&notifRequest)
	if err != nil {
		slog.Error("Failed to send email notification", "error", err)
		return err
	}

	return nil
}

func (userServcie *UserService) QueryMyself(ctx context.Context, userId uuid.UUID) (*domain.User, error) {
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
