package client

import (
	"fmt"
	"os"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/rf003/app_errors"
	"github.com/go-resty/resty/v2"
)

type PostsClient struct {
	host       string
	httpClient *resty.Client
}

func NewPostsClient() *PostsClient {
	host := os.Getenv("POSTS_HOST")
	httpClient := resty.New()

	return &PostsClient{host, httpClient}
}

func (client *PostsClient) GetPosts(queryParams GetPostsQueryParams) ([]Post, error) {
	queryParamsMap := map[string]string{}
	if queryParams.Expire != nil {
		queryParamsMap["expire"] = fmt.Sprint(*queryParams.Expire)
	}
	if queryParams.RouteId != nil {
		queryParamsMap["route"] = *queryParams.RouteId
	}
	if queryParams.UserId != nil {
		queryParamsMap["owner"] = *queryParams.UserId
	}

	var response []Post
	url := fmt.Sprintf("%v/posts", client.host)
	resp, err := client.httpClient.R().
		SetQueryParams(queryParamsMap).
		SetResult(&response).
		Get(url)
	if err != nil {
		return nil, err
	}
	if resp.StatusCode() != 200 {
		return nil, app_errors.ErrInternalServer
	}

	return response, nil
}

func (client *PostsClient) CreatePost(
	request *CreatePostRequest,
) (*CreatePostResponse, error) {
	url := fmt.Sprintf("%v/posts", client.host)
	var response CreatePostResponse
	resp, err := client.httpClient.R().
		SetBody(request).
		SetResult(&response).
		Post(url)
	if err != nil {
		return nil, err
	}
	if resp.StatusCode() == 412 {
		return nil, app_errors.ErrInvalidExpireAt
	}
	if resp.StatusCode() != 201 {
		return nil, app_errors.ErrInternalServer
	}

	return &response, nil
}
