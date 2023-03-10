import json

# charger les résultats depuis une chaîne JSON ou un fichier
resultats = json.loads('[{"championId":161,"championLevel":7,"championPoints":62207,"lastPlayTime":1677889540000,"championPointsSinceLastLevel":40607,"championPointsUntilNextLevel":0,"chestGranted":true,"tokensEarned":0,"summonerId":"kgDgl2ZnQEIRdaLH_wdzI_oSNC-Df0fZ7bnQDiqiB0sTdlxEoVmCuTZPjg"},{"championId":81,"championLevel":6,"championPoints":53193,"lastPlayTime":1678039068000,"championPointsSinceLastLevel":31593,"championPointsUntilNextLevel":0,"chestGranted":true,"tokensEarned":3,"summonerId":"kgDgl2ZnQEIRdaLH_wdzI_oSNC-Df0fZ7bnQDiqiB0sTdlxEoVmCuTZPjg"},{"championId":145,"championLevel":6,"championPoints":51950,"lastPlayTime":1676480533000,"championPointsSinceLastLevel":30350,"championPointsUntilNextLevel":0,"chestGranted":false,"tokensEarned":2,"summonerId":"kgDgl2ZnQEIRdaLH_wdzI_oSNC-Df0fZ7bnQDiqiB0sTdlxEoVmCuTZPjg"}]')

# afficher les résultats
print(resultats)

for resultat in resultats:
    print(resultat['championId'])
    print(resultat['championLevel'])
    print(resultat['championPoints'])

    