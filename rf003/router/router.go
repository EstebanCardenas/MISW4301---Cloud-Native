package router

import (
	"net/http"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/rf003/handlers"
	"github.com/gin-gonic/gin"
)

func NewGinRouter(
	handlers *handlers.Handlers,
) *gin.Engine {
	router := gin.Default()
	reqPath := "/rf003/posts"
	// Register ping handler
	router.HEAD(reqPath, func(ctx *gin.Context) {
		ctx.Header("Content-Type", "application/json")
		ctx.Status(http.StatusOK)
	})
	// Register real handler
	router.POST(reqPath, handlers.RequirementHandler)
	return router
}
