package client

// ROUTES

type CreateRouteRequest struct {
	FlightId           string  `json:"flightId"`
	SourceAirportCode  string  `json:"sourceAirportCode"`
	SourceCountry      string  `json:"sourceCountry"`
	DestinyAirportCode string  `json:"destinyAirportCode"`
	DestinyCountry     string  `json:"destinyCountry"`
	BagCost            float64 `json:"bagCost"`
	PlannedStartDate   string  `json:"plannedStartDate"`
	PlannedEndDate     string  `json:"plannedEndDate"`
}

type CreateRouteResponse struct {
	Id        string `json:"id"`
	CreatedAt string `json:"createdAt"`
}

// POSTS

type CreatePostRequest struct {
	RouteId  string `json:"routeId"`
	ExpireAt string `json:"expireAt"`
	UserId   string `json:"userId"`
}

type CreatePostResponse struct {
	Id        string `json:"id"`
	UserId    string `json:"userId"`
	CreatedAt string `json:"createdAt"`
}

type GetPostsQueryParams struct {
	Expire  *bool
	RouteId *string
	UserId  *string
}

type Post struct {
	ID        string `json:"id"`
	RouteID   string `json:"routeId"`
	UserID    string `json:"userId"`
	ExpireAt  string `json:"expireAt"`
	CreatedAt string `json:"createdAt"`
}
