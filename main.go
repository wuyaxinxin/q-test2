package main

import (
	"fmt"
	"log"
)

// Person represents a person entity
type Person struct {
	Name string
	Age  int
}

// Student represents a student entity
type Student struct {
	Person
	StudentID string
	Grade     string
}

// NewPerson creates a new Person instance
func NewPerson(name string, age int) *Person {
	return &Person{
		Name: name,
		Age:  age,
	}
}

// NewStudent creates a new Student instance
func NewStudent(name string, age int, studentID, grade string) *Student {
	return &Student{
		Person: Person{
			Name: name,
			Age:  age,
		},
		StudentID: studentID,
		Grade:     grade,
	}
}

// GetInfo returns person information
func (p *Person) GetInfo() string {
	return fmt.Sprintf("Name: %s, Age: %d", p.Name, p.Age)
}

// GetInfo returns student information
func (s *Student) GetInfo() string {
	return fmt.Sprintf("Name: %s, Age: %d, StudentID: %s, Grade: %s",
		s.Name, s.Age, s.StudentID, s.Grade)
}

func main() {
	// Create a person
	person := NewPerson("John Doe", 30)
	fmt.Println("Person Info:", person.GetInfo())

	// Create a student
	student := NewStudent("Jane Smith", 20, "S12345", "A")
	fmt.Println("Student Info:", student.GetInfo())

	log.Println("Program executed successfully")
}
