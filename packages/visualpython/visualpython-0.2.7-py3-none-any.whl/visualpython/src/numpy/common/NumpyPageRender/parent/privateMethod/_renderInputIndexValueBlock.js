define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ) {

    /** numpy의 옵션 중 indexValue를 입력하는 블럭을 동적 렌더링하는 메소드
     * numpy의 특정 함수들이 indexValue 옵션을 지정 할 수 도 안할 수도 있다.
     * @param {numpyPageRenderer this} numpyPageRendererThis
     * @param {title} title
     * @param {string || Array<string>} stateParamNameOrArray
    */
    var _renderInputIndexValueBlock = function(numpyPageRendererThis, title, bindFuncData) {
    
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var rootTagSelector = numpyPageRendererThis.getRequiredPageSelector();

        var rootPage = $(importPackageThis.wrapSelector(rootTagSelector));
        var indexValueBlock = $(`<div class="vp-numpy-option-block vp-numpy-${uuid}-block vp-spread" id="vp_blockArea">
                                    <h4>
                                        <div class="vp-panel-area-vertical-btn vp-arrow-up">
                                        </div>
                                        <span class="vp-multilang" data-caption-id="${title}">
                                            ${title}
                                        </span>
                                    </h4>
                                </div>`);
        rootPage.append(indexValueBlock);

        numpyPageRendererThis.renderParamInputArrayEditor(`.vp-numpy-${uuid}-block`, bindFuncData, false)
    
    }

    return _renderInputIndexValueBlock;
});
