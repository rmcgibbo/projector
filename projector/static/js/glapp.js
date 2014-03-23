angular.module('glapp', [])
  .controller('ProteinViewController', function() {
    this.colorOptions = [
      { name: 'Spectrum', value: 'chainbow' }, 
      { name: 'Chain', value: 'chain' }, 
      { name: 'Secondary Structure', value: 'ss' },
      { name: 'Polar/nonpolar', value: 'polarity' }
    ];
    this.mainChainOptions = [
        {name: 'Thick Ribbon', value: 'thickRibbon'},
        {name: 'Thin Ribbon', value: 'ribbon'},
        {name: 'Strand', value: 'strand'},
        {name: 'Cylinder & Plate', value: 'cylinderHelix'},
        {name: 'C alpha trace', value: 'chain'},
        {name: 'Bonds (everything)', value: 'bonds'}
    ];
    this.sideChainsOptions = [
        {name: 'Hide', value: 'hide' },
        {name: 'Line', value: 'line' },
    ];
    this.nonbondedAtomsOptions = [
        {name: 'None', value: 'none' },
        {name: 'Spheres', value: 'spheres'},
        {name: 'Stars', value: 'stars'}
    ];
    this.heteroAtomsOptions = [
        {name: 'Spheres', value: 'sphere' },
        {name: 'Spheres', value: 'ballAndStick'},
        {name: 'Stars', value: 'ballAndStick2'},
        {name: 'Icosahedrons', value: 'icosahedron'},
        {name: 'Line', value: 'line'}
    ];
    this.backgroundColorOptions = [
        {name: 'White', value: 0xFFFFFF },
        {name: 'Black', value: 0x000000 },
    ];
    this.projectionOptions = [
        {name: 'Orthoscopic', value: 'orthoscopic'},
        {name: 'Perspective', value: 'perspective' },
    ];
    this.heatmapIsPaused = false;

    
    // set default values
    this.form = {
        // color: this.colorOptions[0].value,
        color: 'chainbow',
        mainChain: this.mainChainOptions[0].value,
        sideChains: this.sideChainsOptions[0].value,
        nonbondedAtoms: this.nonbondedAtomsOptions[0].value,
        heteroAtoms: this.heteroAtomsOptions[0].value,
        backgroundColor: this.backgroundColorOptions[0].value,
        projection: this.projectionOptions[0].value,
    };
    
    this.getRepresentationOptions = function getRepresentationOptions() {
        return this.form;
    }
    
    this.update = function update() {
        console.log(this.form, glmol);
        glmol.rebuildScene(this.form);
        glmol.show();
    };
    
    this.heatmapMouseMove = function heatmapMouseMove(event) {
        if (this.heatmapIsPaused == true) { return; }
        this.heatmapIsPaused = true;
        var controller = this;
        
        handleHeatMapMouseMove(event, this.form, function() {
            setTimeout(function() {
                controller.heatmapIsPaused = false;
            }, 100);
        });
    };
    
    this.logchange = function logchange() {
        console.log('change!');
    }
    
});
