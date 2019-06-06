import pickle
import logging
import argparse                                                                                                         
from os.path import isfile


parser = argparse.ArgumentParser(
    formatter_class = argparse.RawDescriptionHelpFormatter,
    description = "dump scrap data to a CSV or SVG",
    epilog = "Example:\n$ python3 dump_to_csv.py data2.p"
                )

parser.add_argument("data_file", help="data file name")
parser.add_argument("--debug", action='store_true', help="DEBUG level of logging")
parser.add_argument("--type",  default='csv', type=str, help="the type of the output, csv, svg or eps")
parser.add_argument("--load",  action='store_true', help="dump load itself, not the corresponding colours")
parser.add_argument('-o', '--output-filename', type=str, default='dump_data', help="output filename")
parser.add_argument("--limit-y",  type=str, help="limit the year in the record")
parser.add_argument("--limit-m",  type=str, help="limit the month in the record")
parser.add_argument("--limit-yr", type=str, help="limit the year of the record")
parser.add_argument("--limit-mr", type=str, help="limit the month of the record")


args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

assert args.type in ('csv', 'svg', 'eps')
assert isfile(args.data_file)
output_filename = args.output_filename + '.' + args.type
assert not isfile(output_filename)

with open(args.data_file, 'rb') as f:
    data = pickle.load(f)

logging.debug(type(data))
logging.debug(len(data))

'''
data = {record_tuple (Y, M, WEEK, WD, H):
{(year, month, week, day): load}

long format to csv:
YR,MR,WR,DR,HR,y,m,w,d,load
'''

rgb_colors = {0: (0,0,0),
    1: (76, 153, 0),
    2: (220, 220, 0),
    3: (255, 128, 0),
    4: (255, 51, 51),
    5: (153, 0, 0)}

rgb_colors_str = {col: '#%02X%02X%02X' % cols for col, cols in rgb_colors.items()}

csv_header = 'YR,MR,WR,DR,HR,y,m,w,d,load\n'
csv_ending = '\n'

svg_header = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 4000 2000">
    <rect id="r"
        x="100" y="20"
        width="4" height="1"
        fill="#29e" />

"""
svg_ending = '</svg>\n'

eps_header = """%!

<</PageSize [1000 800] >> setpagedevice

/l {
newpath
setrgbcolor
moveto
0 1 rlineto
4 0 rlineto
0 -1 rlineto
closepath
fill
} def

/l0 {0 0 0 l} def
/l1 {0.297 0.598 0 l} def
/l2 {0.859 0.859 0 l} def
/l3 {0.996 0.5   0 l} def
/l4 {0.996 0.199 0.199 l} def
/l5 {0.598 0     0 l} def


% draw background color
newpath
0.008 0.035 0.055 setrgbcolor
0 0 moveto
0  800 rlineto
1000 0 rlineto
0 -800 rlineto
closepath
fill

% the scale of the plot (year, month etc -> x, y)
0.2 0.2 scale

% the legend
1 1 1 setrgbcolor
%0 0 movto
%(2018) show
/text72 {
/Helvetica 72 selectfont
moveto
show} def

/text54 {
/Helvetica 54 selectfont
moveto
show} def

/text36 {
/Helvetica 36 selectfont
moveto
show} def

/text1 {
/Helvetica 1 selectfont
moveto
show} def

(The history of the Hotel reservations in CERN in 2018-2019) 100 3800    text72
(Recorded by a scrapper built in Python3 with beautifulsoup4, selenium and standard library, running as a cron job on linux Lubuntu.) 100 3728    text36

(The occupancy of the Hotel was recorded from the website for reservations) 100 3584    text72
(four times a day at: 8am, 12am, 18pm, 23pm.) 100 3512    text72

(Vertical axis is the time of recording, horizontal axis is the time of reservations.) 100 3368    text72
(Years, months and weeks are spaced out for readability.) 100 3296    text72

(For example, a zoom into one day with 4 records:)        100 3152    text72

% use live example:

% right justified text
% from http://www.cs.utsa.edu/~wagner/CS3723/postrecs/justify/just.html
/right-justify { % stack: string x y
    /y exch def % handle top of stack: x of the line to justify against, y coord of line
    /x exch def
    dup stringwidth pop % stack: width string
    x y moveto % move to right end
    neg 0 rmoveto % move to left end
    show % print string
} def

% the labels for the live example
/Helvetica 1 selectfont

%1524 1290 l2
100 3008 translate
20 20 scale

