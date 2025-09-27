package http

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/service/mock"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
)

func TestCreateUser(t *testing.T) {
	router := gin.Default()
	mockService := &mock.MockUserService{}
	handler := NewUserHandler(mockService)
	router.POST("/users", handler.CreateUser)

	t.Run("successful user creation", func(t *testing.T) {
		// Mock service
		id := uuid.New()
		mockService.CreateUserFunc = func(ctx context.Context, request *port.CreateUserRequest) (*port.CreateUserResponse, error) {
			return &port.CreateUserResponse{
				Id:        id,
				CreatedAt: time.Date(2025, time.January, 1, 0, 0, 0, 0, time.UTC),
			}, nil
		}
		// Create the request body
		body := CreateUserRequestBody{
			Username: "testuser",
			Password: "password123",
			Email:    "test@example.com",
		}
		jsonBody, _ := json.Marshal(body)
		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodPost, "/users", bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusCreated, w.Code)
		expectedResponse := map[string]any{
			"id":        fmt.Sprint(id),
			"createdAt": "2025-01-01T00:00:00Z",
		}
		var actualResponse map[string]any
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, expectedResponse, actualResponse)
	})

	t.Run("invalid request payload", func(t *testing.T) {
		// Create a request with a bad JSON body
		req, _ := http.NewRequest(http.MethodPost, "/users", bytes.NewBufferString("invalid json"))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusBadRequest, w.Code)
		expectedResponse := map[string]any{
			"error": "Invalid create user payload",
		}
		var response map[string]any
		json.Unmarshal(w.Body.Bytes(), &response)
		assert.Equal(t, expectedResponse, response)
	})

	t.Run("username or email already exists", func(t *testing.T) {
		// Mock the service to return the specific error
		mockService.CreateUserFunc = func(ctx context.Context, request *port.CreateUserRequest) (*port.CreateUserResponse, error) {
			return nil, domain.ErrUsernameOrEmailExists
		}

		// Create a valid request body
		body := CreateUserRequestBody{
			Username: "existinguser",
			Password: "password123",
			Email:    "existing@example.com",
		}
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodPost, "/users", bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusPreconditionFailed, w.Code)
		expectedResponse := map[string]any{
			"error": "Username or email already exists",
		}
		var response map[string]any
		json.Unmarshal(w.Body.Bytes(), &response)
		assert.Equal(t, expectedResponse, response)
	})

	t.Run("missing mandatory fields from request body", func(t *testing.T) {
		// Mock the service to return the specific error
		mockService.CreateUserFunc = func(ctx context.Context, request *port.CreateUserRequest) (*port.CreateUserResponse, error) {
			return nil, domain.ErrInvalidCreateUserPayload
		}

		// Create a valid request body
		body := CreateUserRequestBody{
			Username: "",
			Password: "password123",
			Email:    "existing@example.com",
		}
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodPost, "/users", bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, 400, w.Code)
		expectedResponse := map[string]any{
			"error": "Missing mandatory fields from request body",
		}
		var response map[string]any
		json.Unmarshal(w.Body.Bytes(), &response)
		assert.Equal(t, expectedResponse, response)
	})
}

