package postgres

import (
	"fmt"
	"log/slog"
	"os"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type PostgresConn struct {
	DB *gorm.DB
}

func NewPostgressConn() (*PostgresConn, error) {
	dsnConfig := []struct {
		variable string
		value    string
	}{
		{"host", os.Getenv("DB_HOST")},
		{"user", os.Getenv("DB_USER")},
		{"password", os.Getenv("DB_PASSWORD")},
		{"dbname", os.Getenv("DB_NAME")},
		{"port", os.Getenv("DB_PORT")},
	}
	dsn := ""
	for i, configValue := range dsnConfig {
		dsn += fmt.Sprintf("%v=%v", configValue.variable, configValue.value)
		if i != len(dsnConfig)-1 {
			dsn += " "
		}
	}
	slog.Info("Current DSN", "dsn", dsn)
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		return nil, err
	}

	return &PostgresConn{db}, nil
}
