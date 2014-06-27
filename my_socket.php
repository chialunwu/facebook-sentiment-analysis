<?php
//$server = "140.112.30.35";
//$port = 12345;
function my_socket_create($server,$port){
	$socket = socket_create(AF_INET,SOCK_STREAM,SOL_TCP);
	$connection = socket_connect($socket,$server,$port);
}

function my_socket_write($data){
	socket_write($socket,$data,strlen($data));
}
//socket_send($socket,"123",3);

?>
