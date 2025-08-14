package http

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/service/mock"
	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

func TestLogin(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := gin.Default()
	mockService := &mock.MockAuthService{}
	handler := NewAuthHandler(mockService)
	router.POST("/auth/login", handler.Login)

	t.Run("successful login", func(t *testing.T) {
		// Mock the service to return a successful login response
		expirationTime := time.Date(2025, time.August, 14, 0, 0, 0, 0, time.UTC)
		mockService.LoginFunc = func(ctx context.Context, req *port.LoginRequest) (*port.LoginResponse, error) {
			return &port.LoginResponse{
				Id:       1,
				Token:    "test-token",
				ExpireAt: &expirationTime,
			}, nil
		}

		// Create the request body
		body := LoginRequestBody{Username: "testuser", Password: "password123"}
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodPost, "/auth/login", bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusOK, w.Code)
		expectedResponse := map[string]any{
			"id":       float64(1),
			"token":    "test-token",
			"expireAt": expirationTime.Format(time.RFC3339),
		}
		var actualResponse map[string]any
		json.Unmarshal(w.Body.Bytes(), &actualResponse)
		assert.Equal(t, expectedResponse, actualResponse)
	})

	t.Run("invalid request payload", func(t *testing.T) {
		// Create a request with a bad JSON body
		req, _ := http.NewRequest(http.MethodPost, "/auth/login", bytes.NewBufferString("invalid json"))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusBadRequest, w.Code)
		expectedResponse := map[string]any{
			"error": "Failed to convert request body to JSON",
		}
		var response map[string]any
		json.Unmarshal(w.Body.Bytes(), &response)
		assert.Equal(t, expectedResponse, response)
	})

	t.Run("invalid login payload from service", func(t *testing.T) {
		// Mock the service to return the specific error
		mockService.LoginFunc = func(ctx context.Context, req *port.LoginRequest) (*port.LoginResponse, error) {
			return nil, domain.ErrInvalidLoginPayload
		}
		// Create a valid request body
		body := LoginRequestBody{Username: "", Password: "password123"}
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodPost, "/auth/login", bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusBadRequest, w.Code)
		expectedResponse := map[string]any{
			"error": "Invalid login payload",
		}
		var response map[string]any
		json.Unmarshal(w.Body.Bytes(), &response)
		assert.Equal(t, expectedResponse, response)
	})

	t.Run("user not found or incorrect password", func(t *testing.T) {
		// Mock the service to return the specific error
		mockService.LoginFunc = func(ctx context.Context, req *port.LoginRequest) (*port.LoginResponse, error) {
			return nil, domain.ErrUserDoesNotExist
		}
		// Create a valid request body
		body := LoginRequestBody{Username: "nonexistent", Password: "wrongpassword"}
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodPost, "/auth/login", bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusNotFound, w.Code)
		expectedResponse := map[string]any{
			"error": "Username or password are incorrect",
		}
		var response map[string]any
		json.Unmarshal(w.Body.Bytes(), &response)
		assert.Equal(t, expectedResponse, response)
	})

	t.Run("internal server error from service", func(t *testing.T) {
		// Mock the service to return a generic error
		mockService.LoginFunc = func(ctx context.Context, req *port.LoginRequest) (*port.LoginResponse, error) {
			return nil, assert.AnError
		}
		// Create a valid request body
		body := LoginRequestBody{Username: "testuser", Password: "password123"}
		jsonBody, _ := json.Marshal(body)

		// Create a new HTTP request and a response recorder
		req, _ := http.NewRequest(http.MethodPost, "/auth/login", bytes.NewBuffer(jsonBody))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()

		// Serve the request
		router.ServeHTTP(w, req)

		// Assert the response
		assert.Equal(t, http.StatusInternalServerError, w.Code)
		expectedResponse := map[string]any{
			"error": "Internal server error",
		}
		var response map[string]any
		json.Unmarshal(w.Body.Bytes(), &response)
		assert.Equal(t, expectedResponse, response)
	})
}
