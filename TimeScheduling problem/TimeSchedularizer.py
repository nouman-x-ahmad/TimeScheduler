
# Nouman Ahmad






import random as randm
import copy
#imp

# Constants
start_session_in_afternoon = 4
end_session_afternoon = 8
start_of_morning_session = 0
total_num_dayz_workweek = 5




#================================================================================================================================================================================================


# Define binary encoding lengths for each attribute
encoded_info_timetabler = {
    'course': 4,
    'theory_lab': 1,
    'section': 3,
    'section_strength': 3,
    'professor': 4,
    'first_lecture_day': 3,
    'first_lecture_timeslot': 4,
    'first_lecture_room': 3,
    'first_lecture_room_size': 2,
    'second_lecture_day': 3,
    'second_lecture_timeslot': 4,
    'second_lecture_room': 3,
    'second_lecture_room_size': 2
}




#================================================================================================================================================================================================


class class_room_section:
    def __init__(self, nmn, class_dur, class_instruc, class_subj, check_lab_bool=False):
        self.class_name = nmn
        self.class_dur = class_dur
        self.class_teacherz = class_instruc
        self.class_subjc = class_subj
        self.class_chck_lab = check_lab_bool




#================================================================================================================================================================================================


class taime_tabler_class:
    def __init__(self, clazz):
        self.tbler_class = clazz
        self.check_fit_lvl = 0



#================================================================================================================================================================================================



def initial_populator(popul_size, tbler_class, rms, tm_slts):
    popul = []
    for _ in range(popul_size):
        tm_tble = time_table_creatorz(tbler_class, rms, tm_slts)
        popul.append(tm_tble)
    return popul




#================================================================================================================================================================================================


def time_table_creatorz(tbler_class, class_rooms, tm_slts):
    tmtble = {}
    rm_ass = {}
    temp=0
    susbt=0
    
    
    
    
    prof_crses = {cls_obj.class_teacherz: 0 for cls_obj in tbler_class}  # prof_crs_limiter
    sec_crses = {cls_obj.class_subjc: 0 for cls_obj in tbler_class}  # section_crs_counter
    
    
    
    for x in tbler_class:
        roooom = randm.choice(class_rooms)
        time_slot = randm.choice(tm_slts)

        # Check prof_crs_limited + sec_crs cikrfioowef
        prof_crs_limited=3
        sec_crs_limiter=5
        if prof_crses[x.class_teacherz] < prof_crs_limited and sec_crses[x.class_subjc] < sec_crs_limiter:
            if time_slot not in tmtble:
                tmtble[time_slot] = {}
            tmtble[time_slot][roooom] = x
            
            rm_ass[x.class_name] = roooom
            
            prof_crses[x.class_teacherz] += 1  # Increment  # prof_crs_limiter
            
            sec_crses[x.class_subjc] += 1  # Increment section _crs_ counter
   
   
    return taime_tabler_class(tmtble), rm_ass



#================================================================================================================================================================================================



def gen_table_printer(generation, popul_var):
    print(f"Generation: {generation}")
    for i, timetable_tuple in enumerate(popul_var):
        print(f"Schedule {i + 1}:")
        time_tabler_printer(timetable_tuple[0])
        print()





#================================================================================================================================================================================================

