function download(query) {
   var baseURL = '';
   var uri = "http://www.pdb.org/pdb/files/" + query + ".pdb";

   // $('#loading').show();
   $.get(uri, function(ret) {
       console.log(ret);

//      $("#glmol01_src").val(ret);
//      glmol.loadMolecule();
      glmol.loadMoleculeStr(false, ret);
      //$('#loading').hide();
   });
}
