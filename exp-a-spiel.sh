declare -A games=(
	["dark-hex-3"]="Dh"
	["abrupt-dark-hex-3"]="AbruptDh"
	["phantom-tic-tac-toe"]="Pttt"
	["abrupt-phantom-tic-tac-toe"]="AbruptPttt"
	["corner-dh"]="CornerDh"
)

for name in ${!games[@]}; do
	./exp-a-spiel.py ${games[$name]} exp-a-spiel/$name.efg exp-a-spiel/$name.interp.jsonl
done
