$(function() {
    glmol = new GLmol('proteinView', true);
    $.get("pdb", function(ret) {
      glmol.loadMoleculeStr(false, ret);
    });


    d3.json("heatmap.json", function(data) {
	// loadScatterPoints(points);
	createHeatmap(data);
    });
});
