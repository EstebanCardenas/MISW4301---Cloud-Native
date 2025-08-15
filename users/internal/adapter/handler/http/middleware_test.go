package http

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/auth/mock"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
)

func TestAuthMiddleware(t *testing.T) {
	router := gin.Default()
	mockTokenService := &mock.MockTokenService{}
	dummyHandler := func(ctx *gin.Context) {
		ctx.JSON(http.StatusOK, gin.H{"message": "success"})
	}
	router.GET("/protected", authMiddleware(mockTokenService), dummyHandler)

	t.Run("successful authentication", func(t *testing.T) {
		id := uuid.New()
		mockTokenService.VerifyTokenFunc = func(token string) (*uuid.UUID, error) {
			return &id, nil
		}
		req, _ := http.NewRequest(http.MethodGet, "/protected", nil)
		req.Header.Set("Authorization", "Bearer valid-token")
		w := httptest.NewRecorder()
		router.ServeHTTP(w, req)
		assert.Equal(t, http.StatusOK, w.Code)
		assert.JSONEq(t, `{"message": "success"}`, w.Body.String())
	})

	t.Run("auth header too short", func(t *testing.T) {
		req, _ := http.NewRequest(http.MethodGet, "/protected", nil)
		req.Header.Set("Authorization", "Bearer")
		w := httptest.NewRecorder()
		router.ServeHTTP(w, req)
		assert.Equal(t, http.StatusForbidden, w.Code)
		assert.JSONEq(t, `{"error": "Auth header missing or invalid header length"}`, w.Body.String())
	})

	t.Run("expired token", func(t *testing.T) {
		mockTokenService.VerifyTokenFunc = func(token string) (*uuid.UUID, error) {
			return nil, domain.ErrExpiredToken
		}
		req, _ := http.NewRequest(http.MethodGet, "/protected", nil)
		req.Header.Set("Authorization", "Bearer expired-token")
		w := httptest.NewRecorder()
		router.ServeHTTP(w, req)
		assert.Equal(t, http.StatusUnauthorized, w.Code)
		assert.JSONEq(t, `{"error": "Token has expired"}`, w.Body.String())
	})

	t.Run("invalid token", func(t *testing.T) {
		mockTokenService.VerifyTokenFunc = func(token string) (*uuid.UUID, error) {
			return nil, domain.ErrInvalidToken
		}
		req, _ := http.NewRequest(http.MethodGet, "/protected", nil)
		req.Header.Set("Authorization", "Bearer invalid-token")
		w := httptest.NewRecorder()
		router.ServeHTTP(w, req)
		assert.Equal(t, http.StatusUnauthorized, w.Code)
		assert.JSONEq(t, `{"error": "Token is invalid"}`, w.Body.String())
	})
}
