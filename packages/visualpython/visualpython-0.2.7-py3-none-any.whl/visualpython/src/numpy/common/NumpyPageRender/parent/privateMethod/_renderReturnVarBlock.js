define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ) {
    /** 
     * return 변수를 편집하는 html태그를 동적 렌더링
     * @param {numpyPageRenderer this} numpyPageRendererThis 
     */
    var _renderReturnVarBlock = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;

        /**
         * return 변수 동적 태그 블럭
         */
        var returnVarBlock  = $(`<div class="vp-numpy-option-block vp-spread" id="vp_blockArea">
                                    <h4>
                                        <div class="vp-panel-area-vertical-btn vp-arrow-up">
                                        </div>
                                        <span class="vp-multilang" data-caption-id="inputReturnVariable">
                                            Input Return Variable
                                        </span>
                                    </h4>

                                    <input type="text" class="vp-numpy-return-input" 
                                                       id="vp_numpyReturnVarInput-${uuid}"
                                                       placeholder="변수 입력"/>
                                    <div class="vp-numpy-style-flex-row">
                                        <input class="vp-numpy-input 
                                                      vp-numpy-input-checkbox" 
                                                id="vp_numpyInputCheckBox-${uuid}" type="checkbox" />
                                        <div class="vp-numpy-input-checkbox-title margin-left-5px">
                                            <span class="vp-multilang" data-caption-id="printReturnVar">
                                                return 변수 출력
                                            </span>
                                        </div>
                                    </div>
                                </div>`);
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
       
        var optionPageSelector = numpyPageRendererThis.getOptionPageSelector();
        // var rootTagSelector = numpyPageRendererThis.getRootTagSelector();
        var optionPage = $(importPackageThis.wrapSelector(optionPageSelector));
        optionPage.append(returnVarBlock);

        /** return 변수 입력 */
        $(importPackageThis.wrapSelector(`#vp_numpyReturnVarInput-${uuid}`)).on("change keyup paste", function() {
            numpyStateGenerator.setState({
                returnVariable: $(this).val()
            });
        });

        // return 변수 print 여부 선택
        $(importPackageThis.wrapSelector(`#vp_numpyInputCheckBox-${uuid}`)).click(function() {
            numpyStateGenerator.setState({
                isReturnVariable: $(this).is(":checked")
            });
        });                
    }

    return _renderReturnVarBlock;
});