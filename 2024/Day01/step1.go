package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {
	// Open the input file
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatalf("failed to open file: %s", err)
	}
	defer file.Close()

	// Initialize lists to hold the location IDs
	var leftList, rightList []int

	// Read the file line by line
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		// Split the line into two parts based on the two spaces
		parts := strings.Split(line, "   ")
		if len(parts) != 2 {
			log.Fatalf("unexpected line format: %s", line)
		}
		// Trim any leading or trailing whitespace from the parts
		leftStr := strings.TrimSpace(parts[0])
		rightStr := strings.TrimSpace(parts[1])
		// Parse the numbers into integers
		leftNum, err := strconv.Atoi(leftStr)
		if err != nil {
			log.Fatalf("failed to parse number: %s", err)
		}
		rightNum, err := strconv.Atoi(rightStr)
		if err != nil {
			log.Fatalf("failed to parse number: %s", err)
		}
		// Append the numbers to the respective lists
		leftList = append(leftList, leftNum)
		rightList = append(rightList, rightNum)
	}

	if err := scanner.Err(); err != nil {
		log.Fatalf("error reading file: %s", err)
	}

	// Sort both lists
	sort.Ints(leftList)
	sort.Ints(rightList)

	// Calculate the total distance
	totalDistance := 0
	for i := 0; i < len(leftList); i++ {
		distance := abs(leftList[i] - rightList[i])
		totalDistance += distance
	}

	// Print the total distance
	fmt.Printf("Total distance: %d\n", totalDistance)
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}
