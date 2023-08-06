define([], function () {
    var TwoArrayEditorState = function() {
        this.numpyPageRendererThis;
    }

    TwoArrayEditorState.prototype.setNumpyPageRendererThis = function(numpyPageRendererThis) {
        this.numpyPageRendererThis = numpyPageRendererThis;
    }

    TwoArrayEditorState.prototype.getNumpyPageRendererThis = function() {
        return this.numpyPageRendererThis;
    }
    
    return TwoArrayEditorState;
});