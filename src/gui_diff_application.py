import tkinter as tk
from tkinter import ttk
from difflib import ndiff

class DiffViewerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Diff Viewer Application")

        # Create a PanedWindow
        self.paned_window = ttk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

        # Create left frame for tree view
        self.left_frame = ttk.Frame(self.paned_window, width=200, height=400, relief=tk.SUNKEN)
        self.paned_window.add(self.left_frame, weight=1)

        # Create tree view in the left frame
        self.tree_view = ttk.Treeview(self.left_frame)
        self.tree_view.pack(fill=tk.BOTH, expand=1)

        # Create right frame for diff view
        self.right_frame = ttk.Frame(self.paned_window, width=800, height=400, relief=tk.SUNKEN)
        self.paned_window.add(self.right_frame, weight=4)

        # Create text widgets for side-by-side file view
        self.file1_text = tk.Text(self.right_frame, wrap=tk.NONE, width=40)
        self.file1_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.file2_text = tk.Text(self.right_frame, wrap=tk.NONE, width=40)
        self.file2_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

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
    app.show_diff('source/nl_enum_brace/nl_enum_brace.cpp', 'formatted/nl_enum_brace/nl_enum_brace+nl_enum_brace_force.cpp')
    root.mainloop()


if __name__ == "__main__":
    main()
