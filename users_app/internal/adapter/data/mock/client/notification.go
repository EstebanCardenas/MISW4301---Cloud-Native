package client

import "github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"

type MockNotificationsClient struct {
	SendNotificationFunc func(request *port.SendNotificationRequest) error
}

func (m *MockNotificationsClient) SendNotification(request *port.SendNotificationRequest) error {
	if m.SendNotificationFunc != nil {
		return m.SendNotificationFunc(request)
	}
	return nil
}
