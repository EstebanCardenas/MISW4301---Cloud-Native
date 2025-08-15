package domain

import (
	"time"

	"github.com/google/uuid"
)

type UserStatus string

const (
	PendingVerify UserStatus = "POR_VERIFICAR"
	NotVerified   UserStatus = "NO_VERIFICADO"
	Verified      UserStatus = "VERIFICADO"
)

var UserStatusValues = []UserStatus{
	PendingVerify, NotVerified, Verified,
}

type User struct {
	Id          uuid.UUID
	Username    string
	Email       string
	PhoneNumber *string
	Dni         *string
	FullName    *string
	Password    string
	Salt        string
	Token       *uuid.UUID
	Status      UserStatus
	ExpireAt    *time.Time
	CreatedAt   time.Time
	UpdatedAt   time.Time
}
