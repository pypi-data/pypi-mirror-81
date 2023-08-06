define([

], function () {
    const ENUM_RENDER_DOM_TYPE = {
        TAB: 0,
        BODY: 1,
        INIT: 2
    }
    /** 
    before 상위 디렉토리 검색
    to 특정 폴더 디렉토리 검색
    prev 이전 디렉토리 검색
    init 파일네비게이션 처음 시작할 때 기본 디렉토리 검색
    */
    const ENUM_FOLDER_DIRECTION = {
        BEFORE: 0,
        TO: 1,
        PREV: 2,
        INIT: 3
    }
    /**
     * 
     */
    const ENUM_FOLDER_DIRECTION = {
        IMPORT_CSV: 0,
        IMMORT_VisualPython: 1,
        SAVE_VisualPython: 2,
    }
    return {
        ENUM_RENDER_DOM_TYPE
        , ENUM_FOLDER_DIRECTION
    }
});