func TestUpdateUser(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := gin.Default()
	mockService := &mock.MockUserService{}
	handler := NewUserHandler(mockService)
	router.PUT("/users/:id", handler.UpdateUser)

	// A sample UserStatus to use in the tests
	verifiedStatus := domain.Verified

	t.Run("successful user update", func(t *testing.T) {
		// Mock the service to return a nil error, indicating success
		id := uuid.New()
		mockService.UpdateUserFunc = func(ctx context.Context, userId uuid.UUID, request *port.UpdateUserRequest) error {
			return nil
		}

		// Create the request body
		body := UpdateUserRequestBody{
			FullName:    "Jane Doe",
			PhoneNumber: "1234567890",
			Dni:         "123456789",
			Status:      &verifiedStatus,
		}
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodPut, fmt.Sprintf("/users/%v", id), bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusOK, w.Code)
		expectedResponse := gin.H{"msg": "el usuario ha sido actualizado"}
		var actualResponse gin.H
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, expectedResponse, actualResponse)
	})

	t.Run("invalid user ID", func(t *testing.T) {
		// Create a request with an invalid user ID in the path
		body := UpdateUserRequestBody{
			FullName: "testname",
		}
		jsonBody, _ := json.Marshal(body)
		req, _ := http.NewRequest(http.MethodPut, "/users/abc", bytes.NewBuffer(jsonBody))
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusBadRequest, w.Code)
		expectedResponse := gin.H{"error": "Invalid user ID"}
		var actualResponse gin.H
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, expectedResponse, actualResponse)
	})

	t.Run("invalid request payload", func(t *testing.T) {
		// Create a request with an invalid JSON body
		req, _ := http.NewRequest(http.MethodPut, "/users/1", bytes.NewBufferString("invalid json"))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusBadRequest, w.Code)
		expectedResponse := gin.H{"error": "Failed to convert request body to JSON"}
		var actualResponse gin.H
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, expectedResponse, actualResponse)
	})

	t.Run("invalid update user payload (service layer)", func(t *testing.T) {
		// Mock the service to return the specific error
		mockService.UpdateUserFunc = func(ctx context.Context, userId uuid.UUID, request *port.UpdateUserRequest) error {
			return domain.ErrInvalidUpdateUserPayload
		}

		// Create a valid request body
		body := UpdateUserRequestBody{} // Empty body to trigger the error
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		id := uuid.New()
		req, _ := http.NewRequest(http.MethodPut, fmt.Sprintf("/users/%v", id), bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusBadRequest, w.Code)
		expectedResponse := gin.H{"error": "Request body doesn't contain any expected field"}
		var actualResponse gin.H
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, expectedResponse, actualResponse)
	})

	t.Run("invalid user status (service layer)", func(t *testing.T) {
		// Mock the service to return the specific error
		mockService.UpdateUserFunc = func(ctx context.Context, userId uuid.UUID, request *port.UpdateUserRequest) error {
			return domain.ErrInvalidUserStatus
		}

		// Create a valid request body
		body := UpdateUserRequestBody{
			Status: (*domain.UserStatus)(nil), // Invalid status value will be handled by the service mock
		}
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		id := uuid.New()
		req, _ := http.NewRequest(http.MethodPut, fmt.Sprintf("/users/%v", id), bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusBadRequest, w.Code)
		expectedResponse := gin.H{"error": "User status must be either POR_VERIFICAR, NO_VERIFICADO or VERIFICADO"}
		var actualResponse gin.H
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, expectedResponse, actualResponse)
	})

	t.Run("user does not exist", func(t *testing.T) {
		// Mock the service to return the specific error
		mockService.UpdateUserFunc = func(ctx context.Context, userId uuid.UUID, request *port.UpdateUserRequest) error {
			return domain.ErrUserDoesNotExist
		}

		// Create a request body
		body := UpdateUserRequestBody{
			FullName: "Non-existent User",
		}
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		id := uuid.New()
		req, _ := http.NewRequest(http.MethodPut, fmt.Sprintf("/users/%v", id), bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusNotFound, w.Code)
		expectedResponse := gin.H{"error": "User with given ID doesn't exist"}
		var actualResponse gin.H
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, expectedResponse, actualResponse)
	})

	t.Run("internal server error", func(t *testing.T) {
		// Mock the service to return a generic error
		mockService.UpdateUserFunc = func(ctx context.Context, userId uuid.UUID, request *port.UpdateUserRequest) error {
			return assert.AnError
		}

		// Create a request body
		body := UpdateUserRequestBody{
			FullName: "Server Error",
		}
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		id := uuid.New()
		req, _ := http.NewRequest(http.MethodPut, fmt.Sprintf("/users/%v", id), bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusInternalServerError, w.Code)
		expectedResponse := gin.H{"error": "Internal server error"}
		var actualResponse gin.H
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, expectedResponse, actualResponse)
	})
}

