shopt -s globstar

for nfg in **/*.nfg; do
	./2p0s-nfg-npz.py 2p0s-nfg-npz/${nfg%.*}.npz < $nfg
done
