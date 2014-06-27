<?php
if(isset($_POST['data']))
	$data = $_POST["data"];

require_once "lib/CKIPClient.php";
// CKIP define
define("CKIP_SERVER", "140.109.19.104");
define("CKIP_PORT", 1501);
define("CKIP_USERNAME", "b99902025");
define("CKIP_PASSWORD", "jialunwu");

// to make the token work efficiency
function stringfilter($string){
	$string = str_replace(" ", "\n", $string);
	return $string;
}

// CKIP object
$ckip_client_obj = new CKIPClient(
   CKIP_SERVER,
   CKIP_PORT,
   CKIP_USERNAME,
   CKIP_PASSWORD
);

$data = preg_split("/，/",$data);
$return_term = [];
for($i=0;$i<sizeof($data);$i++){
		//CKIP method
	$return_text = $ckip_client_obj->send($data[$i]);
	$return_sentence = $ckip_client_obj->getSentence();
	$return_term[$i] = $ckip_client_obj->getTerm();
}

//$data = stringfilter($data);
$output = array();
for($i=0;$i<sizeof($return_term);$i++)
	for($j=0;$j<sizeof($return_term[$i]);$j++){

		$term =  $return_term[$i][$j]['term'];
	//	echo $term."/";
		$output[$j] = $term;
	}

//for offline
//$send_obj = json_encode($output);
//echo $send_obj;
//return;

//

$server = "linux7.csie.ntu.edu.tw";
$port = 10000;
$socket = socket_create(AF_INET,SOCK_STREAM,SOL_TCP);
$connection = socket_connect($socket,$server,$port);
//$output = array('你好','好吃','開心','難過','掰掰');
$send_obj = json_encode($output);

//send
socket_write($socket,$send_obj,strlen($send_obj));
//receive
if(false !== ($read_obj = socket_read($socket,1024))){
	//echo "log: read ".strlen($read_obj)." bytes. ".$read_obj."<br>";
}else{
	echo "log: socket_recv() failed; reason: ". socket_strerror(socket_last_error($socket))."\n";
}

echo $read_obj;
$obj = json_decode($read_obj);

//print "pos:".$obj->{'pos'}."<br>";
//print "neg:".$obj->{'neg'}."<br>";

socket_close($socket);
?>
