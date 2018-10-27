#x, y, health
#x_history, y_history, health_history
#update_times

# set x actually adds to x_history
# get x actually gets first element of x_history

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import matplotlib.text as text
import time
import random
import pickle

rad_labels = 'abcdefghijklmnopqrstuvwxyz' #for replay annotations
dir_labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' #for replay annotations

class ReplayHandlerNotTracked:
    # Constructor
    def __init__(self, rad_creeps_history, dir_creeps_history):
        self.rad_creeps_history = rad_creeps_history
        self.dir_creeps_history = dir_creeps_history
        self.index = 0
        self.fig , self.ax = plt.subplots()
        self.sc_r = self.ax.scatter([],[],c=(0.0,1.0,0.0),s=200,edgecolors='face')
        self.sc_d = self.ax.scatter([],[],c=(0.65,0.4,0.3),s=200,edgecolors='face')
        self.annotations = []
        self.ax.set_xlim(0,1920)
        self.ax.set_ylim(1080,0)

    # Print the polygon
    def update(self,_):
        xs_r, ys_r = ([],[])
        xs_d, ys_d = ([],[])
        self.clear_annotations()
        if self.index >= len(self.rad_creeps_history):
            self.index = len(self.rad_creeps_history)-1
        for creep in self.rad_creeps_history[self.index]:
            xs_r.append(creep.x)
            ys_r.append(creep.y)
            # annotation = text.Annotation("%.2f %s" % (creep.health, creep.label),
            annotation = text.Annotation("%i %s" % (len(creep.history), creep.label),
                                         xy=(creep.x,creep.y),
                                         xytext=(-35,-5),
                                         textcoords = 'offset points')
            self.add_annotation(annotation)
        for creep in self.dir_creeps_history[self.index]:
            xs_d.append(creep.x)
            ys_d.append(creep.y)
            annotation = text.Annotation("%.2f" % creep.health,
                                         xy=(creep.x,creep.y),
                                         xytext=(10,0),
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
        self.rad_creeps_history.sort(key=lambda c: c.birth_count)
        self.index = start_index
        self.end_index = end_index
        self.fig, self.ax = plt.subplots()
        self.sc_r = self.ax.scatter([],[],c=(0.0,1.0,0.0),s=200,edgecolors='face')
        self.sc_d = self.ax.scatter([],[],c=(0.65,0.4,0.3),s=200,edgecolors='face')
        self.annotations = []
        self.ax.set_xlim(0,1920)
        self.ax.set_ylim(1080,0)

    # Print the polygon
    def update(self,_):
        xs_r, ys_r = ([],[])
        xs_d, ys_d = ([],[])
        self.clear_annotations()
        if self.index > self.end_index:
            self.index = self.end_index # keep animating last step
        for creep_id, creep in enumerate(self.rad_creeps_history):
            was_born = (self.index >= creep.birth_count)
            # +1 is hack to make xs_r calculation simpler
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
                # labels sorted by time of death
                creep_label = rad_labels[creep_id%len(rad_labels)]
                # annotation = text.Annotation("%.2f %s" % (creep.health, creep.label),
                annotation = text.Annotation(
                    "%.2f %s" % (health, creep_label),
                    xy=(x_coord, y_coord),
                    xytext=(-35,-5),
                    textcoords = 'offset points')
                self.add_annotation(annotation)
        for creep_id, creep in enumerate(self.dir_creeps_history):
            was_born = (self.index >= creep.birth_count)
            # +1 is hack to make xs_r calculation simpler
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
                # labels sorted by time of death
                creep_label = dir_labels[creep_id%len(dir_labels)]
                # annotation = text.Annotation("%.2f %s" % (creep.health, creep.label),
                annotation = text.Annotation(
                    "%s %.2f" % (creep_label, health),
                    xy=(x_coord, y_coord),
                    xytext=(10, -5),
                    textcoords = 'offset points')
                self.add_annotation(annotation)
        # for creep in self.dir_creeps_history:
        #     xs_d.append(creep.x)
        #     ys_d.append(creep.y)
        #     annotation = text.Annotation("%.2f" % creep.health,
        #                                  xy=(creep.x,creep.y),
        #                                  xytext=(10,0),
        #                                  textcoords = 'offset points')
        #     self.add_annotation(annotation)
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


# def update_tracked_creeps(tracked_creeps, iteration):
#     new_tracked_creeps = []
#     find_lowest_cost_map(tracked_creeps, iteration)
#     for creep in tracked_creeps:
#         update_creep(creep, new_creep)
#         if creep.health != 0: # Not dead
#             new_tracked_creeps.append(creep)

label_characters = 'abcdefghijklmnopqrstuvwxyz'
label_list = [c for c in label_characters]
label_list.reverse()

def generate_new_label():
    # print label_list
    return label_list.pop()


def get_costs(old_creeps, new_creeps):
    # if creeps appear or disappear, expect creeps to be more stationary
    reduction_multiplier = (1.0 * min(len(old_creeps),len(new_creeps)) /
                                  max(len(old_creeps),len(new_creeps)))
    avg_x_old = np.average([creep.x for creep in old_creeps])
    avg_x_new = np.average([creep.x for creep in new_creeps])
    avg_y_old = np.average([creep.y for creep in old_creeps])
    avg_y_new = np.average([creep.y for creep in new_creeps])
    avg_dx = avg_x_new - avg_x_old
    avg_dy = avg_y_new - avg_y_old
    corr_dx = avg_dx*reduction_multiplier
    corr_dy = avg_dy*reduction_multiplier
    costs = np.zeros((len(new_creeps),len(old_creeps)))
    for i, new_creep in enumerate(new_creeps):
        for j, old_creep in enumerate(old_creeps):
            dx = (new_creep.x - old_creep.x) - corr_dx #expected: -50-50
            dy = (new_creep.y - old_creep.y) - corr_dy #expected: -50-50
            dh = new_creep.health - old_creep.health  #expected: -0.3-0.05
            cost_x = abs(dx)
            cost_y = abs(dy)
            if dh > 0:
                cost_h = 1000*dh 
            else:
                cost_h = -100*dh
            assert(cost_x >= 0)
            assert(cost_y >= 0)
            assert(cost_h >= 0)
            costs[i,j] = cost_x + cost_y + cost_h
    return costs

def label_creeps_older(old_creeps, new_creeps):
    '''
        assign label to most plausible candidate, duplicates be damned
        modifies new_creeps in-place
    '''
    if len(old_creeps) == 0:
        for creep in new_creeps:
            creep.label = generate_new_label()
    else:
        costs = get_costs(old_creeps, new_creeps)
        old_labels = [creep.label for creep in old_creeps]
        # print costs
        # print costs.shape
        default_cost = 150
        i = 0
        # print "start loop"
        while i < len(new_creeps):
            # print i
            # print costs
            creep = new_creeps[i]
            min_cost = np.min(costs[i,:])
            # print min_cost
            min_index = np.argmin(costs[i,:])
            # print min_index
            if min_cost < default_cost:
                creep.label = old_creeps[min_index].label
            else:
                creep.label = generate_new_label() #tends to get overcalled if reset
            # handle tiebreakers
            labels = [ncreep.label for ncreep in new_creeps[0:i]]
            # print labels, creep.label
            if creep.label in labels and creep.label != -1:
                # try again from 0, but with bias against least-likely label
                cost_c1 = costs[labels.index(creep.label),old_labels.index(creep.label)]
                cost_c2 = costs[i,old_labels.index(creep.label)]
                if cost_c1 <= cost_c2:
                    costs[i,old_labels.index(creep.label)] += 50
                else:
                    costs[labels.index(creep.label),old_labels.index(creep.label)] += 50
                i = 0
            else:
                i += 1


def index_creeps(old_creeps, new_creeps):
    '''
        assign new_creeps an index to most plausible old_creep candidate
        or -1, which equals "new creep"
        returns array of same length as new_creeps of range -1,len(oldcreeps)
    '''
    if len(old_creeps) == 0:
        return np.ones((len(new_creeps)))*-1
    else:
        costs = get_costs(old_creeps, new_creeps)
        # old_labels = [creep.label for creep in old_creeps]
        # print costs
        # print costs.shape
        default_cost = 1000
        i = 0
        # print "start loop"
        indexes = [0]*len(new_creeps)
        while i < len(new_creeps):
            # print i
            # print costs
            creep = new_creeps[i]
            min_cost = np.min(costs[i,:])
            # print min_cost
            min_index = np.argmin(costs[i,:])
            # print min_index
            if min_cost < default_cost:
                indexes[i] = min_index
            else:
                indexes[i] = -1
            # handle tiebreakers
            if indexes[i] in indexes[0:i] and indexes[i] != -1:
                # try again from 0, but with bias against least-likely index
                cost_c1 = costs[indexes.index(min_index),min_index]
                cost_c2 = costs[i,min_index]
                if cost_c1 <= cost_c2:
                    costs[i,min_index] += 50
                else:
                    costs[indexes.index(min_index),min_index] += 50
                i = 0
            else:
                i += 1
        return indexes

def label_creeps_old(old_creeps, new_creeps):
    indexes = index_creeps(old_creeps, new_creeps)
    for i, creep in enumerate(new_creeps):
        if indexes[i] == -1:
            creep.label = generate_new_label()
            creep.history = []
        else:
            # creep.label = old_creeps[indexes[i]].label
            creep.x_history = (old_creeps[indexes[i]].x_history + 
                              [old_creeps[indexes[i]].x])
            creep.y_history = (old_creeps[indexes[i]].y_history + 
                              [old_creeps[indexes[i]].y])
            creep.health_history = (old_creeps[indexes[i]].health_history + 
                                   [old_creeps[indexes[i]].health])
    # for i in range(len(old_creeps)):
    #     if i not in indexes:
    #         print "creep dropped"
    #         print old_creeps[i].health, old_creeps[i].history

def make_tracked_creeps_history(creeps_history):
    tracked_creeps_history = []
    for creep in creeps_history[0]:
        creep.birth_count = 0
        creep.x_history = []
        creep.y_history = []
        creep.health_history = []

    for count in range(1,len(creeps_history)):
        # print i
        old_creeps = creeps_history[count-1]
        new_creeps = creeps_history[count]
        indexes = index_creeps(old_creeps, new_creeps)
        for i, creep in enumerate(new_creeps):
            if indexes[i] == -1:
                creep.birth_count = count
                creep.x_history = []
                creep.y_history = []
                creep.health_history = []
            else:
                # creep.label = old_creeps[indexes[i]].label
                creep.birth_count = old_creeps[indexes[i]].birth_count
                creep.x_history = (old_creeps[indexes[i]].x_history + 
                                  [old_creeps[indexes[i]].x])
                creep.y_history = (old_creeps[indexes[i]].y_history + 
                                  [old_creeps[indexes[i]].y])
                creep.health_history = (old_creeps[indexes[i]].health_history + 
                                       [old_creeps[indexes[i]].health])
        # add newly dead creeps to tracked_creeps_history
        for i in range(len(old_creeps)):
            if i not in indexes:
                tracked_creeps_history.append(old_creeps[i])
                # print "creep dropped"
                # print old_creeps[i].health, old_creeps[i].history
    return tracked_creeps_history


def show_creeps(p, creeps):
    xs, ys = ([],[])
    for creep in creeps:
        xs.append(creep.x)
        ys.append(creep.y)
    # plt.scatter(xs, ys, s=20)
    p.set_data(xs, ys)

def replay_main(rad_creeps_history,dir_creeps_history, start_index=0, end_index=-1):
    if end_index == -1:
        end_index = 1400*5 #len(rad_creeps_history)-1
    tracked_creeps_history = []
    tracked_creeps = []
    # a = time.time()
    # tracked_creeps_history = make_tracked_creeps_history(rad_creeps_history)
    # for i in range(1,len(rad_creeps_history)):
    #     label_creeps(rad_creeps_history[i-1], rad_creeps_history[i])
        # update_tracked_creeps(tracked_creeps, iteration)
        # tracked_creeps_history.append(len(tracked_creeps))
    # print time.time() - a
    # print "AAAAAAAAA"
    R = ReplayHandler(rad_creeps_history, dir_creeps_history, start_index, end_index)
    ani = animation.FuncAnimation(R.fig, R.update, interval=20,blit=False)
    plt.show()
    return tracked_creeps_history

if __name__ == '__main__':
    state = pickle.load( open( "save.p", "rb" ) )
    replay_main(state['rad_creeps_history'], state['dire_creeps_history'], 0, state['counter'])
    
