package handlers

import (
	"log/slog"
	"strings"
	"time"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/rf003/app_errors"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/rf003/client"
	"github.com/gin-gonic/gin"
)

type Handlers struct {
	usersClient  *client.UsersClient
	routesClient *client.RoutesClient
	postsClient  *client.PostsClient
}

func NewHandlers(
	usersClient *client.UsersClient,
	routesClient *client.RoutesClient,
	postsClient *client.PostsClient,
) *Handlers {
	return &Handlers{
		usersClient:  usersClient,
		routesClient: routesClient,
		postsClient:  postsClient,
	}
}

func (handlers *Handlers) RequirementHandler(ctx *gin.Context) {
	var request RequirementRequest
	err := ctx.ShouldBindJSON(&request)
	if err != nil {
		errorResponse(ctx, 400, "Invalid request format")
		return
	}

	// Validate token
	authHeader := ctx.GetHeader("Authorization")
	if authHeader == "" {
		errorResponse(ctx, 403, "No token provided")
		return
	}
	if !strings.HasPrefix(authHeader, "Bearer ") || len(authHeader) < 8 {
		errorResponse(ctx, 401, "Invalid token")
		return
	}
	token := authHeader[7:]
	userJson, err := handlers.usersClient.GetUserInfo(token)
	if err == app_errors.ErrInvalidToken {
		errorResponse(ctx, 401, "Invalid token")
		return
	}
	if err != nil {
		slog.Error("Error validating token", "error", err.Error())
		msgResponse(ctx, 503, outOfServiceMsg)
		return
	}
	userId := userJson["id"].(string)

	// Check if route is already created
	routes, err := handlers.routesClient.GetRoutesByFlightId(request.FlightId)
	if err != nil {
		slog.Error("Failed to get routes by flight id", "error", err.Error())
		msgResponse(ctx, 503, outOfServiceMsg)
		return
	}
	revertStack := []func(){}
	var routeId string
	var routeCreatedAt time.Time
	if len(routes) == 0 { // Create route if it doesn't exist
		slog.Info("Creating new route")
		createRouteReq := client.CreateRouteRequest{
			FlightId:           request.FlightId,
			SourceAirportCode:  request.Origin.AirportCode,
			SourceCountry:      request.Origin.Country,
			DestinyAirportCode: request.Destiny.AirportCode,
			DestinyCountry:     request.Destiny.Country,
			BagCost:            request.BagCost,
			PlannedStartDate:   request.PlannedStartDate.Format(time.RFC3339),
			PlannedEndDate:     request.PlannedEndDate.Format(time.RFC3339),
		}
		response, err := handlers.routesClient.CreateRoute(&createRouteReq)
		if err == app_errors.ErrInvalidRouteDates {
			msgResponse(ctx, 412, "Las fechas del trayecto no son válidas")
			return
		}
		if err != nil {
			slog.Error("Failed to create route", "error", err.Error())
			msgResponse(ctx, 503, outOfServiceMsg)
			return
		}
		deleteFunc := func() {
			err := handlers.routesClient.DeleteRoute(routeId)
			if err != nil {
				slog.Error("Failed to delete route", "error", err.Error())
			}
		}
		revertStack = append(revertStack, deleteFunc)

		routeId = response.Id
		routeCreatedAt, err = time.Parse(time.RFC3339, response.CreatedAt)
		if err != nil {
			slog.Error("Failed to parse routeCreatedAt to time", "error", err.Error())
			msgResponse(ctx, 503, outOfServiceMsg)
			revertTransactions(revertStack)
			return
		}
	} else { // Use existing route data
		routeId = routes[0]["id"].(string)
		routeCreatedAt, err = time.Parse(time.RFC3339, routes[0]["createdAt"].(string))
		if err != nil {
			slog.Error("Failed to parse existing routeCreatedAt to time", "error", err.Error())
			msgResponse(ctx, 503, outOfServiceMsg)
			return
		}
	}

	// Validate user doesn't have a post for same route
	expire := false
	posts, err := handlers.postsClient.GetPosts(client.GetPostsQueryParams{
		Expire:  &expire,
		RouteId: &routeId,
		UserId:  &userId,
	})
	if err != nil {
		slog.Error("Failed to get posts", "error", err.Error())
		msgResponse(ctx, 503, outOfServiceMsg)
		revertTransactions(revertStack)
		return
	}
	if len(posts) > 0 {
		msgResponse(ctx, 412, "El usuario ya tiene una publicación para la misma fecha")
		revertTransactions(revertStack)
		return
	}

	// Create post
	createPostReq := client.CreatePostRequest{
		RouteId:  routeId,
		ExpireAt: request.ExpireAt.Format(time.RFC3339),
		UserId:   userId,
	}
	createPostResp, err := handlers.postsClient.CreatePost(&createPostReq)
	if err == app_errors.ErrInvalidExpireAt {
		msgResponse(ctx, 412, "La fecha expiración no es válida")
		revertTransactions(revertStack)
		return
	}
	if err != nil {
		slog.Error("Failed to create post", "error", err.Error())
		errorResponse(ctx, 503, outOfServiceMsg)
		revertTransactions(revertStack)
		return
	}

	// Successful transaction
	respJson := map[string]any{
		"data": map[string]any{
			"id":        createPostResp.Id,
			"userId":    userId,
			"createdAt": createPostResp.CreatedAt,
			"expireAt":  request.ExpireAt.Format(time.RFC3339),
			"route": map[string]any{
				"id":        routeId,
				"createdAt": routeCreatedAt.Format(time.RFC3339),
			},
		},
		"msg": "Publicación creada exitosamente",
	}
	jsonResponse(ctx, 201, respJson)
}

func revertTransactions(revertStack []func()) {
	for i := len(revertStack) - 1; i >= 0; i-- {
		revertFunc := revertStack[i]
		revertFunc()
	}
}
