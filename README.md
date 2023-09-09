<!DOCTYPE html>
<html>


<body>
    <h1>課題管理 Discord Bot</h1>
    <p>tukaikata.txtはチャンネル名や用途に合わせてカスタムしてください</p>
    <p>以下のようにmain.py内の上にあるチャンネルid、サーバーid、トークンを代入してください</p>
    <hr>
    <pre>
        #############################################
        # サーバーのチャンネルid、サーバーid、トークン設定
        tukaikatachid = 0
        kadaichid = 0
        cmdchid = 0
        osirasechid = 0
        kanrishachid = 0 # 管理用
        logchid = 0     # 管理用
        guildid = 0     # サーバーid
        TOKEN = "YOUR TOKEN" # トークン設定
        #############################################
    </pre>
    <h2>コマンド一覧</h2>
    <ul>
        <li><code>!o 課題名 期日 (cmdchidチャンネルのみ)</code> 課題の定義 例. <code>!o C言語 0910</code></li>
        <li><code>!sss (kanrishachidチャンネルのみ)</code> 使い方をtukaikata.txtから読み取り、tukaikatachidに送信</li>
        <li><code>!reset (kanrishachidのみ)</code> 課題ファイルの削除</li>
    </ul>
    <p><big>以下のコマンドは日付変更時に自動で実行されるので通常実行する必要はないです</big></p>
    <ul>
        <li><code>!ff (kanrishachidチャンネルのみ)</code> ３日前が期日の課題をデータから削除</li>
        <li><code>!fc (kanrishachidチャンネルのみ)</code> 明日が期日の課題を表示、取り組んでいる人をメンション</li>
        <li><code>!fs (kanrishachidチャンネルのみ)</code> 課題に取り組んでいるユーザーごとの課題一覧を送信</li>
    </ul>
    <p>通常これら3つのコマンドは日付が変わって数分後に自動で実行されます</p>
</body>

</html>
