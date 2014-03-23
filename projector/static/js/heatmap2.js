// the scales are declared out here as "globals" so that
// we can access them in handleHeatMapMouseMove
var xScale = null,
    yScale = null;


/*
 
 */
function handleHeatMapMouseMove(event, representationOptions, onFinish) {
    var rect = $("#heatmapcanvas")[0].getBoundingClientRect();
    var xx = xScale.invert(event.clientX - rect.left);
    var yy = yScale.invert(event.clientY - rect.top);

    $.getJSON('/xy', {
        x: xx,
        y: yy
    }, function(ret) {
        var numAtoms = ret.x.length;
        for (var i = 0; i < numAtoms; i++) {
            glmol.atoms[i + 1].x = ret.x[i];
            glmol.atoms[i + 1].y = ret.y[i];
            glmol.atoms[i + 1].z = ret.z[i];
        }
        glmol.rebuildScene(representationOptions);
        glmol.show();
    }).done(onFinish);
}

var createHeatmap = function(data) {
    var heatmap = data.heatmap,
        extent = data.extent;
    var dx = heatmap[0].length,
        dy = heatmap.length;

    var containerWidth = $("#heatmapContainer").width(),
        containerHeight = $("#heatmapContainer").height();
            
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = containerWidth - margin.left - margin.right,
        height = containerHeight - margin.top - margin.bottom;


    xScale = d3.scale.linear()
        .domain([extent.xmin, extent.xmax])
        .range([0, width]);

    yScale = d3.scale.linear()
        .domain([extent.ymin, data.extent.ymax])
        .range([height, 0]);

    var color = d3.scale.linear()
        .domain([0, data.vmax / 20.0])
        .range(colorbrewer.RdBu[9]);

    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom")
        .ticks(10);

    var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left")
        .ticks(10);

    var svg = d3.select("#heatmapsvg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(" + margin.left + "," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + (margin.left - 2) + ", 0)")
        .call(yAxis);


    d3.select("#heatmapcanvas")
        .attr("width", dx)
        .attr("height", dy)
        .style("position", "relative")
        .style("left", margin.left)
        .style("width", width + "px")
        .style("height", height + "px")
        .call(drawImage);

    // Compute the pixel colors; scaled by CSS.

    function drawImage(canvas) {
        var context = canvas.node().getContext("2d"),
            image = context.createImageData(dx, dy);

        for (var y = 0, p = -1; y < dy; ++y) {
            for (var x = 0; x < dx; ++x) {
                var c = d3.rgb(color(heatmap[y][x]));
                image.data[++p] = c.r;
                image.data[++p] = c.g;
                image.data[++p] = c.b;
                image.data[++p] = 255;
            }
        }

        context.putImageData(image, 0, 0);
    }
};
