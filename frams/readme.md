# Żeby odpalić FramsicksEvolution.py

Parametry:
```bash
-path C:\Users\Lenovo\OneDrive\Pulpit\MGR\Framsticks50rc20 -sim eval-allcriteria.sim;deterministic.sim;sample-period-2.sim; -opt vertpos -max_numparts 30 -max_numgenochars 50 -initialgenotype /*9*/BLU -popsize 100 -generations 20 -hof_size 1 -hof_savefile HoF-f9-%%M-%%N.gen
```

Environment Variables:
```bash
PYTHONUNBUFFERED=1;DIR_WITH_FRAMS_LIBRARY=C:\Users\Lenovo\OneDrive\Pulpit\MGR\Framsticks50rc20
```

# Pomysły na pracę:
- testy dla kilku różnych reprezentacji
- testy dla małych pop-size
- testy dla dużych pop-size
- testy na zbiezność
- Przystosowanie pod szybkość
- Przystosowanie pod konkretny kształt
- Wyjaśnienie co to jest Framstik
- Dla każdego eksperymentu, odpalić framsticka i wkleić jego zdjęcie
- Różne architektury - eaSimple / eaMuPlusLambda / eaMuCommaLambda / eaGenerateUpdate


malo -> p_mut, p_cross

# Notatki
## 07.06.2022
vertpos, distance -> period2
slurm
jedno kryterium
long
vertpos
