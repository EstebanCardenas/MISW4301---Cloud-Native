package http

import "github.com/gin-gonic/gin"

func sendResponse(
	ctx *gin.Context,
	statusCode int,
	data any,
) {
	ctx.JSON(statusCode, data)
}
