package repository

import (
	"fmt"
	"testing"

	mockData "github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/data/mock"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/google/uuid"
)

func TestUserRepository_CreateUser_Success(t *testing.T) {
	db, err := mockData.NewTestDb()
	if err != nil {
		t.Fatalf("Failed to create db: %v", err.Error())
	}

	repo, err := NewUserRepository(db)
	if err != nil {
		t.Fatalf("Failed to init user repo: %v", err.Error())
	}

	user := &domain.User{
		Username: "myuser",
		Password: "123",
		Email:    "myemail",
		Salt:     "mysalt",
		Status:   domain.NotVerified,
	}
	err = repo.CreateUser(t.Context(), user)
	if err != nil {
		t.Fatalf("expected err nil, got %v", err.Error())
	}

	// Verify user was created
	got, err := repo.GetUserByUsername(t.Context(), "myuser")
	if err != nil {
		t.Fatalf("expected user to exist, got error: %v", err)
	}
	if got.Username != user.Username || got.Email != user.Email || got.Status != user.Status {
		t.Errorf("user fields do not match: got %+v, want %+v", got, user)
	}
}

func TestUserRepository_CreateUser_UsernameExists(t *testing.T) {
	db, _ := mockData.NewTestDb()
	repo, _ := NewUserRepository(db)

	user1 := &domain.User{
		Username: "duplicateuser",
		Password: "pass",
		Email:    "email1",
		Salt:     "salt",
		Status:   domain.NotVerified,
	}
	_ = repo.CreateUser(t.Context(), user1)

	user2 := &domain.User{
		Username: "duplicateuser",
		Password: "pass2",
		Email:    "email2",
		Salt:     "salt2",
		Status:   domain.NotVerified,
	}
	err := repo.CreateUser(t.Context(), user2)
	if err != domain.ErrUsernameOrEmailExists {
		t.Errorf("expected ErrUsernameOrEmailExists, got %v", err)
	}
}

func TestUserRepository_CreateUser_EmailExists(t *testing.T) {
	db, _ := mockData.NewTestDb()
	repo, _ := NewUserRepository(db)

	user1 := &domain.User{
		Username: "user1",
		Password: "pass",
		Email:    "sameemail",
		Salt:     "salt",
		Status:   domain.NotVerified,
	}
	_ = repo.CreateUser(t.Context(), user1)

	user2 := &domain.User{
		Username: "user2",
		Password: "pass2",
		Email:    "sameemail",
		Salt:     "salt2",
		Status:   domain.NotVerified,
	}
	err := repo.CreateUser(t.Context(), user2)
	if err != domain.ErrUsernameOrEmailExists {
		t.Errorf("expected ErrUsernameOrEmailExists, got %v", err)
	}
}

func TestUserRepository_CreateUser_WithOptionalFields(t *testing.T) {
	db, _ := mockData.NewTestDb()
	repo, _ := NewUserRepository(db)

	dni := "123456"
	fullName := "Test User"
	phone := "555-1234"
	user := &domain.User{
		Username:    "optuser",
		Password:    "pass",
		Email:       "optuser@email.com",
		Salt:        "salt",
		Status:      domain.NotVerified,
		Dni:         &dni,
		FullName:    &fullName,
		PhoneNumber: &phone,
	}
	err := repo.CreateUser(t.Context(), user)
	if err != nil {
		t.Fatalf("expected err nil, got %v", err)
	}

	got, err := repo.GetUserByUsername(t.Context(), "optuser")
	if err != nil {
		t.Fatalf("expected user to exist, got error: %v", err)
	}
	if got.Dni == nil || *got.Dni != dni {
		t.Errorf("expected Dni %v, got %v", dni, got.Dni)
	}
	if got.FullName == nil || *got.FullName != fullName {
		t.Errorf("expected FullName %v, got %v", fullName, got.FullName)
	}
	if got.PhoneNumber == nil || *got.PhoneNumber != phone {
		t.Errorf("expected PhoneNumber %v, got %v", phone, got.PhoneNumber)
	}
}
func TestUserRepository_UpdateUser_Success(t *testing.T) {
	db, _ := mockData.NewTestDb()
	repo, _ := NewUserRepository(db)

	user := &domain.User{
		Username: "updateuser",
		Password: "pass",
		Email:    "update@email.com",
		Salt:     "salt",
		Status:   domain.NotVerified,
	}
	err := repo.CreateUser(t.Context(), user)
	if err != nil {
		t.Fatalf("CreateUser failed: %v", err)
	}

	status := domain.Verified
	req := &port.UpdateUserRequest{
		Status:      &status,
		Dni:         "999999",
		FullName:    "Updated Name",
		PhoneNumber: "123456789",
	}
	err = repo.UpdateUser(t.Context(), user.Id, req)
	if err != nil {
		t.Fatalf("UpdateUser failed: %v", err)
	}

	updated, err := repo.GetUserById(t.Context(), user.Id)
	if err != nil {
		t.Fatalf("GetUserById failed: %v", err)
	}
	if updated.Status != domain.Verified {
		t.Errorf("expected status Verified, got %v", updated.Status)
	}
	if updated.Dni == nil || *updated.Dni != "999999" {
		t.Errorf("expected Dni '999999', got %v", updated.Dni)
	}
	if updated.FullName == nil || *updated.FullName != "Updated Name" {
		t.Errorf("expected FullName 'Updated Name', got %v", updated.FullName)
	}
	if updated.PhoneNumber == nil || *updated.PhoneNumber != "123456789" {
		t.Errorf("expected PhoneNumber '123456789', got %v", updated.PhoneNumber)
	}
}

