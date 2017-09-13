from LibDraw import LibDraw

# demo file for LibDraw API, L. Gonnord for CAP, aug 2017.


def main():
    myg = LibDraw(450, 450, True)  # True for debug mode
    # add two lines
    myg.addLine(10, 0, 450, 300)
    myg.addLine(0, 100, 300, 100)
    # at the end, show
    myg.showPicture()

if __name__ == '__main__':
    main()
