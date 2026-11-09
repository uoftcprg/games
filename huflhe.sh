declare -A games=(
	["kuhn-poker"]="KuhnPoker"
	["leduc-holdem"]="LeducHoldem"
	["royal-rhode-island-holdem"]="RoyalRhodeIslandHoldem"
	["rhode-island-holdem"]="RhodeIslandHoldem"
	["numeral211-holdem"]="Numeral211Holdem"
)

for key in ${!games[@]}; do
	./huflhe.py ${games[$key]} huflhe/$key.interp.jsonl > huflhe/$key.efg
done
