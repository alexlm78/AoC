package day07

import (
	"advent-of-code/utils"
	"fmt"
	"strconv"
	"strings"
)

func Solve(inputPath string) {
	rows := utils.ReadFileToRows(inputPath)

	var sumP1, sumP2 int
	for _, row := range rows {
		target, chain, err := parseInputRow(row)
		if err != nil {
			panic(err)
		}

		// Part 01
		if IsReachable(target, chain, []Operator{ADD, MUL}) {
			sumP1 += target
		}
		// Part 02
		if IsReachable(target, chain, []Operator{ADD, MUL, CONC}) {
			sumP2 += target
		}
	}

	fmt.Printf("Part 01: %v\n", sumP1)
	fmt.Printf("Part 02: %v\n", sumP2)
}

type Operator int

const (
	ADD Operator = iota
	MUL
	CONC
)

func IsReachable(target int, chain []int, operators []Operator) bool {
	if len(chain) == 1 {
		return target == chain[0]
	}
	if chain[0] > target {
		return false
	}

	for _, op := range operators {
		next := op.Apply(chain[0], chain[1])
		if IsReachable(target, append([]int{next}, chain[2:]...), operators) {
			return true
		}
	}
	return false
}

func (op Operator) Apply(left, right int) int {
	switch op {
	case ADD:
		return left + right
	case MUL:
		return left * right
	case CONC:
		result, err := strconv.Atoi(strconv.Itoa(left) + strconv.Itoa(right))
		if err != nil {
			panic(fmt.Errorf("failed to convert string to integer: %v", err))
		}
		return result
	default:
		panic(fmt.Errorf("invalid operator: %v", op))
	}
}

func parseInputRow(row string) (target int, chain []int, err error) {
	parts := strings.Split(row, ":")
	if len(parts) != 2 {
		return 0, nil, fmt.Errorf("invalid input format: %v", row)
	}

	target, err = strconv.Atoi(parts[0])
	if err != nil {
		return target, chain, fmt.Errorf("invalid target '%v': %v", parts[0], err)
	}

	numStrs := strings.Fields(parts[1])
	chain = make([]int, len(numStrs))
	for i, numStr := range numStrs {
		numInt, err := strconv.Atoi(numStr)
		if err != nil {
			return 0, nil, fmt.Errorf("invalid number '%v': %v", numStr, err)
		}
		chain[i] = numInt
	}

	return target, chain, nil
}