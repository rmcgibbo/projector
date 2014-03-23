$(function() {
    glmol = new GLmol('proteinView', true);
    $.get("pdb", function(ret) {
      glmol.loadMoleculeStr(false, ret);

      var representationOptions = angular.element($('#ProteinViewController'))
          .scope().p.getRepresentationOptions();
      glmol.rebuildScene(representationOptions);
      glmol.show();
    });

    $.getJSON("heatmap.json", function(data) {
        createHeatmap(data);
    });
});
