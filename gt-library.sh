export CLASSPATH="build:build/*"

mkdir -p build

for artifact in org.apache.commons:commons-lang3:3.1 org.apache.wicket:wicket:1.4.17 org.jgrapht:jgrapht-jdk1.5:0.7.3; do
	mvn -q dependency:copy -Dartifact=$artifact -DoutputDirectory=build
done

echo "package cz.agents.gtlibrary.algorithms.sequenceform.doubleoracle.improvedBR; public class DoubleOracleWithBestMinmaxImprovement { public enum PlayerSelection {} }" > build/DoubleOracleWithBestMinmaxImprovement.java
echo "package cz.agents.gtlibrary.algorithms.stackelberg.correlated.twoplayer.iterative.iinodes; public class TLAction { public int getIndex() { return 0; } }" > build/TLAction.java
echo "package cz.agents.gtlibrary.domain.oshizumo.ir; public class IROshiZumoGameState {}" > build/IROshiZumoGameState.java
echo "package cz.agents.gtlibrary.utils.io; public class GambitEFG { public void buildAndWrite(Object... o) {} }" > build/GambitEFG.java
javac -nowarn -d build -sourcepath gtlibrary-java/src build/*.java gtlibrary-java/src/cz/agents/gtlibrary/{domain/{aceofspades,artificialchance,bpg,goofspiel,informeraos,liarsdice,mpochm,nfptest,nonlocality,oshizumo,poker/generic,poker/kuhn,pursuit,randomgame,randomgameimproved,randomgameimproved/observationvariants,rps,stacktest,testGame,tron,upordown,wichardtne}/*.java,nfg/simalphabeta/SimABConfig.java}

declare -A games=(
	["ac"]="artificialchance.ACGameInfo artificialchance.ACGameState artificialchance.ACExpander"
	["aos"]="aceofspades.AoSGameInfo aceofspades.AoSGameState aceofspades.AoSExpander"
	["bpg"]="bpg.BPGGameInfo bpg.BPGGameState bpg.BPGExpander graphFile=gtlibrary-java/GridW3-almost-connected.txt"
	["generic-poker-13-2-1-1"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=13 MAX_CARD_OF_EACH_TYPE=2 MAX_RAISES_IN_ROW=1 MAX_DIFFERENT_BETS=1 MAX_DIFFERENT_RAISES=1"
	["generic-poker-15-2-1-1"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=15 MAX_CARD_OF_EACH_TYPE=2 MAX_RAISES_IN_ROW=1 MAX_DIFFERENT_BETS=1 MAX_DIFFERENT_RAISES=1"
	["generic-poker-3-2-1-2"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=3 MAX_CARD_OF_EACH_TYPE=2 MAX_RAISES_IN_ROW=1 MAX_DIFFERENT_BETS=2 MAX_DIFFERENT_RAISES=2"
	["generic-poker-3-2-2-2"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=3 MAX_CARD_OF_EACH_TYPE=2 MAX_RAISES_IN_ROW=2 MAX_DIFFERENT_BETS=2 MAX_DIFFERENT_RAISES=2"
	["generic-poker-3-2-3-2"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=3 MAX_CARD_OF_EACH_TYPE=2 MAX_RAISES_IN_ROW=3 MAX_DIFFERENT_BETS=2 MAX_DIFFERENT_RAISES=2"
	["generic-poker-3-2-4-2"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=3 MAX_CARD_OF_EACH_TYPE=2 MAX_RAISES_IN_ROW=4 MAX_DIFFERENT_BETS=2 MAX_DIFFERENT_RAISES=2"
	["generic-poker-3-3-2-2"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=3 MAX_CARD_OF_EACH_TYPE=3 MAX_RAISES_IN_ROW=2 MAX_DIFFERENT_BETS=2 MAX_DIFFERENT_RAISES=2"
	["generic-poker-35-2-1-1"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=35 MAX_CARD_OF_EACH_TYPE=2 MAX_RAISES_IN_ROW=1 MAX_DIFFERENT_BETS=1 MAX_DIFFERENT_RAISES=1"
	["generic-poker-4-3-1-1"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=4 MAX_CARD_OF_EACH_TYPE=3 MAX_RAISES_IN_ROW=1 MAX_DIFFERENT_BETS=1 MAX_DIFFERENT_RAISES=1"
	["generic-poker-4-3-1-2"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=4 MAX_CARD_OF_EACH_TYPE=3 MAX_RAISES_IN_ROW=1 MAX_DIFFERENT_BETS=2 MAX_DIFFERENT_RAISES=2"
	["generic-poker-4-3-1-3"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=4 MAX_CARD_OF_EACH_TYPE=3 MAX_RAISES_IN_ROW=1 MAX_DIFFERENT_BETS=3 MAX_DIFFERENT_RAISES=3"
	["generic-poker-4-3-1-4"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=4 MAX_CARD_OF_EACH_TYPE=3 MAX_RAISES_IN_ROW=1 MAX_DIFFERENT_BETS=4 MAX_DIFFERENT_RAISES=4"
	["generic-poker-4-3-1-5"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=4 MAX_CARD_OF_EACH_TYPE=3 MAX_RAISES_IN_ROW=1 MAX_DIFFERENT_BETS=5 MAX_DIFFERENT_RAISES=5"
	["generic-poker-4-3-2-1"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=4 MAX_CARD_OF_EACH_TYPE=3 MAX_RAISES_IN_ROW=2 MAX_DIFFERENT_BETS=1 MAX_DIFFERENT_RAISES=1"
	["generic-poker-4-3-2-2"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=4 MAX_CARD_OF_EACH_TYPE=3 MAX_RAISES_IN_ROW=2 MAX_DIFFERENT_BETS=2 MAX_DIFFERENT_RAISES=2"
	["generic-poker-4-3-2-3"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=4 MAX_CARD_OF_EACH_TYPE=3 MAX_RAISES_IN_ROW=2 MAX_DIFFERENT_BETS=3 MAX_DIFFERENT_RAISES=3"
	["generic-poker-4-3-2-4"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=4 MAX_CARD_OF_EACH_TYPE=3 MAX_RAISES_IN_ROW=2 MAX_DIFFERENT_BETS=4 MAX_DIFFERENT_RAISES=4"
	["generic-poker-4-3-3-2"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=4 MAX_CARD_OF_EACH_TYPE=3 MAX_RAISES_IN_ROW=3 MAX_DIFFERENT_BETS=2 MAX_DIFFERENT_RAISES=2"
	["generic-poker-4-3-4-2"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=4 MAX_CARD_OF_EACH_TYPE=3 MAX_RAISES_IN_ROW=4 MAX_DIFFERENT_BETS=2 MAX_DIFFERENT_RAISES=2"
	["generic-poker-5-2-1-1"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=5 MAX_CARD_OF_EACH_TYPE=2 MAX_RAISES_IN_ROW=1 MAX_DIFFERENT_BETS=1 MAX_DIFFERENT_RAISES=1"
	["generic-poker-8-2-1-1"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=8 MAX_CARD_OF_EACH_TYPE=2 MAX_RAISES_IN_ROW=1 MAX_DIFFERENT_BETS=1 MAX_DIFFERENT_RAISES=1"
	["generic-poker-9-2-1-1"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander MAX_CARD_TYPES=9 MAX_CARD_OF_EACH_TYPE=2 MAX_RAISES_IN_ROW=1 MAX_DIFFERENT_BETS=1 MAX_DIFFERENT_RAISES=1"
	["generic-poker"]="poker.generic.GPGameInfo poker.generic.GenericPokerGameState poker.generic.GenericPokerExpander"
	["goofspiel-4-random-binary"]="goofspiel.GSGameInfo goofspiel.GoofSpielGameState goofspiel.GoofSpielExpander CARDS_FOR_PLAYER=[1,2,3,4] depth=4 useFixedNatureSequence=false BINARY_UTILITIES=true"
	["goofspiel-4-random"]="goofspiel.GSGameInfo goofspiel.GoofSpielGameState goofspiel.GoofSpielExpander CARDS_FOR_PLAYER=[1,2,3,4] depth=4 useFixedNatureSequence=false"
	["goofspiel"]="goofspiel.GSGameInfo goofspiel.GoofSpielGameState goofspiel.GoofSpielExpander"
	["ii-goofspiel-5-binary"]="goofspiel.GSGameInfo goofspiel.IIGoofSpielGameState goofspiel.GoofSpielExpander CARDS_FOR_PLAYER=[5,4,3,2,1] depth=5 BINARY_UTILITIES=true"
	["ii-goofspiel-5"]="goofspiel.GSGameInfo goofspiel.IIGoofSpielGameState goofspiel.GoofSpielExpander CARDS_FOR_PLAYER=[1,2,3,4,5] depth=5"
	["ii-goofspiel-6-binary"]="goofspiel.GSGameInfo goofspiel.IIGoofSpielGameState goofspiel.GoofSpielExpander CARDS_FOR_PLAYER=[5,4,3,2,1,0] depth=6 BINARY_UTILITIES=true"
	["ii-goofspiel-6"]="goofspiel.GSGameInfo goofspiel.IIGoofSpielGameState goofspiel.GoofSpielExpander CARDS_FOR_PLAYER=[1,2,3,4,5,6] depth=6"
	["ii-goofspiel"]="goofspiel.GSGameInfo goofspiel.IIGoofSpielGameState goofspiel.GoofSpielExpander"
	["ii-oshi-zumo-10-3-1"]="oshizumo.OZGameInfo oshizumo.IIOshiZumoGameState oshizumo.OshiZumoExpander GENERAL_SUM=false startingCoins=10 locK=3 minBid=1"
	["ii-oshi-zumo-11-3-1"]="oshizumo.OZGameInfo oshizumo.IIOshiZumoGameState oshizumo.OshiZumoExpander GENERAL_SUM=false startingCoins=11 locK=3 minBid=1"
	["ii-oshi-zumo-13-3-1"]="oshizumo.OZGameInfo oshizumo.IIOshiZumoGameState oshizumo.OshiZumoExpander GENERAL_SUM=false startingCoins=13 locK=3 minBid=1"
	["ii-oshi-zumo"]="oshizumo.OZGameInfo oshizumo.IIOshiZumoGameState oshizumo.OshiZumoExpander"
	["informer-aos"]="informeraos.InformerAoSGameInfo informeraos.InformerAoSGameState informeraos.InformerAoSExpander"
	["kuhn-poker"]="poker.kuhn.KPGameInfo poker.kuhn.KuhnPokerGameState poker.kuhn.KuhnPokerExpander"
	["liars-dice"]="liarsdice.LDGameInfo liarsdice.LiarsDiceGameState liarsdice.LiarsDiceExpander"
	["mpochm"]="mpochm.MPoCHMGameInfo mpochm.MPoCHMGameState mpochm.MPoCHMExpander"
	["nfp-test"]="nfptest.TestGameInfo nfptest.TestGameState nfptest.TestExpander"
	["non-loc"]="nonlocality.NonLocInfo nonlocality.NonLocState nonlocality.NonLocExpander"
	["oshi-zumo-10-3-1"]="oshizumo.OZGameInfo oshizumo.OshiZumoGameState oshizumo.OshiZumoExpander GENERAL_SUM=false startingCoins=10 locK=3 minBid=1"
	["oshi-zumo-10-3-1-points"]="oshizumo.OZGameInfo oshizumo.OshiZumoGameState oshizumo.OshiZumoExpander GENERAL_SUM=false BINARY_UTILITIES=false startingCoins=10 locK=3 minBid=1"
	["oshi-zumo"]="oshizumo.OZGameInfo oshizumo.OshiZumoGameState oshizumo.OshiZumoExpander"
	["perfect-information-wichardt"]="wichardtne.WichardtGameInfo wichardtne.PerfectInformationWichardtState wichardtne.WichardtExpander"
	["pursuit-simple-4x4-5"]="pursuit.PursuitGameInfo pursuit.PursuitGameState pursuit.FastImprovedExpander graphFile=gtlibrary-java/pursuit_simple4x4.txt evaderStart=0 p1Start=11 p2Start=15 evaderGoal=-1 depth=5"
	["random-game-improved"]="randomgameimproved.RandomGameInfo randomgameimproved.RandomGameState randomgameimproved.RandomGameExpander"
	["random-game"]="randomgame.RandomGameInfo randomgame.RandomGameState randomgame.RandomGameExpander"
	["rps"]="rps.RPSGameInfo rps.RPSGameState rps.RPSExpander"
	["stack-test"]="stacktest.StackTestGameInfo stacktest.StackTestGameState stacktest.StackTestExpander"
	["test"]="testGame.TestGameInfo testGame.TestGameState testGame.TestGameExpander"
	["tron-4x5"]="tron.TronGameInfo tron.TronGameState tron.TronExpander ROWS=4 COLS=5"
	["tron-5x5"]="tron.TronGameInfo tron.TronGameState tron.TronExpander ROWS=5 COLS=5"
	["tron-6x6"]="tron.TronGameInfo tron.TronGameState tron.TronExpander ROWS=6 COLS=6"
	["tron"]="tron.TronGameInfo tron.TronGameState tron.TronExpander"
	["ud"]="upordown.UDGameInfo upordown.UDGameState upordown.UDExpander"
	["visibility-pursuit-goal-optimized-5"]="pursuit.PursuitGameInfo pursuit.VisibilityPursuitGameState pursuit.FastImprovedExpander graphFile=gtlibrary-java/pursuit_goal_optimized.txt evaderStart=0 p1Start=7 p2Start=13 evaderGoal=10 depth=5 visibility=2"
	["visibility-pursuit-goal-optimized-6"]="pursuit.PursuitGameInfo pursuit.VisibilityPursuitGameState pursuit.FastImprovedExpander graphFile=gtlibrary-java/pursuit_goal_optimized.txt evaderStart=0 p1Start=7 p2Start=13 evaderGoal=10 depth=6 visibility=2"
	["visibility-pursuit-goal-optimized-7"]="pursuit.PursuitGameInfo pursuit.VisibilityPursuitGameState pursuit.FastImprovedExpander graphFile=gtlibrary-java/pursuit_goal_optimized.txt evaderStart=0 p1Start=7 p2Start=13 evaderGoal=10 depth=7 visibility=2"
)

for name in ${!games[@]}; do
	./gt-library.py "${games[$name]}" gt-library/$name.jsonl > gt-library/$name.efg
done
