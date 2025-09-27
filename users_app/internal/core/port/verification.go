package port

type VerificationClient interface {
	CreateVerificationRequest(payload *VerificationRequestPayload) error
}
