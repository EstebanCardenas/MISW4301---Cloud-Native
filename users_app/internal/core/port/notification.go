package port

import "github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/domain"

type NotificationRequestData struct {
	FinalState  domain.UserStatus
	RUV         string
	FullName    string
	DNI         string
	PhoneNumber string
}

type SendNotificationRequest struct {
	Template string
	To       string
	Subject  string
	Data     NotificationRequestData
}

type NotificationsClient interface {
	SendNotification(request *SendNotificationRequest) error
}
