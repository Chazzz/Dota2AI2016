import pickle
import matplotlib.pyplot as plt
import numpy as np

def plot_creep_dh_hist(creep, creep_dhs):
    ax = plt.gca()
    ax.hist(creep_dhs, 50, range=(-0.2,0.2), facecolor='green', alpha=0.75)
    ax.set_title("%s %s %i" % (creep.label, creep.last_hit_success, creep.last_hit))
    ax.set_xlabel("% health lost")
    ax.set_ylabel("# occurrences")
    plt.show()

def plot_creeps_dh_counter(creeps, creep_dhs, num_creeps=-1):
    '''num_creeps is the number of creeps to display
    displaying too many can cause memory overloads'''
    if num_creeps == -1:
        num_creeps = len(creeps)
    for i in range(num_creeps):
        plt.figure(i+1)
        ax = plt.gca()
        ax.bar(np.arange(len(creep_dhs[i])), creep_dhs[i], 1)
        ax.set_title("type=%s?, success=%s, death on frame %i" % (creeps[i].label, creeps[i].last_hit_success, creeps[i].last_hit))
        ax.set_xlim(0,60)
        ax.set_ylim(-0.1,0.2)
        ax.set_xlabel("counts before death")
        ax.set_ylabel("% health lost")
    plt.show()

def plot_creeps_dh_time(creeps, creep_dhs, num_creeps=-1):
    '''num_creeps is the number of creeps to display
    displaying too many can cause memory overloads'''
    if num_creeps == -1:
        num_creeps = len(creeps)
    for i in range(num_creeps):
        plt.figure(i+1)
        ax = plt.gca()
        ax.bar(-1*(np.array(creeps[i].time_history[1:]+[creeps[i].time])-creeps[i].time), creep_dhs[i], 0.05)
        ax.set_title("type=%s(?), success=%s, death on frame %i" % (creeps[i].label, creeps[i].last_hit_success, creeps[i].last_hit))
        ax.set_xlim(0,3)
        ax.set_ylim(-0.1,0.2)
        ax.set_xlabel("secs before (perceived) death")
        ax.set_ylabel("% health lost")
    plt.show()

def get_creep_dh_nonzero(creeps):
    '''all non-zero dh changes'''
    ret = []
    for creep in creeps:
        dhs = []
        # dts = []
        for i in range(1, len(creep.health_history)):
            dh = creep.health_history[i-1] - creep.health_history[i]
            if dh != 0:
                dhs.append(dh)
                # dts.append(i)
        # for last bit
        if creep.health_history != []:
            dh = creep.health_history[-1] - creep.health
            if dh != 0:
                dhs.append(dh)
                # dts.append(len(creeps.health_history))
        ret.append(dhs)
    return ret

def get_creep_dh_counter(creeps):
    '''dh at each count of creeps life'''
    ret = []
    for creep in creeps:
        dhs = []
        for i in range(1, len(creep.health_history)):
            dh = creep.health_history[i-1] - creep.health_history[i]
            dhs.append(dh)
        # for last bit
        if creep.health_history != []:
            dh = creep.health_history[-1] - creep.health
            dhs.append(dh)
        dhs.reverse()
        ret.append(dhs)
    return ret

def get_creep_dh_hist(creeps):
    '''dh at each count of creeps life,
       different from _counter by not having .reverse() step'''
    ret = []
    for creep in creeps:
        dhs = []
        for i in range(1, len(creep.health_history)):
            dh = creep.health_history[i-1] - creep.health_history[i]
            dhs.append(dh)
        # for last bit
        if creep.health_history != []:
            dh = creep.health_history[-1] - creep.health
            dhs.append(dh)
        ret.append(dhs)
    return ret

def main(state):
    print sum([creep.last_hit_success for creep in state['lh_creeps_history']]), "last hits achieved"
    print len(state['lh_creeps_history']), "last hits attempted (includes multiple attemts on 1 creep)"
    print [(creep.label, creep.last_hit_success) for creep in state['lh_creeps_history']]
    ## Histogram display
    # creep_dhs = get_creep_dh_nonzero(state['lh_creeps_history'])
    # assert len(creep_dhs) == len(state['lh_creeps_history'])
    # for i in range(4):#len(creep_dhs)):
    #     plot_creep_dh_hist(state['lh_creeps_history'][i], creep_dhs[i])
    ## Frame-based display
    # creep_dhs = get_creep_dh_counter(state['lh_creeps_history'])
    # assert len(creep_dhs) == len(state['lh_creeps_history'])
    # plot_creeps_dh_counter(state['lh_creeps_history'], creep_dhs, 1)
    ## Time-based display
    creep_dhs = get_creep_dh_hist(state['lh_creeps_history'])
    assert len(creep_dhs) == len(state['lh_creeps_history'])
    plot_creeps_dh_time(state['lh_creeps_history'], creep_dhs, 1)

if __name__ == '__main__':
    state = pickle.load( open( "save.p", "rb" ) )
    main(state)