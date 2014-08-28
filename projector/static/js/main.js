$(function() {
    glmol = new GLmol('proteinView', true);
    $.getJSON("pdb", function(ret) {
      glmol.loadMoleculeStr(false, ret.pdbstring);
      glmol.assignSecondary(ret.helices, ret.sheets);

      var representationOptions = angular.element($('#ProteinViewController'))
          .scope().p.getRepresentationOptions();
      glmol.rebuildScene(representationOptions);
      glmol.show();
    });

    $.getJSON("heatmap.json", function(data) {
        createHeatmap(data);
    });
});
