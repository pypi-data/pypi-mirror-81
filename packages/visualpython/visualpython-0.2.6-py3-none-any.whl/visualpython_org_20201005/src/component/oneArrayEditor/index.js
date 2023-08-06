define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'

    //  
    , 'nbextensions/visualpython/src/component/api/componentConstApi'
    , 'nbextensions/visualpython/src/numpy/api/numpyStateApi'
    , './state'
], function (requirejs, $, vpCommon, vpConst, sb, vpFuncJS,
             componentConstApi, numpyStateApi, OneArrayEditorState ) {


    var sbCode = new sb.StringBuilder();
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "oneArrayEditor"
        , funcID : "JY901"  // TODO: ID 규칙 생성 필요
    }
    var vpFuncJS = new vpFuncJS.VpFuncJS(funcOptProp);
    var { controlToggleInput, closeParamArrayEditor } = componentConstApi;
    var { updateOneArrayIndexValueAndGetNewArray
          , deleteOneArrayIndexValueAndGetNewArray } = numpyStateApi;
    var oneArrayEditorState = new OneArrayEditorState();    

    var oneArrayLength = 0;

    // 로딩을 생성하는 함수
    // var renderLoadingBar = function() {
    //     vpCommon.renderLoadingBar();
    // }

    
    /** initEditor bindEventFunctions 함수는 
     * oneArrayEditor, twoArrayEditor, threeArrayEditor에서 다 동일한 이름의 함수입니다.*/

    /** initEditor 시작 함수
     * @param {this} numpyPageRendererThis 
     * @param {string} stateParamName 
     */

    var initEditor = function(numpyPageRendererThis, stateParamName) {
        controlToggleInput();
        oneArrayEditorState.setNumpyPageRendererThis(numpyPageRendererThis);
        renderParamOneArrayEditor(`.directoryComponent-container`,stateParamName);
    }

    /** 이벤트 바인딩 함수
     * @param {string} stateParamName
     * @param {string} tagSelector
     */
    var bindEventFunctions = function(stateParamName, tagSelector) {
        // oneArrayEditor 편집기를 닫았을때 실행되는 click 함수
        var numpyPageRendererThis =  oneArrayEditorState.getNumpyPageRendererThis();
        $('.directoryComponent-closedBtn').click(() => {
            closeParamArrayEditor(numpyPageRendererThis, tagSelector, stateParamName, 0);
        });
        $('.vp-numpy-arrayEditor-func-confirmBtn').click(() => {
            closeParamArrayEditor(numpyPageRendererThis, tagSelector, stateParamName, 0);
        });
    }

      
   /**
   * resetArrayEditor
   * @param {document} baseDom 
   */
    var resetArrayEditor = function(baseDom) {
        // 동적 랜더링할 태그에 css flex-column 설정
        baseDom.css("display","flex");
        baseDom.css("flexDirection","column");
        // 기존의 렌더링 태그들 리셋하고 아래 로직에서 다시 그림
        baseDom.empty()
    }

    /**
     * renderArrayEditorTitle
     * array 편집기 타이틀을 렌더링한다
     * @param {document} baseDom 
     * @param {string} tagSelector 
     * @param {string} stateParamName 
     */
    var renderArrayEditorTitle = function(baseDom, tagSelector, stateParamName) {
        var numpyPageRendererThis =  oneArrayEditorState.getNumpyPageRendererThis();
        var numpyStateGenerator = numpyPageRendererThis.numpyStateGenerator;
        var dom;

        oneArrayLength = numpyStateGenerator.getState(stateParamName).length;
        dom = $(`<div>
                    <div class="vp-numpy-style-flex-row-center"
                        style="font-size:20px;font-weight:700">
                        <span class="vp-multilang" data-caption-id="one_dimention_array_editor">
                        1D Array Editor
                        </span>
                    </div>
                    <div class="vp-numpy-style-flex-row-center" style="margin-bottom:5px;">
                        <div style="margin:0 5px;">
                            <span  class="vp-multilang" data-caption-id="length-kor">길이 : </span>
                            <input class="vp-numpy-input 
                                          vp-numpy-oneArrayEditor-length-input"
                               value="${oneArrayLength}" 
                               type="text"/>
                        </div>
                        <button class="vp-numpy-func_btn vp-numpy-oneArrayEditor-make-btn">생성</button>
                    </div>
                </div>`);
        baseDom.append(dom);
        $(`.vp-numpy-oneArrayEditor-length-input`).on("change keyup paste", function() {
            oneArrayLength = parseInt($(this).val());
        });
        $(`.vp-numpy-oneArrayEditor-make-btn`).click(function() {
            var newArray = [];
            for(var i = 0; i <  oneArrayLength; i++){
                newArray.push("0");
            }
            numpyStateGenerator.setState({
                paramData: {
                    [`${stateParamName}`]: newArray
                }
            });
            renderParamOneArrayEditor(tagSelector, stateParamName);
        });
    }

    /** renderParamOneArrayEditor
     *  1차원 배열 편집기를 특정 돔 태그에 렌더링한다
     *  @param {this} outerThis renderParamOneArrayEditView함수를 호출한 페이지의 ImportPackage.prototype을 참조하는 this
     *  @param {string} tagSelector 편집기를 동적 랜더링할 태그 이름
     *  @param {string} stateParamName state parameter 이름 -> 편집된 데이터는 이 state parameter에 저장된다
     */

    var renderParamOneArrayEditor = function(tagSelector, stateParamName) {
        var numpyPageRendererThis = oneArrayEditorState.getNumpyPageRendererThis();
        var numpyPageRendererThis = numpyPageRendererThis;
        var numpyStateGenerator = numpyPageRendererThis.numpyStateGenerator;
        
        var onearrayDom = $(tagSelector);
        var flexRowDiv = $(`<div class="vp-numpy-style-flex-row-wrap"></div>`);

        resetArrayEditor(onearrayDom);
        renderArrayEditorTitle(onearrayDom, tagSelector, stateParamName, "JY901");

        /**
         * numpyStateGenerator.getState(stateParamName) 배열의 인덱스 갯수만큼 for문 돌아 편집기 생성
         */
        for (var i = 0; i < numpyStateGenerator.getState(stateParamName).length; i++) {
            (function(j) {
                var uuid = vpCommon.getUUID();
                var oneArrayBlock = $(`<div class="flex-column"
                                            style="margin-top:10px; margin-bottom:10px;">
                                            <div class="text-center">
                                                <strong>${j}</strong>
                                            </div>
                                            
                                            <input class="vp-numpy-input text-center vp-numpy-array-onearray-${j}-input-${uuid}"
                                                value="${numpyStateGenerator.getState(stateParamName)[j]}" 
                                                style="width:40px;" 
                                                type="text"/>
                                            <button class="vp-numpy-func_btn vp-numpy-array-onearray-${j}-func_deleteBtn-${uuid}" 
                                                    style="width:40px;">x</button>
                                        </div>`);
                flexRowDiv.append(oneArrayBlock);
                onearrayDom.append(flexRowDiv);

                /**
                 *  1차원 배열 값 변경
                 */
                $(`.vp-numpy-array-onearray-${j}-input-${uuid}`).on("change keyup paste", function() {
                    var updatedIndexValue = $(`.vp-numpy-array-onearray-${j}-input-${uuid}`).val();
                    var updatedParamOneArray = updateOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), j, updatedIndexValue);

                    numpyStateGenerator.setState({
                        paramData: {
                            [`${stateParamName}`]: updatedParamOneArray
                        }
                    });
                });
                
                /**
                 *  1차원 배열 값 삭제
                 */
                $(`.vp-numpy-array-onearray-${j}-func_deleteBtn-${uuid}`).click(function() {
                    var deletedParamOneArray = deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName),j);

                    numpyStateGenerator.setState({
                        paramData: {
                            [`${stateParamName}`]: deletedParamOneArray
                        }
                    });
    
                    renderParamOneArrayEditor(tagSelector, stateParamName);
       
                });
            })(i);
        }

        onearrayDom.parent().find(`.vp-numpy-array-oneArray-func-plusBtn-${stateParamName}`).remove();

        var plusButton = $(`<button class="vp-numpy-func_btn vp-numpy-array-oneArray-func-plusBtn-${stateParamName}" 
                                    style="width: 100%; padding: 1rem;">
                                <span class="vp-multilang" data-caption-id="numpyPlus">+ 추가</span>
                            </button>`);

        onearrayDom.parent().append(plusButton);
        
        /** 
         * - 1차원 배열 생성 클릭 -
         */
        $(`.vp-numpy-array-oneArray-func-plusBtn-${stateParamName}`).click( function() {
            numpyStateGenerator.setState({
                paramData:{
                    [`${stateParamName}`]: [...numpyStateGenerator.getState(stateParamName), "0"]
                }
            });
            renderParamOneArrayEditor(tagSelector, stateParamName);
        });
    }
    return {
        initEditor,
        bindEventFunctions
    }
});