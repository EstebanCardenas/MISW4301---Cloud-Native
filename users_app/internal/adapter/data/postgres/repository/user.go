package repository

import (
	"context"
	"fmt"
	"time"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/data/postgres/models"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

type UserRepository struct {
	DB                 *gorm.DB
	VerificationClient port.VerificationClient
}

func NewUserRepository(
	db *gorm.DB,
	verificationClient port.VerificationClient,
) (*UserRepository, error) {
	err := db.AutoMigrate(&models.User{})
	if err != nil {
		return nil, err
	}

	return &UserRepository{db, verificationClient}, nil
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

	// Create UUID
	newUuid, err := uuid.NewRandom()
	if err != nil {
		return err
	}
	var usersWithUuidCount int64
	repo.DB.Model(&models.User{}).Where("id = ?", newUuid).Count(&usersWithUuidCount)
	for usersWithUuidCount > 0 {
		newUuid, err = uuid.NewRandom()
		if err != nil {
			return err
		}
		repo.DB.Model(&models.User{}).Where("id = ?", newUuid).Count(&usersWithUuidCount)
	}

	// Create user in DB
	userModel := models.User{
		ID:        newUuid,
		Username:  user.Username,
		Password:  user.Password,
		Email:     user.Email,
		Salt:      user.Salt,
		Status:    user.Status,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
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
	err = gorm.G[models.User](repo.DB).Create(
		ctxBackground,
		&userModel,
	)
	if err != nil {
		return err
	}
	user.Id = userModel.ID

	return nil
}

func (repo *UserRepository) UpdateUser(ctx context.Context, userId uuid.UUID, request *port.UpdateUserRequest) error {
	var userCount int64
	repo.DB.Model(&models.User{}).Where("id = ?", userId).Count(&userCount)
	if userCount == 0 {
		return domain.ErrUserDoesNotExist
	}

	userModel := models.User{ID: userId}
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
	userModel.UpdatedAt = time.Now()
	repo.DB.Save(&userModel)

	return nil
}

func (repo *UserRepository) GetUserByUsername(ctx context.Context, username string) (*domain.User, error) {
	var userModel models.User
	result := repo.DB.Model(&models.User{}).Where("username = ?", username).First(&userModel)
	if result.Error != nil {
		if result.Error == gorm.ErrRecordNotFound {
			return nil, domain.ErrUserDoesNotExist
		}
		return nil, result.Error
	}

	domainUser := userModel.ToDomainModel()
	return domainUser, nil
}

func (repo *UserRepository) SaveUserToken(ctx context.Context, id uuid.UUID) (time.Time, error) {
	var userModel models.User
	result := repo.DB.Model(&models.User{}).Where("id = ?", id).First(&userModel)
	if err := result.Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return time.Time{}, domain.ErrUserDoesNotExist
		}
		return time.Time{}, err
	}

	userModel.Token = &id
	expireAt := time.Now().Add(time.Hour * 48)
	userModel.ExpireAt = &expireAt
	userModel.UpdatedAt = time.Now()
	saveRes := repo.DB.Save(&userModel)
	if err := saveRes.Error; err != nil {
		return time.Time{}, err
	}

	return expireAt, nil
}

func (repo *UserRepository) GetUserById(ctx context.Context, userId uuid.UUID) (*domain.User, error) {
	var userModel models.User
	result := repo.DB.Model(&models.User{}).Where("id = ?", userId).First(&userModel)
	if err := result.Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, domain.ErrUserDoesNotExist
		}
		return nil, err
	}

	return userModel.ToDomainModel(), nil
}

func (repo *UserRepository) CreateVerificationRequest(ctx context.Context, payload *port.VerificationRequestPayload) error {
	err := repo.VerificationClient.CreateVerificationRequest(payload)
	return err
}

func (repo *UserRepository) GetUserCount(ctx context.Context) (uint, error) {
	var usersCount int64
	res := repo.DB.Model(&models.User{}).Count(&usersCount)

	if err := res.Error; err != nil {
		return 0, err
	}

	return uint(usersCount), nil
}

func (repo *UserRepository) ResetUsers(ctx context.Context) error {
	result := repo.DB.Session(&gorm.Session{AllowGlobalUpdate: true}).Unscoped().Delete(&models.User{})
	if err := result.Error; err != nil {
		return err
	}

	return nil
}
