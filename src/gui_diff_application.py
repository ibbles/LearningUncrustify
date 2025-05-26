#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import ttk
from tkinter import Listbox
from difflib import SequenceMatcher
import tkinter.font as tkFont

class DiffViewerApp:
    """Main class for the GUI application.

    Creates the GUI elements, listens for selection events and populates the
    diff view when both a .cfg and .cpp file has been selected.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Diff Viewer Application")

        # Set a larger font for the Treeview to increase row height
        tree_font = tkFont.Font(family="TkDefaultFont", size=14)
        style = ttk.Style(self.master)
        style.configure("Treeview", font=tree_font, rowheight=28, padding=4)

        # Root windows that contains the .cpp files tree view, the .cfg files
        # list view, and the diff view.
        self.paned_window = ttk.PanedWindow(self.master, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

        # Create the .cpp files tree view.
        self.treview_frame = ttk.Frame(self.paned_window, width=200, height=200, relief=tk.SUNKEN)
        self.paned_window.add(self.treview_frame, weight=1)
        self.tree_view = ttk.Treeview(self.treview_frame)
        self.tree_view.pack(fill=tk.BOTH, expand=1)
        self.tree_view.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.populate_tree_view()

        # Create the .cfg list view.
        self.list_frame = ttk.Frame(self.paned_window, width=200, height=200, relief=tk.SUNKEN)
        self.paned_window.add(self.list_frame, weight=1)
        self.list_view = Listbox(self.list_frame)
        self.list_view.pack(fill=tk.BOTH, expand=1)
        self.list_view.bind('<<ListboxSelect>>', self.on_list_select)

        # Create the diff view, which consists of a left and a right text view.
        self.diff_frame = ttk.Frame(self.paned_window, width=800, height=400, relief=tk.SUNKEN)
        self.paned_window.add(self.diff_frame, weight=2)
        self.diff_scrollbar = tk.Scrollbar(self.diff_frame, orient=tk.VERTICAL)
        self.diff_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.left_text = tk.Text(self.diff_frame, wrap=tk.NONE, width=40)
        self.left_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.right_text = tk.Text(self.diff_frame, wrap=tk.NONE, width=40)
        self.right_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.left_text.config(yscrollcommand=self.diff_scrollbar.set)
        self.right_text.config(yscrollcommand=self.diff_scrollbar.set)
        self.diff_scrollbar.config(command=self.yview_all)
        self.bind_mousewheel(self.left_text, self.sync_scroll)
        self.bind_mousewheel(self.right_text, self.sync_scroll)

    def bind_mousewheel(self, widget, command):
        # Different OSs use different names for the scroll wheel.
        widget.bind('<MouseWheel>', command)
        widget.bind('<Button-4>', command)
        widget.bind('<Button-5>', command)

    def yview_all(self, *args):
        self.left_text.yview(*args)
        self.right_text.yview(*args)

    def sync_scroll(self, event):
        if event.delta:
            lines = -1 * int(event.delta / 120)
        elif event.num == 4:  # Button 4, i.e. the scroll wheel.
            lines = -1
        elif event.num == 5:  # Button 5,  i.e. the scroll wheel.
            lines = 1
        else:
            lines = 0
        self.left_text.yview_scroll(lines, "units")
        self.right_text.yview_scroll(lines, "units")
        return "break"

    def populate_tree_view(self):
        source_dir = 'source'
        for root, dirs, files in os.walk(source_dir):
            if root == source_dir:
                for directory in sorted(dirs):
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

    def split_chunks_at_equal_lines(self, opcodes, a, b):
        result = []
        for tag, i1, i2, j1, j2 in opcodes:
            if tag in ("replace", "delete", "insert"):
                ai, bi = i1, j1
                while ai < i2 or bi < j2:
                    # Check if both lines exist and are equal and non-empty
                    if ai < i2 and bi < j2 and a[ai] == b[bi] and a[ai].strip() != "":
                        # Emit previous chunk if any
                        if ai > i1 or bi > j1:
                            result.append((tag, i1, ai, j1, bi))
                        # Emit equal chunk for this line
                        result.append(("equal", ai, ai+1, bi, bi+1))
                        ai += 1
                        bi += 1
                        i1 = ai
                        j1 = bi
                    else:
                        if tag != "delete" and bi < j2:
                            bi += 1
                        if tag != "insert" and ai < i2:
                            ai += 1
                # Emit any trailing chunk that didn't end with an equal
                if (tag == "replace" and (i1 != i2 or j1 != j2)) or \
                   (tag == "delete" and i1 != i2) or \
                   (tag == "insert" and j1 != j2):
                    result.append((tag, i1, i2, j1, j2))
            else:
                result.append((tag, i1, i2, j1, j2))
        return result

    def rematch_change_equal_change(self, opcodes, a, b, min_chunk=3):
        # Matches runs like [change][equal][change], where change is delete/insert/replace
        # and equal is a small chunk
        change_tags = {'delete', 'replace', 'insert'}
        new_opcodes = []
        i = 0
        while i < len(opcodes):
            if (
                i+2 < len(opcodes)
                and opcodes[i][0] in change_tags
                and opcodes[i+1][0] == 'equal'
                and opcodes[i+2][0] in change_tags
            ):
                # Require at least one side to have enough lines for finer matching
                tag1, i1_1, i2_1, j1_1, j2_1 = opcodes[i]
                _, i1_e, i2_e, j1_e, j2_e = opcodes[i+1]
                tag2, i1_2, i2_2, j1_2, j2_2 = opcodes[i+2]

                left_lines = a[i1_1:i2_1] if tag1 in {'delete', 'replace'} else []
                right_lines = b[j1_2:j2_2] if tag2 in {'insert', 'replace'} else []
                # Only attempt if deletion/replace and insert/replace chunks large, and the equal region is small
                if ((len(left_lines) >= min_chunk or len(right_lines) >= min_chunk)
                    and (i2_e - i1_e) <= min_chunk and (j2_e - j1_e) <= min_chunk):
                    sm2 = SequenceMatcher(None, left_lines, right_lines)
                    sub_opcodes = sm2.get_opcodes()
                    # Map sub_opcodes back to original indices
                    for tag, li1, li2, rj1, rj2 in sub_opcodes:
                        new_opcodes.append(
                            (tag,
                             i1_1 + li1, i1_1 + li2,
                             j1_2 + rj1, j1_2 + rj2)
                        )
                    i += 3
                    continue
            new_opcodes.append(opcodes[i])
            i += 1
        return new_opcodes

    def show_diff(self, file1_path: str, file2_path: str):
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()

        # Compute grouped opcodes using SequenceMatcher
        sm = SequenceMatcher(None, file1_lines, file2_lines)
        opcodes = sm.get_opcodes()


        # Commenting out chunk post-processing, it doesn't work reliably.
        # Post-process to split chunks at equal non-empty lines within changes
        # opcodes = self.split_chunks_at_equal_lines(opcodes, file1_lines, file2_lines)
        # Generalized: further re-match [change][equal][change] runs
        # opcodes = self.rematch_change_equal_change(opcodes, file1_lines, file2_lines)

        self.left_text.delete('1.0', tk.END)
        self.right_text.delete('1.0', tk.END)
        line_num1 = 1
        line_num2 = 1

        # Create tags
        self.left_text.tag_config('deleted', background='lightcoral')
        self.right_text.tag_config('added', background='lightgreen')
        self.left_text.tag_config('pad', background='#d3d3d3')  # gray
        self.right_text.tag_config('pad', background='#d3d3d3')  # gray

        for tag, i1, i2, j1, j2 in opcodes:
            n1 = i2 - i1
            n2 = j2 - j1
            maxlen = max(n1, n2)
            # Helper: Return empty line with a newline if at least one of the chunks isn't empty
            def gray_line():
                return '\n'

            for idx in range(maxlen):
                l1 = file1_lines[i1+idx] if idx < n1 else None
                l2 = file2_lines[j1+idx] if idx < n2 else None
                if tag == 'equal':
                    self.left_text.insert(f'{line_num1}.0', l1)
                    self.right_text.insert(f'{line_num2}.0', l2)
                elif tag == 'replace':
                    if l1 is not None:
                        self.left_text.insert(f'{line_num1}.0', l1, ('deleted',))
                    else:
                        self.left_text.insert(f'{line_num1}.0', gray_line(), ('pad',))
                    if l2 is not None:
                        self.right_text.insert(f'{line_num2}.0', l2, ('added',))
                    else:
                        self.right_text.insert(f'{line_num2}.0', gray_line(), ('pad',))
                elif tag == 'delete':
                    if l1 is not None:
                        self.left_text.insert(f'{line_num1}.0', l1, ('deleted',))
                    self.right_text.insert(f'{line_num2}.0', gray_line(), ('pad',))
                elif tag == 'insert':
                    self.left_text.insert(f'{line_num1}.0', gray_line(), ('pad',))
                    if l2 is not None:
                        self.right_text.insert(f'{line_num2}.0', l2, ('added',))
                # Advance line numbers if line was actually added in either field
                if l1 is not None or tag == 'insert' or tag == 'replace':
                    line_num1 += 1
                if l2 is not None or tag == 'delete' or tag == 'replace':
                    line_num2 += 1


def main():
    root = tk.Tk()
    app = DiffViewerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
