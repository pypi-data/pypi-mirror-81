define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'

    // numpy 패키지를 위한 라이브러리import 
    , 'nbextensions/visualpython/src/common/constant_numpy'
    , 'nbextensions/visualpython/src/numpy/api/numpyStateApi'
    , 'nbextensions/visualpython/src/numpy/api/numpyRouteMapApi'
    , 'nbextensions/visualpython/src/numpy/option/numpyOption'
    , 'nbextensions/visualpython/src/component/fileNavigation/index'

], function (requirejs, $, vpCommon, vpConst, sb, vpFuncJS, 
             vpNumpyCommon, NumpyStateApi, NumpyRouteMapApi, NumpyOption, fileNavigation) {

    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "importCsv"
        , funcID : "JY0"  // TODO: ID 규칙 생성 필요
    }

    // numpy 함수의 state 데이터를 다루는 api
    var { changeOldToNewState, findStateValue } = NumpyStateApi;

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var optionLoadCallback = function(callback) {
        // document.getElementsByTagName("head")[0].appendChild(link);
        // 컨테이너에서 전달된 callback 함수가 존재하면 실행.
        if (typeof (callback) === 'function') {
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
        vpCommon.loadHtml(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM), "file_io/importCsv/index.html", optionLoadCallback, callback);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var ImportPackage = function(uuid) {
        this.uuid = uuid; // Load html 영역의 uuid.

        // state 데이터 목록
        this.state = {
            paramData:{
                encoding: "utf-8"
                , delimiter: ","
            },
            returnVariable:"",
            isReturnVariable: false,
        }
    }
    /**
     * vpFuncJS 에서 상속
    */
    ImportPackage.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
     *   state 값 변경 함수
        @param {Object} newState 
    */
    ImportPackage.prototype.setState = function(newState) {
        this.state = changeOldToNewState(this.state, newState);
        this.consoleState();
    }

    /**
     * 특정 state 값 가져오는 함수
     * @param {string} stateKeyName 
     */
    ImportPackage.prototype.getState = function(stateKeyName) {
        return findStateValue(this.state, stateKeyName);
    }
    /**
     * 모든 state 값 가져오는 함수
     */
    ImportPackage.prototype.getStateAll = function() {
        return this.state;
    }
    /**
         state 값 변경 체크 함수
    */
    ImportPackage.prototype.consoleState = function() {
        console.log(this.state);
    }

    /**
     * html 내부 binding 처리
     */
    ImportPackage.prototype.initHtml = function() {
        // bind 이벤트 함수 to html
        this.bindImportPackageGrid();

        // import load css
        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "file_io/importCsv.css");
        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "numpy/index.css");
    }
    /**
     * Import 기본 패키지 바인딩
     */
    ImportPackage.prototype.bindImportPackageGrid = function() {

        var that = this;
        // 파일 네비게이션 오픈 클릭
        $(that.wrapSelector("#vp_openFileNavigationBtn")).click( async function() {
            var loadURLstyle = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH;
            var loadURLhtml = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.SOURCE_PATH + "component/fileNavigation/index.html";
            
            that.loadCss( loadURLstyle + "component/fileNavigation.css");
    
            await $(`<div id="vp_fileNavigation"></div>`)
                    .load(loadURLhtml, () => {

                        $('#vp_fileNavigation').removeClass("hide");
                        $('#vp_fileNavigation').addClass("show");

                        var { vp_init
                              , vp_bindEventFunctions} = fileNavigation;
                    
                        vp_init(that);
                        vp_bindEventFunctions();
                    })
                    .appendTo("#site");
        });

        // FIXME: 베타버전에선 임시로 삭제
        // importCsv Encoding 값 설정
        $(that.wrapSelector(".vp-importCsv-encoding-input-checkbox")).click( function() {
            that.setState({
                paramOption: {
                    encoding: $(this).val()
                }
            });
        });

        // FIXME: 베타버전에선 임시로 삭제
        // importCsv delimiter 값 설정
        $(that.wrapSelector(".vp-importCsv-delimiter-input-checkbox")).click( function() {
            that.setState({
                paramOption: {
                    delimiter: $(this).val()
                }
            });
        });

        // return 변수 입력
        $(that.wrapSelector("#vp_numpyReturnVarInput")).on("change keyup paste", function() {
            that.setState({
                returnVariable: $(this).val()
            });
        });

        // return 변수 print 여부 선택
        $(that.wrapSelector(".vp-numpy-input-checkbox")).click(function() {
            that.setState({
                isReturnVariable: $(this).is(":checked")
            });
        });
    }

    return {
        initOption: initOption
    }
});
