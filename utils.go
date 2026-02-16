package main

import (
	"encoding/json"
	"fmt"
	"regexp"
	"strings"
)

// Validator provides validation utilities
type Validator struct{}

// ValidateEmail validates email format
func (v *Validator) ValidateEmail(email string) bool {
	emailRegex := regexp.MustCompile(`^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$`)
	return emailRegex.MatchString(email)
}

// ValidateAge validates age range
func (v *Validator) ValidateAge(age int) bool {
	return age >= 0 && age <= 150
}

// ValidateStudentID validates student ID format
func (v *Validator) ValidateStudentID(studentID string) bool {
	if len(studentID) == 0 {
		return false
	}
	studentIDRegex := regexp.MustCompile(`^[A-Z]\d{4,6}$`)
	return studentIDRegex.MatchString(studentID)
}

// IsEmpty checks if a string is empty or contains only whitespace
func IsEmpty(str string) bool {
	return len(strings.TrimSpace(str)) == 0
}

// Capitalize capitalizes the first letter of a string
func Capitalize(str string) string {
	if IsEmpty(str) {
		return str
	}
	return strings.ToUpper(str[:1]) + str[1:]
}

// ToJSON converts an object to JSON string
func ToJSON(obj interface{}) (string, error) {
	jsonBytes, err := json.MarshalIndent(obj, "", "  ")
	if err != nil {
		return "", fmt.Errorf("failed to marshal to JSON: %w", err)
	}
	return string(jsonBytes), nil
}

// FromJSON parses JSON string to an object
func FromJSON(jsonStr string, obj interface{}) error {
	err := json.Unmarshal([]byte(jsonStr), obj)
	if err != nil {
		return fmt.Errorf("failed to unmarshal JSON: %w", err)
	}
	return nil
}

// Contains checks if a slice contains a specific element
func Contains(slice []string, item string) bool {
	for _, s := range slice {
		if s == item {
			return true
		}
	}
	return false
}

// Filter filters a slice based on a predicate function
func Filter(slice []string, predicate func(string) bool) []string {
	result := make([]string, 0)
	for _, item := range slice {
		if predicate(item) {
			result = append(result, item)
		}
	}
	return result
}

// Map applies a function to each element in a slice
func Map(slice []string, mapper func(string) string) []string {
	result := make([]string, len(slice))
	for i, item := range slice {
		result[i] = mapper(item)
	}
	return result
}