func TestUserRepository_UpdateUser_UserDoesNotExist(t *testing.T) {
	db, _ := mockData.NewTestDb()
	repo, _ := NewUserRepository(db)

	status := domain.Verified
	req := &port.UpdateUserRequest{
		Status:      &status,
		Dni:         "999999",
		FullName:    "Updated Name",
		PhoneNumber: "123456789",
	}
	err := repo.UpdateUser(t.Context(), uuid.New(), req)
	if err != domain.ErrUserDoesNotExist {
		t.Errorf("expected ErrUserDoesNotExist, got %v", err)
	}
}

func TestUserRepository_UpdateUser_PartialUpdate(t *testing.T) {
	db, _ := mockData.NewTestDb()
	repo, _ := NewUserRepository(db)

	user := &domain.User{
		Username: "partialuser",
		Password: "pass",
		Email:    "partial@email.com",
		Salt:     "salt",
		Status:   domain.NotVerified,
	}
	err := repo.CreateUser(t.Context(), user)
	if err != nil {
		t.Fatalf("CreateUser failed: %v", err)
	}

	req := &port.UpdateUserRequest{
		FullName: "Partial Name",
	}
	err = repo.UpdateUser(t.Context(), user.Id, req)
	if err != nil {
		t.Fatalf("UpdateUser failed: %v", err)
	}

	updated, err := repo.GetUserById(t.Context(), user.Id)
	if err != nil {
		t.Fatalf("GetUserById failed: %v", err)
	}
	if updated.FullName == nil || *updated.FullName != "Partial Name" {
		t.Errorf("expected FullName 'Partial Name', got %v", updated.FullName)
	}
	// Other fields should remain unchanged
	if updated.PhoneNumber != nil {
		t.Errorf("expected nil PhoneNumber, got %v", *updated.PhoneNumber)
	}
	if updated.Dni != nil {
		t.Errorf("expected nil Dni, got %v", *updated.Dni)
	}
	if updated.Status != domain.NotVerified {
		t.Errorf("expected status NotVerified, got %v", updated.Status)
	}
}

func TestUserRepository_UpdateUser_EmptyOptionalFields(t *testing.T) {
	db, _ := mockData.NewTestDb()
	repo, _ := NewUserRepository(db)

	dni := "123456"
	fullName := "Test User"
	phone := "555-1234"
	user := &domain.User{
		Username:    "emptyfieldsuser",
		Password:    "pass",
		Email:       "emptyfields@email.com",
		Salt:        "salt",
		Status:      domain.NotVerified,
		Dni:         &dni,
		FullName:    &fullName,
		PhoneNumber: &phone,
	}
	err := repo.CreateUser(t.Context(), user)
	if err != nil {
		t.Fatalf("CreateUser failed: %v", err)
	}

	req := &port.UpdateUserRequest{
		Dni:         "",
		FullName:    "",
		PhoneNumber: "",
	}
	err = repo.UpdateUser(t.Context(), user.Id, req)
	if err != nil {
		t.Fatalf("UpdateUser failed: %v", err)
	}

	updated, err := repo.GetUserById(t.Context(), user.Id)
	if err != nil {
		t.Fatalf("GetUserById failed: %v", err)
	}
	if *updated.Dni != dni {
		t.Errorf("expected Dni %v, got %v", dni, *updated.Dni)
	}
	if *updated.FullName != fullName {
		t.Errorf("expected FullName %v, got %v", fullName, *updated.FullName)
	}
	if *updated.PhoneNumber != phone {
		t.Errorf("expected PhoneNumber %v, got %v", phone, *updated.PhoneNumber)
	}
}

