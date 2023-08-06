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
     * @class NumpyIndexingPageRender
     * @constructor
    */
    var NumpyIndexingPageRender = function(numpyOptionObj) {
        const { numpyDtypeArray, numpyAxisArray, numpyIndexValueArray, numpyEnumRenderEditorFuncType, 
            numpyTrueFalseArray, numpyRavelOrderArray } = numpyOptionObj;
        this.numpyDtypeArray = numpyDtypeArray;
        this.numpyAxisArray = numpyAxisArray;
        this.numpyIndexValueArray = numpyIndexValueArray;
        this.numpyEnumRenderEditorFuncType = numpyEnumRenderEditorFuncType;
        this.numpyTrueFalseArray = numpyTrueFalseArray
        this.numpyRavelOrderArray = numpyRavelOrderArray;
    };

    /**
     * NumpyPageRender 에서 상속
    */
    NumpyIndexingPageRender.prototype = Object.create(NumpyPageRender.prototype);

    /**
    * NumpyPageRender 클래스의 pageRender 메소드 오버라이드

    */
    NumpyIndexingPageRender.prototype.pageRender = function(tagSelector) {
        this.rootTagSelector = tagSelector || "";

        var numpyPageRenderThis = this;
        const { PARAM_ONE_ARRAY_EDITOR_TYPE, PARAM_TWO_ARRAY_EDITOR_TYPE,
                PARAM_THREE_ARRAY_EDITOR_TYPE, PARAM_INPUT_EDITOR_TYPE, PARAM_ONE_ARRAY_INDEX_N_EDITOR_TYPE,
                PARAM_INDEXING_EDITOR_TYPE } = this.numpyEnumRenderEditorFuncType;
        // state의 paramData 객체의 키값을 string 배열로 리턴
        var stateParamNameStrArray = Object.keys(this.numpyStateGenerator.getState("paramData"));
        var tabTitle = "Indexing Array";
        var tabBlockArray = [
            {
                tabNumber: 1
                , btnText: "Indexing 2D array"
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: [stateParamNameStrArray[0],  stateParamNameStrArray[1]]
                }
            },
            {
                tabNumber: 2
                , btnText: "Indexing 3D array"
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: [ stateParamNameStrArray[2], stateParamNameStrArray[3],
                                                     stateParamNameStrArray[4], stateParamNameStrArray[5]]
                }
            },
            {
                tabNumber: 3
                , btnText: "Indexing ND array"
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_INDEXING_EDITOR_TYPE
                    , stateParamNameStrOrStrArray:  stateParamNameStrArray[6]
                }
            }
        ];
        var tabDataObj = {
            tabTitle,
            tabBlockArray
        }
        this.renderRequiredInputOutputContainer();
        this.renderParamTabBlock(tabDataObj);
        this.renderCallVarBlock();
        
        this.renderReturnVarBlock();

    }

    return NumpyIndexingPageRender;
});