//用于弹出高层提示框

var infostr_1 = "<div class=\"alert ";
var infostr_2_yellow = "alert-warning";
var infostr_2_green = "alert-success";
var infostr_2_red = "alert-danger";
var infostr_2_blue = "alert-info";

var infostr_3 = " alert-dismissible\" role=\"alert\">\n" +
    "<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">" +
    "<span aria-hidden=\"true\">&times;</span></button>\n";
var infostr_4 = "<strong>Warning!</strong> This message come from WangNing.\n";
var infostr_5 = "</div>";


function ShowTopInfo1(infotype,infocontent) {
    $("#Topinfo1").append(infostr_1+infotype+infostr_3+infocontent+infostr_5);
}