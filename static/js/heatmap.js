var numRows = 30,
  numCols = 30,
  size = 400,
  showingScatter = true,
  scatterDirty = false,
  data = null,
  cells = null,
  glmol = null,
  color = d3.interpolateRgb("#0000ff", "#ff0000");

var getEmptyCells = function() {
    var emptyCells = [];
    for (var rowNum = 0; rowNum < numRows; rowNum++) {
        emptyCells.push([]);
        var row = emptyCells[emptyCells.length - 1];
        for (var colNum = 0; colNum < numCols; colNum++) {
            row.push({
                row: rowNum,
                col: colNum,
                density: 0,
                points: []
            });
        }
    }
    return emptyCells;
};

var clearCells = function() {
    for (var rowNum = 0; rowNum < numRows; rowNum++) {
        for (var colNum = 0; colNum < numCols; colNum++) {
            cells[rowNum][colNum].density = 0;
            cells[rowNum][colNum].points = [];
        }
    }
};

var loadScatterPoints = function(points) {
    console.log(points);
    var numPoints = points['x'].length;
    data = [];

    if (cells === null) {
        cells = getEmptyCells();
    }
    else {
        clearCells();
    }

    var minx = Math.min.apply(null, points['x']),
        miny = Math.min.apply(null, points['y']),
        maxx = Math.max.apply(null, points['x']),
        maxy = Math.max.apply(null, points['y']);

    var col, row, x, y;
    for (var i = 0; i < numPoints; i++) {
        x = points['x'][i]
        y = points['y'][i]
	col = Math.min(Math.floor((x - minx) / (maxx - minx) * numRows), numRows-1);
	row = Math.min(Math.floor((y - miny) / (maxy - miny) * numCols), numCols-1);

	console.log(row, col);
	
        data.push({
            x: (x - minx) / (maxx - minx) * size, 
            y: (y - miny) / (maxy - miny) * size,
            col: col,
            row: row,
            cell: cells[row][col],
            ind: i
        });
        cells[row][col].points.push(data[data.length - 1]);
    }
};


 
var onCellOver = function(cell, data) {
    if (data.points.length > 0) {
	console.log(data.points[0]);
	d3.json('/coordinates/' + data.points[0].ind, function(ret) {
	    numAtoms = ret['x'].length;
	    for (var i = 0; i < numAtoms; i++) {
		console.log('ret.x[i]', ret.x[i]);
		console.log('gmol atom i', glmol.atoms[i+1].x);
		glmol.atoms[i+1].x = ret.x[i];
		glmol.atoms[i+1].y = ret.y[i];
		glmol.atoms[i+1].z = ret.z[i];
	    }
	    console.log(ret);
	    glmol.rebuildScene(true);
	    glmol.show()
	});
    }

};

var onCellOut = function(cell, data) {
    // console.log('cellout');
};

var createHeatchart = function() {
    var min = 999;
    var max = -999;
    var l;

    for (var rowNum = 0; rowNum < cells.length; rowNum++) {
        for (var colNum = 0; colNum < numCols; colNum++) {
            l = cells[rowNum][colNum].points.length;

            if (l > max) {
                max = l;
            }
            if (l < min) {
                min = l;
            }
        }
    }

    var heatchart = d3.select("div#heatchart").append("svg:svg").attr("width", size).attr("height", size);

    heatchart.selectAll("g").data(cells).enter().append("svg:g").selectAll("rect").data(function(d) {
        return d;
    }).enter().append("svg:rect")
    .attr("x", function(d, i) { return d.col * (size / numCols); })
    .attr("y", function(d, i) { return d.row * (size / numRows); })
    .attr("width", size / numCols)
    .attr("height", size / numRows)
    .attr("fill", function(d, i) { return color((d.points.length - min) / (max - min)); })
    .on("mouseover", function(d) { onCellOver(this, d); })
    .on("mouseout", function(d) { onCellOut(this, d); });

};

var updateHeatchart = function() {
    var min = 999;
    var max = -999;
    var l;

    for (var rowNum = 0; rowNum < cells.length; rowNum++) {
        for (var colNum = 0; colNum < numCols; colNum++) {
            l = cells[rowNum][colNum].points.length;

            if (l > max) {
                max = l;
            }
            if (l < min) {
                min = l;
            }
        }
    }

    d3.select("div#heatchart").select("svg").selectAll("g").data(cells).selectAll("rect").data(function(d) {
        return d;
    }).attr("x", function(d, i) {
        return d.col * (size / numCols);
    }).attr("y", function(d, i) {
        return d.row * (size / numRows);
    }).attr("fill", function(d, i) {
        return color((d.points.length - min) / (max - min));
    }).attr("cell", function(d) {
        return "r" + d.row + "c" + d.col;
    }).on("mouseover", function(d) {
        onCellOver(this, d);
    }).on("mouseout", function(d) {
        onCellOut(this, d);
    });
};


$(function() {
    glmol = new GLmol('proteinView', true);
    $.get("pdb", function(ret) {
      glmol.loadMoleculeStr(false, ret);
    });


    d3.json("points.json", function(points) {
	loadScatterPoints(points);
	createHeatchart();
    });
});
