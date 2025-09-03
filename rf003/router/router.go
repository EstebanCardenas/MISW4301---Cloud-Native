package router

import (
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/rf003/handlers"
	"github.com/gin-gonic/gin"
)

func NewGinRouter(
	handlers *handlers.Handlers,
) *gin.Engine {
	router := gin.Default()
	router.POST("/rf003/posts", handlers.RequirementHandler)
	return router
}
