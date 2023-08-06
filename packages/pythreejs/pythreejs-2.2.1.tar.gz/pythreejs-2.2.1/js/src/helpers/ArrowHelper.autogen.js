//
// This file auto-generated with generate-wrappers.js
//

var _ = require('underscore');
var Promise = require('bluebird');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');
var serializers = require('../_base/serializers');

var BlackboxModel = require('../objects/Blackbox.js').BlackboxModel;


var ArrowHelperModel = BlackboxModel.extend({

    defaults: function() {
        return _.extend(BlackboxModel.prototype.defaults.call(this), {

            dir: [0,0,1],
            origin: [0,0,0],
            length: 1,
            color: "#ffff00",
            headLength: undefined,
            headWidth: undefined,
            type: "ArrowHelper",

        });
    },

    constructThreeObject: function() {

        var result = new THREE.ArrowHelper(
            this.convertVectorModelToThree(this.get('dir'), 'dir'),
            this.convertVectorModelToThree(this.get('origin'), 'origin'),
            this.convertFloatModelToThree(this.get('length'), 'length'),
            this.convertColorModelToThree(this.get('color'), 'color'),
            this.convertFloatModelToThree(this.get('headLength'), 'headLength'),
            this.convertFloatModelToThree(this.get('headWidth'), 'headWidth')
        );
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        BlackboxModel.prototype.createPropertiesArrays.call(this);

        this.props_created_by_three['type'] = true;
        this.props_created_by_three['matrixWorldNeedsUpdate'] = true;

        this.property_converters['dir'] = 'convertVector';
        this.property_converters['origin'] = 'convertVector';
        this.property_converters['length'] = 'convertFloat';
        this.property_converters['color'] = 'convertColor';
        this.property_converters['headLength'] = 'convertFloat';
        this.property_converters['headWidth'] = 'convertFloat';
        this.property_converters['type'] = null;

        this.property_assigners['dir'] = 'assignVector';
        this.property_assigners['origin'] = 'assignVector';

    },

}, {

    model_name: 'ArrowHelperModel',

    serializers: _.extend({
    },  BlackboxModel.serializers),
});

module.exports = {
    ArrowHelperModel: ArrowHelperModel,
};
