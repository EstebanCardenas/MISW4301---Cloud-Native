package models

import (
	"time"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/google/uuid"
)

type User struct {
	ID          uuid.UUID `gorm:"type:uuid"`
	Username    string
	Email       string
	PhoneNumber *string
	Dni         *string
	FullName    *string
	Password    string
	Salt        string
	Token       *uuid.UUID
	Status      domain.UserStatus
	ExpireAt    *time.Time
	CreatedAt   time.Time
	UpdatedAt   time.Time
}

func (user *User) ToDomainModel() *domain.User {
	return &domain.User{
		Id:          user.ID,
		Username:    user.Username,
		Email:       user.Email,
		PhoneNumber: user.PhoneNumber,
		Dni:         user.Dni,
		FullName:    user.FullName,
		Password:    user.Password,
		Salt:        user.Salt,
		Token:       user.Token,
		Status:      user.Status,
		ExpireAt:    user.ExpireAt,
		CreatedAt:   user.CreatedAt,
		UpdatedAt:   user.UpdatedAt,
	}
}
