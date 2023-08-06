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
], function ( requirejs, $, vpCommon, vpConst, sb, vpFuncJS,
              componentConstApi, numpyStateApi,
              TwoArrayEditorState ) {

    var sbCode = new sb.StringBuilder();
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "twoArrayEditor"
        , funcID : "JY902"  // TODO: ID 규칙 생성 필요
    }
    var vpFuncJS = new vpFuncJS.VpFuncJS(funcOptProp);
    var { controlToggleInput, closeParamArrayEditor } = componentConstApi;
    var { updateOneArrayIndexValueAndGetNewArray
          , deleteOneArrayIndexValueAndGetNewArray } = numpyStateApi;
    var twoArrayEditorState = new TwoArrayEditorState();    

    var twoArrayRow = 0;
    var twoArrayCol = 0;

    // 로딩을 생성하는 함수
    var renderLoadingBar = function() {
        vpCommon.renderLoadingBar();
    }

    /** initEditor bindEventFunctions 함수는 oneArrayEditor, twoArrayEditor, threeArrayEditor 다 동일한 이름의 함수입니다.*/

    /** initEditor 시작 함수
     * @param {this} numpyPageRendererThis 
     * @param {this} numpyPageRenderThis 
     */
    var initEditor = function(numpyPageRendererThis, stateParamName) {
        controlToggleInput();
        twoArrayEditorState.setNumpyPageRendererThis(numpyPageRendererThis);
        renderParamTwoArrayEditor(`.directoryComponent-container`,stateParamName);
    }

    // 이벤트 바인딩 함수
    var bindEventFunctions = function(stateParamName, tagSelector) {
        var numpyPageRendererThis =  twoArrayEditorState.getNumpyPageRendererThis();
        // editor 편집기를 닫았을때 실행되는 click 함수
        $('.directoryComponent-closedBtn').click(() => {
            closeParamArrayEditor(numpyPageRendererThis, tagSelector, stateParamName, 1);
        });
        // 확인 버튼을 누르면 editor 편집기가 닫히는 click 함수
        $('.vp-numpy-arrayEditor-func-confirmBtn').click(() => {
            closeParamArrayEditor(numpyPageRendererThis, tagSelector, stateParamName, 1);
        });
    }

    var resetArrayEditor = function(baseDom) {
        // 동적 랜더링할 태그에 css flex-column 설정
        baseDom.css("display","flex");
        baseDom.css("flexDirection","column");
        // 기존의 렌더링 태그들 리셋하고 아래 로직에서 다시 그림
        baseDom.empty()
    }

    var renderArrayEditorTitle = function(baseDom, tagSelector, stateParamName, funcId) {
        var numpyPageRendererThis =  twoArrayEditorState.getNumpyPageRendererThis();
        var numpyStateGenerator = numpyPageRendererThis.numpyStateGenerator;
        twoArrayRow = numpyStateGenerator.getState(stateParamName).length;
        var maxColNum = 0;
        numpyStateGenerator.getState(stateParamName).forEach(elementArray => {
            var num = elementArray.length;
            maxColNum = Math.max(maxColNum, num);
        });
        twoArrayCol = maxColNum;

        var dom = $(`<div>
                        <div class="vp-numpy-style-flex-row-center"
                            style="font-size:20px;font-weight:700">
                            <span class="vp-multilang" data-caption-id="two_dimention_array_editor">
                            2D Array Editor
                            </span>
                        </div>
                        <div class="vp-numpy-style-flex-row-center" style="margin-bottom:5px;">
                            <div style="margin:0 5px;">
                                <span  class="vp-multilang" data-caption-id="row-kor">행 : </span>
                                <input class="vp-numpy-input
                                              vp-numpy-twoArrayEditor-row-input"
                                    value="${twoArrayRow}"
                                    type="text"/>
                            </div>
                            <div style="margin:0 5px;">
                                <span  class="vp-multilang" data-caption-id="col-kor">열 : </span>
                                <input class="vp-numpy-input 
                                              vp-numpy-twoArrayEditor-col-input" 
                                    value="${twoArrayCol}"
                                    type="text"/>
                            </div>
                            <button class="vp-numpy-func_btn vp-numpy-twoArrayEditor-make-btn">생성</button>
                        </div>
                    </div>`);
        baseDom.append(dom);
        $(`.vp-numpy-twoArrayEditor-row-input`).on("change keyup paste", function() {
            twoArrayRow = parseInt($(this).val());
        });
        $(`.vp-numpy-twoArrayEditor-col-input`).on("change keyup paste", function() {
            twoArrayCol = parseInt($(this).val());
        });
        $(`.vp-numpy-twoArrayEditor-make-btn`).click(function() {
            var newTwoArray = [];
            for(var i = 0; i < twoArrayRow; i++){
                newTwoArray.push([]);
                for(var j = 0; j < twoArrayCol; j++){
                    newTwoArray[i].push("0");
                }
            }
            numpyStateGenerator.setState({
                paramData: {
                    [`${stateParamName}`]: newTwoArray
                }
            });
            renderParamTwoArrayEditor(tagSelector, stateParamName);
        });
    }

    /**
     * renderParamTwoArrayEditor
     * 2차원 배열 편집기를 특정 돔 태그에 렌더링한다
     *  @param {string} tagSelector 편집기를 동적 랜더링할 태그 이름
     *  @param {string} stateParamName state parameter 이름 -> 편집된 데이터는 이 state parameter에 저장된다
     */
    var renderParamTwoArrayEditor = function(tagSelector, stateParamName) {
        var numpyPageRendererThis =  twoArrayEditorState.getNumpyPageRendererThis();
        var numpyStateGenerator = numpyPageRendererThis.numpyStateGenerator;
        var twoarrayDom = $(tagSelector);

        resetArrayEditor(twoarrayDom);
        renderArrayEditorTitle(twoarrayDom, tagSelector, stateParamName, "JY902");
      
        var flexColumnDiv = $(`<div class="flex-column"></div>`);
        var twoArray = numpyStateGenerator.getState(stateParamName);
        // 2차원 배열 열  생성
        for (var i = 0; i < numpyStateGenerator.getState(stateParamName).length; i++) {
            (function(j) {
                var twoArrayBlock = $(`<div class="vp-numpy-arrayEditor-row-block 
                                                    vp-numpy-style-flex-row
                                                    vp-numpy-style-margin-right-10px"
                                            style="margin-right:10px;">
    
                                        <div class="overflow-x-auto vp-numpy-style-flex-row scrollbar" 
                                             style="width: 80%; overflow: auto; margin-top:5px; margin-bottom:5px;">
                                        
                                            <div class="flex-column-center text-center" 
                                                 style="width: 10%;">
                                                <strong>${j}</strong>
                                            </div>
                                            
                                            <div class="flex-column" style="width: 90%;">
                                                <div class="vp-numpy-array-row-container 
                                                            vp-numpy-array-twoArrayEditor-row-${j}-container-${stateParamName} 
                                                            vp-numpy-style-flex-row-wrap" style="width:100%;">
                                                
                                                </div>
                                            
                                            </div>
                                        </div>

                                        <div class="vp-numpy-style-flex-column-center"
                                            style="width:10%;">
                                            <button class="vp-numpy-func_btn 
                                                           vp-numpy-array-twoArrayEditor-col-${j}-func-plusbtn-${stateParamName}" 
                                                style="width: 100%; height:40px; max-height:80px;">+ 열</button>
                                        </div>
                                        <div class="vp-numpy-style-flex-column-center"
                                             style="width:10%;">
                                            <button class="vp-numpy-func_btn vp-numpy-array-twoArrayEditor-${j}-func-deleteBtn-${stateParamName}" 
                                                    style="width: 100%; height:40px; max-height:80px;">x</button>

                                        </div>
                                        
                                    </div>`);
                    flexColumnDiv.append(twoArrayBlock);
                    twoarrayDom.append(flexColumnDiv);
    
                    // 2차원 열 삭제
                    $(`.vp-numpy-array-twoArrayEditor-${j}-func-deleteBtn-${stateParamName}`).click( function() {
                        var deletedParamTwoArray = deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), j);

                        numpyStateGenerator.setState({
                            paramData: {
                                [`${stateParamName}`]: deletedParamTwoArray
                            }
                        });
                        renderParamTwoArrayEditor(tagSelector, stateParamName);
                    });
    
                    // 2차원 열 COL 생성
                    $(`.vp-numpy-array-twoArrayEditor-col-${j}-func-plusbtn-${stateParamName}`).click( function() {
                        var tempNarray = [...numpyStateGenerator.getState(stateParamName)[j], "0"];
                        numpyStateGenerator.setState({
                            paramData:{
                                [`${stateParamName}`]: updateOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), j, tempNarray)
                            }
                        });
                        renderParamTwoArrayEditor(tagSelector, stateParamName);
                    });

                    // 2차원 배열 행 ROW 생성
                    for (var y = 0; y < numpyStateGenerator.getState(stateParamName)[j].length; y++) {
                        (function(z) {
                            var rowContainer = $(`.vp-numpy-array-twoArrayEditor-row-${j}-container-${stateParamName}`);
                            var colBlock = $(`<div class="flex-column"
                                                   style="margin-top:5px; 
                                                          margin-bottom:5px;">
                                                <strong>
                                                    <span class="vp-numpy-style-flex-row-center">${z}</span>
                                                </strong>
                                                <input class="vp-numpy-input text-center vp-numpy-array-twoArrayEditor-${j}-${z}-input-${stateParamName}" 
                                                        value="${numpyStateGenerator.getState(stateParamName)[j][z]}" 
                                                        style="width:40px;" 
                                                        type="text"/>
                                                <button class="vp-numpy-func_btn vp-numpy-array-twoArrayEditor-${j}-${z}-func-deleteBtn-${stateParamName}" 
                                                        style="width:40px;">x</button>
                                                </div>`);
                            rowContainer.append(colBlock);
                            
                            // 2차원 배열 행 삭제
                            $(`.vp-numpy-array-twoArrayEditor-${j}-${z}-func-deleteBtn-${stateParamName}`).click( function() {
                                var tempNarray = deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName)[j], z);
                                numpyStateGenerator.setState({
                                    paramData: {
                                        [`${stateParamName}`]: updateOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), j, tempNarray)
                                    }
                                })
                                renderParamTwoArrayEditor(tagSelector, stateParamName);
                            });
    
                            // 2차원 배열 행 값 변경
                            $(`.vp-numpy-array-twoArrayEditor-${j}-${z}-input-${stateParamName}`).on("change keyup paste", function() {
                                var updatedIndexValue = $(`.vp-numpy-array-twoArrayEditor-${j}-${z}-input-${stateParamName}`).val();
                                var tempNarray = updateOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName)[j], z, updatedIndexValue);
                               
                                numpyStateGenerator.setState({
                                    paramData: {
                                        [`${stateParamName}`]:  updateOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), j, tempNarray)
                                    }
                                })
                            });
                        })(y);
                    }
    
            })(i);
        }
        twoarrayDom.parent().find(`.vp-numpy-array-twoArrayEditor-row-func-plusbtn-${stateParamName}`).off();
        twoarrayDom.parent().find(`.vp-numpy-array-twoArrayEditor-row-func-plusbtn-${stateParamName}`).remove();
        var button = $(`<button class="vp-numpy-func_btn vp-numpy-array-twoArrayEditor-row-func-plusbtn-${stateParamName}" 
                            style="width: 100%; padding: 1rem;" >
                            <span class="vp-multilang" data-caption-id="numpyPlusRow">
                                + 행
                            </span>
                        </button>`);
    
        twoarrayDom.parent().append(button);
        // 2차원 배열 행(row) 생성 클릭
        $(`.vp-numpy-array-twoArrayEditor-row-func-plusbtn-${stateParamName}`).click( function() {
            numpyStateGenerator.setState({
                paramData:{
                    [`${stateParamName}`]: [...numpyStateGenerator.getState(stateParamName), ["0"]]
                }
            });
            renderParamTwoArrayEditor(tagSelector, stateParamName);
        });

    }

    return {
        initEditor,
        bindEventFunctions
    }
});
