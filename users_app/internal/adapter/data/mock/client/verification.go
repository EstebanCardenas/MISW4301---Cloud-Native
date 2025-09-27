package client

import "github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/users/internal/core/port"

type MockVerificationClient struct {
	CreateVerificationFunc func(*port.VerificationRequestPayload) error
}

func (m *MockVerificationClient) CreateVerificationRequest(payload *port.VerificationRequestPayload) error {
	return m.CreateVerificationFunc(payload)
}
