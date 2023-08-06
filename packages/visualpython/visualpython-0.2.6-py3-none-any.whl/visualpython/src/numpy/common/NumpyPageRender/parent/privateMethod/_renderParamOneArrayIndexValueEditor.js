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

    /** FIXME: 추후 이름 변경 예정
     * 배열의 차원과 갯수를 편집하는 편집기를 동적 렌더링하는 메소드 
     *  _renderParamOneArrayEditor가 배열의 값을 CRUD하는 편집기라면,
     *  ex) np.array([1,2,3,4,5,6,7]) -> 1차원 배열 안에 들어있는 값 편집
     * _renderParamOneArrayIndexValueEditor는 배열의 차원과 갯수를 CRUD하는 편집기
     *  ex) np.zero(2,3) -> 2행 3열 배열 생성. 
    */

    var _renderParamOneArrayIndexValueEditor = function(numpyPageRenderThis, tagSelector, stateParamName) {
        var numpyPageRenderThis = numpyPageRenderThis;
        var importPackageThis = numpyPageRenderThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRenderThis.getStateGenerator();
        var editorDom = $(importPackageThis.wrapSelector(tagSelector));
        var uuid = vpCommon.getUUID();
        editorDom.empty();

        /**
         *  1차원 배열의 인덱스 갯수만큼 for문 돌아 편집기 생성
         */
        var flexRowBetweenDiv = $(`<div class="vp-numpy-style-flex-row-between"></div>`);
        for (var i = 0; i < numpyStateGenerator.getState(stateParamName).length; i++) {
            (function(j) {
                var narrayBlock = $(`<div class="vp-numpy-style-flex-row">
                                        <div class="flex-column-center margin-right-5px font-weight-700">n${j + 1}</div> 
                                        <input class="vp-numpy-param-n-${j}-var-input-${stateParamName} 
                                                      vp-numpy-input" 
                                                value="${numpyStateGenerator.getState(stateParamName)[j]}" type="text"
                                                placeholder="입력"/>
                                        <button class="vp-numpy-n-${j}-delete-btn-${stateParamName} vp-numpy-func_btn">x</button>
                                    </div>`);
                flexRowBetweenDiv.append(narrayBlock);
                editorDom.append(flexRowBetweenDiv);

                // 편집기 j번 인덱스의 값 변경
                $(importPackageThis.wrapSelector(`.vp-numpy-param-n-${j}-var-input-${stateParamName}`)).on("change keyup paste", function() {
                    var updatedIndexValue = $(this).val();
                    var updatedParamTwoArray = updateOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), j, updatedIndexValue);
                    numpyStateGenerator.setState({
                        paramData: {
                            [`${stateParamName}`]: updatedParamTwoArray
                        }
                    });
                });
                
                // 편집기 j번 인덱스의 값 삭제
                $(importPackageThis.wrapSelector(`.vp-numpy-n-${j}-delete-btn-${stateParamName}`)).click(function() {
                    numpyStateGenerator.setState({
                        paramData: {
                            [`${stateParamName}`]: deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName),j)
                        }
                    });
                    numpyPageRenderThis.renderParamOneArrayIndexValueEditor(tagSelector, stateParamName);
                });
            })(i);
        }

        editorDom.parent().find(`.vp-numpy-block-empty-shape-n-array-btn-${stateParamName}`).remove();
        // +추가 button 생성 
        var button = $(`<button class="vp-numpy-block-empty-shape-n-array-btn-${stateParamName} vp-numpy-func_btn black" style="width: 100%; padding: 1rem;">
                            <span class="vp-multilang" data-caption-id="numpyPlus">
                                +추가
                            </span>
                        </button>`);

        editorDom.append(button);       
 
        // n차원 배열 추가 차원 입력
        $(importPackageThis.wrapSelector(`.vp-numpy-block-empty-shape-n-array-btn-${stateParamName}`)).click(function() {
            numpyStateGenerator.setState({
                paramData:{
                    [`${stateParamName}`]: [...numpyStateGenerator.getState(stateParamName), ""]
                }
            });

            /**
             * 배열 생성 버튼 삭제 후 다시 렌더링
             */
            numpyPageRenderThis.renderParamOneArrayIndexValueEditor(tagSelector, stateParamName);

        });
    }

    return _renderParamOneArrayIndexValueEditor;
});
