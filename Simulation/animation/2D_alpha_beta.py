import math
import csv
import tkinter as tk
import numpy as np
import subprocess as sp
import os
# CrawlBot settings:
param_file_path = "../dataIn/param.txt"

# Animation settings:
NBR_STEP = 600
CYCLE_PERIOD = 2
ANGLE_FILE_FL = 'FL_angle.csv'
ANGLE_FILE_FR = 'FR_angle.csv'
ANGLE_FILE_RL = 'RL_angle.csv'
ANGLE_FILE_RR = 'RR_angle.csv'
ANGLE_FOLDER_PATH = '../dataOut/angle/'

A_point_2_x = []
B_point_2_x = []
B_point_2_y = []
C_point_2_x = []
C_point_2_y = []
H_point_x = []
H_point_y = []

#  UI settings:
# Colors:
BG_COLOR = '#D6EAF8'
FG_COLOR = '#04035D'
# Fonts:
MAIN_FONT = 'Helvetica'
# Pads:
PADX_DRAW = 10
PADY_DRAW = 10

PADX_BUTT = 10
PADY_BUTT = 5

PADX_INFO = 10
PADY_INFO = 10

# Width:
WIDTH_BUTTON = 15

# Highlight:
show_highlight = 0

# Size (pixels):
MAIN_WIN_MIN_XSIZE = 480
MAIN_WIN_MIN_YSIZE = 360
DRAW_WIN_XSIZE = 150
DRAW_WIN_YSIZE = 150

# State variables
user_stop = 0
user_play = 0
user_pause = 0
user_newParam = 0

step_paused = 0


def read_param(param_file_path):
    param_file = open(param_file_path, 'r')
    param = np.empty((10, 2), dtype='U25')


    for line in param_file:
        line = line.rstrip()
        if line:
            sep_name, sep_val = line.split()
            if sep_name == 'LENGTH_A':
                param[0, 0] = 'LENGTH_A'
                param[0, 1] = sep_val

            if sep_name == 'LENGTH_B':
                param[1, 0] = 'LENGTH_B'
                param[1, 1] = sep_val

            if sep_name == 'LENGTH_C':
                param[2, 0] = 'LENGTH_C'
                param[2, 1] = sep_val

            if sep_name == 'INIT_X':
                param[3, 0] = 'INIT_X'
                param[3, 1] = sep_val

            if sep_name == 'INIT_Y':
                param[4, 0] = 'INIT_Y'
                param[4, 1] = sep_val

            if sep_name == 'INIT_Z':
                param[5, 0] = 'INIT_Z'
                param[5, 1] = sep_val

            if sep_name == 'MAX_Z':
                param[6, 0] = 'MAX_Z'
                param[6, 1] = sep_val

            if sep_name == 'TRAJ_LEG_SAMPLES':
                param[7, 0] = 'TRAJ_LEG_SAMPLES'
                param[7, 1] = sep_val

            if sep_name == 'TILT_ANGLE':
                param[8, 0] = 'TILT_ANGLE'
                param[8, 1] = sep_val

            if sep_name == 'MOVE_SEQUENCE':
                param[9, 0] = 'MOVE_SEQUENCE'
                param[9, 1] = sep_val

    return param


def write_param(param_file_path, param):
    param_file = open(param_file_path, 'r+')
    param_file.truncate(0)
    param_file.write("PARAMETER FILE\n\n")

    param_file.write("LENGTH_A\t\t\t\t\t\t")
    param_file.write(str(param[0])+"\n")
    param_file.write("LENGTH_B\t\t\t\t\t\t")
    param_file.write(str(param[1])+"\n")
    param_file.write("LENGTH_C\t\t\t\t\t\t")
    param_file.write(str(param[2])+"\n\n")

    param_file.write("INIT_X\t\t\t\t\t\t\t")
    param_file.write(str(param[3])+"\n")
    param_file.write("INIT_Y\t\t\t\t\t\t\t")
    param_file.write(str(param[4])+"\n")
    param_file.write("INIT_Z\t\t\t\t\t\t\t")
    param_file.write(str(param[5])+"\n")
    param_file.write("MAX_Z\t\t\t\t\t\t\t\t")
    param_file.write(str(param[6])+"\n\n")

    param_file.write("TRAJ_LEG_SAMPLES\t\t")
    param_file.write(str(param[7])+"\n")
    param_file.write("TILT_ANGLE\t\t\t\t\t")
    param_file.write(str(param[8])+"\n")
    param_file.write("MOVE_SEQUENCE\t\t\t\t")
    param_file.write(str(param[9])+"\n")

    param_file.close()


