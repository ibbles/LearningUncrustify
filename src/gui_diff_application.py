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
        self.paned_window = ttk.PanedWindow(self.master, orient=tk.VERTICAL)
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

        # Add a shared vertical scrollbar for the diff view
        self.diff_scrollbar = tk.Scrollbar(self.right_frame, orient=tk.VERTICAL)
        self.diff_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create text widgets for side-by-side file view
        self.file1_text = tk.Text(self.right_frame, wrap=tk.NONE, width=40)
        self.file1_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.file2_text = tk.Text(self.right_frame, wrap=tk.NONE, width=40)
        self.file2_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # These mappings will be created anew in show_diff()
        self.file1_to_file2 = []
        self.file2_to_file1 = []

        # Attach scroll events
        self.file1_text.config(yscrollcommand=self.on_file1_yscroll)
        self.file2_text.config(yscrollcommand=self.on_file2_yscroll)
        self.diff_scrollbar.config(command=self.on_scrollbar)
        self.bind_mousewheel(self.file1_text, self.sync_scroll_from1)
        self.bind_mousewheel(self.file2_text, self.sync_scroll_from2)

        # Prevent recursion during programmatic scroll
        self.suppress_scroll_callback = False

    def bind_mousewheel(self, widget, command):
        widget.bind('<MouseWheel>', command)
        widget.bind('<Button-4>', command)
        widget.bind('<Button-5>', command)

    def on_file1_yscroll(self, *args):
        self.diff_scrollbar.set(*args)
        if not self.suppress_scroll_callback:
            self.suppress_scroll_callback = True
            self.align_file2_to_file1()
            self.suppress_scroll_callback = False

    def on_file2_yscroll(self, *args):
        self.diff_scrollbar.set(*args)
        if not self.suppress_scroll_callback:
            self.suppress_scroll_callback = True
            self.align_file1_to_file2()
            self.suppress_scroll_callback = False

    def on_scrollbar(self, *args):
        # Pass scrollbar movement to file1_text, then let file1_text's handler sync file2
        self.file1_text.yview(*args)

    def sync_scroll_from1(self, event):
        return self.handle_mousewheel(event, source=1)

    def sync_scroll_from2(self, event):
        return self.handle_mousewheel(event, source=2)

    def handle_mousewheel(self, event, source):
        # Only handle vertical scrolling
        if event.delta:
            lines = -1 * int(event.delta / 120)
        elif event.num == 4:
            lines = -1
        elif event.num == 5:
            lines = 1
        else:
            lines = 0
        widget = self.file1_text if source == 1 else self.file2_text
        widget.yview_scroll(lines, "units")
        # After scroll (calls yscroll callback), suppress default behavior
        return "break"

    def align_file2_to_file1(self):
        # Find topmost visible line in file1_text, map it to file2_text
        index1 = int(self.file1_text.index("@0,0").split('.')[0]) - 1  # zero-based
        if 0 <= index1 < len(self.file1_to_file2):
            target_index2 = self.file1_to_file2[index1]
            if target_index2 is not None:
                self.file2_text.yview_moveto(target_index2 / max(1, len(self.file2_to_file1)))
        # fallback: else, do nothing

    def align_file1_to_file2(self):
        index2 = int(self.file2_text.index("@0,0").split('.')[0]) - 1  # zero-based
        if 0 <= index2 < len(self.file2_to_file1):
            target_index1 = self.file2_to_file1[index2]
            if target_index1 is not None:
                self.file1_text.yview_moveto(target_index1 / max(1, len(self.file1_to_file2)))

    def populate_tree_view(self):
        source_dir = 'source'
        for root, dirs, files in os.walk(source_dir):
            if root == source_dir:
                for directory in dirs:
                    dir_path = os.path.join(root, directory)
                    self.tree_view.insert('', 'end', dir_path, text=directory)
            else:
                parent_dir = os.path.basename(root)
                parent_id = os.path.join(os.path.dirname(root), parent_dir)
                for file in files:
                    if file.endswith('.cpp'):
                        file_path = os.path.join(root, file)
                        self.tree_view.insert(parent_id, 'end', file_path, text=file)

    def on_tree_select(self, event):
        selected_item = self.tree_view.selection()
        if selected_item:
            file_path = selected_item[0]
            directory = os.path.dirname(file_path)
            self.list_view.delete(0, tk.END)
            if os.path.isdir(directory):
                cfg_files = [f for f in os.listdir(directory) if f.endswith('.cfg')]
                for cfg_file in cfg_files:
                    self.list_view.insert(tk.END, cfg_file)

    def on_list_select(self, event):
        selected_index = self.list_view.curselection()
        if selected_index:
            cfg_file = self.list_view.get(selected_index)
            cpp_file_path = self.tree_view.selection()[0]
            directory = os.path.dirname(cpp_file_path)
            cpp_file = os.path.basename(cpp_file_path)
            directory = directory.removeprefix('source/')
            file1_path = f'source/{directory}/{cpp_file}'
            file2_path = f'formatted/{directory}/{cpp_file[:-4]}+{cfg_file[:-4]}.cpp'
            self.show_diff(file1_path, file2_path)

    def show_diff(self, file1_path: str, file2_path: str):
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()
        diff = list(ndiff(file1_lines, file2_lines))
        self.file1_text.delete('1.0', tk.END)
        self.file2_text.delete('1.0', tk.END)
        file1_line_num = 1
        file2_line_num = 1
        # Mapping from file1 text line-number (0-based) -> file2 text line-number (or None)
        file1_to_file2 = []
        # Mapping from file2 text line-number (0-based) -> file1 text line-number (or None)
        file2_to_file1 = []
        for line in diff:
            if line.startswith('  '):
                self.file1_text.insert(f'{file1_line_num}.0', line[2:])
                self.file2_text.insert(f'{file2_line_num}.0', line[2:])
                file1_to_file2.append(file2_line_num-1)
                file2_to_file1.append(file1_line_num-1)
                file1_line_num += 1
                file2_line_num += 1
            elif line.startswith('- '):
                self.file1_text.insert(f'{file1_line_num}.0', line[2:], 'deleted')
                file1_to_file2.append(None)
                file1_line_num += 1
            elif line.startswith('+ '):
                self.file2_text.insert(f'{file2_line_num}.0', line[2:], 'added')
                file2_to_file1.append(None)
                file2_line_num += 1
        self.file1_text.tag_config('deleted', background='lightcoral')
        self.file2_text.tag_config('added', background='lightgreen')
        self.file1_to_file2 = file1_to_file2
        self.file2_to_file1 = file2_to_file1

def main():
    root = tk.Tk()
    app = DiffViewerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
