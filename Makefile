all: pdf image150 image300

pdf:
	ps2pdf dump_data.eps dump_data.pdf

image150:
	convert -density 150 dump_data.pdf -quality 90 image150.jpg

image300:
	convert -density 300 dump_data.pdf -quality 90 image300.jpg

dump_data:
	python3 dump_to_csv.py --type eps data2.p