def load_param():
    parameters = read_param(param_file_path)
    LENGTH_A = float(parameters[0, 1])
    LENGTH_B = float(parameters[1, 1])
    LENGTH_C = float(parameters[2, 1])

    REF_X = float(parameters[3, 1])
    REF_Y = float(parameters[4, 1])
    REF_Z = float(parameters[5, 1])
    MAX_Z = float(parameters[6, 1])

    TRAJ_LEG_SAMPLES = int(parameters[7, 1])
    TILT_ANGLE = float(parameters[8, 1])
    MOVE_SEQ = int(parameters[9, 1])

    return [LENGTH_A, LENGTH_B, LENGTH_C, REF_X, REF_Y, REF_Z, MAX_Z, TRAJ_LEG_SAMPLES, TILT_ANGLE, MOVE_SEQ]


def load_info_frame(main_win, parameters):
    global BG_COLOR, FG_COLOR, PADX_INFO, PADY_INFO, MAIN_FONT
    # Setting the information Tab:
    info_frame = tk.Frame(main_win, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
    info_frame.grid(column=0, row=2, sticky='ns')

    # adding length information:
    length_info_frame = tk.Frame(info_frame, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
    length_info_frame.grid(column=0, row=0, sticky='wns', padx=PADX_INFO, pady=PADY_INFO)
    length_A_label = tk.Label(length_info_frame, text='Length A (mm) = '+str(parameters[0]), font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    length_B_label = tk.Label(length_info_frame, text='Length B (mm) = '+str(parameters[1]), font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    length_C_label = tk.Label(length_info_frame, text='Length C (mm) = '+str(parameters[2]), font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)

    length_A_label.grid(column=0, row=0, sticky='w')
    length_B_label.grid(column=0, row=1, sticky='w')
    length_C_label.grid(column=0, row=2, sticky='w')

    REF_info_frame = tk.Frame(info_frame, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
    REF_info_frame.grid(column=1, row=0, sticky='wns', padx=PADX_INFO, pady=PADY_INFO)
    REFX_label = tk.Label(REF_info_frame, text='Ref X (mm) = '+str(parameters[3]), font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    REFY_label = tk.Label(REF_info_frame, text='Ref Y (mm) = '+str(parameters[4]), font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    REFZ_label = tk.Label(REF_info_frame, text='Ref Z (mm) = '+str(parameters[5]), font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    MAXZ_label = tk.Label(REF_info_frame, text='Max Z (mm) = '+str(parameters[6]), font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)

    REFX_label.grid(column=0, row=0, sticky='w')
    REFY_label.grid(column=0, row=1, sticky='w')
    REFZ_label.grid(column=0, row=2, sticky='w')
    MAXZ_label.grid(column=0, row=3, sticky='w')

    OTHER_info_frame = tk.Frame(info_frame, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
    OTHER_info_frame.grid(column=2, row=0, sticky='wns', padx=PADX_INFO, pady=PADY_INFO)
    traj_leg_samples_label = tk.Label(OTHER_info_frame, text='Step traj samples nbr = '+str(parameters[7]), font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    tilt_angle_label = tk.Label(OTHER_info_frame, text='Tilt angle = '+str(parameters[8]), font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    move_seq_label = tk.Label(OTHER_info_frame, text='Movement sequence ID = '+str(parameters[9]), font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)

    traj_leg_samples_label.grid(column=0, row=0, sticky='w')
    tilt_angle_label.grid(column=0, row=1, sticky='w')
    move_seq_label.grid(column=0, row=2, sticky='w')


def read_data(file_path):
    with open(file_path, newline='') as csvfile:
        data = list(csv.reader(csvfile))
        for x in range(len(data)):
            for y in range(3):
                data[x][y] = float(data[x][y])

        return data


def compute_lines(parameters, data):
    global A_point_2_x, B_point_2_x, B_point_2_y, C_point_2_x, C_point_2_y, H_point_x, H_point_y
    A_point_2_x = []
    B_point_2_x = []
    B_point_2_y = []
    C_point_2_x = []
    C_point_2_y = []
    H_point_x = []
    H_point_y = []

    for i in range(len(data)):
        LENGTH_B_PROJ_V = parameters[1] * math.cos(math.radians(data[i][1]-90))
        LENGTH_C_PROJ_V = parameters[2] * math.sin(math.radians(data[i][2]+data[i][1]-180))
        LENGTH_A_PROJ_H = parameters[0] * math.cos(math.radians(data[i][0]))
        LENGTH_B_PROJ_H = LENGTH_B_PROJ_V * math.cos(math.radians(data[i][0]))
        LENGTH_C_PROJ_H = LENGTH_C_PROJ_V * math.cos(math.radians(data[i][0]))

        A_point_2_x.append(LENGTH_A_PROJ_H)

        B_point_2_x.append(LENGTH_A_PROJ_H + LENGTH_B_PROJ_H)
        B_point_2_y.append(parameters[1] * math.sin(math.radians(data[i][1]-90)))
        # calculation of the C-part of the leg
        C_point_2_x.append(LENGTH_A_PROJ_H + LENGTH_B_PROJ_H + LENGTH_C_PROJ_H)
        C_point_2_y.append(-parameters[2] * math.cos(math.radians(data[i][2]-180+data[i][1])) + B_point_2_y[i])

        # Horizontal view calculation:
        leg_len = parameters[0] + LENGTH_B_PROJ_V + LENGTH_C_PROJ_V
        H_point_x.append(leg_len * math.cos(math.radians(data[i][0])))
        H_point_y.append(leg_len * math.sin(math.radians(data[i][0])))

    points = [[A_point_2_x, B_point_2_x, B_point_2_y, C_point_2_x, C_point_2_y], [H_point_x, H_point_y]]
    return points


def draw_leg(draw_V, draw_H, line_points):
    global NBR_STEP, CYCLE_PERIOD, user_stop, user_play, user_pause, step_paused
    base = 0

    if user_pause == 1:
        user_pause = 0
        base = step_paused
        for n in range(len(draw_V)):
            draw_V[n].delete('all')
            draw_H[n].delete('all')

    for i in range(base, len(line_points[0][0][0])):
        for n in range(len(draw_V)):
            # Drawing our graph for the corresponding angles
            draw_V[n].delete("all")
            draw_H[n].delete('all')
            draw_V[n].after(CYCLE_PERIOD)
            draw_H[n].after(CYCLE_PERIOD)

            if n == 0 or n == 2:
                # A-part of leg:
                draw_V[n].create_line(DRAW_WIN_XSIZE, DRAW_WIN_YSIZE/2, DRAW_WIN_XSIZE-line_points[n][0][0][i], DRAW_WIN_YSIZE/2)
                # B-part of leg:
                draw_V[n].create_line(DRAW_WIN_XSIZE-line_points[n][0][0][i], DRAW_WIN_YSIZE/2, DRAW_WIN_XSIZE-line_points[n][0][1][i], DRAW_WIN_YSIZE/2-line_points[n][0][2][i])
                # C-part of leg:
                draw_V[n].create_line(DRAW_WIN_XSIZE-line_points[n][0][1][i], DRAW_WIN_YSIZE/2-line_points[n][0][2][i], DRAW_WIN_XSIZE-line_points[n][0][3][i], DRAW_WIN_YSIZE/2-line_points[n][0][4][i])
                draw_H[n].create_line(DRAW_WIN_XSIZE, DRAW_WIN_YSIZE/2, DRAW_WIN_XSIZE-line_points[n][1][0][i], DRAW_WIN_YSIZE/2-line_points[n][1][1][i])

            else:
                # A-part of leg:
                draw_V[n].create_line(0, DRAW_WIN_YSIZE/2, line_points[n][0][0][i], DRAW_WIN_YSIZE/2)
                # B-part of leg:
                draw_V[n].create_line(line_points[n][0][0][i], DRAW_WIN_YSIZE/2, line_points[n][0][1][i], DRAW_WIN_YSIZE/2-line_points[n][0][2][i])
                # C-part of leg:
                draw_V[n].create_line(line_points[n][0][1][i], DRAW_WIN_YSIZE/2-line_points[n][0][2][i], line_points[n][0][3][i], DRAW_WIN_YSIZE/2-line_points[n][0][4][i])

                draw_H[n].create_line(0, DRAW_WIN_YSIZE/2, line_points[n][1][0][i], DRAW_WIN_YSIZE/2-line_points[n][1][1][i])

            draw_V[n].update()
            draw_H[n].update()

        base += 1

        if i >= NBR_STEP-1 or user_stop == 1:
            user_stop = 0
            for n in range(len(draw_V)):
                draw_V[n].delete('all')
                draw_H[n].delete('all')

            break

        if user_pause == 1:
            for n in range(len(draw_V)):
                if n == 0 or n == 2:
                    # A-part of leg:
                    draw_V[n].create_line(DRAW_WIN_XSIZE, DRAW_WIN_YSIZE/2, DRAW_WIN_XSIZE-line_points[n][0][0][i], DRAW_WIN_YSIZE/2)
                    # B-part of leg:
                    draw_V[n].create_line(DRAW_WIN_XSIZE-line_points[n][0][0][i], DRAW_WIN_YSIZE/2, DRAW_WIN_XSIZE-line_points[n][0][1][i], DRAW_WIN_YSIZE/2-line_points[n][0][2][i])
                    # C-part of leg:
                    draw_V[n].create_line(DRAW_WIN_XSIZE-line_points[n][0][1][i], DRAW_WIN_YSIZE/2-line_points[n][0][2][i], DRAW_WIN_XSIZE-line_points[n][0][3][i], DRAW_WIN_YSIZE/2-line_points[n][0][4][i])

                    draw_H[n].create_line(DRAW_WIN_XSIZE, DRAW_WIN_YSIZE/2, DRAW_WIN_XSIZE-line_points[n][1][0][i], DRAW_WIN_YSIZE/2-line_points[n][1][1][i])

                else:
                    # A-part of leg:
                    draw_V[n].create_line(0, DRAW_WIN_YSIZE/2, line_points[n][0][0][i], DRAW_WIN_YSIZE/2)
                    # B-part of leg:
                    draw_V[n].create_line(line_points[n][0][0][i], DRAW_WIN_YSIZE/2, line_points[n][0][1][i], DRAW_WIN_YSIZE/2-line_points[n][0][2][i])
                    # C-part of leg:
                    draw_V[n].create_line(line_points[n][0][1][i], DRAW_WIN_YSIZE/2-line_points[n][0][2][i], line_points[n][0][3][i], DRAW_WIN_YSIZE/2-line_points[n][0][4][i])

                    draw_H[n].create_line(0, DRAW_WIN_YSIZE/2, line_points[n][1][0][i], DRAW_WIN_YSIZE/2-line_points[n][1][1][i])

            step_paused = base
            break


def close_win(wins):
    for i in wins:
        i.destroy()


def new_param_compute(mother_win, entry_array):
    global line_points, parameters

    new_param = []
    for i in entry_array:
        new_param.append(i.get())

    print(new_param)

    write_param(param_file_path, new_param)
    os.chdir('../')
    sp.call('./simu')
    os.chdir('animation')

    info_win = tk.Toplevel(mother_win, bg=BG_COLOR)
    info_win.title('Job done')
    info_win.geometry("400x150")
    f = tk.Frame(info_win, bg=BG_COLOR)
    f.pack(expand=True)
    text = tk.Label(f, text='Parameters loaded in the param file and\ndata recomputed with the new settings', font=(MAIN_FONT, 12), bg=BG_COLOR, fg=FG_COLOR)
    text.grid(column=0, row=0, sticky='nsew')
    wins = [info_win, mother_win]
    ok_button = tk.Button(f, text='OK', width=6, bg=FG_COLOR, fg='white', command=lambda: close_win(wins))
    ok_button.grid(column=0, row=1, sticky='nsew')

    parameters = load_param()

    load_info_frame(main_win, parameters)

    data_angle_fl = read_data(ANGLE_FOLDER_PATH+ANGLE_FILE_FL)
    data_angle_fr = read_data(ANGLE_FOLDER_PATH+ANGLE_FILE_FR)
    data_angle_rl = read_data(ANGLE_FOLDER_PATH+ANGLE_FILE_RL)
    data_angle_rr = read_data(ANGLE_FOLDER_PATH+ANGLE_FILE_RR)

    line_points_fl = compute_lines(parameters, data_angle_fl)
    line_points_fr = compute_lines(parameters, data_angle_fr)
    line_points_rl = compute_lines(parameters, data_angle_rl)
    line_points_rr = compute_lines(parameters, data_angle_rr)

    line_points = [line_points_fl, line_points_fr, line_points_rl, line_points_rr]


def newParam_window(main_win, parameters):
    param_window = tk.Toplevel(main_win, bg=BG_COLOR)
    param_window.title('Settings simulation\'s parameters')

    title_label = tk.Label(param_window, text='Chose new parameters for the simulation:', font=(MAIN_FONT, 20), bg=BG_COLOR, fg=FG_COLOR)
    title_label.grid(column=0, row=0, sticky='w', padx=20)
    robot_param_frame = tk.Frame(param_window, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
    robot_param_frame.grid(column=0, row=1, pady=20)

    Length_A_label = tk.Label(robot_param_frame, text='Length A (mm) = ', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    Length_A_label.grid(column=0, row=1, sticky='w')
    Length_A_entry = tk.Entry(robot_param_frame)
    Length_A_entry.insert(10, str(parameters[0]))
    Length_A_entry.grid(column=1, row=1, sticky='w')
    Length_B_label = tk.Label(robot_param_frame, text='Length B (mm) = ', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    Length_B_label.grid(column=0, row=2, sticky='w')
    Length_B_entry = tk.Entry(robot_param_frame)
    Length_B_entry.insert(10, str(parameters[1]))
    Length_B_entry.grid(column=1, row=2, sticky='w')
    Length_C_label = tk.Label(robot_param_frame, text='Length C (mm) = ', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    Length_C_label.grid(column=0, row=3, sticky='w')
    Length_C_entry = tk.Entry(robot_param_frame)
    Length_C_entry.insert(10, str(parameters[2]))
    Length_C_entry.grid(column=1, row=3, sticky='w')

    pos_param_frame = tk.Frame(param_window, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
    pos_param_frame.grid(column=0, row=2, pady=20)
    Init_X_label = tk.Label(pos_param_frame, text='Initial X pos (mm) = ', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    Init_X_label.grid(column=0, row=0, sticky='w')
    Init_X_entry = tk.Entry(pos_param_frame)
    Init_X_entry.insert(10, str(parameters[3]))
    Init_X_entry.grid(column=1, row=0, sticky='w')
    Init_Y_label = tk.Label(pos_param_frame, text='Initial Y pos (mm) = ', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    Init_Y_label.grid(column=0, row=1, sticky='w')
    Init_Y_entry = tk.Entry(pos_param_frame)
    Init_Y_entry.insert(10, str(parameters[4]))
    Init_Y_entry.grid(column=1, row=1, sticky='w')
    Init_Z_label = tk.Label(pos_param_frame, text='Initial Z pos (mm) = ', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    Init_Z_label.grid(column=0, row=2, sticky='w')
    Init_Z_entry = tk.Entry(pos_param_frame)
    Init_Z_entry.insert(10, str(parameters[5]))
    Init_Z_entry.grid(column=1, row=2, sticky='w')
    MAX_Z_label = tk.Label(pos_param_frame, text='Maximum height (mm) = ', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    MAX_Z_label.grid(column=0, row=3, sticky='w')
    MAX_Z_entry = tk.Entry(pos_param_frame)
    MAX_Z_entry.insert(10, str(parameters[6]))
    MAX_Z_entry.grid(column=1, row=3, sticky='w')

    misc_param_frame = tk.Frame(param_window, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
    misc_param_frame.grid(column=0, row=3, pady=20)
    traj_samples_label = tk.Label(misc_param_frame, text='Leg movement resolution (samples nbr) = ', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    traj_samples_label.grid(column=0, row=0, sticky='w')
    traj_samples_entry = tk.Entry(misc_param_frame)
    traj_samples_entry.insert(10, str(parameters[7]))
    traj_samples_entry.grid(column=1, row=0, sticky='w')
    tilt_angle_label = tk.Label(misc_param_frame, text='Leg movement\'s tilt angle (°) = ', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    tilt_angle_label.grid(column=0, row=1, sticky='w')
    tilt_angle_entry = tk.Entry(misc_param_frame)
    tilt_angle_entry.insert(10, str(parameters[8]))
    tilt_angle_entry.grid(column=1, row=1, sticky='w')
    move_seq_label = tk.Label(misc_param_frame, text='Leg movement resolution (samples nbr) = ', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
    move_seq_label.grid(column=0, row=2, sticky='w')
    move_seq_entry = tk.Entry(misc_param_frame)
    move_seq_entry.insert(10, str(parameters[9]))
    move_seq_entry.grid(column=1, row=2, sticky='w')

    entry_array = [Length_A_entry, Length_B_entry, Length_C_entry, Init_X_entry, Init_Y_entry, Init_Z_entry, MAX_Z_entry, traj_samples_entry, tilt_angle_entry, move_seq_entry]
    button_frame = tk.Frame(param_window, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
    button_frame.grid(column=0, row=4, pady=20)
    valid_button = tk.Button(button_frame, text='Confirm and compute', width=WIDTH_BUTTON, bg=FG_COLOR, fg='white', command=lambda: new_param_compute(param_window, entry_array))
    valid_button.grid(column=0, row=0, padx=PADX_BUTT, pady=PADY_BUTT)
    cancel_button = tk.Button(button_frame, text='Cancel', width=WIDTH_BUTTON, bg=FG_COLOR, fg='white', command=lambda: param_window.destroy())
    cancel_button.grid(column=1, row=0, padx=PADX_BUTT, pady=PADY_BUTT)


def user_stop_fct():
    global user_stop
    user_stop = 1


def user_play_fct():
    global user_play
    user_play = 1


def user_pause_fct():
    global user_pause
    user_pause = 1


def user_newParam_fct():
    global user_newParam
    user_newParam = 1


# Size (pixels):
MAIN_WIN_MIN_XSIZE = 480
MAIN_WIN_MIN_YSIZE = 360

# State variables
user_stop = 0
user_play = 0

# Calling setup functions:
parameters = load_param()

# --------------------------------------------------------------------------------------------------- #
# Reading data from files:
data_angle_fl = read_data(ANGLE_FOLDER_PATH+ANGLE_FILE_FL)
data_angle_fr = read_data(ANGLE_FOLDER_PATH+ANGLE_FILE_FR)
data_angle_rl = read_data(ANGLE_FOLDER_PATH+ANGLE_FILE_RL)
data_angle_rr = read_data(ANGLE_FOLDER_PATH+ANGLE_FILE_RR)

line_points_fl = compute_lines(parameters, data_angle_fl)
line_points_fr = compute_lines(parameters, data_angle_fr)
line_points_rl = compute_lines(parameters, data_angle_rl)
line_points_rr = compute_lines(parameters, data_angle_rr)

line_points = [line_points_fl, line_points_fr, line_points_rl, line_points_rr]

# Reading parameters from file:

# --------------------------------------------------------------------------------------------------- #

# --------------------------------------------------------------------------------------------------- #
# Settings the main window
main_win = tk.Tk()
main_win.title("2D leg animation")
main_win.minsize(MAIN_WIN_MIN_XSIZE, MAIN_WIN_MIN_YSIZE)
main_win.config(bg=BG_COLOR)
# --------------------------------------------------------------------------------------------------- #

load_info_frame(main_win, parameters)

# --------------------------------------------------------------------------------------------------- #
# Setting the title frame:
label_title = tk.Label(main_win, text='CrawlBot leg position simulator', font=(MAIN_FONT, 20), bg=BG_COLOR, fg=FG_COLOR)
label_title.grid(column=0, row=0, columnspan=2, sticky='ewns', pady=5)
# --------------------------------------------------------------------------------------------------- #

# --------------------------------------------------------------------------------------------------- #
# Setting the UI frame
draw_frame = tk.Frame(main_win, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
draw_frame.grid(column=0, row=1, sticky='nsew')

RearFront_label = tk.Label(draw_frame, text='Rear to Front point of view', font=(MAIN_FONT, 15), bg=BG_COLOR, fg=FG_COLOR)
RearFront_label.grid(column=0, row=0, sticky='wens')

TopBot_label = tk.Label(draw_frame, text='Top to Bottom point of view', font=(MAIN_FONT, 15), bg=BG_COLOR, fg=FG_COLOR)
TopBot_label.grid(column=1, row=0, sticky='ewns')

draw_frame_RearFront = tk.Frame(draw_frame, bg=BG_COLOR, highlightthickness=1, highlightbackground=FG_COLOR)
draw_frame_RearFront.grid(column=0, row=1, sticky='nsew', padx=PADX_DRAW)

# Setting the Canvas that wil host the drawing
frame_FL_RearFront = tk.Frame(draw_frame_RearFront, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
frame_FL_RearFront.grid(column=0, row=0, padx=PADX_DRAW, pady=PADY_DRAW, sticky='nsew')
label_FL_RearFront = tk.Label(frame_FL_RearFront, text='Front left leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_FL_RearFront.grid(column=0, row=0)
draw_canvas_fl_RearFront = tk.Canvas(frame_FL_RearFront, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_fl_RearFront.grid(column=0, row=1)

frame_FR_RearFront = tk.Frame(draw_frame_RearFront, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
frame_FR_RearFront.grid(column=1, row=0, padx=PADX_DRAW, pady=PADY_DRAW, sticky='nsew')
label_FR_RearFront = tk.Label(frame_FR_RearFront, text='Front right leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_FR_RearFront.grid(column=0, row=0)
draw_canvas_fr_RearFront = tk.Canvas(frame_FR_RearFront, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_fr_RearFront.grid(column=0, row=1)

frame_RL_RearFront = tk.Frame(draw_frame_RearFront, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
frame_RL_RearFront.grid(column=0, row=1, padx=PADX_DRAW, pady=PADY_DRAW, sticky='nsew')
label_RL = tk.Label(frame_RL_RearFront, text='Rear left leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_RL.grid(column=0, row=0)
draw_canvas_rl_RearFront = tk.Canvas(frame_RL_RearFront, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_rl_RearFront.grid(column=0, row=1)

frame_RR_RearFront = tk.Frame(draw_frame_RearFront, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
frame_RR_RearFront.grid(column=1, row=1, padx=PADX_DRAW, pady=PADY_DRAW, sticky='nsew')
label_RR_RearFront = tk.Label(frame_RR_RearFront, text='Rear right leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_RR_RearFront.grid(column=0, row=0)
draw_canvas_rr_RearFront = tk.Canvas(frame_RR_RearFront, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_rr_RearFront.grid(column=0, row=1)

draw_canvas_RearFront = [draw_canvas_fl_RearFront, draw_canvas_fr_RearFront, draw_canvas_rl_RearFront, draw_canvas_rr_RearFront]

draw_frame_TopBot = tk.Frame(draw_frame, bg=BG_COLOR, highlightthickness=1, highlightbackground=FG_COLOR)
draw_frame_TopBot.grid(row=1, column=1, sticky='nsew', padx=PADX_DRAW)

# Setting the Canvas that will host the drawing
frame_FL_TopBot = tk.Frame(draw_frame_TopBot, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
frame_FL_TopBot.grid(row=0, column=0, padx=PADX_DRAW, pady=PADY_DRAW, sticky='nsew')
label_FL_TopBot = tk.Label(frame_FL_TopBot, text='Front left leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_FL_TopBot.grid(row=0, column=0)
draw_canvas_fl_TopBot = tk.Canvas(frame_FL_TopBot, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_fl_TopBot.grid(row=1, column=0)

frame_FR_TopBot = tk.Frame(draw_frame_TopBot, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
frame_FR_TopBot.grid(row=0, column=1, padx=PADX_DRAW, pady=PADY_DRAW, sticky='nsew')
label_FR_TopBot = tk.Label(frame_FR_TopBot, text='Front right leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_FR_TopBot.grid(row=0, column=0)
draw_canvas_fr_TopBot = tk.Canvas(frame_FR_TopBot, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_fr_TopBot.grid(row=1, column=0)

frame_RL_TopBot = tk.Frame(draw_frame_TopBot, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
frame_RL_TopBot.grid(row=1, column=0, padx=PADX_DRAW, pady=PADY_DRAW, sticky='nsew')
label_RL_TopBot = tk.Label(frame_RL_TopBot, text='Rear left leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_RL_TopBot.grid(row=0, column=0)
draw_canvas_rl_TopBot = tk.Canvas(frame_RL_TopBot, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_rl_TopBot.grid(row=1, column=0)

frame_RR_TopBot = tk.Frame(draw_frame_TopBot, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
frame_RR_TopBot.grid(row=1, column=1, padx=PADX_DRAW, pady=PADY_DRAW, sticky='nsew')
label_RR_TopBot = tk.Label(frame_RR_TopBot, text='Rear right leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_RR_TopBot.grid(row=0, column=0)
draw_canvas_rr_TopBot = tk.Canvas(frame_RR_TopBot, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_rr_TopBot.grid(row=1, column=0)

draw_canvas_TopBot = [draw_canvas_fl_TopBot, draw_canvas_fr_TopBot, draw_canvas_rl_TopBot, draw_canvas_rr_TopBot]
# --------------------------------------------------------------------------------------------------- #

# --------------------------------------------------------------------------------------------------- #
# Setting the Simulator command frame:
command_frame = tk.Frame(main_win, bg=BG_COLOR, highlightthickness=show_highlight, highlightbackground=FG_COLOR)
command_frame.grid(column=2, row=1, sticky='sn')

# adding a play button:
play_animation = tk.Button(command_frame, text='PLAY', width=WIDTH_BUTTON, bg=FG_COLOR, fg='white', command=user_play_fct)
play_animation.grid(column=0, row=0, padx=PADX_BUTT, pady=PADY_BUTT)

# adding a pause button:
pause_animation = tk.Button(command_frame, text='PAUSE', width=WIDTH_BUTTON, bg=FG_COLOR, fg='white', command=user_pause_fct)
pause_animation.grid(column=0, row=1, padx=PADX_BUTT, pady=PADY_BUTT)

# adding a stop button:
stop_animation = tk.Button(command_frame, text='STOP', width=WIDTH_BUTTON, bg=FG_COLOR, fg='white', command=user_stop_fct)
stop_animation.grid(column=0, row=2, padx=PADX_BUTT, pady=PADY_BUTT)

# adding new param button :
newParam_button = tk.Button(command_frame, text='Change Params', width=WIDTH_BUTTON, bg=FG_COLOR, fg='white', command=user_newParam_fct)
newParam_button.grid(column=0, row=3, padx=PADX_BUTT, pady=PADY_BUTT)
# --------------------------------------------------------------------------------------------------- #

# --------------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------------- #
# TESTS:

# --------------------------------------------------------------------------------------------------- #

# Opening the window
while True:
    main_win.update_idletasks()
    main_win.update()
    if user_play == 1:
        draw_leg(draw_canvas_RearFront, draw_canvas_TopBot, line_points)
        user_play = 0
        user_newParam = 0

    if user_stop == 1:
        for n in range(len(draw_canvas_RearFront)):
            draw_canvas_RearFront[n].delete('all')
            draw_canvas_TopBot[n].delete('all')
            user_stop = 0
            user_newParam = 0

    if user_newParam == 1:
        newParam_window(main_win, parameters)
        user_newParam = 0