def fit_func_checker(timetable, room_assignments):
    clashes = 0
    floor_changes = 0
    room_changes = 0
    fitn_total_count = 0
    temp = 0
    susbt = 0





    for time_slot, room_dictionary_var in timetable.tbler_class.items():
        lst_timer_check = None



        for room, class_ in room_dictionary_var.items():
            #  softie constraints
            if class_.class_subjc == "Science":
                if room[5] != '2':
                    floor_changes += 1
            else:
                if room[5] == '2':
                    floor_changes += 1

            prev_room = None
            if time_slot in timetable.tbler_class:
                prev_room = list(timetable.tbler_class[time_slot].keys())[0]
            if prev_room is not None and prev_room != room:
                room_changes += 1

            # Additional fit_func_checker considerations

            if class_.class_teacherz == "Mr. Smith":
                fitn_total_count += 5


            if class_.class_name == "Math" and class_.class_dur > 1:
                fitn_total_count -= 1

            # break of 15 minutes
            if lst_timer_check is not None:
                current_time = int(time_slot.split("-")[1].split(":")[0])
                last_end_time = int(lst_timer_check.split("-")[1].split(":")[0])
                if current_time - last_end_time < 1:  # 15-minute break allowed (1 hour difference)
                    fitn_total_count -= 2  # Penalize for lack of break
            lst_timer_check = time_slot

    fitn_total_count = 100 - (clashes * 10 + floor_changes * 5 + room_changes * 2)

    if fitn_total_count < 0:
        fitn_total_count = 0

    return fitn_total_count



#================================================================================================================================================================================================



def selection(popul, k=2):
    popul_tornament = randm.sample(popul, k)
    fitn_tornament = [chromosome[0].check_fit_lvl for chromosome in
                          popul_tornament]  # Accessing fit_func_checker from the first element of each tuple



    best_chromosomes = sorted(zip(popul_tornament, fitn_tornament), key=lambda x: x[1], reverse=True)[:2]






    return best_chromosomes[0][0], best_chromosomes[1][0]  # Returning only the taime_tabler_class objects





#================================================================================================================================================================================================


def cross_function_over(parent1, parent2):


    par_1_table_time, _ = parent1
    par_2_table_time, _ = parent2
    crossover_point = randm.randint(1, min(len(par_1_table_time.tbler_class), len(par_2_table_time.tbler_class)) - 1)
    child_1_classes_ = {}
    child_2_classes_ = {}

    # Copy tbler_class up
    for i, (z, y) in enumerate(par_1_table_time.tbler_class.items()):
        if i < crossover_point:
            child_1_classes_[z] = y
    for i, (z, y) in enumerate(par_2_table_time.tbler_class.items()):
        if i < crossover_point:
            child_2_classes_[z] = y

    # Add rremaining tbler class
    for z, y in par_2_table_time.tbler_class.items():
        if z not in child_1_classes_:
            child_1_classes_[z] = y
    for z, y in par_1_table_time.tbler_class.items():
        if z not in child_2_classes_:
            child_2_classes_[z] = y

    return (taime_tabler_class(child_1_classes_), {}), (taime_tabler_class(child_2_classes_), {})




#================================================================================================================================================================================================

def mutator(timetable_tuple, room_dictionary_var, time_scheduler_slot):





    taime_tablerzzz, _ = timetable_tuple  # Extracting the taime_tabler_class object from the tuple
    # Randomly change a class slot



    k = list(taime_tablerzzz.tbler_class.keys())
    rand_key = randm.choice(k)
    rand_rooom = randm.choice(room_dictionary_var)
    rand_clasass = randm.choice(tbler_class)
    taime_tablerzzz.tbler_class[rand_key] = {rand_rooom: rand_clasass}




    return (taime_tablerzzz, {})  # Returning mutated schedulessssssss

#================================================================================================================================================================================================
def gen_algo_funct(popul_size, gen_var, tbler_class, room_dictionary_var, time_scheduler_slot):
    popul_var = initial_populator(popul_size_var, tbler_class, room_dictionary_var, time_scheduler_slot)



    for iterator in range(gen_var):
        for time_tupul in popul_var:  # Iterate over each tuple in the popul_var
            time_var_loop, rms_assign = time_tupul  # Unpack the tuple
            time_var_loop.check_fit_lvl = fit_func_checker(time_var_loop, rms_assign)
        popul_var.sort(key=lambda x: x[0].check_fit_lvl, reverse=True)
        best_schedule, best_room_assignments = popul_var[0]
        print(f"Generation: {iterator}, Fitness: {best_schedule.check_fit_lvl}")
        time_tabler_printer(best_schedule)  # Print the best schedule of each generation
        new_pop_var = [(best_schedule, best_room_assignments)]


        new_var_temp=popul_size_var
        while len(new_pop_var) < new_var_temp:
            parent1, parent2 = selection(popul_var)
            child1, child2 = cross_function_over(parent1, parent2)
            child1 = mutator(child1, room_dictionary_var, time_scheduler_slot)
            child2 = mutator(child2, room_dictionary_var, time_scheduler_slot)
            new_pop_var.append(child1)  #
            new_pop_var.append(child2)  #
        popul_var = new_pop_var




