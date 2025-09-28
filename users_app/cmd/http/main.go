package main

import (
	"fmt"
	"log/slog"
	"os"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/auth"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/data/client"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/data/postgres"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/data/postgres/repository"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/handler/http"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/adapter/hash"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/service"
	"github.com/joho/godotenv"
)

func main() {
	slog.Info("Starting the application")

	// Init vars
	if os.Getenv("DEBUG") == "true" {
		err := godotenv.Load()
		if err != nil {
			slog.Error("Failed to load .env vars", "error", err)
			os.Exit(1)
		}
	}

	// Init db
	conn, err := postgres.NewPostgressConn()
	if err != nil {
		slog.Error("Failed to init database", "error", err)
		os.Exit(1)
	}
	slog.Info("Connected to database successfully")

	// Bycrypt service
	bycryptService := hash.NewBycryptService()

	// Init user
	verificationClient := client.NewTrueNativeClient()
	userRepo, err := repository.NewUserRepository(conn.DB, verificationClient)
	if err != nil {
		slog.Error("Failed to init userRepo", "error", err)
		os.Exit(1)
	}
	notificationsClient := client.NewEmailNotificationClient()
	userService := service.NewUserService(
		userRepo,
		bycryptService,
		notificationsClient,
	)
	userHandler := http.NewUserHandler(userService)

	// Token service
	tokenService := auth.NewTokenService(userRepo)

	// Init auth
	authService := service.NewAuthService(userRepo, tokenService, bycryptService)
	authHandler := http.NewAuthHandler(authService)

	// Init gin router and start server
	router := http.NewRouter(
		tokenService,
		userHandler,
		authHandler,
	)
	serverUrl := os.Getenv("SERVER_URL")
	serverPort := os.Getenv("SERVER_PORT")
	listenAddr := fmt.Sprintf("%s:%s", serverUrl, serverPort)
	slog.Info("Starting server", "listenAddr", listenAddr)
	err = router.Serve(listenAddr)
	if err != nil {
		slog.Error("Failed to start server", "error", err)
		os.Exit(1)
	}

}
