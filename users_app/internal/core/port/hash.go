package port

type HashService interface {
	HashPassword(password string) (string, string, error)
	ComparePassword(password, hashedPassword string) error
	Hash256(token string) string
}
