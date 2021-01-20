
var taskSizeChart = echarts.init(document.getElementById('taskSize'));
var taskSizeChart2 = echarts.init(document.getElementById('taskSize2'));
var taskSizeChart3 = echarts.init(document.getElementById('taskSize3'));
var taskSizeChart4 = echarts.init(document.getElementById('taskSize4'));

var startTime = new Date();


$(function () {
    taskSizeTj();
    taskSizeV();
    taskSizeS();
    taskSizeAH();
    initTable();

    var namespace = '/ele';
    var show_time=0

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace, {transports: ['websocket']});
        socket.on('server_response', function(res) {
            var res_a=res.a.toFixed(3);
            console.log(res_a);
            $("#aCurrentSpan").text(res_a);
            syncTj(res_a)
            var res_v=res.v.toFixed(3);
            syncV(res_v)
            console.log(res_v);
            $("#vCurrentSpan").text(res_v);
            var res_s=res.s.toFixed(2);
            syncS(res_s)
            console.log(res_s);
            $("#sCurrentSpan").text(res_s);
            var res_ah=res.ah.toFixed(3);
            syncAH(res_ah)
            $("#ahCurrentSpan").text(res_ah);
            console.log(res_ah);
            var alarm=res.alarm;

            if(alarm<1)
            {
                if(show_time<1)
                {
                $("#alarmCurrentSpan").text("正常");
                $("#alarmCurrentSpan").css("color","#00fbfe");
                }
                else
                {
                    show_time=show_time-1
                    $("#alarmCurrentSpan").text("异常");
                    $("#alarmCurrentSpan").css("color","#FF4500");
                }

            }
            else
            {
                $("#alarmCurrentSpan").text("异常");
                $("#alarmCurrentSpan").css("color","#FF4500");
                show_time=10
            }

            });

         socket.on('server_response_quality', function(res) {
            var data=res.table;
            var mileageDay=res.mileageDay;
            var optDay=res.optDay;
            //console.log(res);
            //alert(data[0][0])
            syncTable(data,mileageDay,optDay);

            });

            setInterval(tick, 1000);


});

function tick(){
    var today = new Date();
    document.getElementById("localtime").innerHTML = showLocale(today);

    var t = today - startTime;
    var day = Math.floor(t/1000/60/60/24);
    var hour = Math.floor(t/1000/60/60%24);
    var min = Math.floor(t/1000/60%60);
    var sec = Math.floor(t/1000%60);
    $("#runTimeTj").html(day+" 天 "+hour+" 小时 "+min+" 分 "+sec+" 秒");
}

function syncTj(current_a) {


    var today = new Date();

    var option = taskSizeChart._option;
    var data0 = option.series[0].data;//本次
    //删除第一个
    data0.shift();
    //追加一个新数据
    data0.push(current_a);

    option.xAxis[0].data.shift();
    option.xAxis[0].data.push( today.getMinutes() + ":" + today.getSeconds());//更新x轴

    taskSizeChart.setOption(option);
}
function syncV(current_v) {


    var today = new Date();

    var option = taskSizeChart2._option;
    var data0 = option.series[0].data;//本次

    data0.shift();
    data0.push(current_v);

    option.xAxis[0].data.shift();
    option.xAxis[0].data.push( today.getMinutes() + ":" + today.getSeconds());//更新x轴

    taskSizeChart2.setOption(option);
}
function syncS(current_s) {


    var today = new Date();

    var option = taskSizeChart3._option;
    var data0 = option.series[0].data;//本次

    data0.shift();
    data0.push(current_s);

    option.xAxis[0].data.shift();
    option.xAxis[0].data.push( today.getMinutes() + ":" + today.getSeconds());//更新x轴

    taskSizeChart3.setOption(option);
}

function syncAH(current_ah) {


    var today = new Date();

    var option = taskSizeChart4._option;
    var data0 = option.series[0].data;//本次

    data0.shift();
    data0.push(current_ah);

    option.xAxis[0].data.shift();
    option.xAxis[0].data.push( today.getMinutes() + ":" + today.getSeconds());//更新x轴

    taskSizeChart4.setOption(option);
}

