package mock

type MockHashService struct {
	HashPasswordFunc    func(password string) (string, string, error)
	ComparePasswordFunc func(password, hashedPassword string) error
	Hash256Func         func(token string) string
}

func (m *MockHashService) HashPassword(password string) (string, string, error) {
	if m.HashPasswordFunc != nil {
		return m.HashPasswordFunc(password)
	}
	return "", "", nil
}

func (m *MockHashService) ComparePassword(password, hashedPassword string) error {
	if m.ComparePasswordFunc != nil {
		return m.ComparePasswordFunc(password, hashedPassword)
	}
	return nil
}

func (m *MockHashService) Hash256(token string) string {
	if m.Hash256Func != nil {
		return m.Hash256Func(token)
	}
	return ""
}
