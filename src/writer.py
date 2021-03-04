import sys
sys.path.insert(0, '.')
from pathlib import Path
from typing import List
from src.io import Sentence


def write_file(filename: str, sentences: List[Sentence]):
    path = Path(filename)
    
    output_list = [[[str(t.id),str(t.form),str(t.lemma),str(t.pos),str(t.xpos),str(t.morph),str(t.head),str(t.rel),str(t.x1),str(t.x2)] for t in s.tokens] for s in sentences]

    with path.open('w') as writer:
        for s in output_list:
            for t in s:
                writer.write('\t'.join(t))
                writer.write('\n')
            writer.write('\n')

    assert path.is_file()
