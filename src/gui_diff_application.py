#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import ttk
from tkinter import Listbox
from difflib import ndiff

class DiffViewerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Diff Viewer Application")

        # Create a PanedWindow
        self.paned_window = ttk.PanedWindow(self.master, orient=tk.VERTICAL)  # Change to VERTICAL
        self.paned_window.pack(fill=tk.BOTH, expand=1)

        # Left Frame for Tree View
        self.left_frame = ttk.Frame(self.paned_window, width=200, height=200, relief=tk.SUNKEN)
        self.paned_window.add(self.left_frame, weight=1)

        # Create tree view in the left frame
        self.tree_view = ttk.Treeview(self.left_frame)
        self.tree_view.pack(fill=tk.BOTH, expand=1)

        # Bind the tree view selection event to a callback
        self.tree_view.bind('<<TreeviewSelect>>', self.on_tree_select)

        # Populate the tree view
        self.populate_tree_view()

        # New Frame for List View
        self.list_frame = ttk.Frame(self.paned_window, width=200, height=200, relief=tk.SUNKEN)
        self.paned_window.add(self.list_frame, weight=1)

        # Create list view in the list frame
        self.list_view = Listbox(self.list_frame)
        self.list_view.pack(fill=tk.BOTH, expand=1)

        # Bind the list view selection event to a callback
        self.list_view.bind('<<ListboxSelect>>', self.on_list_select)

        # Create right frame for diff view
        self.right_frame = ttk.Frame(self.paned_window, width=800, height=400, relief=tk.SUNKEN)
        self.paned_window.add(self.right_frame, weight=2)

        # Create text widgets for side-by-side file view
        self.file1_text = tk.Text(self.right_frame, wrap=tk.NONE, width=40)
        self.file1_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.file2_text = tk.Text(self.right_frame, wrap=tk.NONE, width=40)
        self.file2_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    def populate_tree_view(self):
        """
        Populates the tree view with the structure of .cfg files found in the 'source' directory.
        """
        source_dir = 'source'

        for root, dirs, files in os.walk(source_dir):
            if root == source_dir:
                # Add top-level directories to the tree view
                for directory in dirs:
                    dir_path = os.path.join(root, directory)
                    self.tree_view.insert('', 'end', dir_path, text=directory)
            else:
                # Add files to their respective directory
                parent_dir = os.path.basename(root)
                parent_id = os.path.join(os.path.dirname(root), parent_dir)
                for file in files:
                    if file.endswith('.cfg'):
                        file_path = os.path.join(root, file)
                        self.tree_view.insert(parent_id, 'end', file_path, text=file)

    def on_tree_select(self, event):
        """Callback for when a tree node is selected."""
        selected_item = self.tree_view.selection()
        if selected_item:
            # Assuming a single selection mode
            file_path = selected_item[0]
            print(f"Selected file: {file_path}")

            # Get the directory of the selected .cfg file
            directory = os.path.dirname(file_path)

            # Clear the current list view
            self.list_view.delete(0, tk.END)

            # List all .cpp files in the same directory
            if os.path.isdir(directory):
                cpp_files = [f for f in os.listdir(directory) if f.endswith('.cpp')]

                # Populate the list view with .cpp files
                for cpp_file in cpp_files:
                    self.list_view.insert(tk.END, cpp_file)

    def on_list_select(self, event):
        """Callback for when a .cpp file is selected in the list view."""
        selected_index = self.list_view.curselection()
        if selected_index:
            cpp_file = self.list_view.get(selected_index)
            cfg_file_path = self.tree_view.selection()[0]  # Get the selected .cfg file path
            directory = os.path.dirname(cfg_file_path)
            cfg_file = os.path.basename(cfg_file_path)
            # Remove 'source/' from the directory
            directory = directory.removeprefix('source/')
            # Construct the two file paths
            file1_path = f'source/{directory}/{cpp_file}'
            file2_path = f'formatted/{directory}/{cpp_file[:-4]}+{cfg_file[:-4]}.cpp'
            # Show the diff between constructed file paths
            self.show_diff(file1_path, file2_path)

    def show_diff(self, file1_path: str, file2_path: str):
        """Shows the diff between two specified files with side-by-side view and highlights."""

        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()

        # Use ndiff for more granular diffing
        diff = list(ndiff(file1_lines, file2_lines))

        self.file1_text.delete('1.0', tk.END)
        self.file2_text.delete('1.0', tk.END)

        # Highlight lines based on diff
        file1_line_num = 1
        file2_line_num = 1

        for line in diff:
            if line.startswith('  '):  # Unchanged
                self.file1_text.insert(f'{file1_line_num}.0', line[2:])
                self.file2_text.insert(f'{file2_line_num}.0', line[2:])
                file1_line_num += 1
                file2_line_num += 1
            elif line.startswith('- '):  # Deleted from file1
                self.file1_text.insert(f'{file1_line_num}.0', line[2:], 'deleted')
                file1_line_num += 1
            elif line.startswith('+ '):  # Added to file2
                self.file2_text.insert(f'{file2_line_num}.0', line[2:], 'added')
                file2_line_num += 1

        # Configure tags for highlighting
        self.file1_text.tag_config('deleted', background='lightcoral')
        self.file2_text.tag_config('added', background='lightgreen')


def main():
    root = tk.Tk()
    app = DiffViewerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
