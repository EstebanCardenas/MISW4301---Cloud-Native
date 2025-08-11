package repository

import (
	"context"
	"fmt"
	"log/slog"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/data/postgres/models"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"gorm.io/gorm"
)

type UserRepository struct {
	DB *gorm.DB
}

func NewUserRepository(db *gorm.DB) (*UserRepository, error) {
	err := db.AutoMigrate(&models.User{})
	if err != nil {
		return nil, err
	}

	return &UserRepository{db}, nil
}

func (repo *UserRepository) CreateUser(ctx context.Context, user *domain.User) error {
	// Validations
	var usernameCount int64
	repo.DB.Model(&models.User{}).Where("username = ?", user.Username).Count(&usernameCount)
	if usernameCount > 0 {
		return domain.ErrUsernameOrEmailExists
	}
	var emailCount int64
	repo.DB.Model(&models.User{}).Where("email = ?", user.Email).Count(&emailCount)
	if emailCount > 0 {
		return domain.ErrUsernameOrEmailExists
	}

	// Create user in DB
	userModel := models.User{
		Username: user.Username,
		Password: user.Password,
		Email:    user.Email,
		Salt:     user.Salt,
		Status:   user.Status,
	}
	if user.Dni != nil {
		dni := fmt.Sprint(*user.Dni)
		userModel.Dni = &dni
	}
	if user.FullName != nil {
		fullName := fmt.Sprint(*user.FullName)
		userModel.FullName = &fullName
	}
	if user.PhoneNumber != nil {
		phoneNumber := fmt.Sprint(*user.PhoneNumber)
		userModel.PhoneNumber = &phoneNumber
	}

	ctxBackground := context.Background()
	err := gorm.G[models.User](repo.DB).Create(
		ctxBackground,
		&userModel,
	)
	if err != nil {
		return err
	}
	user.Id = userModel.ID
	user.CreatedAt = userModel.CreatedAt

	return nil
}

func (repo *UserRepository) UpdateUser(ctx context.Context, userId int, request *port.UpdateUserRequest) error {
	var userCount int64
	slog.Info("User id", "id", userId)
	repo.DB.Model(&models.User{}).Where("id = ?", userId).Count(&userCount)
	if userCount == 0 {
		return domain.ErrUserDoesNotExist
	}

	userModel := models.User{}
	userModel.ID = uint(userId)
	repo.DB.First(&userModel)
	if request.Status != nil {
		userModel.Status = *request.Status
	}
	if request.Dni != "" {
		userModel.Dni = &request.Dni
	}
	if request.FullName != "" {
		userModel.FullName = &request.FullName
	}
	if request.PhoneNumber != "" {
		userModel.PhoneNumber = &request.PhoneNumber
	}
	repo.DB.Save(&userModel)

	return nil
}

func (repo *UserRepository) GetUserByUsername(ctx context.Context, username string) (*domain.User, error) {
	var userModel models.User
	result := repo.DB.Where("username = ?", username).First(&userModel)
	if result.Error != nil {
		if result.Error == gorm.ErrRecordNotFound {
			return nil, domain.ErrUserDoesNotExist
		}
		return nil, result.Error
	}

	domainUser := userModel.ToDomainModel()
	return domainUser, nil
}

func (repo *UserRepository) SaveUserToken(ctx context.Context, id uint, tokenResponse *port.CreateTokenResponse) error {
	var userModel models.User
	result := repo.DB.Where("id = ?", id).First(&userModel)
	if err := result.Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return domain.ErrUserDoesNotExist
		}
		return err
	}

	userModel.Token = &tokenResponse.Token
	userModel.ExpireAt = &tokenResponse.ExpireAt
	saveRes := repo.DB.Save(&userModel)
	if err := saveRes.Error; err != nil {
		return err
	}

	return nil
}