func TestUserRepository_GetUserByUsername_Success(t *testing.T) {
	db, _ := mockData.NewTestDb()
	repo, _ := NewUserRepository(db)

	// Arrange: Create a user to be retrieved
	userToCreate := &domain.User{
		Username: "findme",
		Password: "pass",
		Email:    "findme@example.com",
		Salt:     "salt",
		Status:   domain.Verified,
	}
	err := repo.CreateUser(t.Context(), userToCreate)
	if err != nil {
		t.Fatalf("failed to create user for retrieval: %v", err)
	}

	// Act: Get the user by their username
	foundUser, err := repo.GetUserByUsername(t.Context(), "findme")

	// Assert
	if err != nil {
		t.Fatalf("expected no error, but got: %v", err)
	}
	if foundUser == nil {
		t.Fatal("expected to find a user, but got nil")
	}
	if foundUser.Username != "findme" {
		t.Errorf("expected username 'findme', got '%s'", foundUser.Username)
	}
}

func TestUserRepository_GetUserByUsername_UserDoesNotExist(t *testing.T) {
	db, _ := mockData.NewTestDb()
	repo, _ := NewUserRepository(db)

	// Act: Try to get a user that doesn't exist
	foundUser, err := repo.GetUserByUsername(t.Context(), "nonexistentuser")

	// Assert
	if err == nil {
		t.Fatal("expected an error, but got none")
	}
	if err != domain.ErrUserDoesNotExist {
		t.Errorf("expected error to be ErrUserDoesNotExist, got: %v", err)
	}
	if foundUser != nil {
		t.Errorf("expected found user to be nil, got: %+v", foundUser)
	}
}

func TestUserRepository_SaveUserToken_Success(t *testing.T) {
	db, _ := mockData.NewTestDb()
	repo, _ := NewUserRepository(db)

	// Arrange: Create a user first
	user := &domain.User{
		Username: "tokenuser",
		Password: "pass",
		Email:    "tokenuser@example.com",
		Salt:     "salt",
		Status:   domain.NotVerified,
	}
	err := repo.CreateUser(t.Context(), user)
	if err != nil {
		t.Fatalf("Failed to create user: %v", err)
	}

	// Act: Save the token for the created user
	expireAt, err := repo.SaveUserToken(t.Context(), user.Id)
	if err != nil {
		t.Fatalf("SaveUserToken failed: %v", err)
	}

	// Assert: Verify the user was updated with the new token
	updatedUser, err := repo.GetUserById(t.Context(), user.Id)
	if err != nil {
		t.Fatalf("Failed to retrieve updated user: %v", err)
	}
	if updatedUser.Token == nil {
		t.Errorf("Expected token not nil, but got nil")
	}
	if updatedUser.ExpireAt == nil {
		t.Errorf("Expected ExpireAt %v, but got %v", expireAt, updatedUser.ExpireAt)
	}
}

func TestUserRepository_SaveUserToken_UserDoesNotExist(t *testing.T) {
	db, _ := mockData.NewTestDb()
	repo, _ := NewUserRepository(db)

	// Arrange: A non-existent user ID
	nonExistentUserID := uuid.New()

	// Act: Try to save a token for a non-existent user
	_, err := repo.SaveUserToken(t.Context(), nonExistentUserID)

	// Assert: Check that the expected error is returned
	if err == nil {
		t.Fatal("Expected an error for non-existent user, but got nil")
	}
	if err != domain.ErrUserDoesNotExist {
		t.Errorf("Expected error to be %v, but got %v", domain.ErrUserDoesNotExist, err)
	}
}

func TestUserRepository_GetUserById_Success(t *testing.T) {
	db, err := mockData.NewTestDb()
	if err != nil {
		t.Fatalf("Failed to create mock DB: %v", err)
	}
	repo, _ := NewUserRepository(db)

	// Arrange: Create a user to be retrieved
	userToCreate := &domain.User{
		Username: "id_test_user",
		Password: "password",
		Email:    "id_test_user@example.com",
		Salt:     "somesalt",
		Status:   domain.NotVerified,
	}
	err = repo.CreateUser(t.Context(), userToCreate)
	if err != nil {
		t.Fatalf("Failed to create user: %v", err)
	}

	// Act: Retrieve the user by their ID
	foundUser, err := repo.GetUserById(t.Context(), userToCreate.Id)

	// Assert
	if err != nil {
		t.Fatalf("Expected no error, but got: %v", err)
	}
	if foundUser == nil {
		t.Fatal("Expected to find a user, but got nil")
	}
	if foundUser.Id != userToCreate.Id {
		t.Errorf("Expected user ID %d, got %d", userToCreate.Id, foundUser.Id)
	}
	if foundUser.Username != "id_test_user" {
		t.Errorf("Expected username 'id_test_user', got '%s'", foundUser.Username)
	}
}

