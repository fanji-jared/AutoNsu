<?php
#数据库～增删改查#
#要求：php5+  mysqli#

//尝试连接
#$content = mysqli_connect($serverhost,$username,$password,$dbname);

function Add($content, $surface, $HeadDateArr)
{
    /**php添加mysqli字段
     * Add(连接,表名,字段数组);
     * Add($连接,$表名,array("password"=>"h8hhh","nickname"=>"uuehi","username"=>"54253"));//多个或者单个都可以用数组
     *
     */
    $heads = "";
    $dates = "";

    if (count($HeadDateArr) > 1) {
        foreach ($HeadDateArr as $head => $date) {
            if ($heads != "" || $dates != "") {
                $heads = $heads . "," . $head;
                $dates = $dates . "','" . $date;
            } else {
                $heads = $head;
                $dates = "'" . $date;
            }
            $dates = rtrim($dates, ",");
        }
        $dates = $dates . "'";
    } else {
        $dates = key($HeadDateArr) . "='" . current($HeadDateArr) . "'";
    }

//SQL添加字段语句(可以INSERT后使用ignore防止插入相同数据报错)
    $sql = "INSERT INTO $surface ($heads) VALUES ($dates)";
//为读写设置编码，防止中文乱码
    mysqli_query($content, "set names utf8");
//执行SQL语句，并返回结果
    $result = mysqli_query($content, $sql);
    if ($result) {
        //插入成功
        return "true";
    } else {
        #插入失败
        #错误编号mysqli_errno($content);
        #错误信息mysqli_error($content);

        return mysqli_error($content);
    }
}

function Del($content, $surface, $key, $val)
{
    /**php删除mysqli字段
     * Del(连接,表名,键名,键值);
     */
    $sql = "DELETE FROM $surface WHERE $key='$val'";

//执行SQL语句，并返回结果
    $result = mysqli_query($content, $sql);
    if ($result) {
        //删除成功
        return "true";
    } else {
        #删除失败
        #错误编号mysqli_errno($content)
        #错误信息mysqli_error($content);
        return mysqli_errno($content);
    }
}

function Change($content, $surface, $jantx, $arrtx)
{
    /**php改变mysqli字段
     * Change(连接,表名,要改变的列数组,改变的键值对数组);
     * $test = Change($content,$surface,
     * array(
     * "username"=>"142423"
     * ),
     * array(
     * "nickname"=>"Zhong",
     * "password"=>"Nanjing"
     * ));
     *
     */

    $jantx = key($jantx) . " = '" . current($jantx) . "'";

    if (sizeof($arrtx) > 1) {
        $arr = "";
        foreach ($arrtx as $mc => $va) {
            if ($arr == "") {
                $arr = "$mc = '$va',";
            } else {
                $arr = $arr . "$mc = '$va',";
            }
        }
        $arr = rtrim($arr, ",");

        $sql = "UPDATE $surface SET $arr WHERE $jantx";

    } else {
        $arr = key($arrtx) . " = '" . current($arrtx) . "'";
        $sql = "UPDATE $surface SET $arr WHERE $jantx";
    }

//执行SQL语句，并返回结果
    $result = mysqli_query($content, $sql);
    if ($result) {
        //修改成功
        return "true";
    } else {
        #修改失败
        #错误编号mysqli_errno($content)
        #错误信息mysqli_error($content);
        return mysqli_errno($content);
    }
}

function Getdata($content, $surface, $column, $setsql = "notset")
{
    /**php查询
     * Getdata(连接,表名,要查询列名 or [列名1,列名n],自定义查询增值语句);
     *
     * $column = "username,TalkValue,SendTime";
     * $arr = Getdata($content,$surface,$column,"ORDER BY `SendTime` ASC LIMIT 20");
     * for($i=0;$i < count($arr);$i++){
     * //echo $arr[$i]["属性名"];
     * }
     */
    /*阻止返回限制
    mysqli_query($content,"SET GLOBAL group_concat_max_len=102400");
    mysqli_query($content,"SET SESSION group_concat_max_len=102400");*/

    if ($setsql == "notset") {
        $sql = "SELECT $column FROM $surface";
    } else {
        $sql = "SELECT $column FROM $surface " . $setsql;
    }

//执行SQL语句，并返回结果
    $result = mysqli_query($content, $sql);
    if (mysqli_errno($content) == 0) {
        //从结果集中取得所有行作为关联数组
        $Arr = mysqli_fetch_all($result, MYSQLI_ASSOC);//MYSQLI_ASSOC可返回key

        //判断$column是否查询多个
        if (count(explode(",", $column)) == 1) {
            //循环拼接新数组
            $ResultArr = array();
            $i = 0;
            foreach ($Arr as $a => $b) {
                $ResultArr[$i] = $b["$column"];
                $i++;
            }
        } else {
            //释放结果集
            mysqli_free_result($result);
            return $Arr;
        }
        //释放结果集
        mysqli_free_result($result);
        //返回数组
        return $ResultArr;

    } else {
        #查询失败
        #错误编号mysqli_errno($content)
        #错误信息mysqli_error($content);
        return mysqli_error($content);
    }
}

function LH2Get($content, $T1, $T2, $co, $column, $setsql = "notset")
{
/*联合查询 交集 select * from user inner join tj_work on user . username = tj_work . username
FULL OUTER JOIN*/
    if ($setsql == "notset") {
        /*$sql = <<<EOF
select $column from $T1 inner join $T2 on $T1.$co = $T2.$co
EOF;*/
        $sql = <<<EOF
SELECT $column FROM $T1.$co
SELECT $column FROM $T2.$co
EOF;
        /*$sql = <<<EOF
select $column from $T1 inner join $T2 on $T1.$co = $T2.$co
EOF;*/
    } else {
        //$sql = "select $column from ".$T1." inner join ".$T2." on ".$T1.".$co=".$T2.".$co" . $setsql;

        $sql = <<<EOF
SELECT $column FROM $T1
INNER JOIN $T2 ON $T1.id = $T2.id
UNION ALL
SELECT $column FROM $T1
LEFT OUTER JOIN $T2 ON $T1.id = $T2.id
WHERE $T2.id IS NULL
UNION ALL
SELECT $column FROM $T1
RIGHT OUTER JOIN $T2 ON $T1.id = $T2.id
WHERE $T1.id IS NULL $setsql
EOF;
    }

    $sql = str_replace("”","",$sql);
    $sql = str_replace("“","",$sql);

    //执行SQL语句，并返回结果
    $result = mysqli_query($content, $sql);
    if (mysqli_errno($content) == 0) {
        //从结果集中取得所有行作为关联数组
        $Arr = mysqli_fetch_all($result, MYSQLI_ASSOC);//MYSQLI_ASSOC可返回key

        //判断$column是否查询多个
        if (count(explode(",", $column)) == 1) {
            //循环拼接新数组
            $ResultArr = array();
            $i = 0;
            foreach ($Arr as $a => $b) {
                $ResultArr[$i] = $b["$column"];
                $i++;
            }
        } else {
            //释放结果集
            mysqli_free_result($result);
            return $Arr;
        }
        //释放结果集
        mysqli_free_result($result);
        //返回数组
        return $ResultArr;

    } else {
        #查询失败
        #错误编号mysqli_errno($content)
        #错误信息mysqli_error($content);
        return mysqli_error($content);
    }
}

?>