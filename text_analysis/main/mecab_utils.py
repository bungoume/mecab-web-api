import re
import MeCab
import unicodedata


# RE_HIRAGANA = re.compile(r'[\u3040-\u309F]')
RE_NOWORD = re.compile(r'[^\w-]')
RE_LX = re.compile(r'[lx]')
RE_ALL = re.compile(r'.')


# node: 1つの形態素を出力, デフォルトは空文字
# unk: 1つの未知語形態素を出力, デフォルトは node と同一フォーマット
# bos: 形態素解析の結果に先だって出力 (header 的役割), デフォルトは空文字
# eos: 形態素解析の結果の後に出力 (footer 的役割), デフォルトは "EOS\n"
# eon: N-best出力で, N-Bestの出力が終了したときに出力, デフォルトは空文字列
# %s: 形態素種類, %m: 形態素の表層文字列, %pS: 先頭に空白を含むか,
# %f[n]:
#   0: 品詞, 1:品詞, 2:品詞, 3:品詞, 4:活用型, 5:活用形, 6:原形, 7:読み, 8:発音
# %pw: 単語生起コスト, %pC: 1つ前の形態素との連接コスト
M_PARSE = MeCab.Tagger('--node-format={0} --unk-format={1} --eos-format=EOS'.format(
    r'%s\v%m\v%pS\v%f[0]\v%f[1]\v%f[2]\v%f[3]\v%f[4]\v%f[5]'
    r'\v%f[6]\v%f[7]\v%f[8]\v%pw\v%pC\r\n',
    r'%s\v%m\v%pS\v%f[0]\v%f[1]\v%f[2]\v%f[3]\v%f[4]\v%f[5]'
    r'\v%f[6]\v%m\v%m\v%pw\v%pC\r\n',
))
M_READING = MeCab.Tagger('-Oyomi')


def remove_mark(w):
    """英語・ハイフン以外のもの(句読点など)を除去
    """
    w = RE_NOWORD.sub('', w)
    return w


def remove_soundmark(w):
    """濁点・半濁点を削除
    """
    w = w.replace('g', 'k')
    w = w.replace('z', 's')
    w = w.replace('d', 't')
    w = w.replace('b', 'h')
    w = w.replace('p', 'h')
    return w


def qwerty_kana(w):
    """QWERTYキーボードのIME向けの予測処理をする
    """
    w = re.sub(r'([qrtypsdfghjlzxcvbm])\1', r'っ\1', w)
    w = re.sub(r'ji?', 'じ', w)
    w = re.sub(r'fu?', 'ふ', w)
    w = re.sub(r'ch?i?', 'ち', w)
    w = re.sub(r'qu?', 'く', w)
    w = re.sub(r'shi?', 'し', w)
    w = re.sub(r'tsu?', 'つ', w)
    w = w.replace('ky', 'きxy')
    w = w.replace('gy', 'ぎxy')
    w = w.replace('sy', 'しxy')
    w = w.replace('zy', 'じxy')
    w = w.replace('ty', 'ちxy')
    w = w.replace('dy', 'ぢxy')
    w = w.replace('ny', 'にxy')
    w = w.replace('hy', 'ひxy')
    w = w.replace('my', 'みxy')
    w = w.replace('ry', 'りxy')
    w = w.replace('nn', 'ん')
    w = re.sub(r'n([^aiueo])', r'ん\1', w)
    return w


ROMAJI_DICT = {
    'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
    'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
    'サ': 'sa', 'シ': 'si', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
    'タ': 'ta', 'チ': 'ti', 'ツ': 'tu', 'テ': 'te', 'ト': 'to',
    'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
    'ハ': 'ha', 'ヒ': 'hi', 'フ': 'hu', 'ヘ': 'he', 'ホ': 'ho',
    'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',
    'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
    'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
    'ワ': 'wa', 'ヰ': 'wi', 'ヱ': 'we', 'ヲ': 'wo',
    'ガ': 'ga', 'ギ': 'gi', 'グ': 'gu', 'ゲ': 'ge', 'ゴ': 'go',
    'ザ': 'za', 'ジ': 'zi', 'ズ': 'zu', 'ゼ': 'ze', 'ゾ': 'zo',
    'ダ': 'da', 'ヂ': 'di', 'ヅ': 'du', 'デ': 'de', 'ド': 'do',
    'バ': 'ba', 'ビ': 'bi', 'ブ': 'bu', 'ベ': 'be', 'ボ': 'bo',
    'パ': 'pa', 'ピ': 'pi', 'プ': 'pu', 'ペ': 'pe', 'ポ': 'po',
    'ヴ': 'vu',
    'ァ': 'xa', 'ィ': 'xi', 'ゥ': 'xu', 'ェ': 'xe', 'ォ': 'xo',
    'ッ': 'xtu',
    'ャ': 'xya', 'ュ': 'xyu', 'ョ': 'xyo',
    'ヮ': 'xwa',
    'ヶ': 'xke', 'ヵ': 'xka',
    'ン': 'nn',
    '、': ',', '。': '.', '・': ';',
    'ー': '-', '－': '-', '‐': '-',
}


