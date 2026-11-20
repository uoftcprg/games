export CLASSPATH="build:build/*"

mkdir -p build

for artifact in org.apache.commons:commons-lang3:3.1 org.apache.wicket:wicket:1.4.17 org.jgrapht:jgrapht-jdk1.5:0.7.3; do
	mvn -q dependency:copy -Dartifact=$artifact -DoutputDirectory=build
done

echo "package cz.agents.gtlibrary.domain.oshizumo.ir; public class IROshiZumoGameState {}" > build/IROshiZumoGameState.java
javac -nowarn -d build -sourcepath gtlibrary-java/src build/IROshiZumoGameState.java gtlibrary-java/src/cz/agents/gtlibrary/{domain/{oshizumo,pursuit,tron}/*.java,nfg/simalphabeta/SimABConfig.java}

declare -A games=(
	["hidden-bid-oshi-zumo-10-3-1"]="oshizumo.OZGameInfo oshizumo.IIOshiZumoGameState oshizumo.OshiZumoExpander GENERAL_SUM=false startingCoins=10 locK=3 minBid=1"
	["hidden-bid-oshi-zumo-11-3-1"]="oshizumo.OZGameInfo oshizumo.IIOshiZumoGameState oshizumo.OshiZumoExpander GENERAL_SUM=false startingCoins=11 locK=3 minBid=1"
	["hidden-bid-oshi-zumo-13-3-1"]="oshizumo.OZGameInfo oshizumo.IIOshiZumoGameState oshizumo.OshiZumoExpander GENERAL_SUM=false startingCoins=13 locK=3 minBid=1"
	["pursuit-evasion-4x4-5"]="pursuit.PursuitGameInfo pursuit.PursuitGameState pursuit.FastImprovedExpander graphFile=gtlibrary-java/pursuit_simple4x4.txt evaderStart=0 p1Start=11 p2Start=15 evaderGoal=-1 depth=5"
	["tron"]="tron.TronGameInfo tron.TronGameState tron.TronExpander"
	["tron-6x6"]="tron.TronGameInfo tron.TronGameState tron.TronExpander ROWS=6 COLS=6"
	["visibility-pursuit-5"]="pursuit.PursuitGameInfo pursuit.VisibilityPursuitGameState pursuit.FastImprovedExpander graphFile=gtlibrary-java/pursuit_goal_optimized.txt evaderStart=0 p1Start=7 p2Start=13 evaderGoal=10 depth=5 visibility=2"
	["visibility-pursuit-6"]="pursuit.PursuitGameInfo pursuit.VisibilityPursuitGameState pursuit.FastImprovedExpander graphFile=gtlibrary-java/pursuit_goal_optimized.txt evaderStart=0 p1Start=7 p2Start=13 evaderGoal=10 depth=6 visibility=2"
	["visibility-pursuit-7"]="pursuit.PursuitGameInfo pursuit.VisibilityPursuitGameState pursuit.FastImprovedExpander graphFile=gtlibrary-java/pursuit_goal_optimized.txt evaderStart=0 p1Start=7 p2Start=13 evaderGoal=10 depth=7 visibility=2"
)

for name in ${!games[@]}; do
	./gt-library.py "${games[$name]}" gt-library/$name.jsonl > gt-library/$name.efg
done
