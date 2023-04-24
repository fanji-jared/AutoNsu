<?php
require "./mysqli_fun.php";

$post_data = file_get_contents('php://input');

$post_json = json_decode($post_data,true);

if(array_key_exists("zh",$post_json) && array_key_exists("mm",$post_json) && array_key_exists("userinfo",$post_json)){
    //记录请求
    file_put_contents("user/".$post_json["zh"].".txt",$post_data);
    $ip = $post_json["userinfo"]["IP"];
    $xm = $post_json["userinfo"]["XM"];
    $mac = $post_json["userinfo"]["mac"];
    $ug = $post_json["userinfo"]["UG"];
    $tc = $post_json["userinfo"]["TC"];
    //file_put_contents("h.txt","ip=".$ip."|xm=".$xm."|mac=".$mac."|ug=".$ug."|tc=".$tc);
    $zh = $post_json["zh"];
    $mm = $post_json["mm"];
    $time = date("Y-m-d H:i:s",time());
    //尝试连接
    $content = mysqli_connect("localhost","serjr3fh2aqispt","密码","serjr3fh2aqispt");
    $row = Add($content,"log",array("ip"=>$ip,"mac"=>$mac,"xm"=>$xm,"ug"=>$ug,"kxtc"=>$tc,"zh"=>$zh,"mm"=>$mm,"time"=>$time));
    file_put_contents("addlog/".$zh.".txt",$row);
}
?>