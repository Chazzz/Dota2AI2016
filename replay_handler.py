import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import matplotlib.text as text
import time
import random
import pickle

rad_labels = 'abcdefghijklmnopqrstuvwxyz' #for replay annotations
dir_labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' #for replay annotations

class ReplayHandler:
    # Constructor
    def __init__(self,
                 rad_creeps_history, 
                 dir_creeps_history, 
                 start_index,
                 end_index,
                 ):
        self.rad_creeps_history = rad_creeps_history
        self.rad_creeps_history.sort(key=lambda c: c.birth_count)
        self.dir_creeps_history = dir_creeps_history
        self.dir_creeps_history.sort(key=lambda c: c.birth_count)
        self.index = start_index
        self.end_index = end_index
        self.fig, self.ax = plt.subplots()
        self.sc_r = self.ax.scatter([],[],c=(0.0,1.0,0.0),s=200,edgecolors='face')
        self.sc_d = self.ax.scatter([],[],c=(0.65,0.4,0.3),s=200,edgecolors='face')
        self.annotations = []
        # set limits to screen width/height
        self.ax.set_xlim(0,1920)
        self.ax.set_ylim(1080,0)

    # Print the creeps
    def update(self,_):
        xs_r, ys_r = ([],[])
        xs_d, ys_d = ([],[])
        self.clear_annotations()
        if self.index > self.end_index:
            self.index = self.end_index # keep animating last step
        for creep_id, creep in enumerate(self.rad_creeps_history):
            was_born = (self.index >= creep.birth_count)
            has_died = (self.index > len(creep.health_history)+creep.birth_count)
            if was_born and not has_died:
                i = self.index-creep.birth_count
                if i == len(creep.x_history):
                    x_coord = creep.x
                    y_coord = creep.y
                    health = creep.health
                else:
                    x_coord = creep.x_history[i]
                    y_coord = creep.y_history[i]
                    health = creep.health_history[i]
                xs_r.append(x_coord)
                ys_r.append(y_coord)
                creep_label = rad_labels[creep_id%len(rad_labels)]
                annotation = text.Annotation(
                    "%.2f %s" % (health, creep_label),
                    xy=(x_coord, y_coord),
                    xytext=(-35,-5),
                    textcoords = 'offset points')
                self.add_annotation(annotation)
        for creep_id, creep in enumerate(self.dir_creeps_history):
            was_born = (self.index >= creep.birth_count)
            has_died = (self.index > len(creep.health_history)+creep.birth_count)
            if was_born and not has_died:
                i = self.index-creep.birth_count
                if i == len(creep.x_history):
                    x_coord = creep.x
                    y_coord = creep.y
                    health = creep.health
                else:
                    x_coord = creep.x_history[i]
                    y_coord = creep.y_history[i]
                    health = creep.health_history[i]
                xs_d.append(x_coord)
                ys_d.append(y_coord)
                creep_label = dir_labels[creep_id%len(dir_labels)]
                annotation = text.Annotation(
                    "%s %.2f" % (creep_label, health),
                    xy=(x_coord, y_coord),
                    xytext=(10, -5),
                    textcoords = 'offset points')
                self.add_annotation(annotation)
        self.ax.set_title("Frame %i" % self.index)
        self.sc_r.set_offsets(np.column_stack((xs_r, ys_r)))
        self.sc_d.set_offsets(np.column_stack((xs_d, ys_d)))
        self.index += 1
        return self.sc_r, #self.sc_d

    def add_annotation(self, annotation):
        self.annotations.append(annotation)
        self.ax.add_artist(annotation)

    def clear_annotations(self):
        for annotation in self.annotations:
            annotation.remove()
        self.annotations = []

def replay_main(rad_creeps_history,dir_creeps_history, start_index=0, end_index=-1):
    R = ReplayHandler(rad_creeps_history, dir_creeps_history, start_index, end_index)
    ani = animation.FuncAnimation(R.fig, R.update, interval=50,blit=False)
    plt.show()

if __name__ == '__main__':
    state = pickle.load( open( "save.p", "rb" ) )
    replay_main(state['rad_creeps_history'], state['dire_creeps_history'], 0, state['counter'])
    
