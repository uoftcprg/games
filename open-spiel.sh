declare -A games=(
	["battleship-3x2-2-3"]="battleship(board_height=3,board_width=2,ship_sizes=[2],ship_values=[4],num_shots=3)"
	["battleship-3x2-2-4"]="battleship(board_height=3,board_width=2,ship_sizes=[2],ship_values=[4],num_shots=4)"
	["coordinated-mp"]="coordinated_mp"
	["first-sealed-auction"]="first_sealed_auction"
	["goofspiel-6"]="turn_based_simultaneous_game(game=goofspiel(imp_info=True,num_cards=6,points_order=descending))"
	["goofspiel-7"]="turn_based_simultaneous_game(game=goofspiel(imp_info=True,num_cards=7,points_order=descending))"
	["kuhn-poker-3p"]="kuhn_poker(players=3)"
	["kuhn-poker-4p"]="kuhn_poker(players=4)"
	["kuhn-poker"]="kuhn_poker"
	["leduc-poker-3p"]="leduc_poker(players=3)"
	["leduc-poker"]="leduc_poker"
	["lewis-signaling"]="lewis_signaling"
	["liars-dice-2-4"]="liars_dice(numdice=2,dice_sides=4)"
	["liars-dice-2-5"]="liars_dice(numdice=2,dice_sides=5)"
	["liars-dice"]="liars_dice"
	["oshi-zumo-4-1-6"]="turn_based_simultaneous_game(game=oshi_zumo(coins=4,size=1,horizon=6))"
	["sheriff"]="sheriff"
	["tiny-bridge-2p"]="tiny_bridge_2p"
	["tiny-hanabi"]="tiny_hanabi"
	["trade-comm"]="trade_comm"
)

for name in ${!games[@]}; do
	./open-spiel.py ${games[$name]} open-spiel/$name.jsonl > open-spiel/$name.efg
done

games=(
	["blotto-3p"]="blotto(players=3)"
	["blotto"]="blotto"
	["matching-pennies-3p"]="matching_pennies_3p"
	["matrix-bos"]="matrix_bos"
	["matrix-brps"]="matrix_brps"
	["matrix-cd"]="matrix_cd"
	["matrix-coordination"]="matrix_coordination"
	["matrix-mp"]="matrix_mp"
	["matrix-pd"]="matrix_pd"
	["matrix-rps"]="matrix_rps"
	["matrix-rpsw"]="matrix_rpsw"
	["matrix-shapleys-game"]="matrix_shapleys_game"
	["matrix-sh"]="matrix_sh"
)

for name in ${!games[@]}; do
	./open-spiel.py ${games[$name]} open-spiel/$name.jsonl > open-spiel/$name.nfg
done
