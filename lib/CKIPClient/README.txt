使用方法
============================================================
※本程式僅支援Big5和UTF-16LE的輸入輸出格式。
----------------------------------------
1.
先設定properties，參數範例如ckipsocket.properties:

host: mirror site的主機位置  ( ex: host=140.122.66.177 )
port: mirror site的連接埠
user: 你的account name
pass: 你的acount password
overwrite: true/false  
charsetcode: big5/utf-16LE

程式設定是輸出
系統會檢查輸出資料夾內是否有與輸入資料夾內相同名稱的檔案，如果有的話就不會再重覆送去斷詞。
但如果設定overwrite=true的話，就不會做這項檢查。
---------------------------------------
2.
執行CkipClient.exe [prop] [input dir] [output dir]

prop: 在步驟1設定的properties
input dir: 你要送去斷詞的文檔所在目錄 (可有子目錄)
output dir: 斷詞結果的目錄。【註一】

斷詞結果會以同樣的子目錄、同樣的檔名儲存在output dir下。
如果跑大量詞彙，有時可能會出現逾時的情況，這時請【註二】。

===================================================================
【註一】切忌與input dir同樣位置。
【註二】砍掉最後一個檔案，設定prop的overwrite=false，然後重新執行。

================================================================
demo：
test.bat是執行範例，測試前請先修改ckipsocket.properties的帳號資訊