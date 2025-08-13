package http

import (
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

type Router struct {
	*gin.Engine
}

func NewRouter(
	tokenService port.TokenService,
	userHandler *UserHandler,
	authHandler *AuthHandler,
) *Router {
	// CORS config
	ginConfig := cors.DefaultConfig()
	ginConfig.AllowOrigins = []string{"*"}

	// Init router
	router := gin.New()
	router.Use(gin.Recovery(), cors.New(ginConfig))

	// Add user EPs
	usersGroup := router.Group("/users")
	usersGroup.POST("/", userHandler.CreateUser)
	usersGroup.PATCH("/:id", userHandler.UpdateUser)
	usersGroup.GET("/me", authMiddleware(tokenService), userHandler.QueryMyself)
	usersGroup.GET("/count", userHandler.GetUserCount)
	usersGroup.POST("/reset", userHandler.ResetUsers)

	// Add auth EPs
	authGroup := usersGroup.Group("/auth")
	authGroup.POST("/", authHandler.Login)

	// Add healthcheck
	pingGroup := usersGroup.Group("/ping")
	pingGroup.GET("/", healthcheck)

	return &Router{router}
}

func (router *Router) Serve(addr string) error {
	err := router.Run(addr)
	if err != nil {
		return err
	}

	return nil
}

func healthcheck(ctx *gin.Context) {
	ctx.String(200, "pong")
}
