"""
file implementing the gui of the application
"""
import tkinter as tk
from typing import Union
import app_data as ad

class DragDropListbox(tk.Listbox):
    """A Listbox with drag-and-drop reordering of items"""
    """
    This class creates a listbox which contains items that can be moved through drag and drop. It is a child class
    that inherits the Listbox widget built into the tkinter module. The list box module creates a box with ordered
    items. This child class lets the user move it around.

    Instance Attributes:
        - curIndex

    """

    curIndex: Union[None, float]

    def __init__(self, root: tk.Tk, background: str):
        """
        Initializes a dragdroplistbox object that lets the user drag around the items in the listbox
        """
        super().__init__(root, bg=background)
        self.bind('<Button-1>', self.set_current)
        self.bind('<B1-Motion>', self.shift_selection)
        self.curIndex = None

    def set_current(self, event):
        """
        When the left mouse is clicked, this function gets called. It takes in the mouse y coordinate and assigns it to
        currIndex.
        """
        self.curIndex = self.nearest(event.y)

    def shift_selection(self, event):
        """
        gets the nearest position where the mouse is moved and then moves it down or above based on whether it is lesser
        or greater than the currIndex
        """

        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i + 1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.curIndex = i


class PrioritizeApp:
    """
    doing something right now i dont really know right now
    """

    attributes_with_weights: dict[str, int]

    def __init__(self, root):
        self.root = root

        # Initial list of items
        self.items = [f"Item {i}" for i in range(1, 11)]
        self.items = [
            "year released",
            "popularity",
            "danceability",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "valence",
            "tempo",
            "genre"
        ]

        # Create a DragDropListbox and fill it with items
        self.listbox = DragDropListbox(root, "gray")
        for item in self.items:
            self.listbox.insert(tk.END, item)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.attributes_with_weights = {}

        # Button to save prioritization
        self.save_button = tk.Button(root, text="Save Prioritization", command=self.save_prioritization)
        self.save_button.pack(pady=50)

    def save_prioritization(self):
        """
        Saves the prioritized items and prints them out for now, this will chance later.
        """
        weight = 9
        prioritized_attributes = self.listbox.get(0, tk.END)
        for attribute in prioritized_attributes:
            self.attributes_with_weights[attribute] = weight
            weight -= 1
        print("Prioritized Items with weights: " + str(self.attributes_with_weights))


def main():
    """
    The main function file, this is where the root and main window is called.
    """
    # Create the tkinter window and PrioritizeApp instance
    g = ad.create_graph_without_edges("songs_test_small.csv")
    root = tk.Tk()
    priority_app = PrioritizeApp(root)
    root.title("MelodyMatcher")
    root.geometry("400x500")

    if priority_app.attributes_with_weights != {}:
        print("working")
        user_selected_song = g.return_chosen_song("Lifestyles of the Rich & Famous")
        g.add_all_weighted_edges(chosen_song=user_selected_song,
                                 prioritylist=priority_app.attributes_with_weights,
                                 explicit=False)
        g.print_weights(chosen_song=user_selected_song)

    root.mainloop()


if __name__ == "__main__":
    main()