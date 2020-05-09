import math
import csv
import tkinter as tk

# CrawlBot settings:
LENGTH_A = 49.5
LENGTH_B = 60
LENGTH_C = 99

# Animation settings:
NBR_STEP = 600
CYCLE_PERIOD = 2
ANGLE_FILE_FL = 'FL_angle.csv'
ANGLE_FILE_FR = 'FR_angle.csv'
ANGLE_FILE_RL = 'RL_angle.csv'
ANGLE_FILE_RR = 'RR_angle.csv'
ANGLE_FOLDER_PATH = '/home/yohann/Desktop/CrawlingBot/Simulation/dataOut/angle/'

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
# Width:
WIDTH_BUTTON = 15

# Size (pixels):
MAIN_WIN_MIN_XSIZE = 480
MAIN_WIN_MIN_YSIZE = 360
DRAW_WIN_XSIZE = 150
DRAW_WIN_YSIZE = 150

# State variables
user_stop = 0
user_play = 0
user_pause = 0

step_paused = 0


def read_data(file_path):
    with open(file_path, newline='') as csvfile:
        data = list(csv.reader(csvfile))
        for x in range(len(data)):
            for y in range(3):
                data[x][y] = float(data[x][y])

        return data


def compute_lines(data):
    global A_point_2_x, B_point_2_x, B_point_2_y, C_point_2_x, C_point_2_y, H_point_x, H_point_y
    A_point_2_x = []
    B_point_2_x = []
    B_point_2_y = []
    C_point_2_x = []
    C_point_2_y = []
    H_point_x = []
    H_point_y = []

    for i in range(len(data)):
        LENGTH_B_PROJ_V = LENGTH_B * math.cos(math.radians(data[i][1]-90))
        LENGTH_C_PROJ_V = LENGTH_C * math.sin(math.radians(data[i][2]+data[i][1]-180))
        LENGTH_A_PROJ_H = LENGTH_A * math.cos(math.radians(data[i][0]))
        LENGTH_B_PROJ_H = LENGTH_B_PROJ_V * math.cos(math.radians(data[i][0]))
        LENGTH_C_PROJ_H = LENGTH_C_PROJ_V * math.cos(math.radians(data[i][0]))

        LENGTH_B_y = LENGTH_B * math.sin(math.radians(data[i][1]-90))
        LENGTH_C_y = LENGTH_C * math.cos(math.radians(data[i][1]+data[i][2]-180))

        LENGTH_B_AFTER_PROJ = math.sqrt(LENGTH_B_PROJ_V*LENGTH_B_PROJ_V + LENGTH_B_y*LENGTH_B_y)
        LENGTH_C_AFTER_PROJ = math.sqrt(LENGTH_C_PROJ_V*LENGTH_C_PROJ_V + LENGTH_C_y*LENGTH_C_y)

        A_point_2_x.append(LENGTH_A_PROJ_H)

        B_point_2_x.append(LENGTH_A_PROJ_H + LENGTH_B_PROJ_H)
        B_point_2_y.append(LENGTH_B * math.sin(math.radians(data[i][1]-90)))
        # calculation of the C-part of the leg
        C_point_2_x.append(LENGTH_A_PROJ_H + LENGTH_B_PROJ_H + LENGTH_C_PROJ_H)
        C_point_2_y.append(-LENGTH_C * math.cos(math.radians(data[i][2]-180+data[i][1])) + B_point_2_y[i])

        # Horizontal view calculation:
        leg_len = LENGTH_A + LENGTH_B_PROJ_V + LENGTH_C_PROJ_V
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


def user_stop_fct():
    global user_stop
    user_stop = 1


def user_play_fct():
    global user_play
    user_play = 1


def user_pause_fct():
    global user_pause
    user_pause = 1


# Size (pixels):
MAIN_WIN_MIN_XSIZE = 480
MAIN_WIN_MIN_YSIZE = 360

# State variables
user_stop = 0
user_play = 0

print(math.degrees(math.asin(math.sin(math.radians(60)))))

# --------------------------------------------------------------------------------------------------- #
# Reading data from files:
data_angle_fl = read_data(ANGLE_FOLDER_PATH+ANGLE_FILE_FL)
data_angle_fr = read_data(ANGLE_FOLDER_PATH+ANGLE_FILE_FR)
data_angle_rl = read_data(ANGLE_FOLDER_PATH+ANGLE_FILE_RL)
data_angle_rr = read_data(ANGLE_FOLDER_PATH+ANGLE_FILE_RR)

line_points_fl = compute_lines(data_angle_fl)
line_points_fr = compute_lines(data_angle_fr)
line_points_rl = compute_lines(data_angle_rl)
line_points_rr = compute_lines(data_angle_rr)

line_points = [line_points_fl, line_points_fr, line_points_rl, line_points_rr]
# --------------------------------------------------------------------------------------------------- #

# --------------------------------------------------------------------------------------------------- #
# Settings the main window
main_win = tk.Tk()
main_win.title("2D leg animation")
main_win.minsize(MAIN_WIN_MIN_XSIZE, MAIN_WIN_MIN_YSIZE)
main_win.config(bg=BG_COLOR)
# --------------------------------------------------------------------------------------------------- #

# --------------------------------------------------------------------------------------------------- #
# Setting the title frame:
label_title = tk.Label(main_win, text='CrawlBot leg position simulator', font=(MAIN_FONT, 20), bg=BG_COLOR, fg=FG_COLOR)
label_title.grid(column=0, row=0, columnspan=2, sticky='ewns')
# --------------------------------------------------------------------------------------------------- #

