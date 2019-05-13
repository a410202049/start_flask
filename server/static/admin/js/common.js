function serializeJson(array){
    var jsonData = {};
    $.each(array, function(i,n){
        if(n.value !="" && n.value !=null){
            jsonData[n.name] = n.value;
        }
    });
    return jsonData;
}

//清除html格式
function CleanPastedHTML(input) {
  // 1. remove line breaks / Mso classes
  var stringStripper = /(\n|\r| class=(")?Mso[a-zA-Z]+(")?)/g;
  var output = input.replace(stringStripper, ' ');
  // 2. strip Word generated HTML comments
  var commentSripper = new RegExp('<!--(.*?)-->','g');
  var output = output.replace(commentSripper, '');
  var tagStripper = new RegExp('<(/)*(meta|link|span|\\?xml:|st1:|o:|font)(.*?)>','gi');
  // 3. remove tags leave content if any
  output = output.replace(tagStripper, '');
  // 4. Remove everything in between and including tags '<style(.)style(.)>'
  var badTags = ['style', 'script','applet','embed','noframes','noscript'];

  for (var i=0; i< badTags.length; i++) {
    tagStripper = new RegExp('<'+badTags[i]+'.*?'+badTags[i]+'(.*?)>', 'gi');
    output = output.replace(tagStripper, '');
  }
  // 5. remove attributes ' style="..."'
  var badAttributes = ['style', 'start'];
  for (var i=0; i< badAttributes.length; i++) {
    var attributeStripper = new RegExp(' ' + badAttributes[i] + '="(.*?)"','gi');
    output = output.replace(attributeStripper, '');
  }
  return output;
}

/* 生成uuid */
function getUUID() {
    var a, j, k, l, len, raw_char, ref, s, uuid_hex_string;
    raw_char = '1234567890abcdrf';
    uuid_hex_string = '';
    ref = [1, 2];
    for (j = 0, len = ref.length; j < len; j++) {
        k = ref[j];
        a = Math.random();
        a = parseInt(String(a).replace('0.', ''));
        for (s = l = 1; l <= 16; s = ++l) {
            uuid_hex_string = uuid_hex_string + raw_char.charAt(a % 16);
            a = a / 16;
        }
    }
    return uuid_hex_string;
}

$(function(){
    //获取get参数
    $.extend(
    {
        /**
         * url get parameters
         * @public
         * @return array()
         */
        urlGet:function()
        {
            var aQuery = window.location.href.split("?");//取得Get参数
            var aGET = new Array();
            if(aQuery.length > 1)
            {
                var aBuf = aQuery[1].split("&");
                for(var i=0, iLoop = aBuf.length; i<iLoop; i++)
                {
                    var aTmp = aBuf[i].split("=");//分离key与Value
                    aGET[aTmp[0]] = aTmp[1];
                }
            }
            return aGET;
        }
    });

    // var keyword = $.urlGet();
    // console.log(keyword['name'])

	// 模态框 垂直居中
	function centerModals(){
	  $('.modal').each(function(i){
	      var $clone = $(this).clone().css('display', 'block').appendTo('body');
	      var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
	      top = top > 0 ? top : 0;
	      $clone.remove();
	      $(this).find('.modal-content').css("margin-top", top);
	  });
	}
	$('.modal').on('show.bs.modal', centerModals);
	$(window).on('resize', centerModals);

	//设置参数
	function setGetParam(paramObj){
		var href = "?";
        $.each(paramObj,function(index,param){
    		href += index+"="+param+"&";
        });
        href=href.substring(0,href.length-1);
        if(href){
            window.location.href = href;
        }else{
            window.location.href = window.location.pathname;
        }
	}

    //得到form表单的数据
    function serializeForm(form){
        var paramObj = {};
        var paramArray = form.serializeArray();
        $.each(paramArray,function(index,param){
            if(param.value != null && param.value.trim() != "" && param.value.trim() != "-1"){
                paramObj[param.name] = param.value;
            }
        });
        return paramObj;
    }


    //搜 索
    $("#search").click(function(){
        var search_data =  serializeForm($('.search-box'));
        setGetParam(search_data);
    });

    $('#reset').click(function(){
    	window.location.href = window.location.pathname;
    });

    //按键监听  回车=搜索
    $("body").keypress(function(e){
        if(e.which == 13){
            var search_data =  serializeForm($('.search-box'));
        }
    });




})