function taskSizeTj(){
    var names = [];
    var values = [];
    var option = {
        color: ['#00b3ac'],
        legend: {
        textStyle:{

                            fontSize: 18,
                            color: '#e9f0fb'
                        },
            data: ['加速度'],
            x: 'center',
            y: 30
        },
        tooltip : {
            trigger: 'axis',
            axisPointer : {
                type : 'shadow'
            }
        },
        xAxis : [
            {
                data : names,
                type: 'category',
                splitLine:{
                    show: false
                },
                axisLabel: {
                    interval: 5,
                    show: true,
                    textStyle: {
                    //更改坐标轴文字颜色
                        color: '#c3dbff',
                        //更改坐标轴文字大小
                        fontSize : 14
                    }
                }
            }
        ],
        yAxis : [
            {
                type : 'value',
                axisLabel: {
                    show: true,
                    textStyle: {
                        color: '#c3dbff'
                    }
                }
            }
        ],
        series : [
            {
                name:'加速度（米/平方秒）',
                type:'line',
                smooth: true,
                barWidth: '60%',
                data:values
            }
        ]
    };
    var _time = new Date().getTime();
    for(var i = 60; i > 0; i--){
        var _tempDate = new Date(_time - 1000 * 10 * i);
        names.push(_tempDate.getMinutes() + ":" + _tempDate.getSeconds());
        values.push(Math.random() * 0.01  );
    }
    option.xAxis[0].data.value = names;
    option.series[0].data.value = values;
    taskSizeChart.setOption(option);
}

function taskSizeV(){
    var names = [];
    var values = [];
    var option = {
        color: ['#00b3ac'],
        legend: {
        textStyle:{

                            fontSize: 18,
                            color: '#e9f0fb'
                        },
            data: ['速度'],
            x: 'center',
            y: 30
        },
        tooltip : {
            trigger: 'axis',
            axisPointer : {
                type : 'shadow'
            }
        },
        xAxis : [
            {
                data : names,
                type: 'category',
                splitLine:{
                    show: false
                },
                axisLabel: {
                    interval: 5,
                    show: true,
                    textStyle: {
                    //更改坐标轴文字颜色
                        color: '#c3dbff',
                        //更改坐标轴文字大小
                        fontSize : 14
                    }
                }
            }
        ],
        yAxis : [
            {
                type : 'value',
                axisLabel: {
                    show: true,
                    textStyle: {
                        color: '#c3dbff'
                    }
                }
            }
        ],
        series : [
            {
                name:'速度（米/秒）',
                type:'line',
                smooth: true,
                barWidth: '60%',
                data:values,
                itemStyle : {
                                normal : {
                                    color:'#00FF00',
                                    lineStyle:{
                                        color:'#00FF00'
                                    }
                                }
                            }

            }
        ]
    };
    var _time = new Date().getTime();
    for(var i = 60; i > 0; i--){
        var _tempDate = new Date(_time - 1000 * 10 * i);
        names.push(_tempDate.getMinutes() + ":" + _tempDate.getSeconds());
        values.push(Math.random() * 0.01  );
    }
    option.xAxis[0].data.value = names;
    option.series[0].data.value = values;
    taskSizeChart2.setOption(option);
}

function taskSizeS(){
    var names = [];
    var values = [];
    var option = {
        color: ['#00b3ac'],
        legend: {
        textStyle:{

                            fontSize: 18,
                            color: '#e9f0fb'
                        },
            data: ['位置'],
            x: 'center',
            y: 30
        },
        tooltip : {
            trigger: 'axis',
            axisPointer : {
                type : 'shadow'
            }
        },
        xAxis : [
            {
                data : names,
                type: 'category',
                splitLine:{
                    show: false
                },
                axisLabel: {
                    interval: 5,
                    show: true,
                    textStyle: {
                    //更改坐标轴文字颜色
                        color: '#c3dbff',
                        //更改坐标轴文字大小
                        fontSize : 14
                    }
                }
            }
        ],
        yAxis : [
            {
                type : 'value',
                axisLabel: {
                    show: true,
                    textStyle: {
                        color: '#c3dbff'
                    }
                }
            }
        ],
        series : [
            {
                name:'位置（米）',
                type:'line',
                smooth: true,
                barWidth: '60%',
                data:values,
                itemStyle : {
                                normal : {
                                    color:'#00BFFF',
                                    lineStyle:{
                                        color:'#00BFFF'
                                    }
                                }
                            }
            }
        ]
    };
    var _time = new Date().getTime();
    for(var i = 60; i > 0; i--){
        var _tempDate = new Date(_time - 1000 * 10 * i);
        names.push(_tempDate.getMinutes() + ":" + _tempDate.getSeconds());
        values.push(Math.random() * 0.1 );
    }
    option.xAxis[0].data.value = names;
    option.series[0].data.value = values;
    taskSizeChart3.setOption(option);
}