func TestQueryMyself(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := gin.Default()
	mockService := &mock.MockUserService{}
	handler := NewUserHandler(mockService)

	// Create a dummy middleware to inject the authenticated user ID into the context
	// This simulates a real-world scenario where middleware would handle authentication.
	router.GET("/users/myself", func(ctx *gin.Context) {
		ctx.Set(UserIdKey, uint(1)) // Use a user ID of 1 for testing
	}, handler.QueryMyself)

	t.Run("successful query of self", func(t *testing.T) {
		// Define the expected user from the service layer
		fullName := "Test User"
		dni := "123"
		phoneNumber := "987"
		expectedUser := &domain.User{
			Id:          uuid.New(),
			Username:    "testuser",
			Email:       "test@example.com",
			FullName:    &fullName,
			Dni:         &dni,
			PhoneNumber: &phoneNumber,
			Status:      domain.Verified,
			CreatedAt:   time.Date(2025, time.January, 1, 0, 0, 0, 0, time.UTC),
			UpdatedAt:   time.Date(2025, time.January, 1, 0, 0, 0, 0, time.UTC),
		}

		// Mock the service to return the expected user
		mockService.QueryMyselfFunc = func(ctx context.Context, userId uuid.UUID) (*domain.User, error) {
			return expectedUser, nil
		}

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodGet, "/users/myself", nil)
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusOK, w.Code)
		var actualResponse gin.H
		json.Unmarshal(w.Body.Bytes(), &actualResponse)

		// Check if the response body matches the expected user data
		assert.Equal(t, fmt.Sprint(expectedUser.Id), actualResponse["id"])
		assert.Equal(t, expectedUser.Username, actualResponse["username"])
		assert.Equal(t, expectedUser.Email, actualResponse["email"])
		assert.Equal(t, *expectedUser.FullName, actualResponse["fullName"])
		assert.Equal(t, *expectedUser.Dni, actualResponse["dni"])
		assert.Equal(t, *expectedUser.PhoneNumber, actualResponse["phoneNumber"])
		assert.Equal(t, string(expectedUser.Status), actualResponse["status"])
	})

	t.Run("internal server error from service", func(t *testing.T) {
		// Mock the service to return an internal server error
		mockService.QueryMyselfFunc = func(ctx context.Context, userId uuid.UUID) (*domain.User, error) {
			return nil, assert.AnError
		}

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodGet, "/users/myself", nil)
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusInternalServerError, w.Code)
		var actualResponse gin.H
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, "Internal server error", actualResponse["error"])
	})
}

func TestGetUserCount(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := gin.Default()
	mockService := &mock.MockUserService{}
	handler := NewUserHandler(mockService)
	router.GET("/users/count", handler.GetUserCount)

	t.Run("successful user count retrieval", func(t *testing.T) {
		// Mock the service to return a successful count
		expectedCount := uint(42)
		mockService.GetUserCountFunc = func(ctx context.Context) (uint, error) {
			return expectedCount, nil
		}

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodGet, "/users/count", nil)
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusOK, w.Code)
		var actualResponse map[string]any
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, float64(expectedCount), actualResponse["count"])
	})

	t.Run("internal server error from service", func(t *testing.T) {
		// Mock the service to return an error
		mockService.GetUserCountFunc = func(ctx context.Context) (uint, error) {
			return 0, assert.AnError
		}

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodGet, "/users/count", nil)
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusInternalServerError, w.Code)
		var actualResponse map[string]any
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, "Internal server error", actualResponse["error"])
	})
}

