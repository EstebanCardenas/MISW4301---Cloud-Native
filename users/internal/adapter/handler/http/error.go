package http

import "github.com/gin-gonic/gin"

type ErrorResponse struct {
	ErrorMsg string `json:"error"`
}

func sendErrorResponse(
	ctx *gin.Context,
	statusCode int,
	msg string,
) {
	ctx.JSON(statusCode, ErrorResponse{
		ErrorMsg: msg,
	})
}
