define([], function () {
    var FileNavigationState = function() {
        this.importPackageThis;
        this.fileNavigatiotype;
        this.baseDirStr = '';
        this.notebookPathStr = '';
        this.notebookFolder = '';
        this.currentDirStr = '';
        this.baseFolderStr = '';
        this.currentFolderStr = '';
        this.nodebookPathStr = '';
        this.relativePathStr = '';
        this.dirHistoryStack = [];
        this.fileOptionData = {};
        this.visualpythonFileName = ``;
    }
    FileNavigationState.prototype.setImportPackageThis = function(importPackageThis) {
        this.importPackageThis = importPackageThis;
    }

    FileNavigationState.prototype.getImportPackageThis = function() {
        return this.importPackageThis;
    }

    FileNavigationState.prototype.setFileNavigationtype = function(paramFileNavigatiotype) {
        this.fileNavigatiotype = paramFileNavigatiotype;
    }
    FileNavigationState.prototype.getFileNavigationtype = function() {
        return this.fileNavigatiotype;
    }
    FileNavigationState.prototype.setBaseDirStr = function(paramBaseDirStr) {
        this.baseDirStr = paramBaseDirStr;
    }
    FileNavigationState.prototype.setBaseFolderStr = function(paramBaseFolderStr) {
        this.baseFolderStr = paramBaseFolderStr;
    }
    FileNavigationState.prototype.setCurrentDirStr = function(paramCurrentDirStr) {
        this.currentDirStr = paramCurrentDirStr;
    }
    FileNavigationState.prototype.setCurrentFolderStr = function(paramCurrentFolderStr) {
        this.currentFolderStr = paramCurrentFolderStr;
    }
    FileNavigationState.prototype.setRelativePathStr = function(paramRelativePathStr) {
        this.relativePathStr = paramRelativePathStr;
    }

    FileNavigationState.prototype.setNotebookPathStr = function(notebookPathStr) {
        this.notebookPathStr = notebookPathStr;
    }

    FileNavigationState.prototype.setVisualPythonFileName = function(visualpythonFileName) {
        this.visualpythonFileName = visualpythonFileName;
    }

    FileNavigationState.prototype.setNotebookFolder = function(notebookFolder) {
        this.notebookFolder = notebookFolder; 
    }
    FileNavigationState.prototype.getVisualPythonFileName = function() {
        return this.visualpythonFileName;
    }
    
    FileNavigationState.prototype.getBaseDirStr = function() {
        return this.baseDirStr;
    }
    FileNavigationState.prototype.getBaseFolderStr = function() {
        return this.baseFolderStr;
    }
    FileNavigationState.prototype.getCurrentDirStr = function() {
        return this.currentDirStr;
    }
    FileNavigationState.prototype.getCurrentFolderStr = function() {
        return this.currentFolderStr;
    }
    FileNavigationState.prototype.getRelativePathStr = function() {
        return this.relativePathStr;
    }

    FileNavigationState.prototype.getDirHistoryStack = function() {
        return this.dirHistoryStack;
    }
    
    FileNavigationState.prototype.getNotebookPathStr = function() {
        return this.notebookPathStr;
    }

    FileNavigationState.prototype.getNotebookFolder = function() {
        return this.notebookFolder;
    }

    FileNavigationState.prototype.pushDirHistoryStack = function(dirInfo) {
        this.dirHistoryStack.push(dirInfo);
    }
    
    //  이전 디렉토리 검색 history stack에 최신 데이터를 pop합니다
    FileNavigationState.prototype.popDirHistoryStackAndGetPopedData = function() {
        if (this.dirHistoryStack.length < 1) {
            return;
        }
        return this.dirHistoryStack.pop();
    }
    
    // 이전 디렉토리 검색 history stack을 리셋합니다
    FileNavigationState.prototype.resetStack = function() {
        this.dirHistoryStack = [];
    }
    
    // importCsv 페이지의 csvOptionData를 set합니다
    FileNavigationState.prototype.setFileOptionData = function(paramCsvOption) {
        this.fileOptionData = paramCsvOption;
    }
    
    // importCsv 페이지의 csvOptionData를 가져옵니다
    FileNavigationState.prototype.getFileOptionData = function() {
        return this.fileOptionData;
    }

    // 현재 이동한 경로를 history stack에 집어 넣고, 절대 경로를 상대 경로로 바꿔 저장한다.
    FileNavigationState.prototype.splitPathStrAndSetStack = function(dirObj, resultInfoArr ,renderDomType){
        var currentDirStr = resultInfoArr[0].current.split('//').join('/');
        var splitedDirStrArr = currentDirStr.split('/');
        var rootFolderName = splitedDirStrArr[splitedDirStrArr.length - 1];

        var firstIndex = currentDirStr.indexOf( this.getNotebookFolder() );

        var currentRelativePathStr = '';
        if ( firstIndex === -1 ) {
            currentRelativePathStr = currentDirStr.substring(this.getNotebookPathStr().length + 1, currentDirStr.length);
        } else {
            currentRelativePathStr = currentDirStr.substring(firstIndex, currentDirStr.length); 
        }

        if ((dirObj.direction === 'before' || dirObj.direction === 'to')) {
            var stackData = {
                prev: this.getCurrentDirStr(),
                next: currentDirStr
            }
            this.pushDirHistoryStack(stackData);
        }

        return {
            currentDirStr,
            currentRelativePathStr,
            rootFolderName
        }
    }

    return FileNavigationState;
});
