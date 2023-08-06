define([], function () {
    var ThreeArrayEditorState = function() {
        this.numpyPageRendererThis;
    }

    ThreeArrayEditorState.prototype.setNumpyPageRendererThis = function(numpyPageRendererThis) {
        this.numpyPageRendererThis = numpyPageRendererThis;
    }

    ThreeArrayEditorState.prototype.getNumpyPageRendererThis = function() {
        return this.numpyPageRendererThis;
    }
    
    return ThreeArrayEditorState;
});