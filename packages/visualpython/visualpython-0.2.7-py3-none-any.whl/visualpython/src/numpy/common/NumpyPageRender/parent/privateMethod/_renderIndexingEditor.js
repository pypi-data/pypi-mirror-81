define ([    
    // + 추가 numpy 폴더  패키지 : 이진용 주임
    'nbextensions/visualpython/src/numpy/api/numpyStateApi' 
], function( numpyStateApi ){
    var { updateOneArrayIndexValueAndGetNewArray, 
          deleteOneArrayIndexValueAndGetNewArray,
          updateTwoArrayIndexValueAndGetNewArray,
          deleteTwoArrayIndexValueAndGetNewArray,
          fixNumpyParameterValue } = numpyStateApi;

    //FIXME: 제거하고 새로 만들 예정
    var _renderIndexingEditor = function(numpyPageRenderThis, tagSelector, stateParamName) {
        var numpyPageRenderThis = numpyPageRenderThis;
        var importPackageThis = numpyPageRenderThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRenderThis.getStateGenerator();
        var editorDom = $(importPackageThis.wrapSelector(tagSelector));
        editorDom.empty();

        var indexingArray = numpyStateGenerator.getState(stateParamName);
        /**
         * indexingArray 배열의 인덱스 갯수만큼 for문 돌아 편집기 생성
         */
        for (var i = 0; i < indexingArray.length; i++) {
            (function(a) {
                var outerDom = $(`<div>
                                    <div style=" font-size: 15px; padding: 0.5rem;">
                                        n${a+1} [] Indexing
                                    </div>
                                    <div class="flex-column" style="width: 90%;">
                                        <div style="font-weight: 700; font-size: 20px; padding: 0 1rem;">[</div>
                                            <div class="vp-numpy-indexing-1-${a+1}-container-${stateParamName} flex-row" style="width:100%;">                 
                                            </div>
                                        <div style="font-weight: 700; font-size: 20px; padding: 0 1rem;">]</div>
                                    </div>
                                    <div class="flex-row">
                                        <div class="vp-numpy-indexing-1-btn-${a+1}" style="margin-left:5px;">
                                            <button class="vp-numpy-func_btn black" style="padding:1rem;">+추가</button>
                                        </div>
                                        <button class="vp-numpy-indexing-1-delete-btn-${a+1} vp-numpy-func_btn" style="padding:1rem;">x</button>
                                    </div>
                                </div>`);
                editorDom.append(outerDom);

                // n차원 안에 인덱스 요소 생성
                $(importPackageThis.wrapSelector(`.vp-numpy-indexing-1-btn-${a+1}`)).click(function() {
                    indexingArray[a].push({
                        value:"0",
                        operator:"",
                        isDisable: false
                    });
                    numpyPageRenderThis.renderIndexingEditor(tagSelector, stateParamName);
               
                });

                // n차원 삭제
                $(importPackageThis.wrapSelector(`.vp-numpy-indexing-1-delete-btn-${a+1}`)).click(function() {
                    numpyStateGenerator.setState({
                        paramData: {
                            [`${stateParamName}`]: deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName),a)
                        }
                    });
                    numpyPageRenderThis.renderIndexingEditor(tagSelector, stateParamName);
                });

                var container = $(importPackageThis.wrapSelector(`.vp-numpy-indexing-1-${a+1}-container-${stateParamName}`));

                for (var j = 0; j < indexingArray[a].length; j++) {
                    ((b) =>  {
                        var forwardDom = "";
                        var backwardDom = "";

                        // 전처리 작업
                        // index b가 짝수 일때
                        if (b % 2 === 0 ) {
                            if (b > 0) {
                                forwardDom = `<select class="vp-numpy-indexing-2-${a}-${b}-operator-select"
                                                   style=" font-size: 16px; padding: 0 1rem;" 
                                                   ${indexingArray[a][b].isDisable === true ? 'disabled': ''}>
                                                <option value="" ${indexingArray[a][b].operator === "" ? 'selected': ''}>선택</option>
                                                <option value=":" ${indexingArray[a][b].operator === ":" ? 'selected': ''}>:</option>
                                                <option value="<" ${indexingArray[a][b].operator === "<" ? 'selected': ''}><</option>
                                                <option value="<=" ${indexingArray[a][b].operator === "<=" ? 'selected': ''}><=</option>
                                                <option value=">" ${indexingArray[a][b].operator === ">" ? 'selected': ''}>></option>
                                                <option value=">=" ${indexingArray[a][b].operator === ">=" ? 'selected': ''}>>=</option>
                                                <option value="," ${indexingArray[a][b].operator === "," ? 'selected': ''}>,</option>
                                                <option value="&" ${indexingArray[a][b].operator === "&" ? 'selected': ''}>&</option>
                                                <option value="|" ${indexingArray[a][b].operator === "|" ? 'selected': ''}>|</option>
                                            </select>

                                            <span class="flex-column-center" 
                                                  style="font-weight: 700; font-size: 20px; padding: 0 1rem;">(</span>`;
                            } else {
                                forwardDom = `<span class="flex-column-center" 
                                                 style="font-weight: 700; font-size: 20px; padding: 0 1rem;">(</span>`;
                            }
              
                        } else {
                            forwardDom = `<select class="vp-numpy-indexing-2-${a}-${b}-operator-select" 
                                              style=" font-size: 16px; padding: 0 1rem;"
                                              ${indexingArray[a][b].isDisable === true ? 'disabled': ''}>
                                        <option value="" ${indexingArray[a][b].operator === "" ? 'selected': ''}>선택</option>
                                        <option value=":" ${indexingArray[a][b].operator === ":" ? 'selected': ''}>:</option>
                                        <option value="<" ${indexingArray[a][b].operator === "<" ? 'selected': ''}><</option>
                                        <option value="<=" ${indexingArray[a][b].operator === "<=" ? 'selected': ''}><=</option>
                                        <option value=">" ${indexingArray[a][b].operator === ">" ? 'selected': ''}>></option>
                                        <option value=">=" ${indexingArray[a][b].operator === ">=" ? 'selected': ''}>>=</option>
                                        <option value="," ${indexingArray[a][b].operator === "," ? 'selected': ''}>,</option>
                                        <option value="&" ${indexingArray[a][b].operator === "&" ? 'selected': ''}>&</option>
                                        <option value="|" ${indexingArray[a][b].operator === "|" ? 'selected': ''}>|</option>
                                    </select>`;
                            backwardDom = `<span class="flex-column-center" 
                                              style="font-weight: 700; font-size: 20px; padding: 0 1rem;">)</span>`;
                        }

                        var innerDom;
                        // b가 홀수 일때
                        if (b % 2 !== 0) {
                            innerDom = $(`<div class="flex-row"> 
                                            ${forwardDom}
                                            <span class="flex-column-center"
                                                   style="font-size: 10px; padding: 0 0.5rem;">${b+1}</span>
                                            <input class="vp-numpy-indexing-2-${a}-${b}-input" 
                                                   style="width: 60px;"
                                                   type="text" 
                                                   value="${indexingArray[a][b].value}"
                                                   ${indexingArray[a][b].isDisable === true ? 'disabled': ''} />
                                            <button class="vp-numpy-indexing-2-toggle-btn-${a+1}-${b+1} vp-numpy-func_btn" 
                                                    style="padding:1rem;">
                                                    ${indexingArray[a][b].isDisable === true ? 'show': 'hide'}
                                            </button>
                                            <button class="vp-numpy-indexing-2-delete-btn-${a+1}-${b+1}  vp-numpy-func_btn" 
                                                    style="padding:1rem;">x</button>
                                         </div>${backwardDom}`);
                        // b가 짝수 일때
                        } else {
                            innerDom = $(`<div class="flex-row"> 
                                            ${forwardDom}
                                            <span class="flex-column-center"
                                                  style="font-size: 10px; padding: 0 0.5rem;">${b+1}</span>
                                            <input class="vp-numpy-indexing-2-${a}-${b}-input" 
                                                   style="width: 60px;"
                                                   type="text" 
                                                   value="${indexingArray[a][b].value}"
                                                   ${indexingArray[a][b].isDisable === true ? 'disabled': ''}/>
                                            <button class="vp-numpy-indexing-2-delete-btn-${a+1}-${b+1} vp-numpy-func_btn" 
                                                    style="padding:1rem;">x</button>
                                         </div>${backwardDom}`); 
                        }
                       
                        container.append(innerDom);

                        // 값 변경
                        $(importPackageThis.wrapSelector(`.vp-numpy-indexing-2-${a}-${b}-input`)).on("change keyup paste", function() {
                            indexingArray[a][b].value = $(this).val();
                        });

                        // 연산자 변경
                        $(importPackageThis.wrapSelector(`.vp-numpy-indexing-2-${a}-${b}-operator-select`)).change(function() {
                            indexingArray[a][b].operator = $(':selected', this).val();
                           
                        });

                        // toggle isDisable
                        $(importPackageThis.wrapSelector(`.vp-numpy-indexing-2-toggle-btn-${a+1}-${b+1}`)).click(function() {
                            if ($(this).hasClass("vp-numpy-isDisable")) {
                                $(this).removeClass("vp-numpy-isDisable");
                                $(this).text("hide");
                                indexingArray[a][b].isDisable = false;
                                $(importPackageThis.wrapSelector(`.vp-numpy-indexing-2-${a}-${b}-operator-select`)).attr("disabled",false);
                                $(importPackageThis.wrapSelector(`.vp-numpy-indexing-2-${a}-${b}-input`)).attr("disabled",false);
                            } else {
                                $(this).addClass("vp-numpy-isDisable");
                                $(this).text("show");
                                indexingArray[a][b].isDisable = true;
                                $(importPackageThis.wrapSelector(`.vp-numpy-indexing-2-${a}-${b}-operator-select`)).attr("disabled",true);
                                $(importPackageThis.wrapSelector(`.vp-numpy-indexing-2-${a}-${b}-input`)).attr("disabled",true);
                            }
                        });
                        
                        // 삭제
                        $(importPackageThis.wrapSelector(`.vp-numpy-indexing-2-delete-btn-${a+1}-${b+1}`)).click(function() {
                            var tempNarray = deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName)[a], b);
                            numpyStateGenerator.setState({
                                paramData: {
                                    [`${stateParamName}`]: updateOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName),a, tempNarray)
                                }
                            })
                            numpyPageRenderThis.renderIndexingEditor(tagSelector, stateParamName);
                        });

                    })(j);
                }

            })(i);
        }

        editorDom.parent().find(`.vp-numpy-indexing-1-func-btn-${stateParamName}`).remove();
        var button = $(`<button class="vp-numpy-indexing-1-func-btn vp-numpy-indexing-1-func-btn-${stateParamName} vp-numpy-func_btn black" 
                            style="width: 100%; padding: 1rem;" >
                            <span class="vp-multilang" data-caption-id="numpyPlusDimention">
                                + 차원
                            </span>
                        </button>`);
        editorDom.parent().append(button);
        $(importPackageThis.wrapSelector(`.vp-numpy-indexing-1-func-btn-${stateParamName}`)).click(function() {
            numpyStateGenerator.setState({
                paramData:{
                    [`${stateParamName}`]: [...numpyStateGenerator.getState(stateParamName), []]
                }
            });
            numpyPageRenderThis.renderIndexingEditor(tagSelector, stateParamName);
        });
    }

    return _renderIndexingEditor;
});
