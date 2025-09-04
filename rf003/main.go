package main

import (
	"fmt"
	"log"
	"log/slog"
	"os"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/rf003/client"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/rf003/handlers"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/rf003/router"
	"github.com/gin-gonic/gin"
)

func main() {
	slog.Info("Starting application")

	// Instantiate clients
	usersClient := client.NewUsersClient()
	routesClient := client.NewRoutesClient()
	postsClient := client.NewPostsClient()

	// Init routes
	handlers := handlers.NewHandlers(
		usersClient, routesClient, postsClient,
	)
	router := router.NewGinRouter(handlers)

	// Start server
	err := startServer(router)
	if err != nil {
		log.Fatalf("Failed to boot server: %v", err.Error())
	}
}

func startServer(router *gin.Engine) error {
	serverUrl := os.Getenv("SERVER_URL")
	serverPort := os.Getenv("SERVER_PORT")
	listenAddr := fmt.Sprintf("%s:%s", serverUrl, serverPort)
	slog.Info("Starting server", "listenAddr", listenAddr)

	return router.Run(listenAddr)
}
