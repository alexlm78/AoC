package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

// Function to check if a report is safe
func isSafeReport(levels []int) bool {
	if len(levels) < 2 {
		return true // A report with less than 2 levels is trivially safe
	}

	// Check if the levels are strictly increasing or decreasing
	increasing := true
	decreasing := true

	for i := 1; i < len(levels); i++ {
		diff := levels[i] - levels[i-1]
		var iDiff int64 = int64(diff)
		iDiff = int64(math.Abs(float64(iDiff)))
		if iDiff < 1 || iDiff > 3 {
			return false
		}
		if iDiff > 0 {
			decreasing = false
		} else if diff < 0 {
			increasing = false
		}
	}

	return increasing || decreasing
}

func main() {
	// Open the input file
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatalf("failed to open file: %s", err)
	}
	defer file.Close()

	// Initialize a counter for safe reports
	safeReportsCount := 0

	// Read the file line by line
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		// Split the line into parts and convert them to integers
		parts := strings.Fields(line)
		var levels []int
		for _, part := range parts {
			level, err := strconv.Atoi(part)
			if err != nil {
				log.Fatalf("failed to parse number: %s", err)
			}
			levels = append(levels, level)
		}

		// Check if the report is safe
		if isSafeReport(levels) {
			safeReportsCount++
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatalf("error reading file: %s", err)
	}

	// Print the number of safe reports
	fmt.Printf("Number of safe reports: %d\n", safeReportsCount)
}
