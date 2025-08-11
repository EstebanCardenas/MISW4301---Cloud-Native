package http

import (
	"time"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/gin-gonic/gin"
)

type AuthHandler struct {
	service port.AuthService
}

func NewAuthHandler(service port.AuthService) *AuthHandler {
	return &AuthHandler{service}
}

type LoginRequestBody struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

func (handler *AuthHandler) Login(ctx *gin.Context) {
	var reqBody LoginRequestBody
	if err := ctx.ShouldBindJSON(&reqBody); err != nil {
		sendErrorResponse(ctx, 400, "Failed to convert request body to JSON")
		return
	}

	loginReq := port.LoginRequest{
		Username: reqBody.Username,
		Password: reqBody.Password,
	}
	tokenRes, err := handler.service.Login(
		ctx,
		&loginReq,
	)
	if err != nil {
		switch err {
		case domain.ErrInvalidLoginPayload:
			sendErrorResponse(ctx, 400, "Invalid login payload")
		case domain.ErrUserDoesNotExist:
			sendErrorResponse(ctx, 404, "Username or password are incorrect")
		default:
			sendErrorResponse(ctx, 500, err.Error())
		}
		return
	}

	sendResponse(ctx, 200, map[string]any{
		"id":       tokenRes.Id,
		"token":    tokenRes.Token,
		"expireAt": tokenRes.ExpireAt.Format(time.RFC3339),
	})
}
