import csv
import sys
import io
import argparse
import pathlib

def loadKanaDic(kanaFile: str) -> dict[str, str]:
    with open(kanaFile, encoding='utf-8') as f:
        reader = csv.reader(f)
        d={(row[0]): row[1] for row in reader}
    return d

# (ipaDic, clist, vlist)
def loadIpa(ipaFile: str) -> tuple[dict[str,list[str]], list[str], list[str]]:
    with open(ipaFile, encoding='utf-8') as f:
        reader = csv.reader(f)
        d = {(row[0]): row[1:] for row in reader}
    vlist = ['a', 'i', 'u', 'e', 'o']
    clist = list(set(d.keys()) - set(vlist))
    return (d, clist, vlist)

def romeToKana(c: str, v: str, kanaDic: dict[str, str]) -> str:
    return kanaDic[c+v]

def romeToIpa(char: str, ipaDic: [str, list[str]]) -> list[str]:
    if char=='':
        return ['']
    return ipaDic[char]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('outfile', nargs='?', help='出力ファイル名。"-"は標準出力')
    parser.add_argument('-k', '--kana', help='ローマ字と仮名の対応表(CSV)を指定する')
    parser.add_argument('-i', '--ipa', help='ローマ字とIPAの対応表(CSV)を指定する')
    args = parser.parse_args()

    outfilename = args.outfile
    if outfilename in (None, '-'):
        outfile = sys.stdout
    else:
        outfilepath = pathlib.Path(outfilename)
        outfilepath.parent.mkdir(parents=True, exist_ok=True)
        outfile = outfilepath.open(mode='w', encoding='utf-8')

    kanaDic = loadKanaDic('kana.csv' if args.kana is None else args.kana)
    (ipaDic, clist, vlist) = loadIpa('ipa.csv' if args.ipa is None else args.ipa)

    for c in clist:
        for v in vlist:
            kana = romeToKana(c, v, kanaDic)
            for cipa in romeToIpa(c, ipaDic):
                for vipa in romeToIpa(v, ipaDic):
                    print(f"{kana}\t{cipa}{vipa}\t短縮よみ", file=outfile)

