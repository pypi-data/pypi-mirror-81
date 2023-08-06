define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    // numpy 패키지를 위한 라이브러리import 
    , 'nbextensions/visualpython/src/common/constant_numpy'
    , 'nbextensions/visualpython/src/numpy/common/NumpyPageRender/parent/NumpyPageRender'
], function( requirejs, vpCommon, 
             vpNumpyConst, NumpyPageRender ) {

    "use strict";
    /**
     * @class NpCopyPageRender
     * @constructor
    */
    var NpCopyPageRender = function() {
        NumpyPageRender.call(this);
    };

    /**
     * NumpyPageRender 에서 상속
    */
    NpCopyPageRender.prototype = Object.create(NumpyPageRender.prototype);

    /**
    * NumpyPageRender 클래스의 pageRender 메소드 오버라이드
    */
    NpCopyPageRender.prototype.pageRender = function(tagSelector) {
        this.rootTagSelector = tagSelector || this.getMainPageSelector();

        this.renderPrefixCode();

        this.renderRequiredInputOutputContainer();
        this.renderParamVarBlock();
        
        this.renderAdditionalOptionContainer();
        this.renderReturnVarBlock();
        
        this.renderPostfixCode();
    }

    return NpCopyPageRender;
});