function taskSizeAH(){
    var names = [];
    var values = [];
    var option = {
        color: ['#00b3ac'],
        legend: {
        //字体大小颜色
            textStyle:{

                            fontSize: 18,
                            color: '#e9f0fb'
                        },
            data: ['加速度'],
            x: 'center',
            y: 30
        },
        tooltip : {
            trigger: 'axis',
            axisPointer : {
                type : 'shadow'
            }
        },
        xAxis : [
            {
                data : names,
                type: 'category',
                splitLine:{
                    show: false
                },
                axisLabel: {
                    interval: 5,
                    show: true,
                    textStyle: {
                    //更改坐标轴文字颜色
                        color: '#c3dbff',
                        //更改坐标轴文字大小
                        fontSize : 14
                    }
                }
            }
        ],
        yAxis : [
            {
                type : 'value',
                axisLabel: {
                    show: true,
                    textStyle: {
                        color: '#c3dbff'
                    }
                }
            }
        ],
        series : [
            {
                name:'加速度（米/平方秒）',
                type:'line',
                smooth: true,
                barWidth: '60%',
                data:values,
                itemStyle : {
                                normal : {
                                    color:'#FF0000',
                                    lineStyle:{
                                        color:'#FF0000'
                                    }
                                }
                            }
            }
        ]
    };
    var _time = new Date().getTime();
    for(var i = 60; i > 0; i--){
        var _tempDate = new Date(_time - 1000 * 10 * i);
        names.push(_tempDate.getMinutes() + ":" + _tempDate.getSeconds());
        values.push(Math.random() * 0.01 );
    }
    option.xAxis[0].data.value = names;
    option.series[0].data.value = values;
    taskSizeChart4.setOption(option);
}

function timestampToTime(fmt, timestamp) {
    var date = new Date(timestamp);
    var ret;
    var opt = {
        "Y+": date.getFullYear().toString(),        // 年
        "m+": (date.getMonth() + 1).toString(),     // 月
        "d+": date.getDate().toString(),            // 日
        "H+": date.getHours().toString(),           // 时
        "M+": date.getMinutes().toString(),         // 分
        "S+": date.getSeconds().toString()          // 秒
        // 有其他格式化字符需求可以继续添加，必须转化成字符串
    };
    for (var k in opt) {
        ret = new RegExp("(" + k + ")").exec(fmt);
        if (ret) {
            fmt = fmt.replace(ret[1], (ret[1].length == 1) ? (opt[k]) : (opt[k].padStart(ret[1].length, "0")))
        };
    };
    return fmt;
}