func TestResetUsers(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := gin.Default()
	mockService := &mock.MockUserService{}
	handler := NewUserHandler(mockService)
	router.DELETE("/users/reset", handler.ResetUsers)

	t.Run("successful user reset", func(t *testing.T) {
		// Mock the service to return a nil error, indicating success
		mockService.ResetUsersFunc = func(ctx context.Context) error {
			return nil
		}

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodDelete, "/users/reset", nil)
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusOK, w.Code)
		var actualResponse map[string]any
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, "Todos los datos fueron eliminados", actualResponse["msg"])
	})

	t.Run("internal server error from service", func(t *testing.T) {
		// Mock the service to return an error
		mockService.ResetUsersFunc = func(ctx context.Context) error {
			return assert.AnError
		}

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodDelete, "/users/reset", nil)
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusInternalServerError, w.Code)
		var actualResponse map[string]any
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, "Internal server error", actualResponse["error"])
	})
}

func TestUpdateUserStatus(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := gin.Default()
	mockService := &mock.MockUserService{}
	handler := NewUserHandler(mockService)
	router.PATCH("/users/status", handler.UpdateUserStatus)

	t.Run("invalid verify token from service", func(t *testing.T) {
		mockService.UpdateUserStatusFunc = func(ctx context.Context, verifyToken string, request *port.UpdateUserStatusRequest) error {
			return domain.ErrInvalidVerifyToken
		}

		// Create request body
		body := UpdateUserStatusRequestBody{
			RUV:            "some-ruv",
			UserIdentifier: "user-123",
			CreatedAt:      "2024-01-01T00:00:00Z",
			Status:         "VERIFICADO",
			Score:          95.5,
			VerifyToken:    "invalid-token",
		}
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodPatch, "/users/status", bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusForbidden, w.Code)
		var actualResponse map[string]any
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, "Verify token is invalid", actualResponse["error"])
	})

	t.Run("user does not exist", func(t *testing.T) {
		mockService.UpdateUserStatusFunc = func(ctx context.Context, verifyToken string, request *port.UpdateUserStatusRequest) error {
			return domain.ErrUserDoesNotExist
		}

		// Create request body
		body := UpdateUserStatusRequestBody{
			RUV:            "some-ruv",
			UserIdentifier: "user-123",
			CreatedAt:      "2024-01-01T00:00:00Z",
			Status:         "VERIFICADO",
			Score:          95.5,
			VerifyToken:    "invalid-token",
		}
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodPatch, "/users/status", bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusNotFound, w.Code)
		var actualResponse map[string]any
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, "User with given ID doesn't exist", actualResponse["error"])
	})

	t.Run("internal server error", func(t *testing.T) {
		mockService.UpdateUserStatusFunc = func(ctx context.Context, verifyToken string, request *port.UpdateUserStatusRequest) error {
			return domain.ErrInternal
		}

		// Create request body
		body := UpdateUserStatusRequestBody{
			RUV:            "some-ruv",
			UserIdentifier: "user-123",
			CreatedAt:      "2024-01-01T00:00:00Z",
			Status:         "VERIFICADO",
			Score:          95.5,
			VerifyToken:    "invalid-token",
		}
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodPatch, "/users/status", bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusInternalServerError, w.Code)
		var actualResponse map[string]any
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, "Internal server error", actualResponse["error"])
	})

	t.Run("successful status update", func(t *testing.T) {
		mockService.UpdateUserStatusFunc = func(ctx context.Context, verifyToken string, request *port.UpdateUserStatusRequest) error {
			return nil
		}

		// Create request body
		body := UpdateUserStatusRequestBody{
			RUV:            "some-ruv",
			UserIdentifier: "user-123",
			CreatedAt:      "2024-01-01T00:00:00Z",
			Status:         "VERIFICADO",
			Score:          95.5,
			VerifyToken:    "invalid-token",
		}
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodPatch, "/users/status", bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusOK, w.Code)
		var actualResponse map[string]any
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, "User status updated successfully", actualResponse["msg"])
	})
}
