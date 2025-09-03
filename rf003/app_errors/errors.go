package app_errors

import "errors"

var (
	ErrInternalServer    = errors.New("internal server error")
	ErrInvalidToken      = errors.New("invalid token")
	ErrInvalidRouteDates = errors.New("invalid route dates")
	ErrInvalidExpireAt   = errors.New("invalid expiration date")
)
