from tkinter import *
from tkinter import ttk
import tkinter

class App(ttk.Frame):
    def __init__(self, root=None):
        ttk.Frame.__init__(self, root)

        self.style = ttk.Style(root)
        self.style.theme_use('vista')
        root.geometry("800x900")

        self.label1 = Label(root, text="HELLO")
        self.label1.grid(row=123, column=0)

        self.emptylabel2 = Label(root)
        self.emptylabel2.grid(row=124, column=0, columnspan=10)

        # gives weight to the cells in the grid
        rows = 50
        while rows < 200:
            root.rowconfigure(rows, weight=1)
            root.columnconfigure(rows, weight=1)
            rows += 1

        # Defines and places the notebook widget
        nb2 = ttk.Notebook(root)
        nb2.grid(row=125, column=0, columnspan=200, rowspan=100, sticky='NESW')

        # ============= Page - 40 =============
        page40 = ttk.Frame(nb2)
        nb2.add(page40, text='xxxx')

        self.msg = ttk.Label(page40, text="LOL LOL LOL LOL")
        self.msg.grid(row=1, column=0, rowspan=10, columnspan=10)

# Tree widget starts here

        tree_columns = ("file", "file", "file", "file")
        tree_data = [
            ("1", "1", "1", "1"),
            ("2", "2", "2", "2"),
            ("3", "3", "3", "3"),
            ("4", "4", "4", "4"),
        ]

        def sortby(self, tree, col, descending):
            """Sort tree contents when a column is clicked on."""
            # grab values to sort
            data = [(tree.set(child, col), child) for child in tree.get_children('')]

            # reorder data
            data.sort(reverse=descending)
            for indx, item in enumerate(data):
                tree.move(item[1], '', indx)

            # switch the heading so that it will sort in the opposite direction
            tree.heading(col,
                         command=lambda col=col: sortby(tree, col, int(not descending)))

            self.container = ttk.Frame(self, page40)
            self.container.grid(row=1, column=1, rowspan=90, columnspan=190)

            self.tree = ttk.Treeview(columns=tree_columns, show="headings")
            vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
            hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
            self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            self.tree.grid(column=0, row=0, sticky='nsew', in_=self.container)
            vsb.grid(column=1, row=0, sticky='ns', in_=self.container)
            hsb.grid(column=0, row=1, sticky='ew', in_=self.container)

            self.container.grid_columnconfigure(0, weight=1)
            self.container.grid_rowconfigure(0, weight=1)

        def _build_tree(page40, self):
            for col in tree_columns:
                self.tree.heading(page40, col, text=col.title(),
                                  command=lambda c=col: sortby(self.tree, c, 0))

                self.tree.column(col, width=tkinter.font.Font().measure(col.title()))

            for item in tree_data:
                self.tree.insert('', 'end', values=item)

                # adjust columns lenghts if necessary
                for indx, val in enumerate(item):
                    ilen = tkinter.font.Font().measure(val)
                    if self.tree.column(tree_columns[indx], width=None) < ilen:
                        self.tree.column(tree_columns[indx], width=ilen)

        page50 = ttk.Frame(nb2)
        nb2.add(page50, text='yyyy')    

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.title("test")
    root.mainloop()