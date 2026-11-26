declare -A games=(
	["d24"]="LiteEFG/LiteEFG/game_instances/D24.game"
	["goofspiel"]="LiteEFG/LiteEFG/game_instances/goofspiel.game"
	["kuhn"]="LiteEFG/LiteEFG/game_instances/kuhn.game"
	["leduc"]="LiteEFG/LiteEFG/game_instances/leduc.game"
	["liars-dice"]="LiteEFG/LiteEFG/game_instances/liars_dice.game"
)

for name in ${!games[@]}; do
	./lite-efg.py lite-efg/$name.jsonl < ${games[$name]} > lite-efg/$name.efg
done
