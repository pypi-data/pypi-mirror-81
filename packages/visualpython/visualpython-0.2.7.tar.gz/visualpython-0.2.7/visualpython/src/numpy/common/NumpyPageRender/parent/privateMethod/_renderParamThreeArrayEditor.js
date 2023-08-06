define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    // + 추가 numpy 폴더  패키지 : 이진용 주임
    , 'nbextensions/visualpython/src/numpy/api/numpyStateApi' 
], function( vpCommon, numpyStateApi ){
    var { updateOneArrayIndexValueAndGetNewArray, 
          deleteOneArrayIndexValueAndGetNewArray,
          updateTwoArrayIndexValueAndGetNewArray,
          deleteTwoArrayIndexValueAndGetNewArray,
          fixNumpyParameterValue } = numpyStateApi;

    var _renderParamThreeArrayEditor = function(numpyPageRenderThis, tagSelector, stateParamName) {
        var numpyPageRenderThis = numpyPageRenderThis;
        var importPackageThis = numpyPageRenderThis.importPackageThis;
        var numpyStateGenerator = numpyPageRenderThis.numpyStateGenerator;
       
        var threeArrayDom = $(importPackageThis.wrapSelector(tagSelector));
    
        numpyPageRenderThis.resetArrayEditor(threeArrayDom);
        numpyPageRenderThis.renderParamArrayEditorTitle(threeArrayDom, tagSelector, stateParamName, "JY903");
        /** 버튼 css 클래스 이름 중복방지 */
        numpyPageRenderThis.renderEditorModalOpenBtn(threeArrayDom, `vp-numpy-open-threeArray-${vpCommon.getUUID()}`, "JY903", "column", stateParamName,tagSelector);
        
        var flexColumnDiv = $(`<div class="flex-column"></div>`);

        // 3차원 배열 렌더링
        for (var i = 0; i < numpyStateGenerator.getState(stateParamName).length; i++) {
            (function(a) {
                var threeArrayBlock = $(`<div>
                                            <div class="scrollbar 
                                                        vp-numpy-array-threeArray-${a}-container-${stateParamName}"
                                                  style="overflow: auto; margin-top:5px; margin-bottom:5px;">
                                            </div>
                                            <button class="vp-numpy-func_btn vp-numpy-array-threeArray-${a}-plus-func_btn-${stateParamName}"
                                                    style="width: 90%; float: left; padding: 1rem;">+2차원 배열</button>
                                            <button class="vp-numpy-func_btn vp-numpy-array-threeArray-${a}-delete-func_btn-${stateParamName}"
                                                    style="width:10%; padding: 1rem;">x</button>
                                         </div>`);
                flexColumnDiv.append(threeArrayBlock);
                threeArrayDom.append(flexColumnDiv);

                // 2차원 배열 생성
                $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-${a}-plus-func_btn-${stateParamName}`)).click( function() {
                    var tempNarray = [...numpyStateGenerator.getState(stateParamName)[a], ["0"]];
                    numpyStateGenerator.setState({
                        paramData:{
                            [`${stateParamName}`]: updateOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), a, tempNarray)
                        }
                    });

                    numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamName);
                });

                // 3차원 배열 삭제
                $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-${a}-delete-func_btn-${stateParamName}`)).click( function() {
                    var deletedParamTwoArray = deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), a);

                    numpyStateGenerator.setState({
                        paramData: {
                            [`${stateParamName}`]: deletedParamTwoArray
                        }
                    });
                    numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamName);
                });
      
                //2차원 배열 렌더링
                var threeArrayContainer = $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-${a}-container-${stateParamName}`));
                for (var j = 0; j < numpyStateGenerator.getState(stateParamName)[a].length; j++) {
                    (function(b) {
                        var twoArrayBlock = $(`<div class="vp-numpy-style-flex-row
                                                            vp-numpy-arrayEditor-row-block
                                                            vp-numpy-style-margin-right-10px" 
                                                    style="margin-top:5px; margin-bottom:5px;">
                                                    <div class="overflow-x-auto 
                                                                vp-numpy-style-flex-row scrollbar" style="width: 80%;">
                                                        <div class="flex-column-center text-center" style="width: 10%;">
                                                        <strong>${b} </strong>
                                                    </div>     
                                                        <div class="flex-column" style="width: 90%;">
                                                            <div class="vp-numpy-array-row-container 
                                                                        vp-numpy-array-threeArray-row-${a}-${b}-container-${stateParamName} 
                                                                        vp-numpy-style-flex-row-wrap" style="width:100%;">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="vp-numpy-style-flex-column-center"
                                                         style="width:10%;">
                                                        <button class="vp-numpy-func_btn 
                                                                    vp-numpy-array-threeArray-col-${a}-${b}-func-plusbtn-${stateParamName}"  
                                                                style="width: 100%; height:40px; max-height:80px;">+</button>
                                                    </div>
                                                    <div class="vp-numpy-style-flex-column-center"
                                                         style="width:10%;">
                                                        <button class="vp-numpy-func_btn 
                                                                   vp-numpy-array-threeArray-${a}-${b}-func-deleteBtn-${stateParamName}" 
                                                                style="width: 100%; height:40px; max-height:80px;">x</button>
                                                    </div>
                                                </div>`);
    
                        threeArrayContainer.append(twoArrayBlock);

                        // 2차원 배열 삭제
                        $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-${a}-${b}-func-deleteBtn-${stateParamName}`)).click( function() {
                            var deletedParamTwoArray = deleteTwoArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), a, b);
                            numpyStateGenerator.setState({
                                paramData: {
                                    [`${stateParamName}`]:deletedParamTwoArray 
                                }
                            });
                            numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamName);
                        });

                        // 1 차원 배열 생성
                        $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-col-${a}-${b}-func-plusbtn-${stateParamName}`)).click( function() {
                         
                            var tempNarray = [...numpyStateGenerator.getState(stateParamName)[a][b], "0"];
                  
                            numpyStateGenerator.setState({
                                paramData:{
                                    [`${stateParamName}`]:  updateTwoArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), a, b, tempNarray )
                                }
                            });
                            
                            numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamName);
                        });

                        //1차원 배열 렌더링
                        for (var z = 0; z < numpyStateGenerator.getState(stateParamName)[a][b].length; z++) {
                            (function(c) {
                                var rowContainer = $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-row-${a}-${b}-container-${stateParamName}`));
                                var colBlock = $(`<div class="flex-column"
                                                       style="margin-bottom:5px;">
                                                    <strong>
                                                        <span class="vp-numpy-style-flex-row-center"
                                                          style="margin-top:5px;">${c}</span>
                                                    </strong>
                                                    <input class="vp-numpy-input text-center vp-numpy-array-threeArray-${a}-${b}-${c}-input-${stateParamName}" 
                                                            value="${numpyStateGenerator.getState(stateParamName)[a][b][c]}" 
                                                            style="width:40px;" 
                                                            type="text"/>
                                                    <button class="vp-numpy-func_btn 
                                                                   vp-numpy-array-threeArray-${a}-${b}-${c}-func_deleteBtn-${stateParamName}" 
                                                            style="width:40px;">x</button>
                                                    </div>`);
                                rowContainer.append(colBlock);


                                // 1차원 배열 행 삭제
                                $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-${a}-${b}-${c}-func_deleteBtn-${stateParamName}`)).click( function() {
                                 
                                    var tempNarray = deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName)[a][b], c);

                                    numpyStateGenerator.setState({
                                        paramData: {
                                            [`${stateParamName}`]: updateTwoArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), a, b, tempNarray )
                                        }
                                    })

                                    numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamName);
                                });
                                // 1차원 배열 행 값 변경
                                $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-${a}-${b}-${c}-input-${stateParamName}`)).on("change keyup paste", function() {
                                    var updatedIndexValue = $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-${a}-${b}-${c}-input-${stateParamName}`)).val();
                        
                                    var tempNarray = updateOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName)[a][b],c,updatedIndexValue);
                                
                                    numpyStateGenerator.setState({
                                        paramData:{
                                            [`${stateParamName}`]:  updateTwoArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), a, b, tempNarray )
                                        }
                                    });
                                
                                });
                            })(z);
                        }
                    })(j);
                }
             
            })(i);
        }

        threeArrayDom.parent().find(`.vp-numpy-array-threeArray-func_plusbtn-${stateParamName}`).off();
        threeArrayDom.parent().find(`.vp-numpy-array-threeArray-func_plusbtn-${stateParamName}`).remove();
        
        var button = $(`<button class="vp-numpy-func_btn 
                                       vp-numpy-array-threeArray-func_plusbtn-${stateParamName}" 
                            style="width: 100%; padding: 1rem; margin-top:5px;"  >
                            <span class="vp-multilang" data-caption-id="numpyPlus3Array">
                                + 3차원 배열
                            </span>
                        </button>`);
        threeArrayDom.parent().append(button);
       

        // 3차원 배열 생성 클릭
        $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-func_plusbtn-${stateParamName}`)).click( function() {
            numpyStateGenerator.setState({
                paramData:{
                    [`${stateParamName}`]: [...numpyStateGenerator.getState(stateParamName), [["0"]]]
                }
            });
            numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamName);
        });
    }

    return _renderParamThreeArrayEditor;
});
