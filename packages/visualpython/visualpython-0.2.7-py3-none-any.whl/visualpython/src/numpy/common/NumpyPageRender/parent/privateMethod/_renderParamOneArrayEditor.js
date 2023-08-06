define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    // + 추가 numpy 폴더  패키지 : 이진용 주임
    ,'nbextensions/visualpython/src/numpy/api/numpyStateApi' 
], function( vpCommon, numpyStateApi ){
    var { updateOneArrayIndexValueAndGetNewArray, 
          deleteOneArrayIndexValueAndGetNewArray,
          updateTwoArrayIndexValueAndGetNewArray,
          deleteTwoArrayIndexValueAndGetNewArray,
          fixNumpyParameterValue } = numpyStateApi;
    
    /** 1차원 배열을 편집하는 편집기를 동적 렌더링하는 메소드 
     *  @param {numpyPageRenderer this} numpyPageRenderThis numpyPageRender.prototype을 가르키는 this
     *  @param {string} tagSelector 1차원 배열 편집기가 렌더링될 css tagSelector 
     *  @param {string} stateParamName 1차원 배열을 생성 변경, 삭제할 state  이름
    */
    var _renderParamOneArrayEditor = function(numpyPageRenderThis, tagSelector, stateParamName) {
        var numpyPageRenderThis = numpyPageRenderThis;
        var importPackageThis = numpyPageRenderThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRenderThis.getStateGenerator();

        var onearrayDom = $(importPackageThis.wrapSelector(tagSelector));
        var uuid = vpCommon.getUUID();

        numpyPageRenderThis.resetArrayEditor(onearrayDom);
        numpyPageRenderThis.renderParamArrayEditorTitle(onearrayDom, tagSelector, stateParamName, "JY901");
        /** 버튼 css 클래스 이름 중복방지 */
        numpyPageRenderThis.renderEditorModalOpenBtn(onearrayDom, `vp-numpy-open-oneArray-${vpCommon.getUUID()}`, "JY901", "row", stateParamName,tagSelector);

        var flexRowDiv = $(`<div class="flex-row-wrap"></div>`);
        /**, 
         * numpyStateGenerator.getState(stateParamName) 배열의 인덱스 갯수만큼 for문 돌아 편집기 생성
         */
        for (var i = 0; i < numpyStateGenerator.getState(stateParamName).length; i++) {
            (function(j) {
                var oneArrayBlock = $(`<div class="flex-column"
                                            style="margin-top:10px; margin-bottom:10px;">
                                            <div class="text-center">
                                                <strong> ${j} </strong>
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
                $(importPackageThis.wrapSelector(`.vp-numpy-array-onearray-${j}-input-${uuid}`)).on("change keyup paste", function() {
                    var updatedIndexValue = $(importPackageThis.wrapSelector(`.vp-numpy-array-onearray-${j}-input-${uuid}`)).val();
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
                $(importPackageThis.wrapSelector(`.vp-numpy-array-onearray-${j}-func_deleteBtn-${uuid}`)).click(function() {
                    var deletedParamOneArray = deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName),j);
    
                    numpyStateGenerator.setState({
                        paramData: {
                            [`${stateParamName}`]: deletedParamOneArray
                        }
                    });
    
                    numpyPageRenderThis.renderParamOneArrayEditor(tagSelector, stateParamName);
       
                });
            })(i);
        }

        onearrayDom.parent().find(`.vp-numpy-array-oneArray-func_plusbtn-${stateParamName}`).off();
        onearrayDom.parent().find(`.vp-numpy-array-oneArray-func_plusbtn-${stateParamName}`).remove();
        var button = $(`<button class="vp-numpy-func_btn vp-numpy-array-oneArray-func_plusbtn-${stateParamName}" 
                                style="width: 100%; padding: 1rem;">
                                <span  class="vp-multilang" data-caption-id="numpyPlus">+ 추가</span>
                        </button>`);
        onearrayDom.parent().append(button);
    
        /**   - 1차원 배열 생성 클릭 - */
        $(importPackageThis.wrapSelector(`.vp-numpy-array-oneArray-func_plusbtn-${stateParamName}`)).click( function() {
            numpyStateGenerator.setState({
                paramData:{
                    [`${stateParamName}`]: [...numpyStateGenerator.getState(stateParamName), "0"]
                }
            });

            numpyPageRenderThis.renderParamOneArrayEditor(tagSelector, stateParamName);
            /**  
             * - 1차원 배열 생성 버튼 클릭 후 배열 다시 렌더링
            */
        });
    }
    
    return _renderParamOneArrayEditor;
});
