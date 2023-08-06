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
     * @class NpTPageRender
     * @constructor
    */
    var NpTPageRender = function() {
        NumpyPageRender.call(this);
    };

    /**
     * NumpyPageRender 에서 상속
    */
    NpTPageRender.prototype = Object.create(NumpyPageRender.prototype);

    /**
    * NumpyPageRender 클래스의 pageRender 메소드 오버라이드
    */
    NpTPageRender.prototype.pageRender = function(tagSelector) {
        this.rootTagSelector = tagSelector || this.getMainPageSelector();

        this.renderPrefixCode();

        this.renderRequiredInputOutputContainer();
        this.renderCallVarBlock();
        
        /** 옵션 창 */
        this.renderAdditionalOptionContainer();
        this.renderReturnVarBlock();

        this.renderPostfixCode();
    }

    return NpTPageRender;
});
