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
              ThreeArrayEditorState ) {


    var sbCode = new sb.StringBuilder();
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "threeArrayEditor"
        , funcID : "JY903"  // TODO: ID 규칙 생성 필요
    }
    var vpFuncJS = new vpFuncJS.VpFuncJS(funcOptProp);
    var { controlToggleInput, closeParamArrayEditor } = componentConstApi;
    var { updateOneArrayIndexValueAndGetNewArray, 
          deleteOneArrayIndexValueAndGetNewArray,
          updateTwoArrayIndexValueAndGetNewArray,
          deleteTwoArrayIndexValueAndGetNewArray,
          fixNumpyParameterValue } = numpyStateApi;

    var threeArrayEditorState = new ThreeArrayEditorState();    
    var threeArrayRow = 0;
    var threeArrayCol = 0;
    var threeArrayDepth = 0;

    // 로딩을 생성하는 함수
    var renderLoadingBar = function() {
        vpCommon.renderLoadingBar();
    }

    /** initEditor bindEventFunctions 함수는 oneArrayEditor, twoArrayEditor, threeArrayEditor 다 동일한 이름의 함수입니다.*/

    /** initEditor 시작 함수
     * @param {this} numpyPageRendererThis 
     * @param {string} stateParamName 
     */
    var initEditor = function(numpyPageRendererThis, stateParamName) {
        controlToggleInput();
        threeArrayEditorState.setNumpyPageRendererThis(numpyPageRendererThis);
        renderParamThreeArrayEditor(`.directoryComponent-container`,stateParamName);
    }

    // 이벤트 바인딩 함수
    var bindEventFunctions = function(stateParamName, tagSelector) {
        var numpyPageRenderThis = threeArrayEditorState.getNumpyPageRendererThis();
        // editor 편집기를 닫았을때 실행되는 click 함수
        $('.directoryComponent-closedBtn').click(() => {
            closeParamArrayEditor(numpyPageRenderThis, tagSelector, stateParamName, 2);
        });
        // 확인 버튼을 누르면 editor 편집기가 닫히는 click 함수
        $('.vp-numpy-arrayEditor-func-confirmBtn').click(() => {
            closeParamArrayEditor(numpyPageRenderThis, tagSelector, stateParamName, 2);
        });
    }

    var resetArrayEditor = function(baseDom) {
        // 동적 랜더링할 태그에 css flex-column 설정
        baseDom.css("display","flex");
        baseDom.css("flexDirection","column");
        // 기존의 렌더링 태그들 리셋하고 아래 로직에서 다시 그림
        baseDom.empty()
    }

    var renderArrayEditorTitle = function(baseDom, tagSelector, stateParamName) {
        var numpyPageRendererThis = threeArrayEditorState.getNumpyPageRendererThis();
        var numpyStateGenerator = numpyPageRendererThis.numpyStateGenerator;

        threeArrayRow = numpyStateGenerator.getState(stateParamName).length;
        var maxColNum = 0;
        var maxDepthNum = 0;
        numpyStateGenerator.getState(stateParamName).forEach(elementArray => {
            var num = elementArray.length;
            maxColNum = Math.max(maxColNum, num);
            elementArray.forEach(innerArray => {
                var num2 = innerArray.length;
                maxDepthNum = Math.max(maxDepthNum, num2);
            });
        });
        threeArrayCol = maxColNum;
        threeArrayDepth = maxDepthNum;
        dom = $(`<div>
                    <div class="vp-numpy-style-flex-row-center"
                         style="font-size:20px;font-weight:700">
                         <span class="vp-multilang" data-caption-id="three_dimention_array_editor">
                         3D Array Editor
                         </span>
                    </div>
                    <div class="vp-numpy-style-flex-row-center" style="margin-bottom:5px;">
                        <div style="margin:0 5px;">
                            <span  class="vp-multilang" data-caption-id="depth-kor">면 : </span>
                            <input class="vp-numpy-input 
                                          vp-numpy-threeArrayEditor-row-input" 
                                value="${threeArrayRow}"
                                type="text"/>
                        </div>
                        <div style="margin:0 5px;">
                            <span  class="vp-multilang" data-caption-id="row-kor">행 : </span>
                            <input class="vp-numpy-input 
                                          vp-numpy-threeArrayEditor-col-input" 
                                value="${threeArrayCol}"
                                type="text"/>
                        </div>
                        <div style="margin:0 5px;">
                            <span  class="vp-multilang" data-caption-id="col-kor">열 : </span>
                            <input class="vp-numpy-input 
                                          vp-numpy-threeArrayEditor-depth-input" 
                                value="${threeArrayDepth}"
                                type="text"/>
                        </div>
                        <button class="vp-numpy-func_btn vp-numpy-threeArrayEditor-make-btn">생성</button>
                    </div>
                </div>`);
        baseDom.append(dom);
        $(`.vp-numpy-threeArrayEditor-row-input`).on("change keyup paste", function() {
            threeArrayRow = parseInt($(this).val());
        });
        $(`.vp-numpy-threeArrayEditor-col-input`).on("change keyup paste", function() {
            threeArrayCol = parseInt($(this).val());
        });   
        $(`.vp-numpy-threeArrayEditor-depth-input`).on("change keyup paste", function() {
            threeArrayDepth = parseInt($(this).val());
        });        
        $(`.vp-numpy-threeArrayEditor-make-btn`).click(function() {
            var newThreeArray = [];
            for(var i = 0; i < threeArrayRow; i++) {
                newThreeArray.push([]);
                for(var j = 0; j < threeArrayCol; j++) {
                    newThreeArray[i].push([]);
                    for(var z = 0; z < threeArrayDepth; z++) {
                        newThreeArray[i][j].push("0");
                    }
                }
            }
            numpyStateGenerator.setState({
                paramData: {
                    [`${stateParamName}`]: newThreeArray
                }
            });
            renderParamThreeArrayEditor(tagSelector, stateParamName);
        });
    }

    var renderParamThreeArrayEditor = function(tagSelector, stateParamName) {
        var numpyPageRendererThis = threeArrayEditorState.getNumpyPageRendererThis();
        var numpyStateGenerator = numpyPageRendererThis.numpyStateGenerator;

        var threeArrayDom = $(tagSelector);

        resetArrayEditor(threeArrayDom);
        renderArrayEditorTitle(threeArrayDom, tagSelector, stateParamName, "JY903");
       
        var flexColumnDiv = $(`<div class="flex-column"></div>`);
        // var threeArray = numpyStateGenerator.getState(stateParamName);

        // 3차원 배열 렌더링
        for (var i = 0; i < numpyStateGenerator.getState(stateParamName).length; i++) {
            (function(a) {
                var threeArrayBlock = $(`<div>
                                            <div class="vp-numpy-array-threeArrayEditor-${a}-container scrollbar"
                                                 style="overflow: auto; margin-top:5px; margin-bottom:5px;">
                                            </div>
                                            <button class="vp-numpy-func_btn vp-numpy-array-threeArrayEditor-${a}-plus-func-btn"
                                                    style="width: 90%; float: left; padding: 1rem;">+2차원 배열</button>
                                            <button class="vp-numpy-func_btn vp-numpy-array-threeArrayEditor-${a}-delete-func-btn"
                                                    style="width:10%; padding: 1rem;">x</button>
                                         </div>`);
                flexColumnDiv.append(threeArrayBlock);
                threeArrayDom.append(flexColumnDiv);

                // 3차원 배열 등록
                $(`.vp-numpy-array-threeArrayEditor-${a}-plus-func-btn`).click( function() {
                    numpyStateGenerator.getState(stateParamName)[a].push(["0"]);
                    renderParamThreeArrayEditor(tagSelector, stateParamName);
                });

                // 3차원 배열 삭제
                $(`.vp-numpy-array-threeArrayEditor-${a}-delete-func-btn`).click( function() {
                    var deletedParamTwoArray = deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), a);

                    numpyStateGenerator.setState({
                        paramData: {
                            [`${stateParamName}`]: deletedParamTwoArray
                        }
                    });
                    renderParamThreeArrayEditor(tagSelector, stateParamName);
                });
      
                //2차원 배열 렌더링
                var twoarrayDom = $(`.vp-numpy-array-threeArrayEditor-${a}-container`);
                for (var j = 0; j < numpyStateGenerator.getState(stateParamName)[a].length; j++) {
                    (function(b) {
                        var twoArrayBlock = $(`<div class="vp-numpy-style-flex-row
                                                             vp-numpy-arrayEditor-row-block
                                                             vp-numpy-style-margin-right-10px">
                                                    <div class="overflow-x-auto vp-numpy-style-flex-row scrollbar" 
                                                         style="width: 80%;">
                                                        <div class="flex-column-center text-center" 
                                                             style="width: 10%;">
                                                             <strong>${b}</strong>
                                                        </div>     
                                                        <div class="flex-column" style="width: 90%;">
                                                            <div class="vp-numpy-array-row-container 
                                                                        vp-numpy-array-threeArrayEditor-row-${a}-${b}-container-${stateParamName} vp-numpy-style-flex-row-wrap" style="width:100%;">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="vp-numpy-style-flex-column-center"
                                                         style="width:10%;">
                                                        <button class="vp-numpy-func_btn 
                                                                       vp-numpy-array-threeArrayEditor-col-${a}-${b}-func-plusbtn-${stateParamName}"  
                                                                style="width: 100%; height:40px; max-height:80px;">+</button>
                                                    </div>
                                                    <div class="vp-numpy-style-flex-column-center"
                                                         style="width:10%;">
                                                        <button class="vp-numpy-func_btn 
                                                                       vp-numpy-array-threeArrayEditor-${a}-${b}-func-deleteBtn-${stateParamName}" 
                                                                style="width: 100%; height:40px; max-height:80px;">x</button>
                                                    </div>
                                                </div>`);
    
                        twoarrayDom.append(twoArrayBlock);

                        // 2차원 열 삭제
                        $(`.vp-numpy-array-threeArrayEditor-${a}-${b}-func-deleteBtn-${stateParamName}`).click( function() {
                            var deletedParamTwoArray = deleteTwoArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), a, b);
                            numpyStateGenerator.setState({
                                paramData: {
                                    [`${stateParamName}`]:deletedParamTwoArray 
                                }
                            });
                            renderParamThreeArrayEditor(tagSelector, stateParamName);
                        });
        
                        // 2차원 열 COL 생성
                        $(`.vp-numpy-array-threeArrayEditor-col-${a}-${b}-func-plusbtn-${stateParamName}`).click( function() {
                            numpyStateGenerator.getState(stateParamName)[a][b].push("0");
         
                            renderParamThreeArrayEditor(tagSelector, stateParamName);
                        });

                        //1차원 배열 렌더링
                        for (var z = 0; z < numpyStateGenerator.getState(stateParamName)[a][b].length; z++) {
                            (function(c) {
                                var rowContainer = $(`.vp-numpy-array-threeArrayEditor-row-${a}-${b}-container-${stateParamName}`);
                                var colBlock = $(`<div class="flex-column"
                                                       style="margin-top:5px;
                                                              margin-bottom:5px;">
                                                    <strong>
                                                        <span class="vp-numpy-style-flex-row-center">${c}</span>
                                                    </strong>
                                                    <input class="vp-numpy-input text-center vp-numpy-array-threeArrayEditor-${a}-${b}-${c}-input-${stateParamName}" 
                                                            value="${numpyStateGenerator.getState(stateParamName)[a][b][c]}" 
                                                            style="width:40px;" 
                                                            type="text"/>
                                                    <button class="vp-numpy-func_btn vp-numpy-array-threeArrayEditor-${a}-${b}-${c}-func-deleteBtn-${stateParamName}" 
                                                            style="width:40px;">x</button>
                                                    </div>`);
                                rowContainer.append(colBlock);
                                
                                // 1차원 배열 행 삭제
                                $(`.vp-numpy-array-threeArrayEditor-${a}-${b}-${c}-func-deleteBtn-${stateParamName}`).click( function() {
                                    numpyStateGenerator.getState(stateParamName)[a][b].splice(c,1);
                                    renderParamThreeArrayEditor(tagSelector, stateParamName);
                                });
                                // 1차원 배열 행 값 변경
                                $(`.vp-numpy-array-threeArrayEditor-${a}-${b}-${c}-input-${stateParamName}`).on("change keyup paste", function() {
                                    var updatedIndexValue = $(`.vp-numpy-array-threeArrayEditor-${a}-${b}-${c}-input-${stateParamName}`).val();
                                    numpyStateGenerator.getState(stateParamName)[a][b][c] = updatedIndexValue;
                                });
                            })(z);
                        }
                    })(j);
                }
             
            })(i);
        }

        threeArrayDom.parent().find(`.vp-numpy-array-threeArrayEditor-func-plusbtn-${stateParamName}`).remove();
        var button = $(`<button class="vp-numpy-func_btn 
                                       vp-numpy-array-threeArrayEditor-func-plusbtn-${stateParamName}" 
                                style="width: 100%; padding: 1rem; margin-top:5px;" >
                            <span class="vp-multilang" data-caption-id="numpyPlusRow">
                                + 3차원 배열
                            </span>
                        </button>`);
   
        threeArrayDom.parent().append(button);

        // 3차원 배열 생성 클릭
        $(`.vp-numpy-array-threeArrayEditor-func-plusbtn-${stateParamName}`).click( function() {
            numpyStateGenerator.setState({
                paramData:{
                    [`${stateParamName}`]: [...numpyStateGenerator.getState(stateParamName), [["0"]]]
                }
            });
            renderParamThreeArrayEditor(tagSelector, stateParamName);
        });
    }

    return {
        initEditor,
        bindEventFunctions
    }
});
