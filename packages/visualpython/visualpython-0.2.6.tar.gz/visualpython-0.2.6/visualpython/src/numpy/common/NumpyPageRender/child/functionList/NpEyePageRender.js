define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    // numpy 패키지를 위한 라이브러리import 
 
    , 'nbextensions/visualpython/src/numpy/common/NumpyPageRender/parent/NumpyPageRender'
], function(requirejs, vpCommon, 
            NumpyPageRender ) {

    "use strict";
    /**
     * @class NpEyePageRender
     * @constructor
    */
    var NpEyePageRender = function(numpyOptionObj) {
        const { numpyDtypeArray, numpyIndexValueArray, numpyEnumRenderEditorFuncType } = numpyOptionObj;
        this.numpyDtypeArray = numpyDtypeArray;
        this.numpyIndexValueArray = numpyIndexValueArray;
        this.numpyEnumRenderEditorFuncType = numpyEnumRenderEditorFuncType;
        NumpyPageRender.call(this);
    };

    /**
     * NumpyPageRender 에서 상속
    */
    NpEyePageRender.prototype = Object.create(NumpyPageRender.prototype);

    /**
    * NumpyPageRender 클래스의 pageRender 메소드 오버라이드
    */
    NpEyePageRender.prototype.pageRender = function(tagSelector) {
        const { PARAM_INPUT_EDITOR_TYPE } = this.numpyEnumRenderEditorFuncType;

        this.rootTagSelector = tagSelector || this.getMainPageSelector();

        var numpyPageRenderThis = this;
        var numpyStateGenerator = numpyPageRenderThis.getStateGenerator();
        // state의 paramData 객체의 키값을 string 배열로 리턴
        var stateParamNameStrArray = Object.keys(numpyStateGenerator.getState("paramData"));

        var bindFuncData = {
            numpyPageRenderThis: numpyPageRenderThis
            , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
            , stateParamNameStrOrStrArray: [stateParamNameStrArray[0]] 
            , paramNameStrArray: ["숫자 파라미터"]
            , placeHolderArray: ["숫자 입력"]
        }

        this.renderPrefixCode();

        this.renderRequiredInputOutputContainer();
        this.renderInputIndexValueBlock("Input Parameter Int Number", bindFuncData);
        
        /** 옵션 창 */
        this.renderAdditionalOptionContainer();
        this.renderSelectIndexValueBlock("Input K index", "paramKIndex");
        this.renderDtypeBlock();
        this.renderReturnVarBlock();

        this.renderPostfixCode();
    }

    return NpEyePageRender;
});
