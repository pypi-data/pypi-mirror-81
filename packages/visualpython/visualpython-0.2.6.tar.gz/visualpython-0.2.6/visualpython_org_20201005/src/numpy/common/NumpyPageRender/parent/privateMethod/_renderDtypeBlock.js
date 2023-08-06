define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ) {
    /**
     * numpy의 dtype을 선택하는 <div> 블록을 생성하는 렌더링 함수
     * numpy의 모든 함수에서 dtype을 입력받는 state 이름은 dtype이다
     * @param {numpyPageRenderer this} numpyPageRendererThis 
     */
    var _renderDtypeBlock = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
        var optionPageSelector = numpyPageRendererThis.getOptionPageSelector();
        // var rootTagSelector = numpyPageRendererThis.getRootTagSelector();
        var optionPage = $(importPackageThis.wrapSelector(optionPageSelector));
        var numpyDtypeArray = numpyPageRendererThis.numpyDtypeArray;

        /** 제이쿼리로 dtype을 선택하는 <div> 블록 생성*/
        var dtypeBlock = $(`<div class="vp-numpy-option-block vp-spread" id="vp_blockArea">
                                <h4>
                                    <div class="vp-panel-area-vertical-btn vp-arrow-up">
                                    </div>
                                    <span class="vp-multilang" data-caption-id="selectDtype">
                                        Select Dtype
                                    </span>
                                </h4>
                                <select class="vp-numpy-select-dtype" id="vp_numpyDtype-${uuid}">
                                </select>
                            </div>`);
        optionPage.append(dtypeBlock);

        /** src/common/const_numpy.js에서 설정한 dtype 배열 값을 <select>태그 안에 
         * <option>태그 value안에 동적 렌더링 
         */
        numpyDtypeArray.forEach(function (element) {
            $(importPackageThis.wrapSelector(`#vp_numpyDtype-${uuid}`)).append(`<option value="${element.value}"> ${element.name}</option>`)
        });

        /** dtype 선택  이벤트 함수 */
        $(importPackageThis.wrapSelector(`#vp_numpyDtype-${uuid}`)).change(function()  {
            numpyStateGenerator.setState({
                dtype: $(':selected', this).val()
            });
        });
    }
    return _renderDtypeBlock;
});
