define([], function () {
    var OneArrayEditorState = function() {
        this.numpyPageRendererThis;
        this.prevUUID;
        this.currUUID;
    }

    OneArrayEditorState.prototype.setNumpyPageRendererThis = function(numpyPageRendererThis) {
        this.numpyPageRendererThis = numpyPageRendererThis;
    }

    OneArrayEditorState.prototype.getNumpyPageRendererThis = function() {
        return this.numpyPageRendererThis;
    }

    return OneArrayEditorState;
});