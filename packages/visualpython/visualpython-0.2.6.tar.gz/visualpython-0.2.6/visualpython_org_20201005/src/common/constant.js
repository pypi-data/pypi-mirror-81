define ([
    'require'
], function(requirejs) {
    "use strict";

    /**
     * path separator
     */
    const pathSeparator = "/";

    /**
     * base path
     */
    const basePath = "nbextensions" + pathSeparator + "visualpython" + pathSeparator;

    /**
     * source path
     */
    const srcPath = "src" + pathSeparator

    /**
     * resource path
     */
    const resourcePath = "resource" + pathSeparator

    /**
     * style sheet path
     */
    const stylePath = "css" + pathSeparator

    /**
     * data path
     */
    const dataPath = "data" + pathSeparator;
    
    /**
     * main style path
     */
    const mainCssURL = "main.css";

    /**
     * container style path
     */
    const vpContainerCssURL = "container" + pathSeparator + "vpContainer.css";

    /**
     * container html path
     */
    const vpContainerPageURL = "container" + pathSeparator + "vpContainer.html";

    /**
     * settings data path
     */
    const vpSettingsURL = "settings.xml";

    /**
     * libraries data path
     */
    const vpLibrariesURL = "libraries.xml";

    /**
     * toolbar btn properties
     */
    const toolbarBtnInfo = {
        HELP: "visualpython 0.2.6"
        , ICON: "fa-angellist"
        , ID: "vpBtnToggle"
        , NAME: "toggle-vp"
        , PREFIX: "vp"
    }

    /**
     * VisualPython position metadata name
     */
    const vpPositionMetaName = "vpPosition";

    /**
     * VisualPython tag id selector prefix
     */
    const vpIDPrefix = "#vp_";

    /**
     * VisualPython tag class selector prefix
     */
    const vpClassPrefix = ".vp-";

    /**
     * VisualPython tag class prefix (private)
     */
    const vpClassPrefixNotSelector = "vp-";

    /**
     * html tag data attribute prefix
     */
    const tagDataPrefix = "data-";

    /**
     * VisualPython container id
     */
    const vpContainerID = "vp-wrapper";

    /**
     * area division container
     */
    const areaDivContainer = vpIDPrefix + "divisionContainer";

    /**
     * top container of task area
     */
    const areaTaskManage = vpIDPrefix + "taskArea";

    /**
     * top container of option area
     */
    const areaGeneOption = vpIDPrefix + "optionArea";

    /**
     * top container of blueprint area
     */
    const areaBP = vpIDPrefix + "blueprintArea";

    /**
     * top container of generate area
     */
    const areaGene = vpIDPrefix + "generateArea";

    /**
     * top container of library area
     */
    const areaLib = vpIDPrefix + "libraryArea";

    /**
     * library area child container
     */
    const libSubContainer = vpClassPrefix + "library-sub";

    /**
     * search result continer
     */
    const srchRsltContainer = vpIDPrefix + "searchResults";

    /**
     * user define variable list container
     */
    const variableList = vpIDPrefix + "variableList";

    /**
     * list grid header
     */
    const listGridHeader = vpClassPrefix + "grid-header";

    /**
     * search result item class
     */
    const srchRsltItemClass = vpClassPrefix + "search-func";

    /**
     * variable list item class
     */
    const varListItemClass = vpClassPrefix + "var-list-item";

    /**
     * naviagtor path item container
     */
    const naviPathContainer = vpIDPrefix + "navigatorPath";

    /**
     * naviagtor path item
     */
    const naviPathItemClass = vpClassPrefix + "navi-path-item";

    /**
     * naviagtor path item
     */
    const naviPathItemDividerClass = vpClassPrefix + "navi-path-item-divider";

    /**
     * navigator buttons container
     */
    const naviBtnContainer = vpIDPrefix + "navigatorButtons";

    /**
     * navigator button class
     */
    const naviBtnClass = vpClassPrefix + "navi-btn";

    /**
     * attribute for navi button content level
     */
    const naviItemLevel = tagDataPrefix + "nav-class";

    /**
     * attribute type navi button group content level
     */
    const naviItemLevelGrp = "grp";

    /**
     * attribute type navi button function content level
     */
    const naviItemLevelFunc = "func";

    /**
     * attribute type navi button prev group content level
     */
    const naviItemLevelPrev = "prev";

    /**
     * temporary area for load option
     */
    const optGreenRoom = vpIDPrefix + "optionGreenRoom";
    
    /**
     * container for loaded option
     */
    const optContainer = vpIDPrefix + "optionBook";

    /**
     * option per tab page
     */
    const optPage = vpClassPrefix + "option-page";

    /**
     * option tab header 
     */
    const optTabItem = vpClassPrefix + "option-tab-page";

    /**
     * container for loaded option tab header
     */
    const optTabContainer = vpIDPrefix + "optionTab";

    /**
     * container for loaded option blueprint
     */
    const optBPContainer = vpClassPrefix + "blueprint-container";

    /**
     * option blueprint item
     */
    const optBPItem = vpClassPrefix + "blueprint-item";

    /**
     * option blueprint item destroy
     */
    const optBPItemClose = vpClassPrefix + "blueprint-item-destroy";

    /**
     * showing loaded item style
     */
    const optBPFocusedItem = vpClassPrefixNotSelector + "focused";

    /**
     * task index label
     */
    const optTaskIdxLabel = vpIDPrefix + "lblOptIdx";
    
    /**
     * option kind label
     */
    const optKindLabel = vpIDPrefix + "lblOptKind";

    /**
     * temp cation for load new option
     */
    const optHeaderTempCaption = tagDataPrefix + "temp-caption";

    /**
     * option paging btn class
     */
    const optPagingBtn = vpClassPrefix + "option-paging-btn";

    /**
     * option save button id
     */
    const optSaveBtn = vpIDPrefix + "optSave";

    /**
     * option save and execute button id
     */
    const optSaveExeBtn = vpIDPrefix + "optSaveExe";

    /**
     * option cancel button id
     */
    const optCancelBtn = vpIDPrefix + "optCancel";

    /**
     * option page prev button id
     */
    const optPrevPageBtn = vpIDPrefix + "optPrevPage";

    /**
     * option page next button id
     */
    const optNextPageBtn = vpIDPrefix + "optNextPage";

    /**
     * opened area style class
     */
    const openedAreaClass = vpClassPrefixNotSelector + "spread";

    /**
     * closed area style class
     */
    const closedAreaClass = vpClassPrefixNotSelector + "minimize";

    /**
     * area style change btn shape class
     */
    const areaBtnUp = vpClassPrefixNotSelector + "arrow-up";

    /**
     * area style change btn shape class
     */
    const areaBtnDown = vpClassPrefixNotSelector + "arrow-down";

    /**
     * area style change btn shape class
     */
    const areaBtnLeft = vpClassPrefixNotSelector + "arrow-left";

    /**
     * area style change btn shape class
     */
    const areaBtnRight = vpClassPrefixNotSelector + "arrow-right";

    /**
     * vertical text style
     */
    const verticalTextClass = vpClassPrefixNotSelector + "vertical";
    
    /**
     * multi language tag class
     */
    const multiLangTagClass = vpClassPrefix + "multilang";

    /**
     * tag attribute for multi language id
     */
    const multiLangCaptionID = tagDataPrefix + "caption-id";

    /**
     * sortable table class
     */
    const sortableTableClass = vpClassPrefix + "tbl-sortable";

    /**
     * sortable column class
     */
    const sortableColumnClass = vpClassPrefix + "sortable-column";

    /**
     * sort value wrapper class
     */
    const sortValueWrapClass = vpClassPrefix + "sort-value";

    /**
     * arrow up shape class
     */
    const arrowUpClass = vpClassPrefix + "arrow-up";
    
    /**
     * arrow down shape class
     */
    const arrowDownClass = vpClassPrefix + "arrow-down";

    /**
     * library item type : package
     */
    const libraryItemTypePkg = "package";

    /**
     * library item type : fucntion
     */
    const libraryItemTypeFnc = "function";

    /**
     * library xml item node name
     */
    const libraryItemTag = "item";

    /**
     * library xml item depth attribute
     */
    const libraryItemDepthAttr = "level";

    /**
     * library xml item id attribute
     */
    const libraryItemIDAttr = "id";
    
    /**
     * library xml item type attribute
     */
    const libraryItemTypeAttr = "type";

    /**
     * library xml item name attribute
     */
    const libraryItemNameAttr = "name";

    /**
     * library xml item tag attribute
     */
    const libraryItemTagAttr = "tag";

    /**
     * library xml item file url node
     */
    const libraryItemFileURLNode = "file";

    /**
     * library xml item path url node
     */
    const libraryItemPathNode = "path";

    /**
     * library xml item desc url node
     */
    const libraryItemDescNode = "desc";
    
    /**
     * attribute for library item content for html tag
     */
    const libraryItemDataID = tagDataPrefix + "item-id";

    /**
     * new task btn id
     */
    const newTaskBtn = vpIDPrefix + "btnNewTask";

    /**
     * task index cell class
     */
    const taskIndexCell = vpClassPrefix + "task-index";

    /**
     * task button class
     */
    const taskBtn = vpClassPrefix + "task-btn";

    /**
     * task index caption prefix
     */
    const taskIndexPrefix = "T";

    /**
     * task label class
     */
    const taskLabelClass = vpClassPrefix + "task-src-view";

    /**
     * task list class
     */
    const taskListTable = vpClassPrefix + "task-tbl";

    /**
     * task list item class
     */
    const taskListRow = vpClassPrefix + "task-row";

    /**
     * task command cell class
     */
    const taskCmdCell = vpClassPrefix + "task-command-cell";

    /**
     * task command btn class
     */
    const taskCmdBtn = vpClassPrefix + "task-command";

    /**
     * task command run btn class
     */
    const taskCmdExeBtn = vpClassPrefix + "task-execute";

    /**
     * task command stop btn class
     */
    const taskCmdStopBtn = vpClassPrefix + "task-stop";

    /**
     * task add line class
     */
    const taskAddCmd = vpClassPrefix + "add-task";

    return {
        PATH_SEPARATOR: pathSeparator
        , BASE_PATH: basePath
        , SOURCE_PATH: srcPath
        , RESOURCE_PATH: resourcePath
        , STYLE_PATH: stylePath
        , DATA_PATH: dataPath
        , MAIN_CSS_URL: mainCssURL
        , VP_CONTAINER_CSS_URL: vpContainerCssURL
        , VP_CONTAINER_PAGE_URL: vpContainerPageURL
        , VP_SETTINGS_XML_URL: vpSettingsURL
        , VP_LIBRARIES_XML_URL: vpLibrariesURL
        , TOOLBAR_BTN_INFO: toolbarBtnInfo
        , VP_POSITION_META_NAME: vpPositionMetaName
        , VP_ID_PREFIX: vpIDPrefix
        , VP_CLASS_PREFIX: vpClassPrefix
        , TAG_DATA_PREFIX: tagDataPrefix
        , VP_CONTAINER_ID: vpContainerID
        , AREA_DIVISION_CONTAINER: areaDivContainer
        , AREA_TASK_MANAGEMENT: areaTaskManage
        , AREA_GENERATE_OPTION: areaGeneOption
        , AREA_BLUEPRINT: areaBP
        , AREA_GENERATE: areaGene
        , AREA_LIBRARY: areaLib
        , LIBRARY_SUB_CONTAINER: libSubContainer
        , SEARCH_RESULT_CONTAINER: srchRsltContainer
        , VARIABLE_LIST_CONTAINER: variableList
        , LIST_GRID_HEADER: listGridHeader
        , SEARCH_RESULT_ITEM_CLASS: srchRsltItemClass
        , VARIABLE_LIST_ITEM_CLASS: varListItemClass
        , NAVIGATOR_PATH_ITEM_CONTAINER: naviPathContainer
        , NAVIGATOR_PATH_ITEM_CLASS: naviPathItemClass
        , NAVIGATOR_PATH_ITEM_DIVIDER: naviPathItemDividerClass
        , NAVIGATOR_BUTTON_CONTAINER: naviBtnContainer
        , NAVIGATOR_BUTTON_CLASS: naviBtnClass
        , NAVIGATOR_BUTTON_LEVEL: naviItemLevel
        , NAVIGATOR_BUTTON_LEVEL_GROUP: naviItemLevelGrp
        , NAVIGATOR_BUTTON_LEVEL_FUNCTION: naviItemLevelFunc
        , NAVIGATOR_BUTTON_LEVEL_PREV_GROUP: naviItemLevelPrev
        , OPTION_GREEN_ROOM: optGreenRoom
        , OPTION_CONTAINER: optContainer
        , OPTION_PAGE: optPage
        , OPTION_TAB_ITEM: optTabItem
        , OPTION_TAB_CONTAINER: optTabContainer
        , OPTION_BLUEPRINT_CONTAINER: optBPContainer
        , OPTION_BLUEPRINT_ITEM: optBPItem
        , OPTION_BLUEPRINT_ITEM_CLOSE: optBPItemClose
        , OPTION_BLUEPRINT_FOCUSED_ITEM: optBPFocusedItem
        , OPTION_TASK_INDEX_LABEL: optTaskIdxLabel
        , OPTION_KIND_LABEL: optKindLabel
        , OPTION_HEADER_TEMP_CAPTION: optHeaderTempCaption
        , OPTION_PAGING_BUTTON: optPagingBtn
        , OPTION_SAVE_BUTTON: optSaveBtn
        , OPTION_SAVE_EXECUTE_BUTTON: optSaveExeBtn
        , OPTION_CANCEL_BUTTON: optCancelBtn
        , OPTION_PREV_PAGE_BUTTON: optPrevPageBtn
        , OPTION_NEXT_PAGE_BUTTON: optNextPageBtn
        , OPENED_AREA_CLASS: openedAreaClass
        , CLOSED_AREA_CLASS: closedAreaClass
        , AREA_BTN_UP: areaBtnUp
        , AREA_BTN_DOWN: areaBtnDown
        , AREA_BTN_LEFT: areaBtnLeft
        , AREA_BTN_RIGHT: areaBtnRight
        , VERTICAL_TEXT_CLASS: verticalTextClass
        , MULTI_LANGUAGE_CLASS: multiLangTagClass
        , LANGUAGE_CAPTION_ID: multiLangCaptionID
        , SORTABLE_TABLE_CLASS: sortableTableClass
        , SORTABLE_COLUMN_CLASS: sortableColumnClass
        , SORT_VALUE_WRAP_CLASS: sortValueWrapClass
        , ARROW_UP_CLASS: arrowUpClass
        , ARROW_DOWN_CLASS: arrowDownClass
        , LIBRARY_ITEM_TYPE_PACKAGE: libraryItemTypePkg
        , LIBRARY_ITEM_TYPE_FUNCTION: libraryItemTypeFnc
        , LIBRARY_ITEM_TAG: libraryItemTag
        , LIBRARY_ITEM_DEPTH_ATTR: libraryItemDepthAttr
        , LIBRARY_ITEM_ID_ATTR: libraryItemIDAttr
        , LIBRARY_ITEM_TYPE_ATTR: libraryItemTypeAttr
        , LIBRARY_ITEM_NAME_ATTR: libraryItemNameAttr
        , LIBRARY_ITEM_TAG_ATTR: libraryItemTagAttr
        , LIBRARY_ITEM_FILE_URL_NODE: libraryItemFileURLNode
        , LIBRARY_ITEM_PATH_NODE: libraryItemPathNode
        , LIBRARY_ITEM_DESCRIPTION_NODE: libraryItemDescNode
        , LIBRARY_ITEM_DATA_ID: libraryItemDataID
        , NEW_TASK_BUTTON: newTaskBtn
        , TASK_INDEX_CELL: taskIndexCell
        , TASK_BUTTON: taskBtn
        , TASK_INDEX_PREFIX: taskIndexPrefix
        , TASK_LABEL_CONTROL: taskLabelClass
        , TASK_LIST_TABLE: taskListTable
        , TASK_LIST_ROW: taskListRow
        , TASK_COMMAND_CELL: taskCmdCell
        , TASK_COMMAND_BUTTON: taskCmdBtn
        , TASK_COMMAND_EXECUTE_BUTTON: taskCmdExeBtn
        , TASK_COMMAND_STOP_BUTTON: taskCmdStopBtn
        , TASK_ADD_CMD: taskAddCmd
    };
});