( 8) -1 0  right-justify
(12) -1 1  right-justify
(18) -1 2  right-justify
(23) -1 3  right-justify

0     0 l5
4     0 l4
8     0 l3
16    0 l3
20    0 l4
24    0 l4
28    0 l4
32    0 l4
36    0 l4
40    0 l3
48    0 l3
52    0 l4
56    0 l5
60    0 l5
64    0 l5
68    0 l4
72    0 l4
80    0 l3
84    0 l4
88    0 l5
92    0 l5
96    0 l5
100   0 l4
104   0 l3
112   0 l3

0   1 l5
4   1 l4
8   1 l3
16  1 l3
20  1 l4
24  1 l4
28  1 l4
32  1 l4
36  1 l4
40  1 l3
48  1 l3
52  1 l3
56  1 l5
60  1 l5
64  1 l5
68  1 l4
72  1 l4
80  1 l3
84  1 l4
88  1 l5
92  1 l5
96  1 l5
100 1 l4
104 1 l3
112 1 l3

0   2 l5
4   2 l5
8   2 l3
16  2 l3
20  2 l4
24  2 l4
28  2 l4
32  2 l4
36  2 l4
40  2 l3
48  2 l3
52  2 l3
56  2 l5
60  2 l5
64  2 l5
68  2 l4
72  2 l4
80  2 l3
84  2 l3
88  2 l5
92  2 l5
96  2 l5
100 2 l4
104 2 l3
112 2 l3

0   3 l5
4   3 l5
8   3 l3
16  3 l3
20  3 l4
24  3 l4
28  3 l4
32  3 l4
36  3 l4
40  3 l3
48  3 l3
52  3 l3
56  3 l5
60  3 l5
64  3 l5
68  3 l4
72  3 l4
80  3 l3
84  3 l3
88  3 l5
92  3 l5
96  3 l5
100 3 l4
104 3 l3
112 3 l3

%4 4 scale
%-250 243 translate

0.05 0.05 scale
-100  -3008 translate

% color legend
1 1 1 setrgbcolor
(The color codes correspond to the occupancy level on the website:) 100 2856    text72

% larger pixels
/lll {
newpath
setrgbcolor
moveto
0 72 rlineto
288 0 rlineto
0 -72 rlineto
closepath
fill
} def

/lll0 {0 0 0 lll} def
/lll1 {0.297 0.598 0 lll} def
/lll2 {0.859 0.859 0 lll} def
/lll3 {0.996 0.5   0 lll} def
/lll4 {0.996 0.199 0.199 lll} def
/lll5 {0.598 0     0 lll} def

100 2712 lll1 1 1 1 setrgbcolor (up to 70%) 450 2712    text72
100 2640 lll2 1 1 1 setrgbcolor (70% - 85%) 450 2640    text72
100 2568 lll3 1 1 1 setrgbcolor (85% - 95%) 450 2568    text72
100 2496 lll4 1 1 1 setrgbcolor (>95%) 450 2496    text72
100 2424 lll5 1 1 1 setrgbcolor (full) 450 2424    text72

% labels
4 setlinewidth

/line {
newpath
setrgbcolor
moveto
rlineto
stroke
} def
%0  96  0    0  1 1 1 line

% leave space for legend on the bottom
0 128 translate

1 1 1 setrgbcolor
% allign to the plot -- the Y starts from 39
0 39 translate
(2018) 0    0    text72
% shift the month names closer to the plot
70 0 translate
(Feb)  200  200  text72
(Mar)  400  400  text72
(Apr)  600  600  text72
(May)  800  800  text72
(Jun)  1000 1000 text72
(Jul)  1200 1200 text72
(Aug)  1400 1400 text72
(Sep)  1600 1600 text72
(Oct)  1800 1800 text72
(Nov)  2000 2000 text72
(Dec)  2200 2200 text72
-70 0 translate

(2019) 2600 2600 text72
70 0 translate
(Feb)  2800 2800 text72
(Mar)  3000 3000 text72
(Apr)  3200 3200 text72
(May)  3400 3400 text72
(Jun)  3600 3600 text72
(Jul)  3800 3800 text72
%(Aug)  4000 4000 text72
%(Sep)  4200 4200 text72
%(Oct)  4400 4400 text72
%(Nov)  4600 4600 text72
%(Dec)  4800 4800 text72
-70 0 translate

0 -39 translate

% shift the plot up from the explanatory labels
200 0 translate

