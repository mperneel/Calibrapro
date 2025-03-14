# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 13:56:46 2023

@author: Maarten
"""
#%% packages
import json
import os
import numpy as np
import pandas as pd

#%%

class Annotations():
    """
    The Annotations class stores all annotation data and has several methods
    to modify the annotation data
    """

    def __init__(self, master):
        self.master = master
        self.points = pd.DataFrame(data=[],
                                   columns=["2Dx", "2Dy", "3Dx", "3Dy", "3Dz"])
        self.names = []
        self.unit_2d = "px"
        self.unit_3d = "mm"
        self.point_id = None #index of currently active point

    def add_point(self,coordinates):
        """
        add a new point
        """
        #check inputs
        if len(coordinates) == 0:
            #no sensible input
            return

        if isinstance(coordinates, list) and\
            isinstance(coordinates[0], list):
            #coordinates is a list of lists, in which each sublist contains
            #the coordinates of a single point
            pass
        elif isinstance(coordinates, list):
            #coordinates is just a simple list with coordinates of a single
            #point
            coordinates = [coordinates]
        else:
            raise ValueError("This method is not yet able to handle the given input" )

        #add point(s) to self.points
        coordinates = np.array(coordinates)
        new_row = pd.DataFrame(data=coordinates,
                               columns=self.points.columns)
        self.points = pd.concat((self.points, new_row),
                                ignore_index=True)

        #add new name to self.names
        if len(self.names) == 0:
            self.names.append("0")
        else: #len(self.names) > 0
            self.names.append(str(int(self.names[-1]) + 1))

        #set point_id to id of new point
        self.point_id = len(self.points) - 1

    def delete_point(self, index=None):
        """
        Delete a point
        """
        if len(self.points) == 0:
            return
        #we use pop(), which is an in-place operator for lists
        self.points.drop(index, inplace=True)
        self.points.reset_index(drop=True, inplace=True) #reset index
        self.names.pop(index)

        #update self.point_id
        if len(self.points) == 0:
            self.point_id = None
        else: #len(self.points) > 0
            self.point_id = min(self.point_id, len(self.points) - 1)
            #if the last point was deleted, this will activate the new last point
            #in all other scenarios, the statement above does not change self.point_id

    def remove_nan_objects(self):
        """
        Remove points without coordinates
        """
        #remove rows which only contain NaN values
        self.points.dropna(axis=0, how="all", inplace=True)

    def save(self, filename):
        """
        save annotations to .json file
        """

        #check inputs
        if ("." not in filename) or\
            (filename.split(".")[-1] != "json"):
            raise ValueError("Specified filename is invalid")

        #remove empty lines
        self.remove_nan_objects()

        #convert annotations to dictionary
        #the object 'names' are not saved
        annotations_dict = {}
        annotations_dict["unit_2d"] = self.unit_2d
        annotations_dict["unit_3d"] = self.unit_3d
        annotations_dict["data"] = self.points.to_dict()

        with  open(filename, 'w') as f:
            #using a with structure closes the file automatically when the
            #body of the with structure is completed
            json.dump(annotations_dict, f, indent=4)

    def import_annotations(self, filename):
        """
        import annotations
        """

        #check inputs
        if not os.path.exists(filename):
            raise ValueError(f"{filename} not found")

        #load annotations
        with open(filename) as f:
            annotations_dict = json.load(f)

        self.unit_2d = annotations_dict["unit_2d"]
        self.unit_3d = annotations_dict["unit_3d"]
        self.points = pd.DataFrame(annotations_dict["data"])
        #the dataframe indices are imported as strings, but should be integers
        self.points.index = [int(i) for i in self.points.index]
        self.names = [str(i) for i in range(len(self.points))]

        #remove lines without points
        self.remove_nan_objects()

    def reset(self):
        """
        Reset the annotations
        """
        self.points = pd.DataFrame(data=[],
                                   columns=["2Dx", "2Dy", "3Dx", "3Dy", "3Dz"])
        self.unit_2d = "px"
        self.unit_3d = "mm"
        self.names = []
        self.point_id = None

    def update_units(self):
        """
        Update units and multiply annotations with correct conversion factor
        """
        #create dictionarry with factors necessary for unit conversion of
        #the annotations
        conversion_dict = {"m": 1,
                           "dm": 10,
                           "cm": 100,
                           "mm": 1000}

        #get current (old) unit of 3D annotations
        unit_3d_old = self.unit_3d

        #update unit for of 3D annotations
        self.unit_3d = self.master.settings.unit_3d

        #get current (new) unit of 3D annotations
        unit_3d_new = self.unit_3d

        #convert annotations to new unit
        for column in ["3Dx", "3Dy", "3Dz"]:
            self.points[column] = self.points[column] *\
                conversion_dict[unit_3d_new] / conversion_dict[unit_3d_old]
