define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    // numpy 패키지를 위한 라이브러리import 
 
    , 'nbextensions/visualpython/src/numpy/common/NumpyPageRender/parent/NumpyPageRender'
], function(requirejs, vpCommon, 
            NumpyPageRender ) {

    "use strict";
    /**
     * @class NpLinalgInvPageRender
     * @constructor
    */
    var NpLinalgInvPageRender = function(numpyOptionObj) {
        const { numpyDtypeArray, numpyIndexValueArray, numpyEnumRenderEditorFuncType } = numpyOptionObj;
        this.numpyDtypeArray = numpyDtypeArray;
        this.numpyIndexValueArray = numpyIndexValueArray;
        this.numpyEnumRenderEditorFuncType = numpyEnumRenderEditorFuncType;
        NumpyPageRender.call(this);
    };

    /**
     * NumpyPageRender 에서 상속
    */
    NpLinalgInvPageRender.prototype = Object.create(NumpyPageRender.prototype);

    /**
    * NumpyPageRender 클래스의 pageRender 메소드 오버라이드
    */
    NpLinalgInvPageRender.prototype.pageRender = function(tagSelector) {
        this.rootTagSelector = tagSelector || this.getMainPageSelector();
        var numpyPageRenderThis = this;

        // state의 paramData 객체의 키값을 string 배열로 리턴
        var stateParamNameStrArray = Object.keys(this.numpyStateGenerator.getState("paramData"));
        var tabTitle = "Input Parameter";
        const { PARAM_TWO_ARRAY_EDITOR_TYPE,
                PARAM_INPUT_EDITOR_TYPE } = this.numpyEnumRenderEditorFuncType;
        var tabBlockArray = [
            {
                tabNumber: 1
                , btnText: "Param Variable"
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: [ stateParamNameStrArray[0]] 
                    , paramNameStrArray: ["변수"]
                    , placeHolderArray: ["변수 입력"]
                }
            },
            {
                tabNumber: 2
                , btnText: "2D Array"
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_TWO_ARRAY_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: stateParamNameStrArray[1]
                }
            }
        ];
        var tabDataObj = {
            tabTitle,
            tabBlockArray
        }
        this.renderPrefixCode();

        this.renderRequiredInputOutputContainer();
        this.renderParamTabBlock(tabDataObj);

        /** 옵션 창 */
        this.renderAdditionalOptionContainer();
        this.renderDtypeBlock();
        this.renderReturnVarBlock();

        this.renderPostfixCode();
    }

    return NpLinalgInvPageRender;
});
