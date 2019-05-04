import statistics
import random
import csv
from collections import defaultdict
import tkinter
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

global test_array 
test_array = []

global percentage
percentage = []

def read_from_csv():
    Tk().withdraw()
    filename = askopenfilename()
    print(filename)
    input_file = filename
    columns = defaultdict(list)
    with open(input_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for (k, v) in row.items():
                columns[k].append(v)

    for min, max in zip(columns['Min'], columns['Max']):
        array = [float(min), float(max)]
        print(array)
        test_array.append(array)

    gen = (per for per in columns['Percentage'] if per not in "")

    for percent in gen:
        percentage.append(percent)
    return input_file    

def write_to_csv(input, output, new_values):
    with open(input, 'r') as fin:
        reader1 = csv.reader(fin, delimiter='\t')
        with open(output, 'w') as fout:
            writer = csv.writer(fout, delimiter='\t')
            writer.writerow(next(reader1) + ["Sigma"] + ["Error"] + ["N"] + ["Average"])
            writer.writerow(next(reader1) + [new_values[0]] +
                            [new_values[1]] +
                            [new_values[2]] +
                            [new_values[3]])
            for row in reader1:
                writer.writerow(row)

def calculate_min_max_list(A):
  min = 0
  max = 0
  for list in A:
    max += list[1]
    min += list[0]
  return [min, max]

def calculate_sigma(list):
  return statistics.stdev(list)

def calculate_error(total, percentage):
  error = (total[1] - total[0]) * (percentage / 100)
  return error

def calculate_num(sigma, error, percentage):
    result = (percentage * sigma) / error
    return result**2;

def calculate_random_array(N, A):
  randomArray = []
  for i in range (1, N):
    r = random.uniform(0, 1) *(A[1] - A[0]) + A[0]
    randomArray.append(r)
  return randomArray  

def calculate_avg(A):
  return sum(A) / (len(A))

def main():
  input_file = read_from_csv()  
  percent = int(percentage[0])

  min_max_list = calculate_min_max_list(test_array)
  print("Min_max_list : ", min_max_list)

  sigma = calculate_sigma(min_max_list)
  print("Sigma: ", sigma)

  error = calculate_error(min_max_list, percent)
  print("Error: ", error)

  iterator = calculate_num(sigma, error, percent)
  print("iterator: ", iterator)

  rand_array = calculate_random_array(int(iterator), min_max_list)
  # print("Rand array: ", rand_array)

  avg = calculate_avg(rand_array)
  print("Final avg : ", avg)

  final_values = [sigma, error, iterator, avg]
  write_to_csv(input_file, "output.csv", final_values)
  
if __name__== "__main__":
  main()
