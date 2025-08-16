package http

import (
	"fmt"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/gin-gonic/gin"
)

const (
	UserIdKey = "UserIdKey"
)

func authMiddleware(tokenService port.TokenService) gin.HandlerFunc {
	return func(ctx *gin.Context) {
		authHeader := ctx.GetHeader("Authorization")
		if len(authHeader) < 8 {
			ctx.AbortWithStatusJSON(403, gin.H{
				"error": "Auth header missing or invalid header length",
			})
			return
		}
		if authHeader[:7] != "Bearer " {
			ctx.AbortWithStatusJSON(401, gin.H{
				"error": "Auth header must be a bearer token",
			})
			return
		}

		token := authHeader[7:]
		payload, err := tokenService.VerifyToken(token)
		if err != nil {
			switch err {
			case domain.ErrExpiredToken:
				ctx.AbortWithStatusJSON(401, gin.H{
					"error": "Token has expired",
				})
			case domain.ErrInvalidToken:
				ctx.AbortWithStatusJSON(401, gin.H{
					"error": "Token is invalid",
				})
			}
			return
		}

		ctx.Set(UserIdKey, fmt.Sprint(*payload))
		ctx.Next()
	}
}
