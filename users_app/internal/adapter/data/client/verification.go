package client

import (
	"encoding/json"
	"fmt"
	"log/slog"
	"os"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/go-resty/resty/v2"
)

type TrueNativeClient struct {
	restyClient *resty.Client
	host        string
	secretToken string
}

func NewTrueNativeClient() *TrueNativeClient {
	restyClient := resty.New()
	host := os.Getenv("TRUE_NATIVE_HOST")
	secretToken := os.Getenv("TRUE_NATIVE_SECRET_TOKEN")

	return &TrueNativeClient{
		restyClient: restyClient,
		host:        host,
		secretToken: secretToken,
	}
}

func (client *TrueNativeClient) CreateVerificationRequest(payload *port.VerificationRequestPayload) error {
	userMap := map[string]any{
		"email": payload.User.Email,
	}
	if payload.User.Dni != nil {
		userMap["dni"] = *payload.User.Dni
	}
	if payload.User.FullName != nil {
		userMap["fullName"] = *payload.User.FullName
	}
	if payload.User.Phone != nil {
		userMap["phone"] = *payload.User.Phone
	}
	respBody := map[string]any{
		"user":                  userMap,
		"transactionIdentifier": payload.TransactionIdentifier,
		"userIdentifier":        payload.UserIdentifier,
		"userWebhook":           payload.UserWebHook,
	}

	var respJson map[string]any
	url := fmt.Sprintf("%v/native/verify", client.host)
	resp, err := client.restyClient.R().
		SetBody(&respBody).
		SetResult(&respJson).
		SetAuthToken(client.secretToken).
		Post(url)
	if err != nil {
		return err
	}
	if resp.StatusCode() != 201 {
		slog.Error("Failed to create verification request", "statusCode", resp.StatusCode())
		slog.Error("Failed to create verification request", "error", resp.Error())
		return domain.ErrInternal
	}

	jsonBytes, err := json.MarshalIndent(respJson, "", "  ")
	if err == nil {
		fmt.Println(string(jsonBytes))
	}

	return nil
}
