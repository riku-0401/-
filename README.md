<!DOCTYPE html>
<html>


<body>
    <h1>単位マモル　プログラム</h1>
    <p>このBOTは複数人で課題を定義、期日まで課題を終えてない人を毎日メンションをし、課題を期日までに出すことを目的としたBOTです</p>
    <p>また、期日が明日の課題を取り組んでいる最中の人のメンションを添えてお知らせします</p>
    <p>tukaikata.txtはチャンネル名や用途に合わせてUTF-8でカスタムしてください</p>
    <p>以下のようにmain.py内の上にあるチャンネルid、サーバーid、トークンを代入してください</p>
    <hr>
    <pre>
        #############################################
        # サーバーのチャンネルid、サーバーid、トークン設定
        graphchid=0　
        admin_id=0 #最悪設定しなくても
        subadmin_id=0　#最悪設定しなくても
        tukaikatachid=0
        kadaichid=0
        cmdchid=0
        osirasechid=0
        mentionchid=0
        kanrishachid=0
        logchid=0
        guildid=0
        TOKEN="YOUR TOKEN HERE"
        #############################################
    </pre>
    <h2>基本的なコマンド</h2>
    <ul>
        <li><code>!o 課題名 期日</code> (cmdchidチャンネルのみ) 課題の定義 例. <code>!o C言語 0910</code></li>
        <li><code>!sss</code> (kanrishachidチャンネルのみ) 使い方をtukaikata.txtから読み取り、tukaikatachidに送信</li>
        <li><code>!reset</code>  (kanrishachidのみ) 課題ファイルの削除</li>
    </ul>
    <p>日付が変わって数分後に自動で課題をメンションします</p>
</body>
</html>
