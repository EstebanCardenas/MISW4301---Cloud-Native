package mock

import (
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func NewTestDb() (*gorm.DB, error) {
	db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	if err != nil {
		return nil, err
	}

	return db, nil
}
