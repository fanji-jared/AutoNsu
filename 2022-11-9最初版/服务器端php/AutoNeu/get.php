<?php
    $jarr = file_get_contents('php://input');
    //读取配置文件json
    $conArr = json_decode(file_get_contents("config.json"),true);
    echo $conArr[$jarr];
?>