package util

import (
	"errors"
	"regexp"

	"golang.org/x/crypto/bcrypt"
)

// HashPassword hashes input password using bcrypt and returns the hashed password and its salt
func HashPassword(password string) (string, string, error) {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return "", "", err
	}

	re := regexp.MustCompile(`^\$2a\$\d{2}\$([./A-Za-z0-9]{22})`)
	hashedPasswordStr := string(hashedPassword)
	matches := re.FindStringSubmatch(hashedPasswordStr)
	if len(matches) > 1 {
		salt := matches[1]
		return hashedPasswordStr, salt, nil
	} else {
		return "", "", errors.New("failed to extract hashed password salt")
	}
}

// ComparePassword compares input password with hashed password
func ComparePassword(password, hashedPassword string) error {
	return bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(password))
}
