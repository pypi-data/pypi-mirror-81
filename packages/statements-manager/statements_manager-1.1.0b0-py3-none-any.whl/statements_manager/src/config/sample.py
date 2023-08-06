sample_toml = """
# プロジェクト名
name = "sample"
# 問題文が存在する場所に応じてモードを選ぶ ("docs" or "local")
# default: "local"
mode = "local"
# 出力ディレクトリの上書きを許容するか
# default: false
allow_rewrite = false

# docs mode に関する設定 (問題文が Google Docs 上にある場合は設定必須)
[docs]
    # credentials.json の場所
    credentials_src = "path/to/credentials.json"
    # token.pickle の場所
    token_src = "path/to/token.pickle"

# 出力される HTML のスタイルに関する設定
[style]
    # HTML テンプレート
    template_src = "path/to/template.html"
    # 出力ディレクトリにコピーすべきファイル (何もない場合は空で構いません)
    copied_files = []

# 問題ごとに定義を書く
[[problem]]
    # 問題 ID (必須: 出力 html 名にも使用される)
    id = "A"
    # 問題文が格納されている場所 (必須)
    # mode が local である場合、Markdown ファイルへのパスを記載する
    # mode が Docs である場合、Google Docs の Document ID を記載する
    # (Document ID とは Docs の URL にある、ランダムのような文字列のことです)
    statement_src = "path/to/A.md"
    # 制約ファイルの出力場所 (出力しなくて良い場合は指定不要)
    params_path = "path/to/params.hpp"
    # 問題制約を書く (以下の例のように書いてください)
    [problem.constraints]
        MIN_N = 1
        MAX_N = 1_000_000_000
        ALL_INPUTS_ARE_INTEGERS = "入力は全て整数で与えられる"
    # 入出力例
    [[problem.samples]]
        # サンプルのタイプ
        # 'default' (既定, この場合 type は省略可): 入出力例がある場合
        # 'input_only': 入力例のみの場合
        # 'output_only': 出力例のみの場合
        # 'interactive': インタラクティブ問題の場合
        type = "default"
        # 入力例ファイルへのパス ('default', 'input_only' で必須)
        input_path = "path/to/00_sample_00.in"
        # 出力例ファイルへのパス ('default', 'output_only' で必須)
        output_path = "path/to/00_sample_00.out"
        # インタラクティブ問題サンプルへのパス ('interactive' で必須)
        # Markdown 形式で書かれたものを指定
        interactive_path = "path/to/00_sample_00.md"
"""
