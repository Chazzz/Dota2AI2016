# class Creep and functions that take a list of creeps as input
# 

class Creep(object):
    '''
    x,y is current x,y position (pixels on screen)
    health is current health (from 1, full health, to 0, dead)
    birthcount is index that creep was created
    history is the history of Creep's health from birth until death
    '''

    def __init__(self, x, y, health, time,
                 x_history=[], y_history=[], health_history=[], time_history=[], birth_count=0):
        self.x = x        
        self.y = y        
        self.health = health
        self.time = time
        self.x_history = x_history
        self.y_history = y_history
        self.health_history = health_history
        self.time_history = time_history
        self.birth_count = birth_count
        self.last_hit = -1
        self.last_hit_success = False
        self.label = ''

    def __repr__(self):
        return "Creep(%s, %s, %s, %s, %s, %s, %s, %s, %s)" % (
            self.x,
            self.y,
            self.health,
            self.time,
            self.x_history,
            self.y_history,
            self.health_history,
            self.time_history,
            self.birth_count,
            )

    def was_born(self, count):
        return count >= self.birth_count

    def has_died(self, count):
        # assume all histories are equal length
        return count > self.birth_count + len(health_history)

    def is_alive(self, count):
        return self.was_born(count) and not self.has_died(count)

    # def register_creep_history(self, )

def get_threshold_creeps(creeps, health_range):
    return [
        creep for creep in creeps if 
        creep.health > health_range[0] and 
        creep.health < health_range[1]]

def get_lowest_creep(creeps):
    return min(creeps, key = lambda l: l.health)

def percent_health_melee(damage):
    #2 armor and 10% rng
    return (damage*0.9*0.9)/550.0

def percent_health_ranged(damage):
    #0 armor and 10% rng
    return (damage*0.9)/300.0

hero = Creep(1204*3/4,520*3/4,1.0,0) #standin for actual hero-detection algorithm