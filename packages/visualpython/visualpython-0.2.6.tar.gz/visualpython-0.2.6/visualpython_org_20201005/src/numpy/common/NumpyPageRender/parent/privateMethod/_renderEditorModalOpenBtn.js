define ([    
    'nbextensions/visualpython/src/common/constant'
    // + 추가 numpy 폴더  패키지 : 이진용 주임
    , 'nbextensions/visualpython/src/numpy/api/numpyStateApi' 

    , 'nbextensions/visualpython/src/component/oneArrayEditor/index'
    , 'nbextensions/visualpython/src/component/twoArrayEditor/index'
    , 'nbextensions/visualpython/src/component/threeArrayEditor/index'
], function( vpConst
            , numpyStateApi
            , oneArrayEditorFuncList, twoArrayEditorFuncList, threeArrayEditorFuncList){
    var _renderEditorModalOpenBtn = function (numpyPageRenderThis, baseDom, buttonTagSelector, funcId, flexType, stateParamName, tagSelector) {
        var numpyPageRenderThis = numpyPageRenderThis;
        var importPackageThis = numpyPageRenderThis.getImportPackageThis();;


        // funcId에 따른 html과 데이터 switch 선택
        var componentPath = ``;
        var funcList;
        switch(funcId) {
            // src/component/oneArrayEditor
            case "JY901":{
                componentPath = "component/oneArrayEditor/index.html";
                funcList = oneArrayEditorFuncList;
                break;
            }
            // src/component/twoArrayEditor
            case "JY902":{
                componentPath = "component/twoArrayEditor/index.html";
                funcList = twoArrayEditorFuncList;
                break;
            }
            // src/component/threeArrayEditor
            case "JY903":{
                componentPath = "component/threeArrayEditor/index.html";
                funcList = threeArrayEditorFuncList;
                break;
            }
            default: {
                break;
            }
        }

        /** open twoArrayModalEditor 버튼 렌더링 */
        var openButton = $(`<div class="vp-numpy-open-arrayEditor-btn-container-${stateParamName} 
                                        vp-numpy-style-flex-row-end">
                                <button class="vp-numpy-func_btn ${buttonTagSelector}"
                                         style="padding: 1rem;">
                                    <span class="vp-multilang" data-caption-id="numpyViewLarger">
                                        크게보기
                                    </span>
                                </button>
                            </div>`);
        baseDom.append(openButton);
     
        /** array editor 모달창 클릭 */
        $(importPackageThis.wrapSelector(`.${buttonTagSelector}`)).click(  function() {
            var loadURLstyle = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH;
            var loadURLhtml = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.SOURCE_PATH + componentPath;
            
            importPackageThis.loadCss( loadURLstyle + "component/fileNavigation.css");
    
             $(`<div id="vp_fileNavigation"></div>`)
                    .load(loadURLhtml, () => {
    
                        $('#vp_fileNavigation').removeClass("hide");
                        $('#vp_fileNavigation').addClass("show");
                        
                        /**  oneArrayEditor, twoArrayEditor, threeArrayEditor가 가지고 있는
                             initEditor 와 bindEventFunctions의 함수 이름은 다 동일 하지만
                             함수가 구현하는 내용이 다르다
                        */
                        var { initEditor
                              , bindEventFunctions } = funcList;
                        
                        // array editor 모달창 생성에 필요한 this와 데이터들을 인자로 전달
                        initEditor(numpyPageRenderThis, stateParamName);
                        bindEventFunctions(stateParamName, tagSelector);
                    })
                    .appendTo("#site");
        });
    }

    return _renderEditorModalOpenBtn;
});
