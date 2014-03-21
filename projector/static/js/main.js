$(function() {
    glmol = new GLmol('proteinView', true);
    $.get("pdb", function(ret) {
      glmol.loadMoleculeStr(false, ret);
//      glmol.redrawScene(true);
//      glmol.show();
    });


    $.getJSON("heatmap.json", function(data) {
        // loadScatterPoints(points);
        createHeatmap(data);
    });
});
