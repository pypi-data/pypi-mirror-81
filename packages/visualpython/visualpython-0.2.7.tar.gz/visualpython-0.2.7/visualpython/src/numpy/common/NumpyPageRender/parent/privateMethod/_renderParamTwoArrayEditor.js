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
    /**
     * 2차원 배열을 편집하는 편집기를 동적 렌더링하는 메소드 
     * @param {numpyPageRenderer this} numpyPageRenderThis 
     * @param {string} tagSelector 2차원 배열 편집기가 렌더링될 css tagSelector 
     * @param {string} stateParamName 2차원 배열을 생성 변경, 삭제할 state 이름
     */
    var _renderParamTwoArrayEditor = function(numpyPageRenderThis, tagSelector, stateParamName) {
        var numpyPageRenderThis = numpyPageRenderThis;
        var importPackageThis = numpyPageRenderThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRenderThis.getStateGenerator();
        var twoarrayDom = $(importPackageThis.wrapSelector(tagSelector));
        var uuid = vpCommon.getUUID();

        /** 기존의 렌더링된 2차원 배열 editor <diV> 블록을 삭제*/
        numpyPageRenderThis.resetArrayEditor(twoarrayDom);
        /** 제목 생성 */
        numpyPageRenderThis.renderParamArrayEditorTitle(twoarrayDom, tagSelector, stateParamName, "JY902");
        /** 크게보기 버튼 생성 */
        numpyPageRenderThis.renderEditorModalOpenBtn(twoarrayDom, `vp-numpy-open-twoArray-${vpCommon.getUUID()}`, "JY902", "column", stateParamName,tagSelector);
        
        var flexColumnDiv = $(`<div class="flex-column"></div>`);
        // var twoArray = numpyStateGenerator.getState(stateParamName);
        // 2차원 배열 열  생성
        for (var i = 0; i < numpyStateGenerator.getState(stateParamName).length; i++) {
            (function(j) {
                var twoArrayBlock = $(`<div class="vp-numpy-arrayEditor-row-block 
                                                   vp-numpy-style-flex-row">
    
                                        <div class="overflow-x-auto 
                                                    vp-numpy-style-flex-row 
                                                    scrollbar" style="width: 80%; overflow: auto; margin-top:5px; margin-bottom:5px;">
                                        
                                            <div class="flex-column-center text-center" style="width: 10%;">
                                                <strong>${j}</strong>
                                            </div>
                                            
                                            <div class="flex-column" style="width: 90%;">
                                                <div class="vp-numpy-array-row-container 
                                                            vp-numpy-array-twoarray-row-${j}-container-${uuid} 
                                                            vp-numpy-style-flex-row-wrap" style="width:100%;">
                                                
                                                </div>
                                            
                                            </div>
                                        </div>
                            
                                        <div class="vp-numpy-style-flex-column-center"
                                                         style="width:10%;">
                                            <button class="vp-numpy-func_btn 
                                                            vp-numpy-array-twoarray-${j}-func_plusbtn-${uuid}"  
                                                    style="width: 100%; height:40px; max-height:80px;">+ 열</button>
                                        </div>
                                        <div class="vp-numpy-style-flex-column-center"
                                            style="width:10%;">
                                            <button class="vp-numpy-func_btn 
                                                            vp-numpy-array-twoarray-${j}-func_deleteBtn-${uuid}" 
                                                    style="width: 100%; height:40px; max-height:80px;">x</button>

                                        </div>
                                      
                                    </div>`);
                    flexColumnDiv.append(twoArrayBlock);
                    twoarrayDom.append(flexColumnDiv);
    
                    // 2차원 열 삭제
                    $(importPackageThis.wrapSelector(`.vp-numpy-array-twoarray-${j}-func_deleteBtn-${uuid}`)).click( function() {
                        var deletedParamTwoArray = deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), j);

                        numpyStateGenerator.setState({
                            paramData: {
                                [`${stateParamName}`]: deletedParamTwoArray
                            }
                        });
                        numpyPageRenderThis.renderParamTwoArrayEditor(tagSelector, stateParamName);
                    });
    
                    // 2차원 열 COL 생성
                    $(importPackageThis.wrapSelector(`.vp-numpy-array-twoarray-${j}-func_plusbtn-${uuid}`)).click( function() {
                        var tempNarray = [...numpyStateGenerator.getState(stateParamName)[j], "0"];
                        numpyStateGenerator.setState({
                            paramData:{
                                [`${stateParamName}`]: updateOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), j, tempNarray)
                            }
                        });
                        numpyPageRenderThis.renderParamTwoArrayEditor(tagSelector, stateParamName);
                    });

                    // 2차원 배열 행 ROW 생성
                    for (var y = 0; y < numpyStateGenerator.getState(stateParamName)[j].length; y++) {
                        (function(z) {
                            var rowContainer = $(importPackageThis.wrapSelector(`.vp-numpy-array-twoarray-row-${j}-container-${uuid}`));
                            var colBlock = $(`<div class="flex-column"
                                                   style="margin-top:5px">
                                                <strong>
                                                    <span class="vp-numpy-style-flex-row-center">${z}</span> 
                                                </strong>
                                                <input class="vp-numpy-input text-center vp-numpy-array-twoarray-${j}-${z}-input-${uuid}" 
                                                        value="${numpyStateGenerator.getState(stateParamName)[j][z]}" 
                                                        style="width:40px;" 
                                                        type="text"/>
                                                <button class="vp-numpy-func_btn vp-numpy-array-twoarray-${j}-${z}-func_deleteBtn-${uuid}" 
                                                        style="width:40px;">x</button>
                                                </div>`);
                            rowContainer.append(colBlock);
                            
                            // 2차원 배열 행 삭제
                            $(importPackageThis.wrapSelector(`.vp-numpy-array-twoarray-${j}-${z}-func_deleteBtn-${uuid}`)).click( function() {
                                var tempNarray = deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName)[j], z);
                                numpyStateGenerator.setState({
                                    paramData: {
                                        [`${stateParamName}`]: updateOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), j, tempNarray)
                                    }
                                })
                                numpyPageRenderThis.renderParamTwoArrayEditor(tagSelector, stateParamName);
                            });

                            // 2차원 배열 행 값 변경
                            $(importPackageThis.wrapSelector(`.vp-numpy-array-twoarray-${j}-${z}-input-${uuid}`)).on("change keyup paste", function() {
                                var updatedIndexValue = $(importPackageThis.wrapSelector(`.vp-numpy-array-twoarray-${j}-${z}-input-${uuid}`)).val();
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
        twoarrayDom.parent().find(`.vp-numpy-array-twoarray-row-func_plusbtn-${stateParamName}`).off();
        twoarrayDom.parent().find(`.vp-numpy-array-twoarray-row-func_plusbtn-${stateParamName}`).remove();
        var button = $(`<button class="vp-numpy-func_btn vp-numpy-array-twoarray-row-func_plusbtn-${stateParamName}" 
                            style="width: 100%; padding: 1rem;" >
                            <span class="vp-multilang" data-caption-id="numpyPlusRow">
                                + 행
                            </span>
                        </button>`);
        twoarrayDom.parent().append(button);

        // 2차원 배열 행(row) 생성 클릭
        $(importPackageThis.wrapSelector(`.vp-numpy-array-twoarray-row-func_plusbtn-${stateParamName}`)).click( function() {
            numpyStateGenerator.setState({
                paramData:{
                    [`${stateParamName}`]: [...numpyStateGenerator.getState(stateParamName), ["0"]]
                }
            });

             /**  
             * - 2차원 배열 생성 버튼 클릭 후 배열 다시 렌더링
            */
            numpyPageRenderThis.renderParamTwoArrayEditor(tagSelector, stateParamName);
           
        });
    }

    return _renderParamTwoArrayEditor;
});
