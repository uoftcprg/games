shopt -s globstar

for efg in open-spiel/latent-ttt.efg; do
	./2p0s-efg-npz.py 2p0s-efg-npz/${efg%.*}.sfps.npz 2p0s-efg-npz/${efg%.*}.us.npz < $efg
done

# for efg in blsp2efg/**/*.efg huflhe/**/*.efg open-spiel/**/*.efg; do
# 	./2p0s-efg-npz.py 2p0s-efg-npz/${efg%.*}.sfps.npz 2p0s-efg-npz/${efg%.*}.us.npz < $efg
# done
# 
# for efg in exp-a-spiel/**/*.efg; do
# 	./2p0s-efg-npz.py --dtype int8 --no-clean 2p0s-efg-npz/${efg%.*}.sfps.npz 2p0s-efg-npz/${efg%.*}.us.npz < $efg
# done
