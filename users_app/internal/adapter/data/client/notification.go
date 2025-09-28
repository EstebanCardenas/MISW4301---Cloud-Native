package client

import (
	"fmt"
	"os"

	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"
	"github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"
	"github.com/go-resty/resty/v2"
)

type EmailNotificationClient struct {
	restyClient *resty.Client
	host        string
}

func NewEmailNotificationClient() *EmailNotificationClient {
	restyClient := resty.New()
	host := os.Getenv("NOTIFICATIONS_HOST")

	return &EmailNotificationClient{
		restyClient: restyClient,
		host:        host,
	}
}

func (client *EmailNotificationClient) SendNotification(request *port.SendNotificationRequest) error {
	url := fmt.Sprintf("%v/notifications", client.host)
	bodyJson := map[string]any{
		"template": request.Template,
		"to":       request.To,
		"subject":  request.Subject,
		"data": map[string]any{
			"estado_final":    request.Data.FinalState,
			"ruv":             request.Data.RUV,
			"nombre_completo": request.Data.FullName,
			"dni":             request.Data.DNI,
			"numero":          request.Data.PhoneNumber,
		},
	}
	resp, err := client.restyClient.R().
		SetBody(&bodyJson).
		Post(url)
	if err != nil {
		return err
	}
	if resp.StatusCode() != 200 {
		return domain.ErrInternal
	}

	return nil
}