function initTable() {
    $("#addTj").html("(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)/50000m");
    $("#updateTj").html("(&nbsp;&nbsp;&nbsp;&nbsp;)/2000次");
    $("#deleteTj").html(" &nbsp;&nbsp;&nbsp;天");

// ['最大加速度', 'A95加速度', '最大减速度', 'A95减速度', '最大速度', '运行总里程','运行总次数' '时间']
    var HTML = "<thead>\n" +
        "        <td title=\"序号\">序号</td>\n" +
        "        <td title=\"运行总次数\">运行总次数</td>\n" +
        "        <td title=\"最大加速度\">最大加速度</td>\n" +
        "        <td title=\"A95加速度\">A95加速度</td>\n" +
        "        <td title=\"最大减速度\">最大减速度</td>\n" +
        "        <td title=\"A95减速度\">A95减速度</td>\n" +
        "        <td title=\"最大速度\">最大速度</td>\n" +
        "        <td title=\"运行总里程\">运行总里程</td>\n" +
        "        <td title=\"状态\">状态</td>\n" +
        "        <td title=\"时间\">时间</td>\n" +
        "        </thead>\n" +
        "        <tbody>\n";
    HTML += "</tbody>";
    $('.commonTable').html(HTML);

}
function syncTable(data,mileageDay,optDay) {

// ['最大加速度', 'A95加速度', '最大减速度', 'A95减速度', '最大速度', '运行总里程','运行总次数' '时间']
    var HTML = "<thead>\n" +
        "        <td title=\"序号\">序号</td>\n" +
        "        <td title=\"运行总次数\">运行总次数</td>\n" +
        "        <td title=\"最大加速度\">最大加速度</td>\n" +
        "        <td title=\"A95加速度\">A95加速度</td>\n" +
        "        <td title=\"最大减速度\">最大减速度</td>\n" +
        "        <td title=\"A95减速度\">A95减速度</td>\n" +
        "        <td title=\"最大速度\">最大速度</td>\n" +
        "        <td title=\"运行总里程\">运行总里程</td>\n" +
        "        <td title=\"状态\">状态</td>\n" +
        "        <td title=\"时间\">时间</td>\n" +
        "        </thead>\n" +
        "        <tbody>\n";
    var d=0;
    var op_times=0

    $(data).each(function (index, ele) {
        d=ele[5].toFixed(1);
        op_times=ele[6];
        HTML += "<tr>\n" +
            "            <td>" + (index + 1) + "</td>\n" +
            "            <td><span style='color: #00cc00'>" + ele[6] + "</span></td>\n" +
            "            <td>" + ele[0] + "</td>\n" +
            "           <td><span style='color: #00cc00'>" + ele[1] + "</span></td>\n" +
            "            <td>" + ele[2] + "</td>\n" +
            "            <td><span style='color: #00cc00'>" + ele[3] + "</span></td>\n" +
            "            <td>" + ele[4] + "</td>\n" +
            "            <td>" + ele[5] + "</td>\n" ;
            if(Math.abs(ele[0])>1.5 || Math.abs(ele[2])>1.5 ||Math.abs(ele[4])>2.5)
            {
                HTML +=" <td><span class=\"btn btn-red\" style=\"width: 80px\" >异常</span></td>\n";
            }
            else
             {
                HTML +=" <td><span class=\"btn btn-small\" style=\"width: 80px\" >正常</span></td>\n";
            }
            HTML +="<td><span style='color: #00cc00;'>" + ele[7] + "</span></td>\n";
    });

    HTML += "</tbody>";
    $('.commonTable').html(HTML);

    var mileage_limit=50000
    var opt_limit=2000
    if(mileageDay<1){
    mileageDay=1000
    }
    if(opt_limit<1){
    optDay=50
    }

    matain_days=(mileage_limit-d)/mileageDay;
    var matain_opt=(opt_limit-op_times)/optDay;
    if(matain_days>matain_opt){
    matain_days=matain_opt
    }
    $("#addTj").html("("+d +")/"+mileage_limit+"米");
    $("#updateTj").html("("+op_times +")/"+opt_limit+"次");
    $("#deleteTj").html(matain_days.toFixed(0) + " 天");



    $("#syncStateSpan").html("<font color='#00cc00'>正常</font>");


}
function showLocale(objD){
    var str,colorhead,colorfoot;
    var yy = objD.getYear();
    if(yy<1900) yy = yy+1900;
    var MM = objD.getMonth()+1;
    if(MM<10) MM = '0' + MM;
    var dd = objD.getDate();
    if(dd<10) dd = '0' + dd;
    var hh = objD.getHours();
    if(hh<10) hh = '0' + hh;
    var mm = objD.getMinutes();
    if(mm<10) mm = '0' + mm;
    var ss = objD.getSeconds();
    if(ss<10) ss = '0' + ss;
    var ww = objD.getDay();
    if  ( ww==0 )  colorhead="<font color=\"#ffffff\">";
    if  ( ww > 0 && ww < 6 )  colorhead="<font color=\"#ffffff\">";
    if  ( ww==6 )  colorhead="<font color=\"#ffffff\">";
    if  (ww==0)  ww="星期日";
    if  (ww==1)  ww="星期一";
    if  (ww==2)  ww="星期二";
    if  (ww==3)  ww="星期三";
    if  (ww==4)  ww="星期四";
    if  (ww==5)  ww="星期五";
    if  (ww==6)  ww="星期六";
    colorfoot="</font>"
    str = colorhead + yy + "-" + MM + "-" + dd + " " + hh + ":" + mm + ":" + ss + "  " + ww + colorfoot;
    return(str);
}

function hideBugBtn() {
    $("#bugBtn").hide();
}