func TestUserRepository_GetUserById_UserDoesNotExist(t *testing.T) {
	db, err := mockData.NewTestDb()
	if err != nil {
		t.Fatalf("Failed to create mock DB: %v", err)
	}
	repo, _ := NewUserRepository(db)

	// Act: Try to get a user that doesn't exist
	nonExistentID := uuid.New()
	foundUser, err := repo.GetUserById(t.Context(), nonExistentID)

	// Assert
	if err == nil {
		t.Fatal("Expected an error, but got none")
	}
	if err != domain.ErrUserDoesNotExist {
		t.Errorf("Expected error to be ErrUserDoesNotExist, got %v", err)
	}
	if foundUser != nil {
		t.Errorf("Expected found user to be nil, got: %+v", foundUser)
	}
}

func TestUserRepository_GetUserCount_Success(t *testing.T) {
	db, err := mockData.NewTestDb()
	if err != nil {
		t.Fatalf("Failed to create mock DB: %v", err)
	}
	repo, _ := NewUserRepository(db)

	// Arrange: Create three users
	for i := 0; i < 3; i++ {
		user := &domain.User{
			Username: fmt.Sprintf("countuser%d", i),
			Password: "pass",
			Email:    fmt.Sprintf("countuser%d@example.com", i),
			Salt:     "salt",
			Status:   domain.NotVerified,
		}
		err := repo.CreateUser(t.Context(), user)
		if err != nil {
			t.Fatalf("Failed to create user: %v", err)
		}
	}

	// Act: Get the user count
	count, err := repo.GetUserCount(t.Context())

	// Assert
	if err != nil {
		t.Fatalf("Expected no error, but got: %v", err)
	}
	if count != 3 {
		t.Errorf("Expected user count to be 3, but got %d", count)
	}
}

func TestUserRepository_GetUserCount_Empty(t *testing.T) {
	db, err := mockData.NewTestDb()
	if err != nil {
		t.Fatalf("Failed to create mock DB: %v", err)
	}
	repo, _ := NewUserRepository(db)

	// Arrange: Ensure the database is empty (or has been reset)
	// mockData.NewTestDb should start with an empty table, but it's good practice to be explicit.
	// We can skip creating users.

	// Act: Get the user count from an empty table
	count, err := repo.GetUserCount(t.Context())

	// Assert
	if err != nil {
		t.Fatalf("Expected no error, but got: %v", err)
	}
	if count != 0 {
		t.Errorf("Expected user count to be 0, but got %d", count)
	}
}

func TestUserRepository_ResetUsers_Success(t *testing.T) {
	db, err := mockData.NewTestDb()
	if err != nil {
		t.Fatalf("Failed to create mock DB: %v", err)
	}
	repo, _ := NewUserRepository(db)

	// Arrange: Create some users
	for i := 0; i < 5; i++ {
		user := &domain.User{
			Username: fmt.Sprintf("resetuser%d", i),
			Password: "pass",
			Email:    fmt.Sprintf("resetuser%d@example.com", i),
			Salt:     "salt",
			Status:   domain.NotVerified,
		}
		err := repo.CreateUser(t.Context(), user)
		if err != nil {
			t.Fatalf("Failed to create user: %v", err)
		}
	}

	// Act: Reset all users
	err = repo.ResetUsers(t.Context())
	if err != nil {
		t.Fatalf("ResetUsers failed: %v", err)
	}

	// Assert: Check if the user count is now zero
	count, err := repo.GetUserCount(t.Context())
	if err != nil {
		t.Fatalf("GetUserCount failed: %v", err)
	}
	if count != 0 {
		t.Errorf("Expected user count to be 0 after reset, but got %d", count)
	}
}

func TestUserRepository_ResetUsers_Empty(t *testing.T) {
	db, err := mockData.NewTestDb()
	if err != nil {
		t.Fatalf("Failed to create mock DB: %v", err)
	}
	repo, _ := NewUserRepository(db)

	// Arrange: Ensure the database starts empty.
	// We can explicitly call ResetUsers to guarantee this, though the test DB should be clean.
	_ = repo.ResetUsers(t.Context())

	// Act: Call ResetUsers on an empty table
	err = repo.ResetUsers(t.Context())

	// Assert: No error should be returned
	if err != nil {
		t.Fatalf("Expected no error when resetting an empty table, but got: %v", err)
	}

	// Double-check the count is still zero
	count, _ := repo.GetUserCount(t.Context())
	if count != 0 {
		t.Errorf("Expected user count to be 0, but got %d", count)
	}
}
