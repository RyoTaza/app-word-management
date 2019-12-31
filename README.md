# app-word-management
## 英単語の登録とCSV出力するシステム
- 登録したい英単語を引数として、words.pyを実行<br>
    _ex. python reg_word_info.py word_
- CSVファイルに登録した単語をCSVファイルに出力する<br>
    _ex. python output_csv.py_
- csv_files/unknown_words.csvにわからない単語を１語ずつ改行して書く。
- csc_files/unknown_words.csvにある単語を１行ずつ拾って、reg_word_info.pyを実行していく。execute.py見たいのを作成して、いっぺんに自動的に行ってしまう形でもいいかもしれない