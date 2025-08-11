package http

import (
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

type Router struct {
	*gin.Engine
}

func NewRouter(
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

	// Add auth EPs
	authGroup := usersGroup.Group("/auth")
	authGroup.POST("/", authHandler.Login)

	return &Router{router}
}

func (router *Router) Serve(addr string) error {
	err := router.Run(addr)
	if err != nil {
		return err
	}

	return nil
}
