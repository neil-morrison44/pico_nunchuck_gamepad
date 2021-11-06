$fa = 0.1;
$fs = 0.1;

$boardWidth = 44.65;  // this one
$boardDepth = 48.65;
$boardHeight = 1.7;

$bottomHeight = 10.8;

$nunBoardWidth = 25.53;
$nunBoardDepth = 17.8;
$nunBoardHeight = 1.6;

$qwiccDepth = 6.1;

module nunchuckConnector() {
    difference() {
        cube([ 12.25, 8.5, 7.3 ], true);
        translate([ 0, 0, (7.3 / 2) ]) cube([ 4.5, 8.6, 1.3 * 2 ], true);
    }
}

module towers() {
    for (x = [ -($boardWidth + 2) / 2, ($boardWidth + 2) / 2 ]) {
        for (y = [ -($boardDepth - 10) / 2, ($boardDepth - 10) / 2 ]) {
            translate([ x, y, 0 ]) children();
        }
    }
}

module bottom() {
    translate([ 0, 0, 2.9 ]) towers() difference() {
        cylinder($bottomHeight, 3, 3, true);
        translate([ 0, 0, 4 ]) cylinder(4, 1.25, 1.55, true);
    }

    translate([ 0, 0, 2.2 ]) difference() {
        cube([ $boardWidth + 8, $boardDepth, $bottomHeight + 1.5 ], true);
        translate([ 0, 0, 1.5 ]) cube(
            [ $boardWidth + 6, $boardDepth + 0.1, $bottomHeight + 1.5 ], true);
    }
}

module top() {
    towers() { cylinder($bottomHeight / 1.5, 1.25, 1.5, true); }

    intersection() {
        scale([ 1, 1, 0.3333 ]) rotate([ 90, 0, 0 ]) difference() {
            cylinder($boardDepth, ($boardWidth + 8) / 2, ($boardWidth + 8) / 2,
                     true);
            cylinder($boardDepth + 10, ($boardWidth + 4) / 2,
                     ($boardWidth + 4) / 2, true);
        }

        translate([ 0, 0, 50 ])
            cube([ $boardDepth + 10, $boardWidth + 10, 100 ], true);
    }
    translate([ -20, 5, 5.5 ])
        cube([ $nunBoardDepth / 2, $nunBoardWidth, 5 ], true);
}

module nunchuckMount() {
    translate([ 0, 5, 0 ]) {
        cube([ $nunBoardWidth, $nunBoardDepth, $nunBoardHeight ], true);
        difference() {
            cube([ $nunBoardWidth, $qwiccDepth, $nunBoardHeight + 4 ], true);
            cube(
                [ $nunBoardWidth - 10, $qwiccDepth + 10, $nunBoardHeight + 10 ],
                true);
        }
    }
    nunchuckConnector();
}

module board() {
    hull() {
        cube([ $boardWidth, $boardDepth, $boardHeight ], true);
        cube([ $boardWidth * 0.9, $boardDepth * 0.9, $boardHeight * 1.5 ],
             true);
    }
}

difference() {
    bottom();
    board();
}

translate([ 0, 0, 10 ]) difference() {
    top();

    translate([ -22.5, 5.1, 3.5 ]) rotate([ 0, 0, -90 ]) nunchuckMount();
}
