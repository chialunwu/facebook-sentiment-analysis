IR_Project
==========
1. CKIPClient/ 
   A client program written by NTNU (http://tm.itc.ntnu.edu.tw/CNLP/?q=node/6) 
   to send request to the Chinese tokenizer server written by Sinica (http://ckipsvr.iis.sinica.edu.tw/)
   
   usage: sh run.sh input_dir output_dir 
          input_dir - contain raw chinese text files (Must be in Big5 or utf-16)
          output_dir - the tokenized texts

2. CKIPClient.php
   PHP client to send requests to tokenizer (https://github.com/fukuball/CKIPClient-PHP)

   usage: $raw_text = "Chinese texts..."
   	  $return_text = $ckip_client_obj->send($raw_text);
	  $return_sentences = $ckip_client_obj->getSentence();
	  $return_terms = $ckip_client_obj->getTerm();
   
   output: $return_text - raw text
   	   $return_sentences
	   	Array
		(
		   [0] => 　獨立(Vi)　音樂(N)　需要(Vt)　大家(N)　一起(ADV)　來(ADV)　推廣(Vt)　，(COMMACATEGORY)
		   [1] => 　歡迎(Vt)　加入(Vt)　我們(N)　的(T)　行列(N)　！(EXCLAMATIONCATEGORY)
		)
	   $return_terms
		Array
		(
		    [0] => Array
			(
			    [term] => 獨立
			    [tag] => Vi
			)
		    ...

3. utf82big5.py
   Articles download using getPTTBoard.py are utf-8, but the tokenizer eats Big5, so convert them to Big5 using utf82big5.py

4. getPTTBoard.py
   get posts of a PTT Board from https://www.ptt.cc/bbs/index.html

   usage: ./getPTTBoard.py board_name index_page_num1 index_page_num2 output_dir
          (it will get pages from index index_page_num1 to index_page_num2)

