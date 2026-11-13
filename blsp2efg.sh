declare -A games=(
	["kuhn"]="sequence-form-py/blsp/kuhn.blsp"
	["leduc"]="sequence-form-py/blsp/leduc.blsp"
	["search5-zero-sum"]="sequence-form-py/blsp/search5_zero_sum.blsp"
)

for name in ${!games[@]}; do
	./blsp2efg.py < ${games[$name]} > blsp2efg/$name.efg
done
