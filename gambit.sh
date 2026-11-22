declare -A games=(
	["bagwell1995"]="journals/geb/bagwell1995"
	["jakobsen2016-fig1a"]="conf/itcs/jakobsen2016/fig1a"
	["jakobsen2016-fig1b"]="conf/itcs/jakobsen2016/fig1b"
	["jakobsen2016-fig1c"]="conf/itcs/jakobsen2016/fig1c"
	["jakobsen2016-fig3"]="conf/itcs/jakobsen2016/fig3"
	["myerson1991-fig2-1"]="books/myerson1991/fig2_1"
	["myerson1991-fig4-2"]="books/myerson1991/fig4_2"
	["reiley2008-fig1"]="journals/other/reiley2008/fig1"
	["selten1975-fig1"]="journals/ijgt/selten1975/fig1"
	["selten1975-fig2"]="journals/ijgt/selten1975/fig2"
	["selten1975-fig3"]="journals/ijgt/selten1975/fig3"
	["shohamleytonbrown2008-fig5-10"]="books/shohamleytonbrown2008/fig5_10"
	["shohamleytonbrown2008-fig5-11"]="books/shohamleytonbrown2008/fig5_11"
	["shohamleytonbrown2008-fig5-15"]="books/shohamleytonbrown2008/fig5_15"
	["shohamleytonbrown2008-fig5-1"]="books/shohamleytonbrown2008/fig5_1"
	["shohamleytonbrown2008-fig5-2"]="books/shohamleytonbrown2008/fig5_2"
	["shohamleytonbrown2008-fig5-9"]="books/shohamleytonbrown2008/fig5_9"
	["shohamleytonbrown2008-fig6-2"]="books/shohamleytonbrown2008/fig6_2"
	["shohamleytonbrown2008-fig6-8"]="books/shohamleytonbrown2008/fig6_8"
	["vonstengel2022-fig10-12"]="books/vonstengel2022/fig10.12"
	["vonstengel2022-fig10-1"]="books/vonstengel2022/fig10.1"
	["vonstengel2022-fig10-5"]="books/vonstengel2022/fig10.5"
	["vonstengelforges2008-fig1"]="journals/mor/vonstengelforges2008/fig1"
	["vonstengelforges2008-fig6"]="journals/mor/vonstengelforges2008/fig6"
	["vonstengelforges2008-fig9"]="journals/mor/vonstengelforges2008/fig9"
	["watson2013-exercise29-6"]="books/watson2013/exercise29_6"
	["watson2013-fig29-1"]="books/watson2013/fig29_1"
)

for name in ${!games[@]}; do
	./gambit.py "${games[$name]}" gambit/$name.jsonl > gambit/$name.efg
done

games=(
	["nau2004-sec3"]="journals/ijgt/nau2004/sec3"
	["nau2004-sec4"]="journals/ijgt/nau2004/sec4"
	["nau2004-sec5"]="journals/ijgt/nau2004/sec5"
	["nau2004-sec6"]="journals/ijgt/nau2004/sec6"
	["shapley1974-fig2"]="journals/other/shapley1974/fig2"
	["shapley1974-fig3"]="journals/other/shapley1974/fig3"
)

for name in ${!games[@]}; do
	./gambit.py "${games[$name]}" gambit/$name.jsonl > gambit/$name.nfg
done
