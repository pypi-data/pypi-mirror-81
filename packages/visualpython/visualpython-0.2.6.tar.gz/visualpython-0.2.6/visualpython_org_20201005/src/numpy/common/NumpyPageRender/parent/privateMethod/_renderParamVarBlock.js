define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ) {
    /** paramVariable 변수 입력 <div> 블록을 동적 렌더링하는 메소드
     * @param {numpyPageRenderer this} numpyPageRendererThis 
     */
    var _renderParamVarBlock = function(numpyPageRendererThis, title) {
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
        var rootTagSelector = numpyPageRendererThis.getRequiredPageSelector();
        var paramVarBlock = $(`<div class="vp-numpy-option-block vp-spread" id ="vp_blockArea">
                                    <h4>
                                        <div class="vp-panel-area-vertical-btn vp-arrow-up">
                                        </div>
                                        <span class="vp-multilang" data-caption-id="InputParameter">
                                            ${title || `Input Parameter Variable`}
                                        </span>
                                    </h4>

                                    <input type="text" class="vp-numpy-input vp-numpy-paramVar-input" 
                                           id="vp_numpyParamVarInput-${uuid}"
                                           placeholder="변수 입력"/>
                                </div>`);

        var optionPage = $(importPackageThis.wrapSelector(rootTagSelector));
        optionPage.append(paramVarBlock);

        /** paramVariable 변수 입력 */
        $(importPackageThis.wrapSelector(`#vp_numpyParamVarInput-${uuid}`)).on("change keyup paste", function() {
            numpyStateGenerator.setState({
                paramVariable: $(this).val()
            });
        });
    }

    return _renderParamVarBlock;
});
