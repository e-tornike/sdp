Install:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Train and evaluate:

`python3 src/main.py --train ./data/english/train/wsj_train.only-projective.first-1k.conll06 --dev ./data/english/dev/wsj_dev.conll06.blind --test ./data/english/test/wsj_test.conll06.blind --shuffle True --epochs 5 --debug False`

Evaluate with official script:

`perl eval07pl.sec -g data/english/dev/wsj_dev.conll06.gold -s data/english/dev/wsj_dev.conll06.preds`
