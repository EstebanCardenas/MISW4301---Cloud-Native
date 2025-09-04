package handlers

import "github.com/gin-gonic/gin"

func jsonResponse(ctx *gin.Context, code int, body map[string]any) {
	ctx.JSON(code, body)
}

func errorResponse(ctx *gin.Context, code int, msg string) {
	ctx.JSON(code, gin.H{
		"error": msg,
	})
}

func msgResponse(ctx *gin.Context, code int, msg string) {
	ctx.JSON(code, gin.H{
		"msg": msg,
	})
}
