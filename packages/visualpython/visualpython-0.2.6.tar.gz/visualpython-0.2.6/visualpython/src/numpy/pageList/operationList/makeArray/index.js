define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpFuncJS'

    // numpy 패키지를 위한 라이브러리import 
    , 'nbextensions/visualpython/src/common/constant_numpy'
    , 'nbextensions/visualpython/src/numpy/api/numpyStateApi'
    , 'nbextensions/visualpython/src/numpy/api/numpyRouteMapApi'
    , 'nbextensions/visualpython/src/numpy/option/numpyOption'
 
], function ( requirejs, $, vpCommon, vpConst, vpFuncJS, 
              vpNumpyConst, numpyStateApi, numpyRouteMapApi, numpyOption ) {
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "numpyMakeArray"
        , funcID : "JY103"  // TODO: ID 규칙 생성 필요
    }

    // numpy 함수의 state 데이터를 다루는 api
    var { changeOldToNewState, findStateValue} = numpyStateApi;
    // FuncId에 맞는 FuncData를 맵핑하는 api
    var { mapFuncIdToNumpyFuncData } = numpyRouteMapApi;
    // FuncId에 맵핑된 numpyCodeGenerator, numpyCodeValidator를 가져온다
    // FuncId에 맵핑된 numpyCodeGenerator은 코드를 만들고 numpyCodeValidator은 코드 실행 전 입력된 state 값을 검증한다.
    var { numpyCodeGenerator, numpyCodeValidator, numpyPageRender, htmlUrlPath } = mapFuncIdToNumpyFuncData(funcOptProp.funcID);

    // numpy 함수 페이지에 대한 옵션 정의
    var numpyOption = numpyOption;

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var optionLoadCallback = function(callback) {
        // document.getElementsByTagName("head")[0].appendChild(link);
        // 컨테이너에서 전달된 callback 함수가 존재하면 실행.
        if (typeof(callback) === 'function') {
            var uuid = vpCommon.getUUID();
            // 최대 10회 중복되지 않도록 체크
            for (var idx = 0; idx < 10; idx++) {
                // 이미 사용중인 uuid 인 경우 다시 생성
                if ($(vpConst.VP_CONTAINER_ID).find("." + uuid).length > 0) {
                    uuid = vpCommon.getUUID();
                }
            }
            $(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM)).find(vpConst.OPTION_PAGE).addClass(uuid);
            // 옵션 객체 생성
            var ipImport = new ImportPackage(uuid);
            // 옵션 속성 할당.
            ipImport.setOptionProp(funcOptProp);
            // html 설정.
            ipImport.initHtml();
            callback(ipImport);  // 공통 객체를 callback 인자로 전달
        }
    }
    /**
     * html 로드. 
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
    */
    var initOption = function(callback) {
        vpCommon.loadHtml(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM), htmlUrlPath, optionLoadCallback, callback);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
    */
    var ImportPackage = function(uuid) {
        this.uuid = uuid; // Load html 영역의 uuid.

        // state 데이터 목록
        
        this.state = {
            paramOption1: "1"
            , paramOption1_1: "1"
            , paramOption1_2: "1"
            , paramOption2: "1"
            , paramData:{
                npArrayParamOneArray: ["0"]
                , npArrayParamTwoArray: [["0"]]
                , npArrayParamThreeArray: [[["0"]]]
                , npArrayParamScalar: ""
                , npArrayParamVariable: ""

                , npArangeParam1Start:""
                , npArangeParam2Start:""
                , npArangeParam2Stop:""
                , npArangeParam3Start:""
                , npArangeParam3Stop:""
                , npArangeParam3Step:""

                , npReshapeParam1Length: ""
                , npReshapeParam2Row: ""
                , npReshapeParam2Col: ""
                , npReshapeParam3Row: ""
                , npReshapeParam3Col: ""
                , npReshapeParam3Depth: ""

            }
            , returnVariable: ""
            , isReturnVariable: false

            , makedCodeStr: "",
        }
    }

    /**
     * vpFuncJS 에서 상속
    */
    ImportPackage.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
        state 값 변경 함수
        @param {Object} newState
    */
    ImportPackage.prototype.setState = function(newState) {
        this.state = changeOldToNewState(this.state, newState);
        this.consoleState();
    }

    /**
        모든 state 값을 가져오는 함수
    */
    ImportPackage.prototype.getStateAll = function() {
        return this.state;
    }

    /**
        특정 state Name 값을 가져오는 함수
        @param {string} stateKeyName
    */
    ImportPackage.prototype.getState = function(stateKeyName) {
        return findStateValue(this.state, stateKeyName);
    }

    /**
        state 값 변경 체크 함수
        state 데이터의 변경 흐름을 console.log로 체크하는 함수
    */
    ImportPackage.prototype.consoleState = function() {
        if( numpyOption.IS_CONSOLE_STATE === true) {
            console.log(this.state);
        }
    }

    /**
     * 유효성 검사
     * @returns 유효성 검사 결과. 적합시 true
    */
    ImportPackage.prototype.optionValidation = function() {
        // FIXME: 디버깅을 위해 Validation 검사 보류
        return true;
        // return numpyCodeValidator.validate(this.state);
    }

    /**
     * html 내부 binding 처리
     */
    ImportPackage.prototype.initHtml = function() {
        var importPackageThis = this;
        // 동적 html 태그들을 index.html에 렌더링 
        // numpyPageRender.pageRender(this);
   
        // bind 이벤트 함수 to html
        this.bindImportPackageGrid();

        // import load css
        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + vpNumpyConst.NUMPY_BASE_CSS_PATH);

        // html init render  init HTML 초기 설정
        $(this.wrapSelector(`.vp-numpy-tab-block-element-1`)).css("display","none");
        $(this.wrapSelector(`.vp-numpy-tab-block-element-1-1`)).css("display","block");
        $(this.wrapSelector(`.vp-numpy-tab-block-element-2`)).css("display","none");
        $(this.wrapSelector(`.vp-numpy-tab-block-element-2-1`)).css("display","block");

        var stateParamNameArray = [`npArrayParamOneArray`, `npArrayParamTwoArray`,`npArrayParamThreeArray`,
                                    `npArrayParamScalar`,`npArrayParamVariable`];
        var stateParamOptionName = `paramOption1_1`;
    
        numpyPageRender[0].renderNpArrayBlock( importPackageThis, ".vp-numpy-tab-block-element-1-1-view", 
                                                                stateParamNameArray, stateParamOptionName);
    }

    /**
     * Import 기본 패키지 바인딩
     */
    ImportPackage.prototype.bindImportPackageGrid = function() {
        var importPackageThis = this;
        var stateParamNameArray = [`npArrayParamOneArray`, `npArrayParamTwoArray`,`npArrayParamThreeArray`,
                                    `npArrayParamScalar`,`npArrayParamVariable`];
        var stateParamOptionName = `paramOption1_1`;

        var npArangeStateParamNameArray = [`npArangeParam1Start`, `npArangeParam2Start`,`npArangeParam2Stop`,
                                            `npArangeParam3Start`,`npArangeParam3Stop`,`npArangeParam3Step`];
        var npArangeStateParamOptionName = `paramOption1_2`;

        // param 옵션 1 ~ 2탭 선택
        for(var i = 1; i < 3; i++){
            (function(j) {
                $(importPackageThis.wrapSelector(`.vp-numpyTabBtn-1-${j}`)).click(function() {
                    $(importPackageThis.wrapSelector(".vp-numpy-tab-block-element-1")).css("display","none");
                    $(importPackageThis.wrapSelector(`.vp-numpy-tab-block-element-1-${j}`)).css("display","block");

                    $(this).removeClass("vp-numpy-selected");
                    if ($(this).hasClass("vp-numpy-selected")){
                        $(this).removeClass("vp-numpy-selected");
                    } else {
                        $(this).addClass("vp-numpy-selected");
                    }

                    switch(`${j}`) {
                        // param 옵션 1 : np.array
                        case "1": {
                            numpyPageRender[0].renderNpArrayBlock( importPackageThis, ".vp-numpy-tab-block-element-1-1-view", 
                                                                stateParamNameArray, stateParamOptionName);
                            break;
                        }
                        // param 옵션 2 : np.arange
                        case "2": {
                            numpyPageRender[1].renderNpArangeBlock( importPackageThis, ".vp-numpy-tab-block-element-1-2-view", 
                                                                 npArangeStateParamNameArray, npArangeStateParamOptionName);
                            break;
                        }

                        default: {
                            break;
                        }
                    }
                    importPackageThis.setState({
                        paramOption1: `${j}`
                    });

                });
            })(i);
        }

        // param 옵션 1 ~ 3탭 선택
        for(var i = 1; i < 4; i++){
            (function(j) {
                $(importPackageThis.wrapSelector(`.vp-numpyTabBtn-2-${j}`)).click(function() {
                    $(importPackageThis.wrapSelector(".vp-numpy-tab-block-element-2")).css("display","none");
                    $(importPackageThis.wrapSelector(`.vp-numpy-tab-block-element-2-${j}`)).css("display","block");

                    $(this).removeClass("vp-numpy-selected");
                    if ($(this).hasClass("vp-numpy-selected")){
                        $(this).removeClass("vp-numpy-selected");
                    } else {
                        $(this).addClass("vp-numpy-selected");
                    }

                    switch(`${j}`) {
                        // param 옵션 1
                        case "1": {
                            // numpyPageRender[2].pageRender(importPackageThis, false);
                            break;
                        }
                        // param 옵션 2
                        case "2": {
                            break;
                        }
                        case "3": {
                            break;
                        }

                        default: {
                            break;
                        }
                    }
                    importPackageThis.setState({
                        paramOption2: `${j}`
                    });

                });
            })(i);
        }

        // np.reshape state 입력
        $(importPackageThis.wrapSelector("#vp_numpyParamOption1Length")).on("change keyup paste", function() {
            importPackageThis.setState({
                npReshapeParam1Length: $(this).val()
            });
        });
        $(importPackageThis.wrapSelector("#vp_numpyParamOption2Row")).on("change keyup paste", function() {
            importPackageThis.setState({
                npReshapeParam2Row: $(this).val()
            });
        });
        $(importPackageThis.wrapSelector("#vp_numpyParamOption2Col")).on("change keyup paste", function() {
            importPackageThis.setState({
                npReshapeParam2Col: $(this).val()
            });
        });
        $(importPackageThis.wrapSelector("#vp_numpyParamOption3Row")).on("change keyup paste", function() {
            importPackageThis.setState({
                npReshapeParam3Row: $(this).val()
            });
        });
        $(importPackageThis.wrapSelector("#vp_numpyParamOption3Col")).on("change keyup paste", function() {
            importPackageThis.setState({
                npReshapeParam3Col: $(this).val()
            });
        });
        $(importPackageThis.wrapSelector("#vp_numpyParamOption3Depth")).on("change keyup paste", function() {
            importPackageThis.setState({
                npReshapeParam3Depth: $(this).val()
            });
        });

        // return 변수 입력
        $(importPackageThis.wrapSelector("#vp_numpyReturnVarInput")).on("change keyup paste", function() {
            importPackageThis.setState({
                returnVariable: $(this).val()
            });
        });
        // return 변수 print 여부 선택
        $(importPackageThis.wrapSelector(".vp-numpy-input-checkbox")).click(function() {
            importPackageThis.setState({
                isReturnVariable: $(this).is(":checked")
            });
        });            
    }

    /**
     * 코드 생성
     * @param {boolean} exec 실행여부
     */
    ImportPackage.prototype.generateCode = function(exec) {
        // validate code 
        if (!this.optionValidation()) return;
        // make code
        numpyCodeGenerator.makeCode(this.state);
        // execute code
        this.cellExecute(numpyCodeGenerator.getCodeAndClear(), exec);
    }

    return {
        initOption: initOption
    };
});
