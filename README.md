課題管理discordbot</p>
このBOTは複数人で課題を定義することができ、課題が終わっていない人に毎日メンションでお知らせをするBOTです</p>
tukaikata.txtはチャンネル名や用途に合わせてカスタムしてください</p>
以下のようにmain.py内の上にあるチャンネルid、サーバーid、トークンを代入してください</p>
#############################################</p>
#サーバーのチャンネルid、サーバーid、トークン設定</p>
tukaikatachid=0</p>
kadaichid=0</p>
cmdchid=0</p>
osirasechid=0</p>
</p>
kanrishachid=0 #管理用</p>
logchid=0 #管理用</p>
</p>
guildid=0 #サーバーid</p>
</p>
TOKEN="YOUR TOKEN" #トークン設定</p>
#############################################</p></p>
コマンド一覧</p>
!o 課題名 期日 (cmdchidチャンネルのみ) 課題の定義 例.!o C言語 0910</p>
!sss (kanrishachidチャンネルのみ) 使い方をtukaikata.txtから読み取り、tukaikatachidに送信 </p>
!reset (kanrishachidのみ) 課題ファイルの削除</p></p>
以下のコマンドは日付変更時に自動で実行されるので通常実行する必要はないです</p>
!ff (kanrishachidチャンネルのみ) ３日前が期日の課題をデータから削除</p>
!fc (kanrishachidチャンネルのみ) 明日が期日の課題を表示、取り組んでいる人をメンション</p>
!fs (kanrishachidチャンネルのみ) 課題に取り組んでいるユーザーごとの課題一覧を送信</p>
通常これら3つのコマンドは日付が変わって数分後に自動で実行されます</p>