Date.prototype.Format = function (fmt) {
    var fmt = fmt||"yyyy-MM-dd";
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
};

var common = {
    getDate:function(){
        var date = arguments[0]||"now";
        var now = new Date().getTime();
        var nowdays = new Date();
        var hasFunc = (typeof(arguments[1])=="function");
        if ((typeof(date)=="number")) {
            var type = hasFunc?"default":arguments[1]
                ,func = hasFunc?arguments[1]:arguments[arguments.length-1]
                ,result = (Number(date)*1000*3600*24)
            switch(type){
                case "ago":
                    result = (new Date(now-result)).Format()
                    break
                case "later":
                default :
                    result = (new Date(now+result)).Format()
                    break
            }
            if(typeof(func)=="function")func(result)
            return result
        }
        var result;
        switch (date){
            case "now":
                result = (new Date()).Format()
                break
            case "today":
                result = [this.getDate(),this.getDate()]
                break;
            case "last-7-days":
                result = [this.getDate(-6),nowdays.Format()]
                break
            case "yesterday":
                result = [this.getDate(-1),this.getDate(-1)]
                break
            case "this-week":
                result=[(new Date(now-((nowdays.getDay()-1)*1000*3600*24))).Format(),nowdays.Format()]
                break;
            case "last-week":
                var prevDay =  new Date(now-(7000*3600*24));
                var startDay = prevDay.getTime()-((prevDay.getDay()-1)*1000*3600*24);
                result = [new Date(startDay).Format(),new Date(startDay+(6*1000*3600*24)).Format()]
                break;
            case "last-month": {
                var year = nowdays.getFullYear();
                var month = nowdays.getMonth();
                if(month==0)
                {
                    month=12;
                    year=year-1;
                }
                if (month < 10) {
                    month = "0" + month;
                }
                var myDate = new Date(year, month, 0);
                result=[(year + "-" + month + "-" + "01"),(year + "-" + month + "-" + myDate.getDate())]
                break
            }
            case "this-month": {
                var year = nowdays.getFullYear();
                var month = nowdays.getMonth()+1;
                var day = nowdays.getDate();
                if (month < 10) {
                    month = "0" + month;
                }
                if(day < 10){
                    day = "0"+day;
                }

                var firstDay = year + "-" + month + "-" + "01";//这个月的第一天
                var myDate = new Date(year, month, 0);
                var lastDay = year + "-" + month + "-" + day;//今天
                result=[firstDay,lastDay]
                break
            }
            case "last-3-months":{
                var year = nowdays.getFullYear();
                var month = parseInt(nowdays.getMonth())+1;
                var day = nowdays.getDate();

                var startMonth = month-2;
                if(startMonth<=0)
                {
                    startMonth+=12;
                    var startYear=year-1;
                }else{
                    var startYear=year;
                }
                if (startMonth < 10) {
                    startMonth = "0" + startMonth;
                }
                if (month < 10) {
                    month = "0" + month;
                }
                if(day < 10){
                    day = "0"+day;
                }
                var myDate = new Date(year, month, 0);
                result=[(startYear + "-" + startMonth + "-" + "01"),(year + "-" + month + "-" + day)]
                break
            }
            default:
                result=date;
                console.warn("Invalid Date Range Argument Value: "+date)
                break
        }
        var func = hasFunc?arguments[1]:arguments[arguments.length-1];
        if(typeof(func)=="function")func(result)
        return result;

    }
};