def to_romaji(w):
    """カタカナ・ひらがなをローマ字書きに変換する
    一般的なローマ字ではなく、IMEでの単体文字入力となる形に変換して予測候補を出しやすくする
    ref: http://developers.linecorp.com/blog/?p=367
    """
    def ctoromaji(c):
        c = c.group(0)

        # if RE_HIRAGANA.search(c):
        #     c = chr(ord(c)+96)
        if c in ROMAJI_DICT:
            return ROMAJI_DICT[c]
        else:
            return c

    return RE_ALL.sub(ctoromaji, w)


def reading_sentence(sentence, nbest_num=10):
    sentence = unicodedata.normalize('NFKC', sentence)
    sentence = sentence.replace('\v', '')
    sentence = sentence.replace('\r', '')
    sentence = sentence.replace('\n', '')

    parsed_text = M_READING.parseNBest(nbest_num, sentence)
    nbests = parsed_text.strip().split('\n')

    ans_list = []
    for reading in nbests:
        reading = reading.lower()
        if reading in map(lambda x: x['reading'], ans_list):
            continue
        roma = remove_mark(to_romaji(reading))
        no_soundmark = remove_soundmark(roma)
        ret = {
            'reading': reading,
            'romaji': roma,
            # 日本語変換前の語句をひらがなに（弊害で英語名検索不可)
            'qwerty_romaji': to_romaji(qwerty_kana(reading)),
            # 濁点・半濁点を削除
            'ignore_soundmark_romaji': no_soundmark,
            # 小書き文字を通常の仮名と同一視する
            'ignore_kogaki_romaji': RE_LX.sub('', roma),
            'ignore_all_romaji': RE_LX.sub('', no_soundmark),
        }
        ans_list.append(ret)

    return ans_list


def parse_sentence(sentence, nbest_num=3):
    sentence = unicodedata.normalize('NFKC', sentence)
    sentence = sentence.replace('\v', '')
    sentence = sentence.replace('\r', '')

    parsed_text = M_PARSE.parseNBest(nbest_num, sentence)
    nbests = parsed_text.strip()
    nbests = nbests.split('\r\nEOS')[:-1]

    def parse_line(line):
        x = line.split('\v')
        MORPHEME_TYPE = {'0': '通常', '1': '未知語', '2': '文頭', '3': '文末'}
        w_cost = int(x[12])
        c_cost = int(x[13])
        return {
            'morpheme': MORPHEME_TYPE[x[0]],  # 形態素種類
            'surface': x[1],  # 形態素の表層文字列
            'with_whitespace': bool(len(x[2])),  # 先頭に空白を含むか
            'pos': x[3],           # 品詞
            'pos_detail1': x[4],   # 品詞細分類1
            'pos_detail2': x[5],   # 品詞細分類2
            'pos_detail3': x[6],   # 品詞細分類3
            'conjugated_type': x[7],  # 活用型
            'conjugated_form': x[8],  # 活用形
            'baseform': x[9],         # 原形
            'reading': x[10],         # 読み
            'pronunciation': x[11],   # 発音
            'word_cost': w_cost,      # 単語生起コスト
            'c_cost': c_cost,         # 1つ前の形態素との連接コスト
            'cost': w_cost+c_cost,    # その形態素単独
            'ime_romaji': to_romaji(x[10]).lower(),  # ローマ字
        }

    ans_list = []
    for nbest in nbests:
        words = list(map(parse_line, nbest.strip().split('\r\n')))
        readings = list(map(lambda x: x['reading'], words))
        roma = to_romaji(''.join(readings)).lower()

        ret = {
            'all': {
                'normalized': sentence,
                'length': len(sentence),
                'cost': sum(map(lambda x: x['cost'], words)),
                'reading': ''.join(readings),
                'ime_romaji': remove_mark(roma),
                'wakati': ' '.join(map(lambda x: x['surface'], words)),
                'wakati_reading': ' '.join(readings),
            },
            'words': words
        }
        ans_list.append(ret)
    return ans_list
