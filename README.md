IR_Project
==========
1. CKIPClient/ is a client program written by NTNU (http://tm.itc.ntnu.edu.tw/CNLP/?q=node/6) 
   to send request to the Chinese tokenizer server written by Sinica (http://ckipsvr.iis.sinica.edu.tw/)
   
   usage: sh run.sh input_dir output_dir 
          input_dir - contain raw chinese text files (Must be in Big5 or utf-16)
          output_dir - the tokenized texts

Articles download using getPTTBoard.py are utf-8, but the tokenizer eats Big5, so convert them to Big5 using utf82big5.py
