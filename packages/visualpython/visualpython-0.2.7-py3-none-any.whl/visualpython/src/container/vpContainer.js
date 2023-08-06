define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpXMLHandler'
    , 'nbextensions/visualpython/src/pandas/fileNavigation/index'
], function (requirejs, $, vpCommon, vpConst, xmlHandler, fileNavigation) {
    "use strict";
    
    /* 전역 변수 영역 */
    let xmlLibraries;
    let loadedFuncJS;
    let generatedCode;
    let generatedMetaData;
    let loadedFuncID;
    let nodeIndex = 0;
    let sb = requirejs(vpConst.BASE_PATH + vpConst.SOURCE_PATH + "common/StringBuilder");
    var events;

    try {
        // events 에 대한 예외 발생 가능할 것으로 예상.
        events = requirejs('base/js/events');
    } catch (err) {
        if (window.events === undefined) {
            var Events = function () { };
            window.events = $([new Events()]);
        }
        events = window.events;
    }

    /**
     * FIXME: 개발 임시 로그.
     * @param {String} str 로그 내용
     * @param {boolean} alrt 알림 사용 여부(true : 알림)
     */
    var mylog = function(str, alrt = false) {
        console.log("Log in vp cont >>> " + str);
        if (alrt) {
            alert(str);
        }
    }

    /* actions */

    /**
     * 모드 셀렉트 화면으로 이동
     */
    var openModeSelector = function() {
        $(vpCommon.wrapSelector(vpConst.VP_BODY_CONTAINER)).children("div").hide();
        $(vpCommon.wrapSelector(vpConst.PAGE_MODE_SELECTOR)).show();
    }

    /**
     * API 모드로 이동 - API Browser open
     */
    var openAPIBrowser = function() {
        $(vpCommon.wrapSelector(vpConst.VP_BODY_CONTAINER)).children("div").hide();
        $(vpCommon.wrapSelector(vpConst.PAGE_API_BROWSER)).show();
        $(vpCommon.wrapSelector(vpConst.PAGE_API_BROWSER))
            .css('height', $(vpCommon.getVPContainer()).height() - $(vpCommon.wrapSelector(vpConst.PAGE_API_BROWSER)).position().top);
    }

    /**
     * 라이브러리 옵션모드 이동
     */
    var openOptionBook = function() {
        $(vpCommon.wrapSelector(vpConst.VP_BODY_CONTAINER)).children("div").hide();
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).show();
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTROL_PANEL)).show();
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER))
            .css('height', $(vpCommon.getVPContainer()).height() - $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).position().top
            - $(vpCommon.wrapSelector(vpConst.OPTION_CONTROL_PANEL)).height());
    }

    /**
     * load libraries data
     */
    var loadLibraries = function() {
        var libraryURL = window.location.origin + vpConst.PATH_SEPARATOR + vpConst.BASE_PATH + vpConst.DATA_PATH + vpConst.VP_LIBRARIES_XML_URL;
        xmlLibraries = new xmlHandler.VpXMLHandler(libraryURL);
        xmlLibraries.loadFile(libraryLoadCallback);
    }

    /**
     * library load complete callback
     */
    var libraryLoadCallback = function() {
        $(vpCommon.wrapSelector(vpConst.PAGE_API_BROWSER)).append(bindNavigatorButtons($(xmlLibraries.getXML()).children(vpConst.LIBRARY_ITEM_WRAP_NODE)));
        // bindSearchAutoComplete();
    }

    /**
     * Navigator area initialize
     * @param {xmlNode} node mother node for binding
     */
    var bindNavigatorButtons = function(node) {
        var container = $(vpCommon.wrapSelector(vpConst.PAGE_API_BROWSER));
        // $(container).empty();
        var sbNaviItems = new sb.StringBuilder();

        // 하위 그룹 바인딩
        $(node).children(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_PACKAGE + "]").each(function() {
            sbNaviItems.appendLine(makeNavigatorGroupTag($(this)));
            
            sbNaviItems.appendLine(bindNavigatorButtons($(this)));
            
            // 하위 함수 바인딩
            $(this).children(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_FUNCTION + "]").each(function() {
                sbNaviItems.appendLine(makeNavigatorFunctionButton($(this)));
            });
            
            sbNaviItems.appendLine("</div>");
        });
        
        return sbNaviItems.toString();
    }

    /**
     * create navigator group button
     * @param {xmlNode} node library item for create button
     * @returns html tag string
     */
    var makeNavigatorGroupTag = function(node) {
        var sbGrpNode = new sb.StringBuilder();
        sbGrpNode.appendFormatLine("<div class='{0}' {1}>"
            , vpConst.API_GROUP_BOX.replace(".", ""), ($(node).attr("level") == 0) ? "" : "style='display:none;'");
        sbGrpNode.appendFormatLine("<div><span class='{0} {1}'></span>"
            , vpConst.NAVI_GROUP_TOGGLE.replace(".", ""), vpConst.ARROW_BTN_RIGHT);
        sbGrpNode.appendFormatLine("<span>{0}</span><br/></div>", $(node).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));

        return sbGrpNode.toString();
    }
    
    /**
     * create navigator group button
     * @param {xmlNode} node library item for create button
     * @returns html tag string
     */
    var makeNavigatorFunctionButton = function(node) {
        var sbFuncNode = new sb.StringBuilder();
        sbFuncNode.appendFormat("<button class='vp-btn {0} {1}' type='button' style='display:none;' {2}='{3}' title='{4}'>"
            , vpConst.NAVI_FUNCION_BUTTON.replace(".", ""), "btn-gray"
            , vpConst.LIBRARY_ITEM_DATA_ID, $(node).attr(vpConst.LIBRARY_ITEM_ID_ATTR)
            , $(node).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
        sbFuncNode.appendFormat("<span>{0}</span>", $(node).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
        sbFuncNode.appendLine("</button>");

        return sbFuncNode.toString();
    }

    /**
     * 네비게이션 그룹 표시 토글
     * @param {HTMLtag} btn 
     */
    var toggleNaviGroupShow = function(btn) {
        if ($(btn).hasClass(vpConst.ARROW_BTN_RIGHT)) {
            $(btn).parent().parent().children().show();
            $(btn).toggleClass(vpConst.ARROW_BTN_RIGHT).toggleClass(vpConst.ARROW_BTN_DOWN);
        } else {
            $(btn).parent().parent().children(":gt(0)").hide();
            $(btn).toggleClass(vpConst.ARROW_BTN_RIGHT).toggleClass(vpConst.ARROW_BTN_DOWN);
        }
    }

    /**
     * 노드 에디터 모드 오픈
     */
    var openAPIBlock = function() {
        // $(vpCommon.wrapSelector(vpConst.VP_BODY_CONTAINER)).children("div").hide();
        // $(vpCommon.wrapSelector(vpConst.NODE_EDIT_PALETTE)).show();
        // $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).show();
        // $(vpCommon.wrapSelector(vpConst.OPTION_CONTROL_PANEL)).show();
        // $(vpCommon.wrapSelector(vpConst.NODE_EDIT_PALETTE))
        //     .css('height', ($(vpCommon.getVPContainer()).height() - $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).position().top) / 2);
        // $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER))
        //     .css('height', $(vpCommon.getVPContainer()).height() - $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).position().top
        //     - $(vpCommon.wrapSelector(vpConst.OPTION_CONTROL_PANEL)).height());
        // //FIXME:
        loadOption("api_block", optionPageLoadCallback);
    }

    /**
     * 옵션 페이지 로드
     * @param {String} funcID xml 함수 id
     * @param {function} callback 로드 완료시 실행할 함수
     */
    var loadOption = function(funcID, callback) {
        var loadUrl = getOptionPageURL(funcID);
        // 옵션 페이지 url 로딩이 정상처리 된 경우 js 파일 로드
        if (loadUrl !== "") {
            // 옵션 로드
            loadedFuncID = funcID;
            generatedCode = undefined;
            requirejs([loadUrl], function (loaded) {
                loaded.initOption(callback);
            });
        }
    }

    /**
     * 옵션 페이지 URL 조회
     * @param {*} funcID xml 함수 id
     * @param {object} taskObj saved task TODO: 현재 미정.
     */
    var getOptionPageURL = function(funcID, taskObj) {
        var sbURL = new sb.StringBuilder();
        sbURL.clear();
        sbURL.append(Jupyter.notebook.base_url);
        sbURL.append(vpConst.BASE_PATH);
        sbURL.append(vpConst.SOURCE_PATH);
        // 함수 경로 바인딩
        var optionData = $(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + funcID + "]");
        var filePath = $(optionData).find(vpConst.LIBRARY_ITEM_FILE_URL_NODE).text();
            
        // 경로가 조회되지 않는 경우
        if (filePath === undefined || filePath === "") {
            alert("Function id not founded!");
            return "";
        }

        sbURL.append(filePath);
        return sbURL.toString();
    }

        
    /**
     * 옵션 페이지 로드 완료 callback.
     * @param {funcJS} funcJS 옵션 js 객체
     */
    var optionPageLoadCallback = function(funcJS) {
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).children(vpConst.OPTION_PAGE).remove();

        loadedFuncJS = funcJS;
        makeUpGreenRoomHTML();
    }
    
    var optionPageLoadCallbackAndLoad = function(funcJS) {
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).children(vpConst.OPTION_PAGE).remove();

        loadedFuncJS = funcJS;
        
        loadedFuncJS.loadMeta(loadedFuncJS, generatedMetaData);
        makeUpGreenRoomHTML();
    }

    /**
     * 옵션 페이지 html 처리 및 헤더 바인딩
     */
    var makeUpGreenRoomHTML = function() {
        $(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM, vpConst.OPTION_PAGE)).each(function() {
            $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).append($(this));
        });
        openOptionBook();
        $(vpCommon.wrapSelector(vpConst.OPTION_PAGE + (":gt(0)"), "h3")).hide();
    }

    /**
     * 제네레이트 코드 셀에 추가. true 인 경우 바로 셀 실행
     * @param {boolean} run 실행여부
     */
    var addLibraryToJupyterCell = function(run) {
        // TODO: valitate
        if (!loadedFuncJS.optionValidation()) {
            return false;
        }
        // TODO: 타스크 추가
        loadedFuncJS.funcID = loadedFuncID;
        loadedFuncJS.generateCode(run);
        generatedCode = loadedFuncJS.generatedCode;
        generatedMetaData = loadedFuncJS.metadata;

        if (generatedCode === "BREAK_RUN") {
            // alert("Error occurred during add task. Request breaked.");
            console.log("[vp] Error occurred during add task. Request breaked.");
            // console.warn("generated code is undefined");
            return false;
        }
        
        // closeLibraryOption();
    }

    /**
     * 옵션 페이지 닫고 홈으로 이동
     */
    var closeLibraryOption = function() {
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).children(vpConst.OPTION_PAGE).remove();
        loadedFuncJS = null;
        openAPIBrowser();
    }

    /**
     * 템플릿 영역 클리어
     */
    var clearNoteArea = function() {
        $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER, vpConst.NOTE_NODE_CLASS)).remove();
        nodeIndex = 0;
    }

    /**
     * 템플릿 영역 오픈
     */
    var openNoteArea = function() {
        // loadedFuncJS.metaTest();
        $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).show();
        $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER))
            .css('height', $(vpCommon.getVPContainer()).height() - $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).position().top);
        console.log($(vpCommon.getVPContainer()).width() / 3);
        if ($(vpCommon.getVPContainer()).width() / 3 > 200) {
            $(vpCommon.wrapSelector(vpConst.VP_BODY_CONTAINER)).css('width', $(vpCommon.getVPContainer()).width() / 3 * 2);
            $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).css('width', $(vpCommon.getVPContainer()).width() / 3);
        } else {
            $(vpCommon.wrapSelector(vpConst.VP_BODY_CONTAINER)).css('width', $(vpCommon.getVPContainer()).width() - 200);
            $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).css('width', 200);
        }
    }

    /**
     * 노트 노드 추가
     * @param {string} gCode generated code
     * @param {string} gMeta generated meta
     */
    var addNoteNode = function(gCode, gMeta) {
        var sbNoteNode = new sb.StringBuilder();
        sbNoteNode.appendFormatLine("<div class='{0}'>", vpConst.NOTE_NODE_CLASS.replace(".", ""));
        sbNoteNode.appendFormatLine("<span class='{0}'>Node {1}</span>", vpConst.NOTE_NODE_INDEX.replace(".", ""), ++nodeIndex);
        sbNoteNode.appendFormat("<select class='{0}'>", vpConst.NOTE_NODE_TYPE.replace(".", ""));
        sbNoteNode.appendFormat("<option value='{0}'>{1}</option>", "list", "API List");
        sbNoteNode.appendFormat("<option value='{0}'>{1}</option>", "mark", "Markdown");
        sbNoteNode.appendFormat("<option value='{0}'>{1}</option>", "block", "API Block");
        sbNoteNode.appendLine("</select>");
        sbNoteNode.appendFormatLine("<span class='{0} {1}'>{2}</span>"
            , vpConst.NOTE_NODE_CODE.replace(".", ""), vpConst.NOTE_NODE_CODE_ELLIPSIS.replace(".", ""), gCode);
        sbNoteNode.appendFormat("<div class='{0}'>", vpConst.NOTE_BTN_CONTAINER.replace(".", ""));
        sbNoteNode.appendFormat("<button class='vp-btn vp-tiny {0}' type='button'><span>{1}</span></button>", "vp-node-open-option", "&lt;");
        sbNoteNode.appendFormat("<button class='vp-btn vp-tiny {0}' type='button'><span>{1}</span></button>", "vp-toggle-ellipsis", "+");
        sbNoteNode.appendFormat("<button class='vp-btn vp-tiny {0}' type='button'><span>{1}</span></button>", "vp-node-moveup", "U");
        sbNoteNode.appendFormat("<button class='vp-btn vp-tiny {0}' type='button'><span>{1}</span></button>", "vp-node-movedown", "D");
        sbNoteNode.appendFormat("<button class='vp-btn vp-tiny {0}' type='button'><span>{1}</span></button>", "vp-node-delete", "X");
        sbNoteNode.appendLine("</div>");
        sbNoteNode.appendFormatLine("<input type='hidden' class='{0}' value='{1}'/>"
            , vpConst.NOTE_NODE_GENE_META.replace(".", ""), JSON.stringify(gMeta));
        sbNoteNode.appendLine("</div>");

        $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).append(sbNoteNode.toString());
        console.log(JSON.parse($(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).find(vpConst.NOTE_NODE_GENE_META).val()));
    }

    /**
     * 노드 옵션 로드
     * @param {HTMLtag} btn 
     */
    var loadNoteNodeOption = function(btn) {
        generatedMetaData = JSON.parse($(btn).parent().parent().children(vpConst.NOTE_NODE_GENE_META).val());
        console.log(generatedMetaData.funcID);
        loadOption(generatedMetaData.funcID, optionPageLoadCallbackAndLoad);
    }

    /**
     * 노드 코드 생략 토글
     * @param {HTMLtag} btn 
     */
    var nodeToggleEllipsis = function(btn) {
        $(btn).parent().parent().children(vpConst.NOTE_NODE_CODE)
            .toggleClass(vpConst.NOTE_NODE_CODE_ELLIPSIS.replace(".", "")).toggleClass(vpConst.NOTE_NODE_CODE_ALL.replace(".", ""));
        if ($(btn).parent().parent().children(vpConst.NOTE_NODE_CODE).hasClass(vpConst.NOTE_NODE_CODE_ALL.replace(".", ""))) {
            $(btn).text("-");
        } else {
            $(btn).text("+");
        }
    }

    /**
     * 노드 위로
     * @param {HTMLtag} btn 
     */
    var nodeMoveUp = function(btn) {
        var thisIndex = $(btn).parent().parent().index(vpConst.NOTE_NODE_CLASS);
        if (thisIndex > 0) {
            $(btn).parent().parent().parent().children(vpConst.NOTE_NODE_CLASS + ":eq(" + (thisIndex - 1) + ")").before($(btn).parent().parent());
        }
    }

    /**
     * 노드 아래로
     * @param {HTMLtag} btn 
     */
    var nodeMoveDown = function(btn) {
        var thisIndex = $(btn).parent().parent().index(vpConst.NOTE_NODE_CLASS);

        if (thisIndex + 1 < $(btn).parent().parent().parent().children(vpConst.NOTE_NODE_CLASS).length) {
            $(btn).parent().parent().parent().children(vpConst.NOTE_NODE_CLASS + ":eq(" + (thisIndex + 1) + ")").after($(btn).parent().parent());
        }
    }
    
    /**
     * 노드 제거
     * @param {HTMLtag} btn 
     */
    var nodeDelete = function(btn) {
        $(btn).parent().parent().remove();
    }
    
    /**
     * 노트 로딩
     */
    var loadNoteFile = function() {
        clearNoteArea();
        openNoteArea();

        fetch($(vpCommon.wrapSelector('#noteFilePath')).val())
            .then(data => data.text()).then(html => {
                $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).append(html);
                nodeIndex = 0;
                $(html).find(vpConst.NOTE_NODE_INDEX).each(function() {
                    var tmp = $(this).html().replace("Node", "").trim();
                    if (tmp > nodeIndex) {
                        nodeIndex = tmp;
                    }
                });
            });
    }

    /**
     * 노트 파일 저장
     */
    var saveNoteFile = function() {
        var noteClone = $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).clone();
        $(noteClone).children().not(vpConst.NOTE_NODE_CLASS).remove();
        console.log($(noteClone).html());
        
        var sbNoteData = new sb.StringBuilder();
        sbNoteData.appendFormatLine("%%writefile {0}", $(vpCommon.wrapSelector('#noteFilePath')).val());
        sbNoteData.appendLine($(noteClone).html());

        Jupyter.notebook.kernel.execute(sbNoteData.toString());
    }

    let loadedWorkflow = false;
    /**
     * 워크 플로우 오픈
     */
    var openWorkflow = function() {
        window.open(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.SOURCE_PATH + "workflow/index.html", "vpWorkflow", "width=600, height=450, left=100, top=50");
    }

    /**
     * 영역 사이즈 계산
     */
    var calculateDivisionSize = function() {
        $(vpCommon.wrapSelector(vpConst.VP_BODY_CONTAINER))
            .css('height', $(vpCommon.getVPContainer()).height() - $(vpCommon.wrapSelector(vpConst.VP_BODY_CONTAINER)).position().top);

        if ($(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).is(":visible")) {
            if ($(vpCommon.getVPContainer()).width() / 3 > 200) {
                $(vpCommon.wrapSelector(vpConst.VP_BODY_CONTAINER)).css('width', $(vpCommon.getVPContainer()).width() / 3 * 2);
                $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).css('width', $(vpCommon.getVPContainer()).width() / 3);
            } else {
                $(vpCommon.wrapSelector(vpConst.VP_BODY_CONTAINER)).css('width', $(vpCommon.getVPContainer()).width() - 200);
                $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).css('width', 200);
            }
        } else {
            $(vpCommon.wrapSelector(vpConst.VP_BODY_CONTAINER)).css('width', $(vpCommon.getVPContainer()).width());
        }
        // var subContainerHeight = $(vpCommon.getVPContainer()).height() - 85;
        // $(vpCommon.wrapSelector(vpConst.VP_BODY_CONTAINER)).children("div").attr("height", subContainerHeight);
        // console.log(subContainerHeight);
    }

    /**
     * 영역 수직 최소화, 복원
     * @param {HTMLtag} btnObj 
     */
    var toggleVerticalMinimizeArea = function(btnObj) {
        $(btnObj).parent().parent().toggleClass(vpConst.OPENED_AREA_CLASS).toggleClass(vpConst.CLOSED_AREA_CLASS);
        $(btnObj).toggleClass(vpConst.ARROW_BTN_UP).toggleClass(vpConst.ARROW_BTN_DOWN);
    }

    /* event bind */

    /**
     * home
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.BTN_MODE_SELECTOR), function() {
        openModeSelector();
    });
    
    /**
     * API List 모드 시작
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.VP_ID_PREFIX + "openAPIList"), function() {
        openAPIBrowser();
    });

    /**
     * API Block 모드 시작
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.VP_ID_PREFIX + "openAPIBlock"), function() {
        openAPIBlock();
    });
    
    /**
     * VP Note 모드 시작
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.VP_ID_PREFIX + "openVPNote"), function() {
        openNoteArea();
    });

    /**
     * workflow 모드 시작
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.VP_ID_PREFIX + "openWorkflow"), function() {
        openWorkflow();
    });

    /**
     * api browser 
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.API_GROUP_BOX, vpConst.NAVI_GROUP_TOGGLE), function() {
        toggleNaviGroupShow($(this));
    });

    /**
     * navi 함수 클릭(옵션 로드)
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.NAVI_FUNCION_BUTTON), function() {
        loadOption($(this).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, "")), optionPageLoadCallback);
    });

    /**
     * 옵션 주피터 셀에 추가
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.VP_ID_PREFIX + "addOnCell"), function() {
        addLibraryToJupyterCell(false);
    });

    /**
     * 옵션 주피터 셀에 추가, 실행
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.VP_ID_PREFIX + "runCell"), function() {
        addLibraryToJupyterCell(true);
    });

    /**
     * 옵션 템플릿에 추가
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.VP_ID_PREFIX + "saveOption"), function() {
        // if (confirm("옵션을 저장할 템플릿을 불러오겠습니까?")) {
        //     alert(">> 파일브라우저 오픈");
        // }
        if (generatedCode === undefined || generatedCode === "BREAK_RUN") {
            alert("Code not generated");
            return;
        }
        addNoteNode(generatedCode, generatedMetaData);
        openNoteArea();
    });

    /**
     * option close
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.VP_ID_PREFIX + "closeOption"), function() {
        closeLibraryOption();
    });

    /**
     * 새 노트
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.VP_ID_PREFIX + "newNote"), function() {
        clearNoteArea();
    });

    /**
     * 노트 영역 닫기
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.VP_ID_PREFIX + "closeNote"), function() {
        $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).hide();
        clearNoteArea();
        calculateDivisionSize();
    });

    /**
     * 수직 최소화 버튼 클릭시 영역 표시 변환
     */
    $(document).on("click", vpCommon.wrapSelector(".vp-panel-area-vertical-btn"), function() {
        toggleVerticalMinimizeArea($(this));
    });

    var noteBrowser = function(obj) {
        // file navigation : state 데이터 목록
        this.state = {
            paramData:{
                encoding: "utf-8" // 인코딩
                , delimiter: ","  // 구분자
            },
            returnVariable:"",    // 반환값
            isReturnVariable: false,
            fileExtension: "vp" // 확장자
        }; 
        this.fileResultState = {
            pathInputId : vpCommon.wrapSelector('#noteFilePath')
        };
        var that = obj;
    }

    var nbNote = new noteBrowser(this);

    /**
     * 노트 모드 오픈
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.LOAD_NOTE_BTN), async function() {
        var loadURLstyle = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH;
        var loadURLhtml = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.SOURCE_PATH + "component/fileNavigation/index.html";
        
        vpCommon.loadCss( loadURLstyle + "component/fileNavigation.css");

        await $(`<div id="vp_fileNavigation"></div>`).load(loadURLhtml, () => {
            $('#vp_fileNavigation').removeClass("hide");
            $('#vp_fileNavigation').addClass("show");
            
            var {vp_init, vp_bindEventFunctions } = fileNavigation;
                
            fileNavigation.vp_init(nbNote);
            fileNavigation.vp_bindEventFunctions();
        }).appendTo("#site");
    });

    /**
     * 노트 저장
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.VP_ID_PREFIX + "saveNote"), async function() {
        // saveNoteFile();
        var loadURLstyle = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH;
        var loadURLhtml = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.SOURCE_PATH + "component/fileNavigation/index.html";
        
        vpCommon.loadCss( loadURLstyle + "component/fileNavigation.css");

        await $(`<div id="vp_fileNavigation"></div>`).load(loadURLhtml, () => {
            $('#vp_fileNavigation').removeClass("hide");
            $('#vp_fileNavigation').addClass("show");
            
            var {vp_init, vp_bindEventFunctions } = fileNavigation;
                
            fileNavigation.vp_init(nbNote, "SAVE_FILE");
            fileNavigation.vp_bindEventFunctions();
        }).appendTo("#site");
    });

    /**
     * 노트 노드 셀에 적용
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.NOTE_BTN_CONTAINER, vpConst.VP_CLASS_PREFIX + "node-open-option"), function() {
        loadNoteNodeOption($(this));
    });

    /**
     * 노트 노드 확장
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.NOTE_BTN_CONTAINER, vpConst.VP_CLASS_PREFIX + "toggle-ellipsis"), function() {
        nodeToggleEllipsis($(this));
    });

    /**
     * 노트 노드 위로
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.NOTE_BTN_CONTAINER, vpConst.VP_CLASS_PREFIX + "node-moveup"), function() {
        nodeMoveUp($(this));
    });

    /**
     * 노트 노드 아래로
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.NOTE_BTN_CONTAINER, vpConst.VP_CLASS_PREFIX + "node-movedown"), function() {
        nodeMoveDown($(this))
    });

    /**
     * 노트 노드 제거
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.NOTE_BTN_CONTAINER, vpConst.VP_CLASS_PREFIX + "node-delete"), function() {
        nodeDelete($(this))
    });

    /**
     * 노트 파일 로드
     */
    $(document).on("fileReadSelected.fileNavigation", function() {
        loadNoteFile();
    })
    
    /**
     * 노트 파일 세이브
     */
    $(document).on("fileSaveSelected.fileNavigation", function() {
        saveNoteFile();
    })

    /**
     * 컨테이너 사이즈 변경시 division resize
     */
    events.on('resize-container.vp-wrapper', function() {
        calculateDivisionSize();
    });

    /**
     * 노트북 셀 선택 변경시
     */
    events.on('select.Cell', function (event, data) {
        var index = Jupyter.notebook.find_cell_index(data.cell);
        console.log(index);
    });

    /**
     * 메인 UI init
     */
    var containerInit = function() {
        loadLibraries();
    }

    return {
        containerInit: containerInit
    // TEST: 김민주 코드 추가 : 다른 옵션페이지로 넘어가는 함수 필요 (matplotlib/figure.js)
    // , tabPageShow: tabPageShow
    };
});
