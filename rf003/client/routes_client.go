package client

import (
	"fmt"
	"os"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/rf003/app_errors"
	"github.com/go-resty/resty/v2"
)

type RoutesClient struct {
	host       string
	httpClient *resty.Client
}

func NewRoutesClient() *RoutesClient {
	host := os.Getenv("ROUTES_HOST")
	httpClient := resty.New()

	return &RoutesClient{host, httpClient}
}

func (client *RoutesClient) GetRoutesByFlightId(flightId string) ([](map[string]any), error) {
	url := fmt.Sprintf("%v/routes?flight=%v", client.host, flightId)
	respJson := []map[string]any{}
	resp, err := client.httpClient.R().
		SetResult(&respJson).
		Get(url)
	if err != nil {
		return nil, err
	}
	if resp.StatusCode() != 200 {
		return nil, app_errors.ErrInternalServer
	}

	return respJson, nil
}

func (client *RoutesClient) CreateRoute(request *CreateRouteRequest) (*CreateRouteResponse, error) {
	url := fmt.Sprintf("%v/routes", client.host)
	var response CreateRouteResponse
	resp, err := client.httpClient.R().
		SetBody(request).
		SetResult(&response).
		Post(url)
	if err != nil {
		return nil, err
	}
	if resp.StatusCode() == 412 {
		return nil, app_errors.ErrInvalidRouteDates
	}
	if resp.StatusCode() != 201 {
		return nil, app_errors.ErrInternalServer
	}

	return &response, nil
}

func (client *RoutesClient) DeleteRoute(routeId string) error {
	url := fmt.Sprintf("%v/routes/%v", client.host, routeId)
	resp, err := client.httpClient.R().
		Delete(url)
	if err != nil {
		return err
	}
	if resp.StatusCode() != 200 {
		return app_errors.ErrInternalServer
	}

	return nil
}
