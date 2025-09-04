package client

import (
	"fmt"
	"os"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/rf003/app_errors"
	"github.com/go-resty/resty/v2"
)

type UsersClient struct {
	host       string
	httpClient *resty.Client
}

func NewUsersClient() *UsersClient {
	host := os.Getenv("USERS_HOST")
	httpClient := resty.New()

	return &UsersClient{
		host:       host,
		httpClient: httpClient,
	}
}

func (client *UsersClient) GetUserInfo(token string) (map[string]any, error) {
	url := fmt.Sprintf("%v/users/me", client.host)
	var respJson map[string]any
	resp, err := client.httpClient.R().
		SetAuthToken(token).
		SetResult(&respJson).
		Get(url)
	if err != nil {
		return nil, err
	}
	if resp.StatusCode() == 401 {
		return nil, app_errors.ErrInvalidToken
	}
	if resp.StatusCode() != 200 {
		return nil, app_errors.ErrInternalServer
	}

	return respJson, nil
}
