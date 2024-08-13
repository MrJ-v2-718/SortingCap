# MrJ       |
# Sorting   |
# 7/16/2024 |
# ----------

import tkinter as tk
from tkinter import filedialog, messagebox, font
import time
import statistics


# Sorting Algorithms

def timsort(arr):
    return sorted(arr)


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# Explanations for Sorting Algorithms

explanations = {
    "Timsort": "Timsort is a hybrid sorting algorithm derived from merge sort and insertion sort. It divides the array "
               "into small segments, sorts them using insertion sort, and then merges them using merge sort.",
    "Quicksort": "Quicksort is a divide-and-conquer algorithm. It works by selecting a 'pivot' element and partitioning"
                 " the other elements into two sub-arrays, according to whether they are less than or greater than the "
                 "pivot. The sub-arrays are then sorted recursively.",
    "Merge Sort": "Merge Sort is a divide-and-conquer algorithm that divides the array into two halves, sorts each "
                  "half, and then merges the sorted halves to produce the final sorted array.",
    "Bubble Sort": "Bubble Sort repeatedly steps through the list, compares adjacent elements, and swaps them if they "
                   "are in the wrong order. The pass through the list is repeated until the list is sorted.",
    "Selection Sort": "Selection Sort divides the input list into two parts: a sorted sublist of items which is built "
                      "up from left to right and a sublist of the remaining unsorted items. The algorithm proceeds by "
                      "finding the smallest element in the unsorted sublist, swapping it with the leftmost unsorted "
                      "element, and moving the sublist boundaries one element to the right."
}


def about_click():
    messagebox.showinfo(
        "About",
        f"Created by MrJ\n        2024©"
    )


def help_click():
    messagebox.showinfo(
        "Help",
        "Open a file, select a sort type, and select a sort order to start sorting with the sorting cap."
    )


# GUI Application
class SortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SortingCap")
        self.root.geometry("512x768")

        self.sort_type = tk.StringVar(value="Timsort")
        self.sort_order = tk.StringVar(value="Ascending")
        self.theme = tk.StringVar(value="Light")

        self.create_menu()
        self.create_widgets()
        self.apply_theme()

        self.file_path = None
        self.numbers = []
        self.sorted_numbers = []

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Save Sorted File", command=self.save_sorted_file)

        sort_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Sort", menu=sort_menu)
        sort_menu.add_radiobutton(label="Timsort", variable=self.sort_type, value="Timsort")
        sort_menu.add_radiobutton(label="Quicksort", variable=self.sort_type, value="Quicksort")
        sort_menu.add_radiobutton(label="Merge Sort", variable=self.sort_type, value="Merge Sort")
        sort_menu.add_radiobutton(label="Bubble Sort", variable=self.sort_type, value="Bubble Sort")
        sort_menu.add_radiobutton(label="Selection Sort", variable=self.sort_type, value="Selection Sort")

        order_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Order", menu=order_menu)
        order_menu.add_radiobutton(label="Ascending", variable=self.sort_order, value="Ascending")
        order_menu.add_radiobutton(label="Descending", variable=self.sort_order, value="Descending")

        theme_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_radiobutton(label="Light", variable=self.theme, value="Light", command=self.apply_theme)
        theme_menu.add_radiobutton(label="Dark", variable=self.theme, value="Dark", command=self.apply_theme)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help", command=help_click)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=about_click)

    def create_widgets(self):
        self.font_style = font.Font(family="Helvetica", size=14)

        self.start_button = tk.Button(self.root, text="Start Sorting", command=self.start_sorting, font=self.font_style)
        self.start_button.pack(pady=10)

        self.result_text = tk.Text(self.root, font=self.font_style, wrap=tk.WORD)
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.file_path:
            with open(self.file_path, "r") as file:
                self.numbers = list(map(int, file.read().split()))
            messagebox.showinfo("File Opened", "File loaded successfully.")

    def save_sorted_file(self):
        if not self.sorted_numbers:
            messagebox.showwarning("No Data", "No sorted data to save.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if save_path:
            with open(save_path, "w") as file:
                for num in self.sorted_numbers:
                    file.write(f"{num}\n")
            messagebox.showinfo("File Saved", "Sorted file saved successfully.")

    def start_sorting(self):
        if not self.file_path:
            messagebox.showwarning("No File", "Please open a file first.")
            return

        sort_func = self.get_sort_function()
        start_time = time.time()

        self.sorted_numbers = sort_func(self.numbers[:])
        if self.sort_order.get() == "Descending":
            self.sorted_numbers = self.sorted_numbers[::-1]

        end_time = time.time()
        elapsed_time = end_time - start_time

        self.display_results(elapsed_time)

    def get_sort_function(self):
        sort_type = self.sort_type.get()
        if sort_type == "Quicksort":
            return quicksort
        elif sort_type == "Merge Sort":
            return merge_sort
        elif sort_type == "Bubble Sort":
            return bubble_sort
        elif sort_type == "Selection Sort":
            return selection_sort
        else:
            return timsort

    def display_results(self, elapsed_time):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Sorted using: {self.sort_type.get()}\n")
        self.result_text.insert(tk.END, f"Sort Order: {self.sort_order.get()}\n")
        self.result_text.insert(tk.END, f"Time Taken: {elapsed_time:.6f} seconds\n\n")
        self.result_text.insert(tk.END, f"Min Number: {min(self.sorted_numbers)}\n")
        self.result_text.insert(tk.END, f"Max Number: {max(self.sorted_numbers)}\n")
        self.result_text.insert(tk.END, f"Average: {statistics.mean(self.sorted_numbers):.2f}\n")
        self.result_text.insert(tk.END, f"Count: {len(self.sorted_numbers)}\n\n")
        self.result_text.insert(tk.END, "Explanation of the Sort:\n")
        self.result_text.insert(tk.END, explanations[self.sort_type.get()] + "\n\n")
        self.result_text.insert(tk.END, "Sorted Numbers:\n")
        self.result_text.insert(tk.END, "\n".join(map(str, self.sorted_numbers)))

    def apply_theme(self):
        theme = self.theme.get()
        if theme == "Light":
            bg_color = "white"
            fg_color = "black"
            self.root.config(bg=bg_color)
        else:
            bg_color = "#2e2e2e"
            fg_color = "white"
            self.root.config(bg=bg_color)

        self.start_button.config(bg=bg_color, fg=fg_color)
        self.result_text.config(bg=bg_color, fg=fg_color)


# Run the Application

if __name__ == "__main__":
    root = tk.Tk()
    app = SortApp(root)
    root.mainloop()