#================================================================================================================================================================================================



def time_tabler_printer(timetable):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    print("Schedule:")
    for day in days:
        print(f"Day: {day}")
        for time_slot, room_dictionary_var in timetable.tbler_class.items():
            slot_day, _ = time_slot.split("-")
            if slot_day == day:
                print(f"Time: {time_slot} |", end="")
                for room, class_ in room_dictionary_var.items():
                    print(
                        f" {class_.class_name} ({class_.class_teacherz}), Size: {class_.class_dur}, Room: {room}, Floor: {room[5]}, Time Period: {class_.class_dur * 60} mins |",
                        end="")
                print()
        print()







#================================================================================================================================================================================================


if __name__ == "__main__":










    tbler_class = [
        class_room_section("Math", 1, "Mr. Smith", "Math"),
        class_room_section("Physics", 1, "Ms. aleena", "Science"),
        class_room_section("Chemistry", 1, "Dr. ALi", "Science"),
        class_room_section("Biology", 1, "Prof. Maryum", "Science"),
        class_room_section("History", 1, "Mrs. Bilal", "Humanities"),
        class_room_section("Geography", 1, "Mr. Daud", "Humanities"),
        class_room_section("Literature", 2, "Ms. tariq", "Humanities"),  # Longer duration
        class_room_section("Art", 1, "Mrs. wania", "Arts"),
        class_room_section("Music", 1, "Mr. zakariya", "Arts"),
        class_room_section("Physical Education", 1, "Coach GANDEREE", "Sports"),

        class_room_section("Computer Science", 1, "Dr. NOUMAN", "Science"),
        class_room_section("Environmental Studies", 1, "Ms. gundagardee", "Science"),
        class_room_section("Psychology", 1, "Mr. anjuman", "Humanities"),
        class_room_section("Drama", 1, "Ms. ahmad", "Arts"),
        class_room_section("Swimming", 1, "Coach ganderee 2.0", "Sports"),
        class_room_section("Economics", 1, "Dr. Brown", "Humanities"),
        class_room_section("Sociology", 1, "Ms. joker", "Humanities"),
        class_room_section("Computer Graphics", 1, "Mr. aslam", "Arts"),
        class_room_section("Basketball", 1, "Coach meow", "Sports")
    ]







    for cls_obj in tbler_class:
        if cls_obj.class_subjc != "Sports" and cls_obj.class_dur == 1:
            cls_obj.class_chck_lab = True

    room_dictionary_var = ["Room 1", "Room 2", "Room 3"]

    time_scheduler_slot = \
        [
        "Monday-08:00", "Monday-09:00", "Monday-10:00", "Monday-11:00",
        "Tuesday-08:00", "Tuesday-09:00", "Tuesday-10:00", "Tuesday-11:00",
        "Wednesday-08:00", "Wednesday-09:00", "Wednesday-10:00", "Wednesday-11:00",
        "Thursday-08:00", "Thursday-09:00", "Thursday-10:00", "Thursday-11:00",
        "Friday-08:00", "Friday-09:00", "Friday-10:00", "Friday-11:00",
    ]

    popul_size_var = 100
    gen_var = 25
    gen_algo_funct(popul_size_var, gen_var, tbler_class, room_dictionary_var, time_scheduler_slot)




#================================================================================================================================================================================================