% mark some common hollidays
% relative_move from_starting_point color line
/Helvetica 54 selectfont
1 setlinewidth
0 288 0 54   1 1 1 line
(New)  -4 288  right-justify
(Year) -4 234  right-justify

0 288 632 644   1 1 1 line
(Easter)  628 920  right-justify

0 216 2336 2370   1 1 1 line
(Christmas)  2332 2496  right-justify

0 504        1236 1236  1 1 1 line
(High Load,) 1232 1644  right-justify
(Summer)     1232 1590  right-justify
(Students)   1232 1536  right-justify

0 336 2600 2612   1 1 1 line
(New)  2596 2888  right-justify
(Year) 2596 2834  right-justify

%

2 setlinewidth
32 0  0 -16  1 1 1 line
(week)  -112 -16 text36

200 0  0 -48  1 1 1 line
(month) -112 -48 text36

2366 0  0 -80  1 1 1 line
(year)  -112 -80 text36

"""

eps_ending = '\n'

headers = {
'csv': csv_header,
'svg': svg_header,
'eps': eps_header
}

endings = {
'csv': csv_ending,
'svg': svg_ending,
'eps': eps_ending
}


# point_x1 = norm(((p[:,5] - 2015)*650 + p[:,6]*50 + p[:,7]*8 + p[:,8])*4)
# point_y1 = norm(((p[:,0] - 2015)*650 + p[:,1]*50 + p[:,2]*9 + p[:,3])*4 + p[:,4])

#norm_scale = 1 / 200.
#def norm(v_px):
#    return (v_px - 5500) * norm_scale

norm_year  = 2018 # 2015
norm_month = 1 # 0

def recorded_date_to_x(Y, M, W, D):
    return ((Y - norm_year)*650 + (M - norm_month)*50 + W*8 + D)*4

def record_time_to_y(YR, MR, WR, DR, HR):
    return ((YR - norm_year)*650 + (MR - norm_month)*50 + WR*9 + DR)*4 + HR # //6 -- already divided in data!?

y_min, y_max = None, None
x_min, x_max = None, None

all_y  = set()
all_hr = set()

with open(output_filename, 'w') as f:
    if args.type in headers:
        # write other definitions
        f.write(headers[args.type])

    for (YR,MR,WR,DR,HR), record in data.items():
        for (Y,M,W,D), load in record.items():
            if YR < 2018: continue

            if args.type == 'svg':
                if Y < 2018: continue
                svg_element = '<use xlink:href="#r" x="{x}" y="{y}" fill="{fill}"/>\n'
                x = recorded_date_to_x(Y, M, W, D)
                y = record_time_to_y(YR, MR, WR, DR, HR)
                col = rgb_colors_str[load]
                f.write(svg_element.format(x=x, y=y, fill=col))

            elif args.type == 'eps':
                if Y < 2018: continue
                if args.limit_y:
                    if Y != int(args.limit_y): continue
                if args.limit_yr:
                    if YR != int(args.limit_yr): continue
                if args.limit_m:
                    if M != int(args.limit_m): continue
                if args.limit_mr:
                    if MR != int(args.limit_mr): continue

                eps_element = '{x} {y} l{load}\n'
                #eps_element = '{y} {x} l{load}\n'
                x = recorded_date_to_x(Y, M, W, D)
                y = record_time_to_y(YR, MR, WR, DR, HR)
                f.write(eps_element.format(x=x, y=y, load=load))

                all_y.add(y)
                all_hr.add(HR)

                if YR == 2019 and MR == 5:
                    #print("yay!")
                    pass

                if not x_min or x<x_min: x_min = x
                if not x_max or x>x_max: x_max = x
                if not y_min or y<y_min: y_min = y
                if not y_max or y>y_max: y_max = y

            else:
              if args.load:
                f.write('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n' % (YR,MR,WR,DR,HR, Y,M,W,D, load))
              else:
                # convert load to color
                col = rgb_colors_str[load]
                f.write('%d,%d,%d,%d,%d,%d,%d,%d,%d,%s\n' % (YR,MR,WR,DR,HR, Y,M,W,D, col))
            # ggplot is crazy with colors, it cannot take them from a coloumn

    if args.type in endings:
        f.write(endings[args.type])

print(sorted(all_y)[:10])
print(sorted(all_y)[-10:])
print(sorted(all_hr)[-10:])

if x_min:
    print("x", x_min, x_max)
    print("y", y_min, y_max)

