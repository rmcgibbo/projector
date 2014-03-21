var width = 700,
    height = 700;

var createHeatmap = function(data) {
    var heatmap = data.heatmap,
        extent = data.extent;
    var dx = heatmap[0].length,
        dy = heatmap.length;

  $("#heatmapContainer").width(width).height(height);

  var x = d3.scale.linear()
      .domain([extent.xmin, extent.xmax])
      .range([0, width]);

  var y = d3.scale.linear()
      .domain([extent.ymin, data.extent.ymax])
      .range([height, 0]);

  var color = d3.scale.linear()
      .domain([0, 1, 2, 4, 10])
      .range(["#0a0", "#6c0", "#ee0", "#eb4", "#eb9", "#fff"]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("top")
      .ticks(20);

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("right")
      .ticks(20);

  $("#heatmapsvg").mousemove(function( event ) {
     var rect = $("#heatmapcanvas")[0].getBoundingClientRect();
     var xx = x.invert(event.clientX - rect.left);
     var yy = y.invert(event.clientY - rect.top);
     console.log(xx, yy);
  });
      
  var svg = d3.select("#heatmapsvg")
      .attr("width", width)
      .attr("height", height);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

  d3.select("#heatmapcanvas")
      .attr("width", dx)
      .attr("height", dy)
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
