package handlers

import "time"

type RequirementRequest struct {
	FlightId         string    `json:"flightId" binding:"required"`
	ExpireAt         time.Time `json:"expireAt" binding:"required"`
	PlannedStartDate time.Time `json:"plannedStartDate" binding:"required"`
	PlannedEndDate   time.Time `json:"plannedEndDate" binding:"required"`
	Origin           Airport   `json:"origin" binding:"required"`
	Destiny          Airport   `json:"destiny" binding:"required"`
	BagCost          float64   `json:"bagCost" binding:"required"`
}

type Airport struct {
	AirportCode string `json:"airportCode" binding:"required"`
	Country     string `json:"country" binding:"required"`
}
