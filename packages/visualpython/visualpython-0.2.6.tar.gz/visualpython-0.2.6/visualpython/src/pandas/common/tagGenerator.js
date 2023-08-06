define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/common/vpMakeDom'
    , 'nbextensions/visualpython/src/pandas/common/commonPandas'
], function(requirejs, $, vpCommon, vpConst, sb, vpFuncJS, vpMakeDom, libPandas) {

    /**
     * 코드 실행 후 결과값 보여주기 여부
     */
    var _VP_SHOW_RESULT = true;

    /**
     * 변수 조회 시 제외해야할 변수명
     */
    var _VP_NOT_USING_VAR = ['_html', '_nms', 'NamespaceMagics', '_Jupyter', 'In', 'Out', 'exit', 'quit', 'get_ipython'];
    /**
     * 변수 조회 시 제외해야할 변수 타입
     */
    var _VP_NOT_USING_TYPE = ['module', 'function', 'builtin_function_or_method', 'instance', '_Feature', 'type', 'ufunc'];

    var funcOptProp = {
        stepCount : 1
        , funcName : "tagGenerator"
        , funcID : "MJ000"  // TODO: ID 규칙 생성 필요
    }
    var vpFuncJS = new vpFuncJS.VpFuncJS(funcOptProp);

    // make dom
    var { renderInput
        , renderSelectBox
        , renderOption
        , renderLabel } = vpMakeDom;

    /**
     * @class TagGenerator
     * @constructor
     * @param {Object} pageThis Page Object
     * @param {string} funcId Function Id ex)pd001
     */
    var TagGenerator = function(pageThis, funcId) {
        this.funcId = funcId;
        this.pageThis = pageThis;
        this.package = libPandas[funcId];

        // 기본 표시 div tag
        this.ioDiv = 'vp_inputOutputBox';
        this.optionDiv = 'vp_optionBox';

        // Form Id
        this.formId = 'vp_optionForm';
    }

    /**
     * Manually set package
     * @param {object} package 
     */
    TagGenerator.prototype.setPackage = function(package) {
        this.package = package;
    }

    // TODO: 전체 태그 생성
    /**
     * Generate Label & Input tags
     */
    TagGenerator.prototype.generateTags = function() {
        var package = this.package;
        var that = this.pageThis;

        var ioBox = $(that.wrapSelector(this.ioDiv));
        var optBox = $(that.wrapSelector(this.optionDiv));

        // generate tag for variable options
        package.variable.forEach(opt => {
            // create tag
            var label = this.generateLabel(opt);
            var input = this.generateTag(opt);
            
            if (opt.required == true) {
                // if required, add to inputOutputBox
                ioBox.append( 
                    $('tr').append($('td').append(label))
                        .append($('td').append(input))
                );
            } else {
                // else add to optionBox
                optBox.append( 
                    $('tr').append($('td').append(label))
                        .append($('td').append(input))
                );
            }
        });

        // generate tag for ouput option
        package.output.forEach(opt => {
            // create tag
            var label = this.generateLabel(opt);
            var input = this.generateTag(opt);

            // add to inputOutputBox
            ioBox.append( 
                $('tr').append($('td').append(label))
                    .append($('td').append(input))
            );
        });
    }

    /**
     * Create Label Tag
     * @param {object} optObj 
     */
    TagGenerator.prototype.generateLabel = function(optObj) {
        var textValue = optObj.label;
        if (optObj.required == true) {
            // FIXME: required option label format
            // if required, highlight with * (default)
            textValue = '* ' + textValue;
        }

         // make label tag
        var label = vpMakeDom.renderLabel({
            class: 'vp-label'
            , for: optObj.name
            , text: textValue
        });

        return label;
    }

    // TODO: 단순 태그 생성기
    /**
     * Create Input Tag
     * @param {object} optObj 
     * @returns {HTMLElement} Tag Element
     */
    TagGenerator.prototype.generateTag = function(optObj) {
        // cases for components
        switch (optObj.component) {
            case 'option': 
                // make select tag
                var select = vpMakeDom.renderSelectBox(
                    {
                        class: 'vp-select'
                        , id: optObj.name
                    }
                );

                // option tag for 'option' list
                select = vpMakeDom.renderOption(select, {
                    class: 'vp-option'
                }, optObj.options);
                return select;
            case 'option_bool':
                // make select tag
                var select = vpMakeDom.renderSelectBox(
                    {
                        class: 'vp-select vp-select-bool'
                        , id: optObj.name
                    }
                );

                // option tag for True/False & default
                var options = ['', 'True', 'False'];
                var options_label = ['Default', 'True', 'False'];
                select = vpMakeDom.renderOption(select, {
                    class: 'vp-option'
                }, options);
                return select;
            case 'input': 
                // make select tag for 'type' list

                // select type event
                // if var
                // if str
                // if num
                // if format

                break;
        }

    }

    // TODO: 변수 조회해서 Select 태그 생성
    /**
     * Search variables with corresponding data types and append to select tag
     * @param {object} slctTag 
     * @param {Array<string>} types 
     * @param {string} defaultValue 
     */
    TagGenerator.prototype.generateVarSelectTag = function(slctTag, types, defaultValue = '') {
        // Index related types
        var INDEX_TYPES = ['RangeIndex', 'CategoricalIndex', 'MultiIndex', 'IntervalIndex', 'DatetimeIndex', 'TimedeltaIndex', 'PeriodIndex', 'Int64Index', 'UInt64Index', 'Float64Index'];
        // GroupBy related types
        var GROUPBY_TYPES = ['DataFrameGroupBy', 'SeriesGroupBy']

        // include related types
        if (types.indexOf('Index') >= 0) {
            types = types.concat(INDEX_TYPES);
        }
        if (types.indexOf('GroupBy') >= 0) {
            types = types.concat(GROUPBY_TYPES);
        }

        // search variable list
        this.searchVarList(types, function (result) {
            var jsonVars = result.replace(/'/gi, `"`);
            var varList = JSON.parse(jsonVars);
            
            // option 태그 구성 FIXME: vpMakeDom 사용
            varList.forEach(listVar => {
                if (types.includes(listVar.varType) && listVar.varName[0] !== '_') {
                    var option = document.createElement('option');
                    $(option).attr({
                        'value':listVar.varName,
                        'text':listVar.varName
                    });
                    // cell metadata test : defaultValue에 따라서 selected 적용
                    if (listVar.varName == defaultValue) {
                        $(option).prop('selected', true);
                    }
                    option.append(document.createTextNode(listVar.varName));
                    $(slctTag).append(option);
                }
            });

            // val-multi 일 경우(select multiple) value list 등록
            var classname = $(tag).attr('class');
            if (classname == 'var-multi') {
                $(slctTag).val(defaultValue);
            }
        });
    }

    /**
     * Return variables with specific data types
     * @param {Array<string>} types 조회할 변수들의 데이터유형 목록
     * @param {function} callback 조회 후 실행할 callback. parameter로 result를 받는다
     */
    TagGenerator.prototype.searchVarList = function(types, callback) {
        // make command for searching variable list
        var cmdSB = new sb.StringBuilder();
        cmdSB.append(`print([{'varName': v, 'varType': type(eval(v)).__name__}`);
        cmdSB.appendFormat(`for v in dir() if (v not in {0}) `, JSON.stringify(_VP_NOT_USING_VAR));
        cmdSB.appendFormat(`& (type(eval(v)).__name__ not in {0}) `, JSON.stringify(_VP_NOT_USING_TYPE));
        // if no data types passed, exclude it
        if (types != undefined && types.length > 0) {
            cmdSB.appendFormat(`& (type(eval(v)).__name__ in {0})`, JSON.stringify(types));
        }
        cmdSB.appendFormat(`])`);

        // execute on kernel
        vpFuncJS.vp_executePython(cmdSB.toString(), function(result) {
            callback(result);
        });
    }

    return {
        TagGenerator: TagGenerator
    }
});