define ([     
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ) {
    /**
     * _renderSelectAxisBlock
     * numpy 옵션 Axis를 편집하는 html태그를 동적 렌더링
     * @param {numpyPageRenderer this} numpyPageRendererThis 
     */
    var _renderSelectAxisBlock = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
        var numpyAxisArray = numpyPageRendererThis.numpyAxisArray;
        
        var optionPageSelector = numpyPageRendererThis.getOptionPageSelector();
        // var rootTagSelector = numpyPageRendererThis.getRootTagSelector();
        var optionPage = $(numpyPageRendererThis.importPackageThis.wrapSelector(optionPageSelector));

        /**
         *  indexNBlock
         *  Axis 편집 동적 태그 블럭
         */
        var indexNBlock = $(`<div class="vp-numpy-option-block vp-spread" id="vp_blockArea">
                                <h4>
                                    <div class="vp-panel-area-vertical-btn vp-arrow-up">
                                    </div>
                                    <span class="vp-multilang" data-caption-id="Select Axis">
                                        Select Axis
                                    </span>
                                </h4>
                                <select class="vp-numpy-select-indexN" id="vp_numpyIndexN-${uuid}">
                                </select>
                            </div>`);

        optionPage.append(indexNBlock);

        /**
         * numpyAxis 배열을 option 태그에 동적 렌더링 
         */ 
        numpyAxisArray.forEach((element) => {
            $(importPackageThis.wrapSelector(`#vp_numpyIndexN-${uuid}`)).append(`<option value="${element}"> ${element}</option>`)
        });

        /**
         * Axis change 이벤트 함수
         */
        $(importPackageThis.wrapSelector(`#vp_numpyIndexN-${uuid}`)).change(function() {
            numpyStateGenerator.setState({
                axis: $(':selected', this).val()
            });
        });
    }
    return _renderSelectAxisBlock;
});
