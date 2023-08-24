
prof:
# 	python -m cProfile -o speedup_lin.prof  speedup_lin.py
# 	python -m pyprof2calltree -i speedup_lin.prof -o speedup_lin.prof_all.prof
# 	snakeviz speedup_lin.prof
	viztracer  speedup_lin.py
	vizviewer.exe .\result.json
