# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:06:29 2023

@author: Maarten
"""

#%% packages
import tkinter as tk
import numpy as np

#%%

class DataField(tk.Frame):
    """
    Frame to show the coordinates of a point
    """

    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)

        #assign master
        self.master = master

        #update idletasks
        self.master.master.update_idletasks()

        #attribute with annotations object
        self.annotations = self.master.annotations

        #boolean attribute to enable/disabel synchronisation
        self.enable_synchronisation = True

        #create variables
        self.var_d2_x = tk.StringVar(value="")
        self.var_d2_y = tk.StringVar(value="")
        self.var_d3_x = tk.StringVar(value="")
        self.var_d3_y = tk.StringVar(value="")
        self.var_d3_z = tk.StringVar(value="")

        #add attributes to store old value
        self.var_d2_x.old_value = self.var_d2_x.get()
        self.var_d2_y.old_value = self.var_d2_x.get()
        self.var_d3_x.old_value = self.var_d2_x.get()
        self.var_d3_y.old_value = self.var_d2_x.get()
        self.var_d3_z.old_value = self.var_d2_x.get()

        #add attributes to store corresponding column name in self.annotations
        self.var_d2_x.annotations_column = "2Dx"
        self.var_d2_y.annotations_column = "2Dy"
        self.var_d3_x.annotations_column = "3Dx"
        self.var_d3_y.annotations_column = "3Dy"
        self.var_d3_z.annotations_column = "3Dz"

        #use .trace() to add a method to the tkinter variables that synchronises
        #the application and annotations when the user modified data
        self.var_d2_x.trace('w',
            lambda *args : self.synchronise(self.var_d2_x))
        self.var_d2_y.trace('w',
            lambda *args : self.synchronise(self.var_d2_y))
        self.var_d3_x.trace('w',
            lambda *args : self.synchronise(self.var_d3_x))
        self.var_d3_y.trace('w',
            lambda *args : self.synchronise(self.var_d3_y))
        self.var_d3_z.trace('w',
            lambda *args : self.synchronise(self.var_d3_z))

        #create frames for entry fields and their labels
        self.frm_d2_x = tk.Frame(master=self)
        self.frm_d2_y = tk.Frame(master=self)
        self.frm_d3_x = tk.Frame(master=self)
        self.frm_d3_y = tk.Frame(master=self)
        self.frm_d3_z = tk.Frame(master=self)

        #create labels
        title_width = 20
        self.label_d2 = tk.Label(master=self,
                                 text="2D",
                                 anchor="w",
                                 width=title_width)
        self.label_white_line = tk.Label(master=self,
                                         text="",
                                         anchor="w",
                                         width=title_width)
        self.label_d3 = tk.Label(master=self,
                                 text="3D",
                                 anchor="w",
                                 width=title_width)

        label_width = 2
        self.label_d2_x = tk.Label(master=self.frm_d2_x,
                                   text="x",
                                   anchor="w",
                                   width=label_width)
        self.label_d2_y = tk.Label(master=self.frm_d2_y,
                                   text="y",
                                   anchor="w",
                                   width=label_width)
        self.label_d3_x = tk.Label(master=self.frm_d3_x,
                                   text="x",
                                   anchor="w",
                                   width=label_width)
        self.label_d3_y = tk.Label(master=self.frm_d3_y,
                                   text="y",
                                   anchor="w",
                                   width=label_width)
        self.label_d3_z = tk.Label(master=self.frm_d3_z,
                                   text="z",
                                   anchor="w",
                                   width=label_width)

        unit_width = 5
        self.label_d2_x_unit = tk.Label(master=self.frm_d2_x,
                                        text="px",
                                        anchor="w",
                                        width=unit_width)
        self.label_d2_y_unit = tk.Label(master=self.frm_d2_y,
                                        text="px",
                                        anchor="w",
                                        width=unit_width)
        self.label_d3_x_unit = tk.Label(master=self.frm_d3_x,
                                        text=self.master.settings.unit_3d,
                                        anchor="w",
                                        width=unit_width)
        self.label_d3_y_unit = tk.Label(master=self.frm_d3_y,
                                        text=self.master.settings.unit_3d,
                                        anchor="w",
                                        width=unit_width)
        self.label_d3_z_unit = tk.Label(master=self.frm_d3_z,
                                        text=self.master.settings.unit_3d,
                                        anchor="w",
                                        width=unit_width)

        #creat entry fields
        entry_width = 7
        self.field_d2_x = tk.Entry(self.frm_d2_x,
                                    width=entry_width,
                                    textvariable=self.var_d2_x)
        self.field_d2_y = tk.Entry(self.frm_d2_y,
                                    width=entry_width,
                                    textvariable=self.var_d2_y)
        self.field_d3_x = tk.Entry(self.frm_d3_x,
                                    width=entry_width,
                                    textvariable=self.var_d3_x)
        self.field_d3_y = tk.Entry(self.frm_d3_y,
                                    width=entry_width,
                                    textvariable=self.var_d3_y)
        self.field_d3_z = tk.Entry(self.frm_d3_z,
                                    width=entry_width,
                                    textvariable=self.var_d3_z)

        #outline all elements

        self.label_d2.pack(anchor="w", pady=5)

        self.frm_d2_x.pack(anchor="w", pady=5)
        self.label_d2_x.pack(side="left")
        self.field_d2_x.pack(side="left")
        self.label_d2_x_unit.pack(side="left")

        self.frm_d2_y.pack(anchor="w", pady=5)
        self.label_d2_y.pack(side="left")
        self.field_d2_y.pack(side="left")
        self.label_d2_y_unit.pack(side="left")

        self.label_white_line.pack(anchor="w", pady=5)

        self.label_d3.pack(anchor="w", pady=5)

        self.frm_d3_x.pack(anchor="w", pady=5)
        self.label_d3_x.pack(side="left")
        self.field_d3_x.pack(side="left")
        self.label_d3_x_unit.pack(side="left")

        self.frm_d3_y.pack(anchor="w", pady=5)
        self.label_d3_y.pack(side="left")
        self.field_d3_y.pack(side="left")
        self.label_d3_y_unit.pack(side="left")

        self.frm_d3_z.pack(anchor="w", pady=5)
        self.label_d3_z.pack(side="left")
        self.field_d3_z.pack(side="left")
        self.label_d3_z_unit.pack(side="left")

    def check_numeric_value(self, textvar):
        """
        Check if the changes to a numeric attribute still result in a valid entry
        (positive number)

        If the changes would result in an invalid entry, the changes are undone
        by replacing the invalid entry with the value stored in the attribute
        .old_value
        """

        #If the field is empty (equal to a zero entry); accept this
        if textvar.get() == "":
            #update textvar.old_value
            textvar.old_value = textvar.get()
            return

        #valid textvar: only digits, maximum one comma and possibly a
        #negative sign at the beginning of the string

        #preprocess textvar value so we can check the conditions specified above
        value = textvar.get()
        #replace a single comma by ""
        value = value.replace(".", "", 1)
        #remove a negative sign at the beginning
        if value[0] == "-":
            if len(value) >= 2:
                value = value[1:]
            else: #len(value) == 1:
                #value is just '-', accept this
                #update textvar.old_value
                textvar.old_value = textvar.get()
                return

        if value.isdigit():
            textvar.old_value = textvar.get()
        else:
            #textvar is unvalid
            #resons for unvalidity: presence of charaters, more than one
            #decimal separator, negative sign on another position then the first
            textvar.set(textvar.old_value)

    def synchronise(self, textvar):
        """
        Synchronise annotation and application after the user modifies coordinates
        """

        if not self.enable_synchronisation:
            return

        #set status of data_field to active
        self.master.activate_data_field()

        if self.annotations.point_id is None:
            #the condition above will be True when the single and only point
            #was deleted. In that case, there is nothing to synchronise
            return

        #check if entry of user is valid
        self.check_numeric_value(textvar)

        #textvar now has certainly a valid value

        #update annotations
        value = textvar.get()
        if value in ["", "-"]:
            value = np.nan
        else:
            value = float(value)

        self.annotations.points.loc[self.annotations.point_id, textvar.annotations_column]=\
            value

    def update_data(self, point_id=None):
        """
        Show coordinates of a point

        Parameters
        ----------
        point_id : int
            index of the point of which coordinates should be shown
        """

        #if no point_id was given, the data of the currently active point has to
        #be shown
        if point_id is None:
            if self.annotations.point_id is not None:
                point_id = self.annotations.point_id

        textvars = [self.var_d2_x, self.var_d2_y,
                    self.var_d3_x, self.var_d3_y, self.var_d3_z]
        column_names = ["2Dx", "2Dy", "3Dx", "3Dy", "3Dz"]

        #disable synchronisation
        self.enable_synchronisation = False

        if point_id is not None:

            #get coordinates of point
            point = self.annotations.points.iloc[point_id,:]
            #point is a pandas.series

            for textvar, column_name in zip(textvars, column_names):
                if np.isnan(point[column_name]):
                    textvar.set("")
                else: #not np.isnan(point[column_name]):
                    textvar.set(np.round(point[column_name], 2))

        else: #point_id is None
            #if no point_id as given and there is no active point, no data has to be shown

            for textvar in textvars:
                textvar.set("")

        #enable synchronisation
        self.enable_synchronisation = True

    def next_point(self, direction=1):
        """
        Show data of next point

        Parameters
        ----------
        direction : Int, optional
            1 :  show next point (default)\n
            -1 : show previous point
        """

        self.annotations.point_id = (self.annotations.point_id + 1 * direction)\
            % len(self.annotations.points)

        self.update_data()

    def update_units(self):
        """
        Update the used units for the 3D point coordinates
        """
        self.label_d3_x_unit.config(text=self.master.settings.unit_3d)
        self.label_d3_y_unit.config(text=self.master.settings.unit_3d)
        self.label_d3_z_unit.config(text=self.master.settings.unit_3d)
