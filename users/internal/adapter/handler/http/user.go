package http

import (
	"log/slog"
	"strconv"
	"time"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/gin-gonic/gin"
)

type UserHandler struct {
	service port.UserService
}

func NewUserHandler(service port.UserService) *UserHandler {
	return &UserHandler{service}
}

type CreateUserRequestBody struct {
	Username    string  `json:"username"`
	Password    string  `json:"password"`
	Email       string  `json:"email"`
	Dni         *string `json:"dni"`
	FullName    *string `json:"fullName"`
	PhoneNumber *string `json:"phoneNumber"`
}

func (handler *UserHandler) CreateUser(ctx *gin.Context) {
	var reqBody CreateUserRequestBody
	if err := ctx.ShouldBindJSON(&reqBody); err != nil {
		sendErrorResponse(ctx, 400, "Missing fields from request body")
		return
	}

	createUserReq := port.CreateUserRequest{
		Username:    reqBody.Username,
		Password:    reqBody.Password,
		Email:       reqBody.Email,
		Dni:         reqBody.Dni,
		FullName:    reqBody.FullName,
		PhoneNumber: reqBody.PhoneNumber,
	}
	res, err := handler.service.CreateUser(ctx, &createUserReq)
	if err != nil {
		slog.Info("Error while creating user", "error", err)
		switch err {
		case domain.ErrUsernameOrEmailExists:
			sendErrorResponse(ctx, 412, "Username or email already exists")
		case domain.ErrInvalidCreateUserPayload:
			sendErrorResponse(ctx, 400, "Missing fields from request body")
		default:
			sendErrorResponse(ctx, 500, err.Error())
		}
		return
	}

	sendResponse(ctx, 201, map[string]any{
		"id":        res.Id,
		"createdAt": res.CreatedAt.Format(time.RFC3339),
	})
}

type UpdateUserRequestBody struct {
	FullName    string             `json:"fullName"`
	PhoneNumber string             `json:"phoneNumber"`
	Dni         string             `json:"dni"`
	Status      *domain.UserStatus `json:"status"`
}

func (handler *UserHandler) UpdateUser(ctx *gin.Context) {
	var reqBody UpdateUserRequestBody
	if err := ctx.ShouldBindJSON(&reqBody); err != nil {
		sendErrorResponse(ctx, 400, "Failed to convert request body to JSON")
		return
	}

	id, err := strconv.Atoi(ctx.Param("id"))
	if err != nil {
		sendErrorResponse(ctx, 400, "Invalid user ID")
		return
	}
	updateUserReq := port.UpdateUserRequest{
		FullName:    reqBody.FullName,
		PhoneNumber: reqBody.PhoneNumber,
		Dni:         reqBody.Dni,
		Status:      reqBody.Status,
	}
	err = handler.service.UpdateUser(ctx, id, &updateUserReq)
	if err != nil {
		switch err {
		case domain.ErrInvalidUpdateUserPayload:
			sendErrorResponse(ctx, 400, "Request body doesn't contain any expected field")
		case domain.ErrInvalidUserStatus:
			sendErrorResponse(ctx, 400, "User status must be either POR_VERIFICAR, NO_VERIFICADO or VERIFICADO")
		case domain.ErrUserDoesNotExist:
			sendErrorResponse(ctx, 404, "User with given ID doesn't exist")
		default:
			sendErrorResponse(ctx, 500, "Internal server error")
		}
		return
	}

	sendResponse(ctx, 200, map[string]string{
		"msg": "el usuario ha sido actualizado",
	})
}
