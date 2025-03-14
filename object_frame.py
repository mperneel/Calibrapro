# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 13:09:09 2021

@author: Maarten
"""
#%% import packages
import tkinter as tk

#%%

class ObjectFrame(tk.Frame):
    """
    The ObjectFrame shows all defined objects (points) and allows to select and/or
    delete one of the previously defined points
    """

    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)

        #assign master
        self.master = master

        #update idletasks
        self.master.master.update_idletasks()

        #create listbox and scrollbar
        self.list_points = tk.Listbox(master=self)
        self.scrollbar = tk.Scrollbar(self,
                                      orient="vertical",
                                      width=20)

        #configure scrollbar
        self.scrollbar.config(command=self.list_points.yview)
        self.list_points.config(yscrollcommand=self.scrollbar.set)

        #bind events to self.list_points
        self.list_points.bind("<<ListboxSelect>>",
                               lambda event: self.activate_point_from_listbox())

        #create button_frm
        self.buttons_frm = tk.Frame(master=self)
        self.btn_draw_new_point = tk.Button(master=self.buttons_frm,
                                           text="draw new",
                                           command=self.draw_new_point)
        self.btn_delete_point = tk.Button(master=self.buttons_frm,
                                         text='delete',
                                         command=self.delete_button_pressed)

        self.btn_previous_point = tk.Button(master=self.buttons_frm,
                                         text='previous (F11)',
                                         command=lambda :self.activate_next_point(direction=-1))
        self.btn_next_point = tk.Button(master=self.buttons_frm,
                                         text='next (F12)',
                                         command=lambda :self.activate_next_point(direction=1))

        #position all elements

        #format self.buttons_frm
        self.btn_draw_new_point.grid(row=0,
                                    column=0,
                                    sticky='news')
        self.btn_delete_point.grid(row=0,
                                  column=1,
                                  sticky='news')
        self.btn_previous_point.grid(row=0,
                                  column=2,
                                  sticky='news')
        self.btn_next_point.grid(row=0,
                                  column=3,
                                  sticky='news')
        self.buttons_frm.columnconfigure(0, weight=1)
        self.buttons_frm.columnconfigure(1, weight=1)
        self.buttons_frm.columnconfigure(2, weight=1)
        self.buttons_frm.columnconfigure(3, weight=1)

        #format self
        self.buttons_frm.pack(side='bottom',
                              fill="x")
        self.list_points.pack(side="left",
                             fill=tk.BOTH,
                             expand=True)
        self.scrollbar.pack(side="left",
                            fill="y")


        #set attributes containing information about the application state
        self.active_point_index = None
        #index (within listbox) of currently active line

        #attribute with annotations object
        self.annotations = self.master.annotations

    def reset(self):
        """
        delete all current points
        """
        self.list_points.delete(0, tk.END)

    def load_points(self):
        """
        Load the points in self.list_points
        """
        #delete all current points
        self.list_points.delete(0, tk.END)

        #load new/updated points
        for name in zip(self.annotations.names):
            self.list_points.insert(tk.END, name)

    def delete_point(self):
        """
        Delete a point
        """
        #this method may only be invoked if object_frame is active
        if not self.master.object_frame_active:
            return

        if len(self.list_points.curselection()) == 0:
            #if no points are selected (or declared), no line may be deleted
            return

        self.annotations.delete_point(index=self.active_point_index)
        self.load_points()
        self.activate_point(list_index=self.annotations.point_id)
        self.master.annotation_canvas.update_image(mode=0)

    def delete_button_pressed(self):
        """
        Actions which should be performed when the delet button is invoked
        """
        #set status of object_frame to active
        self.master.activate_object_frame()

        #if the button was invoked after a point was activated by selection of
        #some keypoint in the annotation canvas, firstly the method activate_line
        #should be executed.
        #if this is not the case, no changes will happen as a result of invoking
        #activate_line()
        self.activate_point()

        #delete line
        self.delete_point()

        #de-activate object_frame is active from the perspective of annotation_canvas
        self.master.annotation_canvas.object_frame_active = False

    def activate_point(self, list_index=None):
        """
        Executive method to change active point
        """

        if list_index is None:
            current_selection = self.list_points.curselection()
            if len(current_selection) > 0:
                self.active_point_index = current_selection[0]
            else:
                self.active_point_index = self.annotations.point_id
        else:
            self.active_point_index = list_index


        self.master.annotations.point_id=self.active_point_index
        self.master.data_field.update_data()
        self.master.annotation_canvas.update_image(mode=0)
        self.list_points.select_clear(0, tk.END)

        if self.active_point_index is not None:
            self.list_points.activate(self.active_point_index)
            self.list_points.selection_set(self.active_point_index)

    def draw_new_point(self):
        """
        Start the drawing of a new point
        """
        self.active_point_index = None
        self.list_points.select_clear(0, tk.END)

    def activate_next_point(self, direction=1):
        """
        Activate the next point

        Parameters
        ----------
        direction : Int, optional
            1 :  show next point (default)\n
            -1 : show previous point
        """

        #set status of object_frame to active
        self.master.activate_object_frame()

        if self.active_point_index is None:
            if len(self.annotations.points) == 0:
                #there are no annotations
                return

            #len(self.annotations.points) > 0

            #show first point in annotations
            self.activate_point(list_index=0)
        else:
            list_index = (self.active_point_index + direction * 1) \
                % len(self.list_points.get(0,tk.END))
            self.activate_point(list_index=list_index)

    def activate_point_from_listbox(self):
        """
        Decisive method to activate an object after it was selected in the listbox
        """

        #set status of object_frame to active
        self.master.activate_object_frame()

        self.activate_point()