# --------------------------------------------------------------------------------------------------- #
# Setting the UI frame
draw_frame = tk.Frame(main_win, bg=BG_COLOR)
draw_frame.grid(column=0, row=1)

# Setting the Canvas that wil host the drawing
frame_FL = tk.Frame(draw_frame, bg=BG_COLOR)
frame_FL.grid(row=0, column=0)
label_FL = tk.Label(frame_FL, text='Front left leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_FL.grid(row=0, column=0)
draw_canvas_fl = tk.Canvas(frame_FL, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_fl.grid(row=1, column=0)

frame_FR = tk.Frame(draw_frame, bg=BG_COLOR)
frame_FR.grid(row=0, column=1, padx=PADX_DRAW, pady=PADY_DRAW)
label_FR = tk.Label(frame_FR, text='Front right leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_FR.grid(row=0, column=0)
draw_canvas_fr = tk.Canvas(frame_FR, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_fr.grid(row=1, column=0)

frame_RL = tk.Frame(draw_frame, bg=BG_COLOR)
frame_RL.grid(row=1, column=0)
label_RL = tk.Label(frame_RL, text='Rear left leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_RL.grid(row=0, column=0)
draw_canvas_rl = tk.Canvas(frame_RL, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_rl.grid(row=1, column=0)

frame_RR = tk.Frame(draw_frame, bg=BG_COLOR)
frame_RR.grid(row=1, column=1)
label_RR = tk.Label(frame_RR, text='Rear right leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_RR.grid(row=0, column=0)
draw_canvas_rr = tk.Canvas(frame_RR, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_rr.grid(row=1, column=0)

draw_canvas = [draw_canvas_fl, draw_canvas_fr, draw_canvas_rl, draw_canvas_rr]


draw_frame_H = tk.Frame(main_win, bg=BG_COLOR)
draw_frame_H.grid(row=1, column=1)

# Setting the Canvas that will host the drawing
frame_FL_H = tk.Frame(draw_frame_H, bg=BG_COLOR)
frame_FL_H.grid(row=0, column=0)
label_FL_H = tk.Label(frame_FL_H, text='Front left leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_FL_H.grid(row=0, column=0)
draw_canvas_fl_H = tk.Canvas(frame_FL_H, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_fl_H.grid(row=1, column=0)

frame_FR_H = tk.Frame(draw_frame_H, bg=BG_COLOR)
frame_FR_H.grid(row=0, column=1, padx=PADX_DRAW, pady=PADY_DRAW)
label_FR_H = tk.Label(frame_FR_H, text='Front right leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_FR_H.grid(row=0, column=0)
draw_canvas_fr_H = tk.Canvas(frame_FR_H, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_fr_H.grid(row=1, column=0)

frame_RL_H = tk.Frame(draw_frame_H, bg=BG_COLOR)
frame_RL_H.grid(row=1, column=0)
label_RL_H = tk.Label(frame_RL_H, text='Rear left leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_RL_H.grid(row=0, column=0)
draw_canvas_rl_H = tk.Canvas(frame_RL_H, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_rl_H.grid(row=1, column=0)

frame_RR_H = tk.Frame(draw_frame_H, bg=BG_COLOR)
frame_RR_H.grid(row=1, column=1)
label_RR_H = tk.Label(frame_RR_H, text='Rear right leg', font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
label_RR_H.grid(row=0, column=0)
draw_canvas_rr_H = tk.Canvas(frame_RR_H, height=DRAW_WIN_YSIZE, width=DRAW_WIN_XSIZE, bg='white', highlightthickness=1, highlightbackground=FG_COLOR)
draw_canvas_rr_H.grid(row=1, column=0)

draw_canvas_H = [draw_canvas_fl_H, draw_canvas_fr_H, draw_canvas_rl_H, draw_canvas_rr_H]
# --------------------------------------------------------------------------------------------------- #

# --------------------------------------------------------------------------------------------------- #
# Setting the Simulator command frame:
command_frame = tk.Frame(main_win, bg=BG_COLOR)
command_frame.grid(column=2, row=1, sticky='new')

# adding a stop button to the command:
play_animation = tk.Button(command_frame, text='PLAY', width=WIDTH_BUTTON, bg=FG_COLOR, fg='white', command=user_play_fct)
play_animation.grid(column=0, row=0, padx=PADX_BUTT, pady=PADY_BUTT)

pause_animation = tk.Button(command_frame, text='PAUSE', width=WIDTH_BUTTON, bg=FG_COLOR, fg='white', command=user_pause_fct)
pause_animation.grid(column=0, row=1, padx=PADX_BUTT, pady=PADY_BUTT)

stop_animation = tk.Button(command_frame, text='STOP', width=WIDTH_BUTTON, bg=FG_COLOR, fg='white', command=user_stop_fct)
stop_animation.grid(column=0, row=2, padx=PADX_BUTT, pady=PADY_BUTT)
# --------------------------------------------------------------------------------------------------- #

# --------------------------------------------------------------------------------------------------- #
# TESTS:

# --------------------------------------------------------------------------------------------------- #

# Opening the window
while True:
    main_win.update_idletasks()
    main_win.update()
    if user_play == 1:
        draw_leg(draw_canvas, draw_canvas_H, line_points)
        user_play = 0

    if user_stop == 1:
        for n in range(len(draw_canvas)):
            draw_canvas[n].delete('all')
            draw_canvas_H[n].delete('all')
            user_stop = 0
