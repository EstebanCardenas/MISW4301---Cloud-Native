package domain

import "errors"

var (
	ErrInternal                 = errors.New("internal server error")
	ErrInvalidCreateUserPayload = errors.New("invalid create user payload")
	ErrUsernameOrEmailExists    = errors.New("user with given username or email already exists")
	ErrTokenCreation            = errors.New("failed to create token")
	ErrExpiredToken             = errors.New("token is expired")
	ErrInvalidToken             = errors.New("token is invalid")
	ErrInvalidUpdateUserPayload = errors.New("update user payload doesn't contain any of the expected fields")
	ErrUserDoesNotExist         = errors.New("user does not exist")
	ErrInvalidUserStatus        = errors.New("user status is invalid")
	ErrInvalidLoginPayload      = errors.New("invalid login payload")
	ErrUserPendingVerify        = errors.New("user is pending for verification")
	ErrUserNotVerified          = errors.New("user is not verified")
	ErrInvalidVerifyToken       = errors.New("invalid verify token")
)
