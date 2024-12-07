package main

import (
	"encoding/csv"
	"fmt"
	"math"
	"os"
	"strconv"
	"sort"
)

func main() {
	// Replace "input.csv" with the path to your input file
	filePath := "day_1.input"

	// Open the file for reading
	file, err := os.Open(filePath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	// Create a CSV reader
	reader := csv.NewReader(file)
	reader.Comma = ' '
	// Read all records from the CSV file
	records, err := reader.ReadAll()
	if err != nil {
		fmt.Println("Error reading CSV file:", err)
		return
	}

	column_x := make([]int, len(records))
	column_y := make([]int, len(records))
	map_of_existence := make(map[int]bool)
	map_of_occurence := make(map[int]int)

	// Process each record
	for rowIndex, record := range records {
		for colIndex, field := range record {
			num, err := strconv.Atoi(field)
			if err != nil {
			//	fmt.Printf("Error converting '%s' to integer on row %d, column %d: %v\n", field, rowIndex+1, colIndex+1, err)
				continue
			}
//			fmt.Printf("Row %d, Column %d: %d\n", rowIndex+1, colIndex+1, num)
			if colIndex == 0 {
				column_x[rowIndex] = num
				_, exists := map_of_existence[num]
			        if !exists {
			           map_of_existence[num] = true 
			        }
			}
		  	if colIndex == 3 {
				column_y[rowIndex] = num
				count, exists := map_of_occurence[num]
			        if exists {
			           map_of_occurence[num] = count + 1 
			        } else {
				   map_of_occurence[num] = 1
				}
			}

		}
	}
	
	sort.Ints(column_x)
	sort.Ints(column_y)
	var running_sum = 0.0
	for i, val_x := range column_x {
		running_sum += math.Abs(float64(val_x - column_y[i]))
	}
	part_2_sum := 0
	for key, _ := range map_of_existence {
		occ, exists := map_of_occurence[key]
		if exists {
			part_2_sum += key*occ
		}
	}
	fmt.Printf("%.2f\n", running_sum)
	fmt.Printf("%d\n", part_2_sum)
}
