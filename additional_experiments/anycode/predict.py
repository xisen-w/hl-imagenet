"""Classifier: random forest of 21 decision trees compiled to Python code.
Interface: predict(image: np.ndarray) -> str

CONSTRAINT: No stored training data. Each tree is pure if/else code.
The forest captures feature interactions via conjunctive splits
and uses ensemble voting to reduce overfitting.

21 trees, max_depth=20, 71 features including spatial grid."""

import cv2
import numpy as np
from collections import Counter


CLASSES = [
    "golden_retriever", "mushroom", "teapot", "school_bus", "banana",
    "orange", "brown_bear", "king_penguin", "jellyfish", "sports_car",
]


def predict(image: np.ndarray) -> str:
    f = _extract_features(image)
    votes = [_tree_0(f), _tree_1(f), _tree_2(f), _tree_3(f), _tree_4(f), _tree_5(f), _tree_6(f), _tree_7(f), _tree_8(f), _tree_9(f), _tree_10(f), _tree_11(f), _tree_12(f), _tree_13(f), _tree_14(f), _tree_15(f), _tree_16(f), _tree_17(f), _tree_18(f), _tree_19(f), _tree_20(f)]
    counts = Counter(votes)
    return CLASSES[counts.most_common(1)[0][0]]


def _tree_0(f):
    if f[1] <= -57.2456:
        if f[29] <= 54.8204:
            if f[3] <= 0.0978:
                return 8
            else:
                return 8
        else:
            return 8
    else:
        if f[7] <= 186.4824:
            if f[19] <= 0.6935:
                if f[17] <= 0.0666:
                    if f[10] <= 5904.0057:
                        if f[68] <= 59.5977:
                            if f[70] <= 0.255:
                                if f[29] <= -22.2748:
                                    return 2
                                else:
                                    return 2
                            else:
                                return 6
                        else:
                            if f[63] <= 104.8757:
                                return 9
                            else:
                                return 8
                    else:
                        if f[28] <= 0.7767:
                            return 2
                        else:
                            if f[33] <= 0.0588:
                                return 6
                            else:
                                if f[19] <= 0.664:
                                    if f[25] <= 0.374:
                                        return 9
                                    else:
                                        return 2
                                else:
                                    if f[5] <= 0.0129:
                                        return 5
                                    else:
                                        return 9
                else:
                    if f[26] <= 84.6938:
                        if f[21] <= 6.0824:
                            if f[58] <= 21.6709:
                                if f[29] <= -11.4183:
                                    return 2
                                else:
                                    return 2
                            else:
                                if f[25] <= 0.332:
                                    if f[69] <= 0.3335:
                                        if f[59] <= 107.3695:
                                            return 2
                                        else:
                                            if f[8] <= 0.0325:
                                                return 1
                                            else:
                                                return 9
                                    else:
                                        return 7
                                else:
                                    return 6
                        else:
                            if f[13] <= 37.1001:
                                if f[62] <= 196.2106:
                                    if f[29] <= -31.2314:
                                        return 6
                                    else:
                                        if f[57] <= 0.3525:
                                            if f[21] <= 15.8169:
                                                return 9
                                            else:
                                                if f[64] <= 84.8652:
                                                    return 4
                                                else:
                                                    return 4
                                        else:
                                            return 1
                                else:
                                    if f[37] <= 0.0309:
                                        return 5
                                    else:
                                        return 3
                            else:
                                if f[18] <= 0.0198:
                                    return 9
                                else:
                                    return 9
                    else:
                        if f[40] <= 0.8235:
                            if f[6] <= 0.0698:
                                if f[45] <= 0.1172:
                                    if f[34] <= 0.9948:
                                        return 1
                                    else:
                                        return 8
                                else:
                                    if f[14] <= 0.6488:
                                        return 3
                                    else:
                                        return 6
                            else:
                                if f[29] <= 21.5296:
                                    if f[25] <= 0.2414:
                                        return 4
                                    else:
                                        if f[24] <= 0.0474:
                                            if f[68] <= 43.7368:
                                                return 9
                                            else:
                                                if f[52] <= 152.5156:
                                                    return 3
                                                else:
                                                    return 3
                                        else:
                                            return 3
                                else:
                                    if f[62] <= 147.1229:
                                        if f[33] <= 0.1147:
                                            return 9
                                        else:
                                            return 9
                                    else:
                                        return 3
                        else:
                            return 9
            else:
                if f[45] <= 0.0847:
                    if f[40] <= 0.432:
                        if f[21] <= 54.0777:
                            if f[59] <= 117.1701:
                                if f[20] <= 0.0766:
                                    if f[41] <= 2.0387:
                                        return 2
                                    else:
                                        return 7
                                else:
                                    if f[57] <= 0.1066:
                                        return 8
                                    else:
                                        if f[2] <= 0.0:
                                            if f[7] <= 15.9844:
                                                return 7
                                            else:
                                                return 6
                                        else:
                                            if f[21] <= 26.4675:
                                                return 7
                                            else:
                                                if f[49] <= 0.2754:
                                                    return 7
                                                else:
                                                    return 7
                            else:
                                if f[49] <= 0.2129:
                                    return 8
                                else:
                                    return 6
                        else:
                            if f[13] <= 42.0205:
                                return 0
                            else:
                                return 6
                    else:
                        if f[34] <= 0.9612:
                            if f[70] <= 0.375:
                                if f[22] <= 1.1411:
                                    if f[62] <= 98.083:
                                        if f[47] <= 62.2275:
                                            return 7
                                        else:
                                            return 7
                                    else:
                                        if f[10] <= 11722.3625:
                                            if f[43] <= 2.2532:
                                                return 6
                                            else:
                                                if f[57] <= 0.3406:
                                                    return 6
                                                else:
                                                    return 6
                                        else:
                                            if f[22] <= 0.9896:
                                                return 7
                                            else:
                                                if f[5] <= 0.056:
                                                    return 1
                                                else:
                                                    return 6
                                else:
                                    if f[69] <= 0.3847:
                                        if f[18] <= 0.0603:
                                            if f[37] <= 0.006:
                                                return 7
                                            else:
                                                return 2
                                        else:
                                            if f[4] <= 0.0076:
                                                return 9
                                            else:
                                                return 1
                                    else:
                                        return 1
                            else:
                                if f[56] <= 97.9547:
                                    return 1
                                else:
                                    if f[44] <= 0.0467:
                                        return 6
                                    else:
                                        return 6
                        else:
                            if f[38] <= 0.4236:
                                if f[11] <= 78.4412:
                                    if f[61] <= 0.3496:
                                        if f[41] <= 1.4444:
                                            if f[27] <= 127.5311:
                                                return 7
                                            else:
                                                if f[64] <= 114.4595:
                                                    return 8
                                                else:
                                                    return 8
                                        else:
                                            if f[19] <= 0.8804:
                                                if f[25] <= 0.3218:
                                                    return 7
                                                else:
                                                    return 8
                                            else:
                                                return 5
                                    else:
                                        return 6
                                else:
                                    if f[66] <= 118.3177:
                                        if f[55] <= 95.6934:
                                            return 3
                                        else:
                                            return 2
                                    else:
                                        if f[46] <= 73.332:
                                            return 9
                                        else:
                                            return 9
                            else:
                                if f[31] <= 0.0022:
                                    if f[42] <= 1.388:
                                        if f[55] <= 94.2734:
                                            if f[8] <= 0.418:
                                                if f[30] <= 0.4025:
                                                    if f[69] <= 0.2438:
                                                        return 6
                                                    else:
                                                        return 4
                                                else:
                                                    return 1
                                            else:
                                                return 0
                                        else:
                                            return 9
                                    else:
                                        if f[13] <= 45.7202:
                                            if f[15] <= 0.1426:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            return 3
                                else:
                                    if f[10] <= 7784.3991:
                                        if f[63] <= 174.3229:
                                            return 7
                                        else:
                                            return 2
                                    else:
                                        return 3
                else:
                    if f[10] <= 5733.9813:
                        if f[44] <= 0.2908:
                            if f[34] <= 1.178:
                                if f[22] <= 0.8128:
                                    return 8
                                else:
                                    if f[30] <= 0.3545:
                                        if f[70] <= 0.2599:
                                            if f[23] <= 0.1716:
                                                return 5
                                            else:
                                                if f[34] <= 0.9582:
                                                    return 4
                                                else:
                                                    return 0
                                        else:
                                            if f[14] <= 0.4766:
                                                return 0
                                            else:
                                                if f[24] <= 0.001:
                                                    return 0
                                                else:
                                                    if f[25] <= 0.2969:
                                                        if f[33] <= 0.2844:
                                                            return 0
                                                        else:
                                                            return 0
                                                    else:
                                                        return 0
                                    else:
                                        if f[9] <= 0.2839:
                                            if f[34] <= 0.989:
                                                if f[7] <= 98.3641:
                                                    return 6
                                                else:
                                                    return 6
                                            else:
                                                return 2
                                        else:
                                            return 0
                            else:
                                if f[37] <= 0.0061:
                                    return 0
                                else:
                                    if f[37] <= 0.0289:
                                        if f[52] <= 143.2661:
                                            return 2
                                        else:
                                            return 2
                                    else:
                                        return 3
                        else:
                            if f[70] <= 0.2943:
                                if f[63] <= 127.9751:
                                    if f[57] <= 0.1982:
                                        if f[21] <= 9.231:
                                            return 4
                                        else:
                                            return 2
                                    else:
                                        if f[3] <= 0.0845:
                                            return 7
                                        else:
                                            return 7
                                else:
                                    if f[68] <= 21.8521:
                                        if f[58] <= 43.4248:
                                            if f[25] <= 0.2676:
                                                return 4
                                            else:
                                                if f[0] <= 141.6089:
                                                    return 0
                                                else:
                                                    return 1
                                        else:
                                            return 5
                                    else:
                                        if f[5] <= 0.022:
                                            return 4
                                        else:
                                            if f[1] <= 48.7528:
                                                return 8
                                            else:
                                                if f[11] <= 57.992:
                                                    return 4
                                                else:
                                                    return 4
                            else:
                                if f[44] <= 0.5916:
                                    if f[48] <= 119.4111:
                                        if f[3] <= 0.0837:
                                            return 6
                                        else:
                                            return 4
                                    else:
                                        if f[65] <= 147.7027:
                                            if f[1] <= 22.853:
                                                return 0
                                            else:
                                                return 0
                                        else:
                                            return 5
                                else:
                                    if f[52] <= 132.0762:
                                        if f[70] <= 0.3203:
                                            return 7
                                        else:
                                            return 6
                                    else:
                                        if f[68] <= 24.2129:
                                            if f[4] <= 0.4317:
                                                return 4
                                            else:
                                                return 4
                                        else:
                                            return 1
                    else:
                        if f[29] <= 19.1697:
                            if f[53] <= 0.3467:
                                if f[10] <= 7174.3482:
                                    if f[56] <= 114.4703:
                                        if f[50] <= 26.0312:
                                            return 6
                                        else:
                                            return 6
                                    else:
                                        if f[44] <= 0.1605:
                                            return 0
                                        else:
                                            if f[5] <= 0.003:
                                                return 2
                                            else:
                                                return 2
                                else:
                                    if f[26] <= 83.7622:
                                        if f[26] <= 72.5727:
                                            return 5
                                        else:
                                            if f[14] <= 0.4958:
                                                return 0
                                            else:
                                                return 9
                                    else:
                                        if f[43] <= 2.3768:
                                            if f[61] <= 0.3457:
                                                if f[24] <= 0.0381:
                                                    if f[30] <= 0.1465:
                                                        return 0
                                                    else:
                                                        return 4
                                                else:
                                                    if f[46] <= 21.666:
                                                        return 3
                                                    else:
                                                        return 3
                                            else:
                                                if f[51] <= 104.8643:
                                                    if f[24] <= 0.0845:
                                                        return 4
                                                    else:
                                                        return 0
                                                else:
                                                    return 1
                                        else:
                                            if f[45] <= 0.1592:
                                                if f[64] <= 90.4837:
                                                    return 3
                                                else:
                                                    return 2
                                            else:
                                                if f[60] <= 96.3398:
                                                    return 3
                                                else:
                                                    return 3
                            else:
                                if f[29] <= -20.5596:
                                    if f[19] <= 1.0317:
                                        if f[9] <= 0.0107:
                                            return 3
                                        else:
                                            if f[6] <= 0.1311:
                                                return 6
                                            else:
                                                return 6
                                    else:
                                        if f[63] <= 122.2087:
                                            return 6
                                        else:
                                            return 0
                                else:
                                    if f[13] <= 14.2688:
                                        if f[30] <= 0.0991:
                                            return 5
                                        else:
                                            if f[46] <= 24.3281:
                                                return 6
                                            else:
                                                return 6
                                    else:
                                        if f[53] <= 0.3508:
                                            return 7
                                        else:
                                            if f[11] <= 120.9045:
                                                if f[39] <= 25.4431:
                                                    if f[61] <= 0.3662:
                                                        if f[17] <= 0.3208:
                                                            if f[67] <= 82.5597:
                                                                return 0
                                                            else:
                                                                return 0
                                                        else:
                                                            return 3
                                                    else:
                                                        return 1
                                                else:
                                                    return 6
                                            else:
                                                if f[34] <= 0.7695:
                                                    return 3
                                                else:
                                                    return 3
                        else:
                            if f[57] <= 0.3223:
                                if f[63] <= 139.9263:
                                    if f[60] <= 110.6975:
                                        if f[30] <= 0.7598:
                                            if f[39] <= 49.2275:
                                                return 2
                                            else:
                                                return 4
                                        else:
                                            return 8
                                    else:
                                        return 0
                                else:
                                    if f[59] <= 153.792:
                                        return 3
                                    else:
                                        return 3
                            else:
                                if f[60] <= 122.8314:
                                    if f[39] <= 29.1711:
                                        return 6
                                    else:
                                        if f[2] <= 0.0081:
                                            if f[14] <= 0.5209:
                                                return 1
                                            else:
                                                if f[30] <= 0.6855:
                                                    return 1
                                                else:
                                                    return 1
                                        else:
                                            return 0
                                else:
                                    if f[7] <= 126.2139:
                                        if f[27] <= 162.4561:
                                            if f[11] <= 80.4303:
                                                return 7
                                            else:
                                                if f[49] <= 0.3208:
                                                    return 2
                                                else:
                                                    return 1
                                        else:
                                            if f[54] <= 19.4043:
                                                return 0
                                            else:
                                                return 0
                                    else:
                                        if f[18] <= 0.2865:
                                            return 1
                                        else:
                                            return 1
        else:
            if f[27] <= 164.8536:
                if f[31] <= 0.1143:
                    if f[68] <= 98.6465:
                        if f[61] <= 0.3096:
                            if f[67] <= 211.8193:
                                if f[40] <= 0.6691:
                                    if f[48] <= 64.6928:
                                        return 2
                                    else:
                                        if f[54] <= 13.04:
                                            return 4
                                        else:
                                            return 5
                                else:
                                    return 3
                            else:
                                if f[70] <= 0.1889:
                                    return 5
                                else:
                                    return 4
                        else:
                            if f[41] <= 1.7857:
                                return 1
                            else:
                                return 1
                    else:
                        return 8
                else:
                    if f[3] <= 0.6311:
                        if f[68] <= 18.0218:
                            if f[28] <= 1.3991:
                                return 1
                            else:
                                return 4
                        else:
                            return 4
                    else:
                        return 5
            else:
                if f[26] <= 79.6859:
                    if f[23] <= 0.2485:
                        if f[11] <= 67.598:
                            if f[3] <= 0.3064:
                                return 5
                            else:
                                return 5
                        else:
                            if f[29] <= 9.1951:
                                if f[39] <= 13.1821:
                                    return 4
                                else:
                                    return 5
                            else:
                                return 5
                    else:
                        return 4
                else:
                    if f[35] <= 0.0508:
                        if f[6] <= 0.3907:
                            return 2
                        else:
                            if f[31] <= 0.0991:
                                return 5
                            else:
                                return 4
                    else:
                        return 9


def _tree_1(f):
    if f[22] <= 0.4129:
        return 8
    else:
        if f[1] <= 41.8219:
            if f[10] <= 7423.6108:
                if f[70] <= 0.2159:
                    if f[2] <= 0.1843:
                        if f[31] <= 0.0067:
                            if f[68] <= 73.5688:
                                if f[40] <= 0.7039:
                                    if f[33] <= 0.642:
                                        if f[21] <= 50.2007:
                                            if f[44] <= 0.0069:
                                                if f[61] <= 0.2151:
                                                    return 2
                                                else:
                                                    return 2
                                            else:
                                                return 2
                                        else:
                                            return 1
                                    else:
                                        return 1
                                else:
                                    if f[44] <= 0.4151:
                                        return 9
                                    else:
                                        return 4
                            else:
                                if f[30] <= 0.7275:
                                    if f[18] <= 0.0159:
                                        if f[30] <= 0.0645:
                                            return 7
                                        else:
                                            return 5
                                    else:
                                        return 2
                                else:
                                    return 8
                        else:
                            if f[8] <= 0.159:
                                if f[5] <= 0.0908:
                                    if f[25] <= 0.2773:
                                        if f[26] <= 35.3715:
                                            return 4
                                        else:
                                            return 4
                                    else:
                                        return 2
                                else:
                                    return 1
                            else:
                                if f[18] <= 0.002:
                                    return 2
                                else:
                                    if f[40] <= 0.6191:
                                        return 7
                                    else:
                                        return 3
                    else:
                        if f[23] <= 0.0173:
                            if f[56] <= 164.8389:
                                return 8
                            else:
                                return 8
                        else:
                            if f[19] <= 0.7244:
                                return 3
                            else:
                                if f[66] <= 121.9101:
                                    if f[21] <= 3.9087:
                                        return 8
                                    else:
                                        return 6
                                else:
                                    return 5
                else:
                    if f[25] <= 0.3232:
                        if f[55] <= 43.1299:
                            if f[6] <= 0.0058:
                                if f[42] <= 0.9958:
                                    if f[40] <= 0.4636:
                                        return 7
                                    else:
                                        return 0
                                else:
                                    return 2
                            else:
                                if f[36] <= 0.5073:
                                    if f[60] <= 87.0332:
                                        return 7
                                    else:
                                        return 7
                                else:
                                    return 4
                        else:
                            if f[23] <= 0.1519:
                                if f[61] <= 0.248:
                                    if f[42] <= 1.0933:
                                        if f[29] <= -31.1467:
                                            return 7
                                        else:
                                            return 7
                                    else:
                                        return 4
                                else:
                                    if f[65] <= 121.9888:
                                        if f[19] <= 0.6311:
                                            return 6
                                        else:
                                            if f[25] <= 0.3057:
                                                if f[37] <= 0.0525:
                                                    if f[67] <= 72.4659:
                                                        return 2
                                                    else:
                                                        if f[68] <= 72.0461:
                                                            return 4
                                                        else:
                                                            return 0
                                                else:
                                                    return 7
                                            else:
                                                if f[50] <= 65.9961:
                                                    return 1
                                                else:
                                                    return 2
                                    else:
                                        if f[8] <= 0.017:
                                            return 6
                                        else:
                                            return 8
                            else:
                                if f[17] <= 0.0837:
                                    if f[12] <= 73.123:
                                        return 0
                                    else:
                                        return 6
                                else:
                                    if f[0] <= 93.8169:
                                        if f[37] <= 0.0423:
                                            if f[23] <= 0.4001:
                                                if f[61] <= 0.332:
                                                    if f[33] <= 0.3823:
                                                        return 2
                                                    else:
                                                        return 2
                                                else:
                                                    return 3
                                            else:
                                                if f[35] <= 0.3076:
                                                    return 0
                                                else:
                                                    return 2
                                        else:
                                            return 6
                                    else:
                                        if f[56] <= 93.2217:
                                            return 1
                                        else:
                                            if f[40] <= 0.5396:
                                                return 4
                                            else:
                                                return 3
                    else:
                        if f[23] <= 0.2212:
                            if f[55] <= 136.5449:
                                if f[38] <= 0.0921:
                                    if f[42] <= 1.0125:
                                        return 6
                                    else:
                                        return 6
                                else:
                                    if f[56] <= 172.3812:
                                        if f[13] <= 62.5364:
                                            if f[52] <= 147.8801:
                                                if f[36] <= 0.291:
                                                    if f[4] <= 0.0019:
                                                        return 0
                                                    else:
                                                        if f[37] <= 0.02:
                                                            return 7
                                                        else:
                                                            return 9
                                                else:
                                                    return 7
                                            else:
                                                if f[19] <= 0.8371:
                                                    return 0
                                                else:
                                                    if f[24] <= 0.2354:
                                                        return 8
                                                    else:
                                                        return 2
                                        else:
                                            return 2
                                    else:
                                        return 6
                            else:
                                if f[2] <= 0.0044:
                                    return 1
                                else:
                                    if f[36] <= 0.1115:
                                        return 3
                                    else:
                                        return 3
                        else:
                            if f[63] <= 122.1004:
                                if f[10] <= 2997.8567:
                                    if f[39] <= 15.2798:
                                        return 6
                                    else:
                                        return 0
                                else:
                                    if f[41] <= 1.7636:
                                        return 6
                                    else:
                                        return 0
                            else:
                                if f[49] <= 0.242:
                                    return 7
                                else:
                                    if f[44] <= 0.545:
                                        return 0
                                    else:
                                        return 0
            else:
                if f[70] <= 0.3438:
                    if f[40] <= 0.5616:
                        if f[55] <= 50.2402:
                            if f[11] <= 98.7192:
                                if f[29] <= -50.1336:
                                    return 0
                                else:
                                    if f[12] <= 67.7428:
                                        return 7
                                    else:
                                        return 7
                            else:
                                if f[49] <= 0.2402:
                                    return 2
                                else:
                                    if f[50] <= 46.0102:
                                        return 9
                                    else:
                                        return 0
                        else:
                            if f[16] <= 0.2854:
                                if f[4] <= 0.0029:
                                    return 8
                                else:
                                    return 8
                            else:
                                if f[6] <= 0.0781:
                                    if f[47] <= 62.0078:
                                        return 6
                                    else:
                                        return 6
                                else:
                                    if f[50] <= 35.4277:
                                        if f[11] <= 114.6787:
                                            if f[63] <= 99.4472:
                                                return 1
                                            else:
                                                return 6
                                        else:
                                            return 5
                                    else:
                                        if f[62] <= 92.5853:
                                            return 7
                                        else:
                                            if f[57] <= 0.3428:
                                                return 3
                                            else:
                                                return 3
                    else:
                        if f[45] <= 0.0978:
                            if f[69] <= 0.3631:
                                if f[24] <= 0.0649:
                                    if f[66] <= 144.0745:
                                        return 8
                                    else:
                                        return 9
                                else:
                                    if f[12] <= 37.0102:
                                        return 4
                                    else:
                                        if f[25] <= 0.3535:
                                            if f[61] <= 0.3447:
                                                if f[60] <= 144.3604:
                                                    return 9
                                                else:
                                                    return 9
                                            else:
                                                return 1
                                        else:
                                            return 2
                            else:
                                if f[11] <= 127.0129:
                                    return 7
                                else:
                                    return 7
                        else:
                            if f[29] <= -16.8882:
                                if f[64] <= 169.094:
                                    if f[4] <= 0.16:
                                        if f[23] <= 0.2642:
                                            return 3
                                        else:
                                            return 3
                                    else:
                                        return 2
                                else:
                                    if f[40] <= 0.6148:
                                        return 6
                                    else:
                                        return 1
                            else:
                                if f[30] <= 0.5607:
                                    if f[6] <= 0.1138:
                                        if f[7] <= 85.875:
                                            if f[46] <= 45.7045:
                                                return 0
                                            else:
                                                return 9
                                        else:
                                            if f[1] <= 20.9436:
                                                return 3
                                            else:
                                                return 1
                                    else:
                                        return 3
                                else:
                                    if f[19] <= 0.7609:
                                        if f[35] <= 0.1387:
                                            return 3
                                        else:
                                            if f[45] <= 0.2478:
                                                return 9
                                            else:
                                                return 9
                                    else:
                                        return 1
                else:
                    if f[60] <= 99.7119:
                        if f[5] <= 0.0021:
                            return 7
                        else:
                            if f[64] <= 89.4426:
                                if f[29] <= -0.0791:
                                    return 1
                                else:
                                    if f[21] <= 8.5017:
                                        return 1
                                    else:
                                        return 1
                            else:
                                if f[63] <= 127.3445:
                                    if f[44] <= 0.2803:
                                        return 9
                                    else:
                                        return 3
                                else:
                                    return 1
                    else:
                        if f[29] <= 2.0615:
                            if f[22] <= 1.4291:
                                if f[5] <= 0.0422:
                                    if f[30] <= 0.2842:
                                        if f[8] <= 0.2075:
                                            if f[58] <= 47.4866:
                                                return 0
                                            else:
                                                return 7
                                        else:
                                            if f[18] <= 0.012:
                                                return 3
                                            else:
                                                return 6
                                    else:
                                        return 1
                                else:
                                    if f[18] <= 0.0047:
                                        return 6
                                    else:
                                        if f[16] <= 0.9889:
                                            return 6
                                        else:
                                            return 6
                            else:
                                if f[35] <= 0.1289:
                                    return 9
                                else:
                                    return 4
                        else:
                            if f[7] <= 84.3727:
                                if f[18] <= 0.0093:
                                    if f[67] <= 29.9695:
                                        return 6
                                    else:
                                        if f[69] <= 0.3616:
                                            return 2
                                        else:
                                            return 7
                                else:
                                    if f[65] <= 91.923:
                                        if f[25] <= 0.3682:
                                            if f[10] <= 10151.3248:
                                                return 7
                                            else:
                                                return 2
                                        else:
                                            return 6
                                    else:
                                        if f[13] <= 24.0635:
                                            return 0
                                        else:
                                            return 0
                            else:
                                if f[14] <= 0.6359:
                                    if f[17] <= 0.2014:
                                        return 1
                                    else:
                                        return 1
                                else:
                                    if f[7] <= 95.0459:
                                        return 2
                                    else:
                                        return 3
        else:
            if f[66] <= 205.0729:
                if f[31] <= 0.1382:
                    if f[34] <= 1.1426:
                        if f[11] <= 94.6201:
                            if f[64] <= 134.1126:
                                if f[38] <= 0.1104:
                                    if f[19] <= 1.1916:
                                        if f[70] <= 0.3338:
                                            if f[9] <= 0.2156:
                                                if f[54] <= 13.7607:
                                                    return 4
                                                else:
                                                    if f[24] <= 0.038:
                                                        return 1
                                                    else:
                                                        return 2
                                            else:
                                                return 8
                                        else:
                                            if f[31] <= 0.1065:
                                                if f[44] <= 0.1137:
                                                    return 1
                                                else:
                                                    return 1
                                            else:
                                                return 4
                                    else:
                                        return 0
                                else:
                                    if f[11] <= 81.5924:
                                        return 5
                                    else:
                                        return 6
                            else:
                                if f[53] <= 0.2793:
                                    if f[20] <= 0.4283:
                                        if f[37] <= 0.0032:
                                            if f[4] <= 0.0032:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            return 0
                                    else:
                                        if f[44] <= 0.2077:
                                            return 5
                                        else:
                                            return 4
                                else:
                                    if f[39] <= 7.0728:
                                        return 1
                                    else:
                                        if f[7] <= 168.6543:
                                            return 0
                                        else:
                                            return 0
                        else:
                            if f[29] <= 13.0227:
                                if f[13] <= 44.2407:
                                    if f[23] <= 0.0122:
                                        return 5
                                    else:
                                        if f[46] <= 22.6074:
                                            if f[38] <= 0.1111:
                                                if f[14] <= 0.5905:
                                                    return 1
                                                else:
                                                    return 6
                                            else:
                                                return 2
                                        else:
                                            if f[17] <= 0.3284:
                                                if f[6] <= 0.2234:
                                                    return 6
                                                else:
                                                    return 0
                                            else:
                                                if f[55] <= 131.1631:
                                                    return 3
                                                else:
                                                    return 3
                                else:
                                    if f[37] <= 0.0551:
                                        return 9
                                    else:
                                        return 9
                            else:
                                if f[56] <= 151.9355:
                                    if f[4] <= 0.0379:
                                        return 0
                                    else:
                                        if f[35] <= 0.2043:
                                            return 1
                                        else:
                                            return 1
                                else:
                                    return 3
                    else:
                        if f[45] <= 0.5833:
                            if f[27] <= 132.1052:
                                if f[5] <= 0.0164:
                                    return 2
                                else:
                                    return 9
                            else:
                                if f[29] <= -48.8339:
                                    return 2
                                else:
                                    if f[41] <= 1.2926:
                                        return 2
                                    else:
                                        if f[34] <= 1.6712:
                                            return 5
                                        else:
                                            return 5
                        else:
                            if f[15] <= 0.0125:
                                return 4
                            else:
                                if f[59] <= 143.2852:
                                    return 2
                                else:
                                    return 2
                else:
                    if f[10] <= 10184.7205:
                        if f[40] <= 0.4699:
                            if f[50] <= 19.3813:
                                return 4
                            else:
                                if f[64] <= 126.9517:
                                    return 4
                                else:
                                    return 4
                        else:
                            if f[6] <= 0.1591:
                                if f[69] <= 0.1533:
                                    return 2
                                else:
                                    if f[55] <= 94.6589:
                                        return 4
                                    else:
                                        if f[56] <= 131.6967:
                                            return 0
                                        else:
                                            return 0
                            else:
                                if f[27] <= 204.6211:
                                    if f[41] <= 1.1258:
                                        if f[0] <= 151.8345:
                                            return 7
                                        else:
                                            return 1
                                    else:
                                        if f[24] <= 0.026:
                                            if f[61] <= 0.3213:
                                                return 4
                                            else:
                                                if f[64] <= 124.1705:
                                                    return 0
                                                else:
                                                    return 4
                                        else:
                                            if f[4] <= 0.3251:
                                                if f[66] <= 149.5737:
                                                    return 2
                                                else:
                                                    return 5
                                            else:
                                                if f[62] <= 164.8661:
                                                    return 4
                                                else:
                                                    return 4
                                else:
                                    if f[56] <= 188.2264:
                                        return 9
                                    else:
                                        return 5
                    else:
                        if f[70] <= 0.3473:
                            if f[42] <= 0.9872:
                                return 3
                            else:
                                return 3
                        else:
                            if f[47] <= 133.1621:
                                if f[63] <= 147.3542:
                                    return 5
                                else:
                                    return 0
                            else:
                                if f[34] <= 0.7085:
                                    return 1
                                else:
                                    return 1
            else:
                if f[9] <= 0.006:
                    if f[64] <= 165.6854:
                        if f[69] <= 0.2039:
                            return 5
                        else:
                            return 4
                    else:
                        return 5
                else:
                    if f[4] <= 0.3145:
                        if f[27] <= 164.5862:
                            if f[54] <= 38.7363:
                                if f[70] <= 0.2999:
                                    if f[3] <= 0.826:
                                        return 5
                                    else:
                                        return 4
                                else:
                                    return 1
                            else:
                                return 8
                        else:
                            if f[69] <= 0.2919:
                                if f[68] <= 19.835:
                                    return 5
                                else:
                                    return 5
                            else:
                                return 5
                    else:
                        if f[61] <= 0.3408:
                            return 4
                        else:
                            return 1


def _tree_2(f):
    if f[11] <= 87.4953:
        if f[22] <= 0.6896:
            if f[6] <= 0.3074:
                if f[61] <= 0.2996:
                    if f[25] <= 0.2012:
                        return 7
                    else:
                        return 8
                else:
                    return 6
            else:
                if f[50] <= 99.7615:
                    if f[37] <= 0.0155:
                        if f[34] <= 1.29:
                            return 8
                        else:
                            return 8
                    else:
                        return 7
                else:
                    return 8
        else:
            if f[7] <= 192.8518:
                if f[6] <= 0.1284:
                    if f[23] <= 0.2205:
                        if f[31] <= 0.0032:
                            if f[33] <= 0.29:
                                if f[40] <= 0.4348:
                                    if f[36] <= 0.3186:
                                        if f[56] <= 89.3262:
                                            return 7
                                        else:
                                            return 7
                                    else:
                                        return 6
                                else:
                                    if f[53] <= 0.3481:
                                        if f[58] <= 40.3932:
                                            if f[59] <= 24.873:
                                                return 4
                                            else:
                                                return 0
                                        else:
                                            if f[21] <= -0.6802:
                                                if f[57] <= 0.3525:
                                                    return 1
                                                else:
                                                    return 2
                                            else:
                                                return 6
                                    else:
                                        if f[7] <= 47.7949:
                                            return 1
                                        else:
                                            return 1
                            else:
                                if f[20] <= 0.0765:
                                    if f[21] <= 6.7705:
                                        return 2
                                    else:
                                        return 7
                                else:
                                    if f[11] <= 58.6475:
                                        if f[25] <= 0.2983:
                                            if f[19] <= 0.8979:
                                                return 2
                                            else:
                                                if f[13] <= 21.1291:
                                                    return 7
                                                else:
                                                    if f[46] <= 86.718:
                                                        return 8
                                                    else:
                                                        return 4
                                        else:
                                            if f[10] <= 1535.6999:
                                                return 8
                                            else:
                                                return 8
                                    else:
                                        if f[12] <= 37.3686:
                                            return 9
                                        else:
                                            if f[45] <= 0.0485:
                                                if f[44] <= 0.0567:
                                                    if f[60] <= 161.5029:
                                                        return 9
                                                    else:
                                                        return 0
                                                else:
                                                    return 2
                                            else:
                                                return 6
                        else:
                            if f[9] <= 0.0073:
                                if f[31] <= 0.1404:
                                    if f[37] <= 0.0029:
                                        return 2
                                    else:
                                        if f[16] <= 0.8567:
                                            return 0
                                        else:
                                            return 1
                                else:
                                    if f[68] <= 28.001:
                                        return 6
                                    else:
                                        return 4
                            else:
                                if f[22] <= 1.1568:
                                    if f[19] <= 0.5791:
                                        return 3
                                    else:
                                        return 7
                                else:
                                    if f[29] <= 28.9758:
                                        if f[67] <= 80.9737:
                                            if f[21] <= 3.5679:
                                                return 6
                                            else:
                                                return 4
                                        else:
                                            if f[63] <= 133.5833:
                                                return 7
                                            else:
                                                return 1
                                    else:
                                        if f[5] <= 0.052:
                                            return 4
                                        else:
                                            return 8
                    else:
                        if f[26] <= 60.9647:
                            if f[25] <= 0.2938:
                                if f[17] <= 0.5385:
                                    if f[40] <= 0.4623:
                                        return 7
                                    else:
                                        return 0
                                else:
                                    if f[4] <= 0.0112:
                                        return 1
                                    else:
                                        return 2
                            else:
                                if f[4] <= 0.2168:
                                    if f[61] <= 0.2715:
                                        return 0
                                    else:
                                        if f[18] <= 0.0336:
                                            if f[58] <= 31.46:
                                                return 2
                                            else:
                                                return 0
                                        else:
                                            if f[30] <= 0.4678:
                                                return 0
                                            else:
                                                return 0
                                else:
                                    return 2
                        else:
                            if f[32] <= 0.188:
                                if f[63] <= 123.2446:
                                    if f[10] <= 6751.5645:
                                        return 6
                                    else:
                                        if f[0] <= 80.094:
                                            if f[19] <= 1.0262:
                                                return 7
                                            else:
                                                return 7
                                        else:
                                            return 8
                                else:
                                    if f[49] <= 0.3682:
                                        if f[55] <= 125.918:
                                            if f[25] <= 0.3564:
                                                if f[11] <= 64.7446:
                                                    return 4
                                                else:
                                                    if f[36] <= 0.4539:
                                                        if f[8] <= 0.1313:
                                                            return 0
                                                        else:
                                                            return 0
                                                    else:
                                                        return 0
                                            else:
                                                return 6
                                        else:
                                            return 6
                                    else:
                                        if f[2] <= 0.0008:
                                            return 5
                                        else:
                                            return 6
                            else:
                                if f[21] <= 78.3649:
                                    if f[14] <= 0.7094:
                                        if f[13] <= 19.36:
                                            if f[24] <= 0.0488:
                                                if f[49] <= 0.1578:
                                                    return 2
                                                else:
                                                    return 4
                                            else:
                                                return 1
                                        else:
                                            return 0
                                    else:
                                        return 2
                                else:
                                    return 3
                else:
                    if f[31] <= 0.0442:
                        if f[68] <= 72.383:
                            if f[42] <= 1.2622:
                                if f[10] <= 4080.3095:
                                    if f[33] <= 0.3936:
                                        if f[44] <= 0.1949:
                                            if f[18] <= 0.3433:
                                                return 0
                                            else:
                                                return 0
                                        else:
                                            return 1
                                    else:
                                        return 5
                                else:
                                    if f[25] <= 0.3126:
                                        if f[60] <= 106.2969:
                                            if f[66] <= 116.128:
                                                return 3
                                            else:
                                                return 9
                                        else:
                                            if f[50] <= 25.915:
                                                return 2
                                            else:
                                                return 5
                                    else:
                                        if f[24] <= 0.0741:
                                            if f[50] <= 33.6373:
                                                return 1
                                            else:
                                                return 6
                                        else:
                                            return 6
                            else:
                                if f[27] <= 161.1672:
                                    if f[22] <= 1.3375:
                                        return 1
                                    else:
                                        if f[5] <= 0.0515:
                                            return 2
                                        else:
                                            return 2
                                else:
                                    if f[2] <= 0.0325:
                                        return 5
                                    else:
                                        return 8
                        else:
                            if f[39] <= 90.5789:
                                if f[26] <= 46.2741:
                                    if f[1] <= 7.1189:
                                        return 8
                                    else:
                                        return 8
                                else:
                                    return 9
                            else:
                                return 2
                    else:
                        if f[70] <= 0.3239:
                            if f[4] <= 0.2901:
                                if f[62] <= 193.093:
                                    if f[11] <= 55.5225:
                                        if f[43] <= 2.1942:
                                            if f[49] <= 0.1309:
                                                return 4
                                            else:
                                                return 4
                                        else:
                                            return 8
                                    else:
                                        if f[1] <= 66.4801:
                                            if f[48] <= 90.5752:
                                                return 4
                                            else:
                                                if f[10] <= 5619.6582:
                                                    return 0
                                                else:
                                                    return 3
                                        else:
                                            return 2
                                else:
                                    if f[68] <= 24.1719:
                                        return 5
                                    else:
                                        return 4
                            else:
                                if f[17] <= 0.7212:
                                    return 4
                                else:
                                    if f[40] <= 0.311:
                                        return 4
                                    else:
                                        return 2
                        else:
                            if f[12] <= 53.8329:
                                if f[36] <= 0.0431:
                                    return 4
                                else:
                                    return 1
                            else:
                                return 0
            else:
                if f[64] <= 168.8269:
                    if f[40] <= 0.3863:
                        if f[34] <= 1.3187:
                            return 4
                        else:
                            return 4
                    else:
                        if f[31] <= 0.0:
                            if f[27] <= 128.0:
                                return 8
                            else:
                                return 2
                        else:
                            if f[27] <= 146.6495:
                                if f[61] <= 0.3223:
                                    if f[39] <= 28.0024:
                                        if f[61] <= 0.2559:
                                            if f[48] <= 144.1999:
                                                return 4
                                            else:
                                                return 4
                                        else:
                                            return 0
                                    else:
                                        return 5
                                else:
                                    return 1
                            else:
                                if f[40] <= 0.6954:
                                    if f[14] <= 0.5159:
                                        if f[55] <= 225.638:
                                            return 4
                                        else:
                                            return 5
                                    else:
                                        return 5
                                else:
                                    if f[46] <= 25.7168:
                                        return 4
                                    else:
                                        return 1
                else:
                    if f[42] <= 1.2749:
                        if f[56] <= 238.3291:
                            return 5
                        else:
                            return 5
                    else:
                        if f[25] <= 0.2969:
                            return 5
                        else:
                            return 0
    else:
        if f[17] <= 0.0759:
            if f[40] <= 0.5974:
                if f[33] <= 0.0347:
                    if f[19] <= 0.9135:
                        return 1
                    else:
                        return 1
                else:
                    if f[24] <= 0.1978:
                        if f[53] <= 0.3606:
                            if f[38] <= 0.6509:
                                if f[68] <= 90.8008:
                                    if f[29] <= 72.5748:
                                        if f[39] <= 59.5491:
                                            return 0
                                        else:
                                            return 1
                                    else:
                                        return 8
                                else:
                                    return 9
                            else:
                                return 2
                        else:
                            if f[10] <= 14338.0104:
                                return 6
                            else:
                                return 6
                    else:
                        if f[21] <= 17.2754:
                            if f[6] <= 0.0134:
                                return 7
                            else:
                                return 7
                        else:
                            return 0
            else:
                if f[70] <= 0.343:
                    if f[53] <= 0.3708:
                        if f[24] <= 0.052:
                            return 2
                        else:
                            if f[58] <= 114.9675:
                                if f[28] <= 0.8347:
                                    return 2
                                else:
                                    if f[24] <= 0.4307:
                                        return 9
                                    else:
                                        return 6
                            else:
                                return 8
                    else:
                        return 3
                else:
                    if f[32] <= 0.0511:
                        return 6
                    else:
                        if f[16] <= 0.5057:
                            if f[18] <= 0.0388:
                                return 3
                            else:
                                return 9
                        else:
                            return 1
        else:
            if f[2] <= 0.0054:
                if f[39] <= 35.415:
                    if f[1] <= 64.8256:
                        if f[11] <= 118.4536:
                            if f[69] <= 0.3284:
                                if f[61] <= 0.3057:
                                    return 3
                                else:
                                    if f[53] <= 0.2285:
                                        return 2
                                    else:
                                        if f[31] <= 0.0442:
                                            return 9
                                        else:
                                            return 4
                            else:
                                if f[23] <= 0.2745:
                                    if f[50] <= 34.9404:
                                        if f[3] <= 0.0846:
                                            return 1
                                        else:
                                            return 1
                                    else:
                                        return 6
                                else:
                                    if f[37] <= 0.0135:
                                        return 0
                                    else:
                                        if f[29] <= 11.8514:
                                            return 6
                                        else:
                                            return 6
                        else:
                            if f[31] <= 0.0832:
                                if f[12] <= 53.7004:
                                    return 9
                                else:
                                    return 1
                            else:
                                if f[18] <= 0.0681:
                                    return 3
                                else:
                                    return 3
                    else:
                        if f[50] <= 28.8672:
                            if f[37] <= 0.019:
                                return 2
                            else:
                                if f[0] <= 147.4429:
                                    return 4
                                else:
                                    return 4
                        else:
                            return 5
                else:
                    if f[30] <= 0.2846:
                        if f[27] <= 148.9255:
                            if f[23] <= 0.2026:
                                return 2
                            else:
                                if f[23] <= 0.3289:
                                    return 6
                                else:
                                    return 6
                        else:
                            if f[67] <= 65.7411:
                                return 3
                            else:
                                if f[20] <= 0.228:
                                    return 0
                                else:
                                    return 1
                    else:
                        if f[66] <= 87.6259:
                            if f[18] <= 0.0122:
                                return 1
                            else:
                                return 2
                        else:
                            if f[5] <= 0.024:
                                if f[41] <= 1.6216:
                                    return 1
                                else:
                                    return 1
                            else:
                                return 1
            else:
                if f[26] <= 83.0078:
                    if f[44] <= 0.2076:
                        if f[51] <= 171.6104:
                            if f[33] <= 0.1424:
                                return 6
                            else:
                                if f[64] <= 109.7222:
                                    return 3
                                else:
                                    return 0
                        else:
                            return 5
                    else:
                        if f[14] <= 0.4589:
                            return 4
                        else:
                            if f[44] <= 0.3493:
                                if f[11] <= 105.5237:
                                    return 2
                                else:
                                    return 0
                            else:
                                if f[65] <= 79.5298:
                                    return 2
                                else:
                                    if f[21] <= -10.9065:
                                        return 9
                                    else:
                                        return 9
                else:
                    if f[29] <= -6.3011:
                        if f[13] <= 28.3786:
                            if f[35] <= 0.1818:
                                return 6
                            else:
                                if f[13] <= 24.4845:
                                    return 3
                                else:
                                    return 4
                        else:
                            if f[33] <= 0.0251:
                                return 6
                            else:
                                if f[3] <= 0.0516:
                                    if f[43] <= 2.5407:
                                        return 3
                                    else:
                                        return 3
                                else:
                                    if f[21] <= -24.2629:
                                        return 3
                                    else:
                                        return 3
                    else:
                        if f[5] <= 0.0162:
                            if f[33] <= 0.0742:
                                return 0
                            else:
                                if f[9] <= 0.3115:
                                    return 9
                                else:
                                    return 9
                        else:
                            if f[43] <= 3.2145:
                                if f[61] <= 0.3598:
                                    if f[19] <= 0.9578:
                                        if f[35] <= 0.3442:
                                            if f[22] <= 2.1602:
                                                if f[37] <= 0.0226:
                                                    return 3
                                                else:
                                                    if f[33] <= 0.2483:
                                                        return 3
                                                    else:
                                                        return 3
                                            else:
                                                return 3
                                        else:
                                            if f[6] <= 0.1583:
                                                return 3
                                            else:
                                                return 9
                                    else:
                                        if f[61] <= 0.3252:
                                            return 2
                                        else:
                                            return 0
                                else:
                                    if f[38] <= 0.1306:
                                        return 1
                                    else:
                                        if f[45] <= 0.0754:
                                            return 7
                                        else:
                                            return 3
                            else:
                                if f[34] <= 0.9311:
                                    return 3
                                else:
                                    if f[14] <= 0.5832:
                                        return 9
                                    else:
                                        return 4


def _tree_3(f):
    if f[22] <= 0.7951:
        if f[67] <= 142.8295:
            if f[42] <= 1.2133:
                if f[54] <= 96.4082:
                    if f[25] <= 0.3418:
                        if f[14] <= 0.5955:
                            return 9
                        else:
                            return 3
                    else:
                        return 0
                else:
                    if f[22] <= 0.6515:
                        return 6
                    else:
                        if f[47] <= 94.4125:
                            return 7
                        else:
                            return 7
            else:
                if f[22] <= 0.6646:
                    return 8
                else:
                    return 7
        else:
            if f[3] <= 0.086:
                if f[59] <= 175.3629:
                    if f[7] <= 145.7373:
                        return 8
                    else:
                        return 7
                else:
                    return 8
            else:
                if f[5] <= 0.0009:
                    return 8
                else:
                    return 5
    else:
        if f[11] <= 92.652:
            if f[1] <= 106.9941:
                if f[59] <= 44.6686:
                    if f[19] <= 0.8526:
                        if f[35] <= 0.7809:
                            if f[69] <= 0.3341:
                                if f[11] <= 50.05:
                                    if f[23] <= 0.105:
                                        return 5
                                    else:
                                        return 4
                                else:
                                    if f[25] <= 0.3047:
                                        if f[36] <= 0.3904:
                                            return 3
                                        else:
                                            return 0
                                    else:
                                        return 9
                            else:
                                return 6
                        else:
                            if f[46] <= 95.1738:
                                if f[21] <= -31.8677:
                                    return 2
                                else:
                                    return 2
                            else:
                                return 7
                    else:
                        if f[31] <= 0.0:
                            if f[43] <= 2.0008:
                                if f[55] <= 11.9248:
                                    if f[40] <= 0.4628:
                                        return 6
                                    else:
                                        return 2
                                else:
                                    if f[45] <= 0.2347:
                                        return 7
                                    else:
                                        return 0
                            else:
                                if f[68] <= 61.5205:
                                    return 0
                                else:
                                    return 8
                        else:
                            if f[22] <= 1.221:
                                if f[26] <= 112.1939:
                                    if f[40] <= 0.5135:
                                        return 7
                                    else:
                                        if f[5] <= 0.0414:
                                            return 0
                                        else:
                                            return 7
                                else:
                                    return 2
                            else:
                                return 4
                else:
                    if f[31] <= 0.1666:
                        if f[34] <= 1.0332:
                            if f[64] <= 133.0972:
                                if f[29] <= -1.9524:
                                    if f[67] <= 152.9004:
                                        if f[34] <= 0.9949:
                                            if f[66] <= 137.9402:
                                                if f[44] <= 0.5977:
                                                    if f[53] <= 0.293:
                                                        return 6
                                                    else:
                                                        return 6
                                                else:
                                                    return 2
                                            else:
                                                return 4
                                        else:
                                            if f[59] <= 73.2419:
                                                return 0
                                            else:
                                                return 5
                                    else:
                                        if f[63] <= 127.9472:
                                            return 1
                                        else:
                                            return 1
                                else:
                                    if f[11] <= 70.6646:
                                        if f[48] <= 92.3174:
                                            return 0
                                        else:
                                            if f[23] <= 0.22:
                                                if f[39] <= 18.874:
                                                    return 4
                                                else:
                                                    if f[54] <= 30.3188:
                                                        return 1
                                                    else:
                                                        if f[42] <= 1.0171:
                                                            return 5
                                                        else:
                                                            return 8
                                            else:
                                                return 0
                                    else:
                                        if f[54] <= 65.2725:
                                            if f[23] <= 0.2947:
                                                if f[2] <= 0.0051:
                                                    if f[17] <= 0.0305:
                                                        return 1
                                                    else:
                                                        return 1
                                                else:
                                                    return 3
                                            else:
                                                if f[47] <= 55.9971:
                                                    return 0
                                                else:
                                                    if f[53] <= 0.3501:
                                                        return 1
                                                    else:
                                                        return 6
                                        else:
                                            if f[6] <= 0.0234:
                                                return 6
                                            else:
                                                return 2
                            else:
                                if f[18] <= 0.0159:
                                    if f[18] <= 0.0073:
                                        if f[8] <= 0.1143:
                                            return 8
                                        else:
                                            return 2
                                    else:
                                        return 6
                                else:
                                    if f[23] <= 0.1489:
                                        if f[35] <= 0.0078:
                                            return 4
                                        else:
                                            return 2
                                    else:
                                        if f[9] <= 0.0005:
                                            return 2
                                        else:
                                            if f[31] <= 0.0215:
                                                if f[6] <= 0.1849:
                                                    return 0
                                                else:
                                                    return 0
                                            else:
                                                if f[15] <= 0.0395:
                                                    return 4
                                                else:
                                                    return 0
                        else:
                            if f[23] <= 0.1801:
                                if f[31] <= 0.0:
                                    if f[65] <= 80.2943:
                                        if f[11] <= 84.5562:
                                            if f[18] <= 0.23:
                                                if f[57] <= 0.2463:
                                                    if f[59] <= 84.4859:
                                                        return 2
                                                    else:
                                                        return 2
                                                else:
                                                    return 8
                                            else:
                                                if f[56] <= 72.8369:
                                                    return 5
                                                else:
                                                    return 0
                                        else:
                                            return 9
                                    else:
                                        if f[14] <= 0.8606:
                                            if f[54] <= 51.2789:
                                                if f[53] <= 0.2052:
                                                    return 8
                                                else:
                                                    return 2
                                            else:
                                                return 8
                                        else:
                                            return 2
                                else:
                                    if f[28] <= 1.077:
                                        if f[15] <= 0.0834:
                                            if f[31] <= 0.0366:
                                                return 1
                                            else:
                                                return 4
                                        else:
                                            if f[34] <= 1.1592:
                                                return 3
                                            else:
                                                if f[20] <= 0.374:
                                                    if f[51] <= 41.5303:
                                                        return 7
                                                    else:
                                                        return 7
                                                else:
                                                    return 2
                                    else:
                                        if f[27] <= 149.1376:
                                            if f[56] <= 123.5167:
                                                if f[61] <= 0.2154:
                                                    return 4
                                                else:
                                                    if f[13] <= 32.5571:
                                                        return 1
                                                    else:
                                                        return 3
                                            else:
                                                if f[7] <= 200.5568:
                                                    return 2
                                                else:
                                                    return 5
                                        else:
                                            if f[49] <= 0.2576:
                                                return 5
                                            else:
                                                return 4
                            else:
                                if f[5] <= 0.0034:
                                    if f[4] <= 0.0049:
                                        if f[7] <= 43.459:
                                            return 2
                                        else:
                                            if f[40] <= 0.5748:
                                                return 0
                                            else:
                                                return 0
                                    else:
                                        if f[16] <= 0.6018:
                                            return 3
                                        else:
                                            if f[63] <= 152.2552:
                                                if f[26] <= 44.3046:
                                                    if f[12] <= 41.5372:
                                                        return 2
                                                    else:
                                                        return 0
                                                else:
                                                    if f[30] <= 0.084:
                                                        return 2
                                                    else:
                                                        return 2
                                            else:
                                                return 1
                                else:
                                    if f[38] <= 0.6177:
                                        if f[59] <= 73.4785:
                                            if f[61] <= 0.3376:
                                                if f[57] <= 0.2736:
                                                    return 1
                                                else:
                                                    if f[52] <= 76.592:
                                                        return 7
                                                    else:
                                                        return 7
                                            else:
                                                return 6
                                        else:
                                            if f[58] <= 23.6123:
                                                if f[20] <= 0.2059:
                                                    if f[4] <= 0.071:
                                                        return 0
                                                    else:
                                                        return 0
                                                else:
                                                    return 2
                                            else:
                                                if f[4] <= 0.0544:
                                                    if f[58] <= 38.3885:
                                                        return 2
                                                    else:
                                                        return 7
                                                else:
                                                    return 1
                                    else:
                                        return 3
                    else:
                        if f[4] <= 0.2561:
                            if f[56] <= 116.5654:
                                if f[32] <= 0.3228:
                                    return 4
                                else:
                                    return 4
                            else:
                                if f[31] <= 0.2261:
                                    if f[34] <= 1.0424:
                                        return 0
                                    else:
                                        if f[8] <= 0.079:
                                            return 5
                                        else:
                                            return 4
                                else:
                                    if f[15] <= 0.1306:
                                        return 2
                                    else:
                                        return 5
                        else:
                            if f[33] <= 0.1018:
                                if f[6] <= 0.2605:
                                    if f[15] <= 0.0967:
                                        return 6
                                    else:
                                        return 7
                                else:
                                    return 1
                            else:
                                if f[7] <= 119.1086:
                                    if f[5] <= 0.001:
                                        return 4
                                    else:
                                        if f[20] <= 0.0921:
                                            return 6
                                        else:
                                            return 0
                                else:
                                    if f[9] <= 0.0002:
                                        return 2
                                    else:
                                        if f[68] <= 43.7754:
                                            if f[17] <= 0.8191:
                                                return 4
                                            else:
                                                return 4
                                        else:
                                            return 4
            else:
                if f[19] <= 1.3606:
                    if f[14] <= 0.5154:
                        if f[34] <= 1.2096:
                            return 4
                        else:
                            return 5
                    else:
                        if f[55] <= 182.0793:
                            if f[30] <= 0.001:
                                return 5
                            else:
                                return 0
                        else:
                            if f[69] <= 0.1337:
                                return 5
                            else:
                                if f[11] <= 78.179:
                                    return 5
                                else:
                                    return 5
                else:
                    return 4
        else:
            if f[17] <= 0.0747:
                if f[61] <= 0.3447:
                    if f[19] <= 0.8065:
                        if f[6] <= 0.0142:
                            if f[32] <= 0.147:
                                return 6
                            else:
                                return 9
                        else:
                            if f[56] <= 177.9971:
                                if f[10] <= 6186.594:
                                    return 9
                                else:
                                    return 9
                            else:
                                return 0
                    else:
                        if f[44] <= 0.0872:
                            if f[37] <= 0.0415:
                                if f[39] <= 17.1812:
                                    return 0
                                else:
                                    return 9
                            else:
                                return 2
                        else:
                            if f[5] <= 0.0378:
                                return 7
                            else:
                                return 2
                else:
                    if f[33] <= 0.0142:
                        if f[63] <= 132.4449:
                            return 1
                        else:
                            return 1
                    else:
                        if f[2] <= 0.0386:
                            if f[14] <= 0.6511:
                                if f[25] <= 0.3408:
                                    return 7
                                else:
                                    return 6
                            else:
                                return 4
                        else:
                            if f[54] <= 69.1758:
                                return 9
                            else:
                                if f[10] <= 15236.5373:
                                    return 1
                                else:
                                    return 7
            else:
                if f[2] <= 0.0078:
                    if f[1] <= 73.9385:
                        if f[30] <= 0.3449:
                            if f[53] <= 0.3658:
                                if f[19] <= 0.9651:
                                    if f[42] <= 0.9408:
                                        if f[44] <= 0.358:
                                            return 1
                                        else:
                                            if f[42] <= 0.9392:
                                                return 7
                                            else:
                                                return 5
                                    else:
                                        if f[65] <= 143.199:
                                            if f[70] <= 0.3385:
                                                if f[44] <= 0.7606:
                                                    if f[55] <= 133.6217:
                                                        if f[1] <= 31.5267:
                                                            if f[1] <= 22.6936:
                                                                return 3
                                                            else:
                                                                return 6
                                                        else:
                                                            return 3
                                                    else:
                                                        return 2
                                                else:
                                                    return 9
                                            else:
                                                return 6
                                        else:
                                            return 4
                                else:
                                    if f[19] <= 1.0388:
                                        return 0
                                    else:
                                        return 0
                            else:
                                if f[23] <= 0.5054:
                                    if f[41] <= 1.3696:
                                        return 6
                                    else:
                                        return 0
                                else:
                                    return 0
                        else:
                            if f[57] <= 0.3428:
                                if f[1] <= 24.8108:
                                    return 2
                                else:
                                    if f[3] <= 0.1362:
                                        return 1
                                    else:
                                        return 9
                            else:
                                if f[31] <= 0.0764:
                                    if f[14] <= 0.6657:
                                        return 1
                                    else:
                                        return 0
                                else:
                                    return 6
                    else:
                        if f[42] <= 0.9986:
                            if f[39] <= 27.9694:
                                return 4
                            else:
                                return 5
                        else:
                            if f[51] <= 137.4563:
                                return 3
                            else:
                                return 4
                else:
                    if f[26] <= 93.655:
                        if f[19] <= 0.5138:
                            return 9
                        else:
                            if f[59] <= 111.9548:
                                if f[60] <= 112.665:
                                    if f[51] <= 75.9014:
                                        return 2
                                    else:
                                        if f[21] <= -9.7222:
                                            return 9
                                        else:
                                            return 9
                                else:
                                    if f[3] <= 0.0085:
                                        return 7
                                    else:
                                        if f[5] <= 0.0962:
                                            if f[37] <= 0.0158:
                                                return 2
                                            else:
                                                if f[58] <= 29.3398:
                                                    return 2
                                                else:
                                                    if f[5] <= 0.0037:
                                                        return 6
                                                    else:
                                                        return 6
                                        else:
                                            return 0
                            else:
                                if f[29] <= -14.8135:
                                    if f[9] <= 0.1556:
                                        return 3
                                    else:
                                        return 3
                                else:
                                    if f[31] <= 0.1685:
                                        return 5
                                    else:
                                        if f[2] <= 0.0127:
                                            return 4
                                        else:
                                            return 4
                    else:
                        if f[29] <= -15.6246:
                            if f[53] <= 0.3604:
                                return 3
                            else:
                                return 6
                        else:
                            if f[33] <= 0.0535:
                                if f[11] <= 112.6363:
                                    if f[52] <= 129.5996:
                                        return 0
                                    else:
                                        return 0
                                else:
                                    if f[11] <= 170.9392:
                                        if f[12] <= 61.5991:
                                            if f[4] <= 0.1472:
                                                return 9
                                            else:
                                                return 4
                                        else:
                                            return 1
                                    else:
                                        return 3
                            else:
                                if f[3] <= 0.0501:
                                    if f[41] <= 1.7831:
                                        return 3
                                    else:
                                        return 9
                                else:
                                    if f[24] <= 0.0688:
                                        if f[15] <= 0.0662:
                                            if f[19] <= 0.8703:
                                                if f[39] <= 37.7769:
                                                    return 9
                                                else:
                                                    return 9
                                            else:
                                                return 2
                                        else:
                                            if f[9] <= 0.1409:
                                                return 3
                                            else:
                                                return 3
                                    else:
                                        if f[69] <= 0.2545:
                                            return 3
                                        else:
                                            return 3


def _tree_4(f):
    if f[2] <= 0.3518:
        if f[11] <= 91.2246:
            if f[22] <= 3.1162:
                if f[70] <= 0.2855:
                    if f[31] <= 0.1719:
                        if f[19] <= 1.1758:
                            if f[28] <= 0.7901:
                                if f[18] <= 0.0:
                                    return 8
                                else:
                                    return 1
                            else:
                                if f[7] <= 150.3784:
                                    if f[53] <= 0.3109:
                                        if f[9] <= 0.5449:
                                            if f[34] <= 2.0415:
                                                if f[10] <= 7376.2475:
                                                    if f[45] <= 0.0061:
                                                        if f[22] <= 1.0079:
                                                            return 2
                                                        else:
                                                            return 2
                                                    else:
                                                        if f[10] <= 574.9093:
                                                            return 8
                                                        else:
                                                            if f[42] <= 1.0705:
                                                                if f[28] <= 1.0952:
                                                                    if f[52] <= 133.7852:
                                                                        return 7
                                                                    else:
                                                                        if f[0] <= 32.7944:
                                                                            return 2
                                                                        else:
                                                                            return 6
                                                                else:
                                                                    if f[23] <= 0.1777:
                                                                        return 5
                                                                    else:
                                                                        return 1
                                                            else:
                                                                if f[51] <= 57.4346:
                                                                    if f[62] <= 159.7228:
                                                                        if f[40] <= 0.4957:
                                                                            return 1
                                                                        else:
                                                                            if f[3] <= 0.0117:
                                                                                return 2
                                                                            else:
                                                                                return 2
                                                                    else:
                                                                        if f[51] <= 51.1191:
                                                                            if f[62] <= 193.2753:
                                                                                return 1
                                                                            else:
                                                                                return 4
                                                                        else:
                                                                            return 0
                                                                else:
                                                                    if f[39] <= 68.9339:
                                                                        if f[68] <= 32.2715:
                                                                            if f[37] <= 0.0193:
                                                                                return 2
                                                                            else:
                                                                                return 2
                                                                        else:
                                                                            if f[68] <= 39.7624:
                                                                                return 0
                                                                            else:
                                                                                return 2
                                                                    else:
                                                                        return 0
                                                else:
                                                    if f[4] <= 0.0034:
                                                        return 9
                                                    else:
                                                        if f[41] <= 1.5032:
                                                            return 5
                                                        else:
                                                            return 3
                                            else:
                                                return 7
                                        else:
                                            if f[17] <= 0.0144:
                                                return 8
                                            else:
                                                return 8
                                    else:
                                        if f[29] <= -33.2429:
                                            if f[6] <= 0.0251:
                                                return 6
                                            else:
                                                return 6
                                        else:
                                            if f[1] <= 28.3926:
                                                if f[60] <= 111.8143:
                                                    return 4
                                                else:
                                                    if f[20] <= 0.1458:
                                                        return 7
                                                    else:
                                                        return 7
                                            else:
                                                if f[25] <= 0.3398:
                                                    return 0
                                                else:
                                                    return 0
                                else:
                                    if f[10] <= 3204.7783:
                                        if f[63] <= 116.4911:
                                            if f[31] <= 0.0115:
                                                return 8
                                            else:
                                                return 1
                                        else:
                                            if f[50] <= 23.3117:
                                                return 4
                                            else:
                                                if f[2] <= 0.0325:
                                                    return 5
                                                else:
                                                    return 5
                                    else:
                                        if f[23] <= 0.0242:
                                            return 9
                                        else:
                                            if f[14] <= 0.7123:
                                                if f[8] <= 0.0799:
                                                    return 1
                                                else:
                                                    return 5
                                            else:
                                                return 2
                        else:
                            if f[9] <= 0.0132:
                                if f[32] <= 0.3962:
                                    if f[1] <= 27.5063:
                                        return 0
                                    else:
                                        return 5
                                else:
                                    return 4
                            else:
                                if f[22] <= 1.5982:
                                    if f[55] <= 94.8809:
                                        if f[26] <= 89.5008:
                                            return 7
                                        else:
                                            return 7
                                    else:
                                        if f[37] <= 0.0213:
                                            return 7
                                        else:
                                            return 2
                                else:
                                    if f[31] <= 0.0448:
                                        return 8
                                    else:
                                        return 4
                    else:
                        if f[1] <= 111.9783:
                            if f[29] <= -78.9763:
                                return 2
                            else:
                                if f[7] <= 123.0879:
                                    if f[4] <= 0.5258:
                                        if f[16] <= 0.6841:
                                            return 8
                                        else:
                                            if f[42] <= 1.2546:
                                                return 2
                                            else:
                                                return 4
                                    else:
                                        return 7
                                else:
                                    if f[18] <= 0.1579:
                                        if f[17] <= 0.8101:
                                            return 4
                                        else:
                                            return 1
                                    else:
                                        return 2
                        else:
                            return 5
                else:
                    if f[58] <= 18.5832:
                        if f[64] <= 119.231:
                            if f[54] <= 21.3965:
                                if f[31] <= 0.0:
                                    if f[44] <= 0.0368:
                                        return 4
                                    else:
                                        return 8
                                else:
                                    return 1
                            else:
                                return 6
                        else:
                            if f[4] <= 0.1604:
                                if f[36] <= 0.0182:
                                    return 7
                                else:
                                    if f[67] <= 149.1726:
                                        return 0
                                    else:
                                        return 0
                            else:
                                return 4
                    else:
                        if f[6] <= 0.0778:
                            if f[67] <= 37.9993:
                                if f[60] <= 163.8594:
                                    if f[41] <= 1.3344:
                                        if f[39] <= 12.2949:
                                            return 7
                                        else:
                                            return 0
                                    else:
                                        if f[18] <= 0.02:
                                            return 7
                                        else:
                                            return 7
                                else:
                                    return 6
                            else:
                                if f[15] <= 0.2251:
                                    if f[3] <= 0.0691:
                                        if f[53] <= 0.333:
                                            if f[62] <= 105.8966:
                                                return 6
                                            else:
                                                return 6
                                        else:
                                            if f[4] <= 0.0015:
                                                return 0
                                            else:
                                                if f[8] <= 0.074:
                                                    if f[19] <= 0.9515:
                                                        return 2
                                                    else:
                                                        return 6
                                                else:
                                                    return 1
                                    else:
                                        if f[65] <= 87.2954:
                                            if f[40] <= 0.4875:
                                                return 0
                                            else:
                                                return 0
                                        else:
                                            return 6
                                else:
                                    if f[23] <= 0.2806:
                                        if f[13] <= 54.8023:
                                            if f[2] <= 0.0048:
                                                if f[40] <= 0.3682:
                                                    return 1
                                                else:
                                                    return 8
                                            else:
                                                if f[0] <= 41.733:
                                                    return 0
                                                else:
                                                    if f[10] <= 4812.8426:
                                                        return 7
                                                    else:
                                                        return 7
                                        else:
                                            return 2
                                    else:
                                        if f[21] <= 46.27:
                                            if f[61] <= 0.2998:
                                                return 0
                                            else:
                                                return 0
                                        else:
                                            return 6
                        else:
                            if f[5] <= 0.1289:
                                if f[35] <= 0.0869:
                                    if f[42] <= 0.7766:
                                        return 2
                                    else:
                                        if f[56] <= 97.2422:
                                            return 6
                                        else:
                                            if f[41] <= 1.3453:
                                                return 0
                                            else:
                                                if f[61] <= 0.2994:
                                                    return 5
                                                else:
                                                    return 5
                                else:
                                    if f[62] <= 142.1425:
                                        if f[40] <= 0.3626:
                                            return 7
                                        else:
                                            if f[29] <= -31.0081:
                                                return 6
                                            else:
                                                if f[61] <= 0.3608:
                                                    if f[11] <= 60.3881:
                                                        return 8
                                                    else:
                                                        return 0
                                                else:
                                                    return 2
                                    else:
                                        if f[26] <= 65.6374:
                                            return 4
                                        else:
                                            if f[10] <= 7679.2917:
                                                return 1
                                            else:
                                                return 1
                            else:
                                if f[69] <= 0.3538:
                                    if f[43] <= 2.5334:
                                        if f[26] <= 57.0091:
                                            if f[11] <= 70.3659:
                                                return 0
                                            else:
                                                return 1
                                        else:
                                            if f[16] <= 0.9984:
                                                return 1
                                            else:
                                                return 1
                                    else:
                                        return 7
                                else:
                                    if f[55] <= 140.9109:
                                        if f[26] <= 81.4544:
                                            return 6
                                        else:
                                            return 4
                                    else:
                                        return 1
            else:
                if f[27] <= 181.3507:
                    if f[44] <= 0.4986:
                        if f[27] <= 142.4934:
                            if f[40] <= 0.6036:
                                if f[25] <= 0.2694:
                                    return 4
                                else:
                                    return 0
                            else:
                                return 2
                        else:
                            if f[11] <= 81.8723:
                                if f[60] <= 178.306:
                                    if f[52] <= 110.2979:
                                        return 5
                                    else:
                                        return 5
                                else:
                                    return 0
                            else:
                                return 4
                    else:
                        if f[59] <= 215.5867:
                            if f[52] <= 128.728:
                                return 4
                            else:
                                return 4
                        else:
                            if f[27] <= 167.6326:
                                return 4
                            else:
                                return 5
                else:
                    if f[10] <= 4346.6669:
                        return 5
                    else:
                        if f[30] <= 0.0625:
                            return 5
                        else:
                            return 4
        else:
            if f[17] <= 0.0759:
                if f[61] <= 0.334:
                    if f[69] <= 0.3668:
                        if f[41] <= 1.4559:
                            if f[13] <= 43.3022:
                                if f[69] <= 0.2976:
                                    return 2
                                else:
                                    return 0
                            else:
                                if f[51] <= 34.1104:
                                    return 9
                                else:
                                    return 9
                        else:
                            if f[39] <= 0.1555:
                                return 9
                            else:
                                if f[19] <= 0.9022:
                                    if f[63] <= 102.3787:
                                        if f[53] <= 0.315:
                                            return 9
                                        else:
                                            return 9
                                    else:
                                        return 9
                                else:
                                    return 9
                    else:
                        if f[2] <= 0.0435:
                            return 6
                        else:
                            return 7
                else:
                    if f[34] <= 0.6883:
                        return 1
                    else:
                        if f[61] <= 0.3648:
                            if f[6] <= 0.0291:
                                if f[20] <= 0.0387:
                                    return 0
                                else:
                                    if f[45] <= 0.0032:
                                        return 7
                                    else:
                                        return 7
                            else:
                                if f[70] <= 0.3544:
                                    if f[52] <= 138.5137:
                                        if f[47] <= 45.0439:
                                            return 2
                                        else:
                                            return 2
                                    else:
                                        return 9
                                else:
                                    return 1
                        else:
                            if f[20] <= 0.1156:
                                if f[68] <= 65.6805:
                                    return 4
                                else:
                                    return 7
                            else:
                                if f[30] <= 0.165:
                                    return 6
                                else:
                                    return 6
            else:
                if f[57] <= 0.3438:
                    if f[68] <= 19.7295:
                        if f[38] <= 0.0854:
                            if f[41] <= 1.3902:
                                return 1
                            else:
                                if f[69] <= 0.3348:
                                    return 1
                                else:
                                    return 3
                        else:
                            if f[49] <= 0.256:
                                return 2
                            else:
                                if f[24] <= 0.0463:
                                    return 5
                                else:
                                    return 6
                    else:
                        if f[26] <= 80.9504:
                            if f[0] <= 162.9045:
                                if f[40] <= 0.5124:
                                    return 0
                                else:
                                    if f[19] <= 0.5466:
                                        return 9
                                    else:
                                        if f[37] <= 0.0462:
                                            if f[35] <= 0.2588:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            if f[3] <= 0.0558:
                                                return 1
                                            else:
                                                return 5
                            else:
                                return 4
                        else:
                            if f[29] <= 11.5015:
                                if f[3] <= 0.0497:
                                    if f[47] <= 47.0908:
                                        if f[4] <= 0.0487:
                                            return 0
                                        else:
                                            return 3
                                    else:
                                        if f[7] <= 81.7742:
                                            return 9
                                        else:
                                            return 9
                                else:
                                    if f[23] <= 0.2676:
                                        if f[34] <= 1.1451:
                                            if f[61] <= 0.2021:
                                                return 2
                                            else:
                                                return 3
                                        else:
                                            return 0
                                    else:
                                        if f[9] <= 0.1074:
                                            if f[29] <= -37.5339:
                                                return 0
                                            else:
                                                return 3
                                        else:
                                            if f[5] <= 0.0048:
                                                return 6
                                            else:
                                                return 9
                            else:
                                if f[19] <= 0.9472:
                                    if f[27] <= 177.3732:
                                        if f[46] <= 35.8819:
                                            if f[69] <= 0.2478:
                                                return 2
                                            else:
                                                return 0
                                        else:
                                            if f[28] <= 1.013:
                                                return 3
                                            else:
                                                if f[23] <= 0.1474:
                                                    return 9
                                                else:
                                                    return 2
                                    else:
                                        if f[10] <= 12230.2425:
                                            return 3
                                        else:
                                            return 3
                                else:
                                    if f[0] <= 95.5818:
                                        return 7
                                    else:
                                        return 1
                else:
                    if f[55] <= 163.9316:
                        if f[43] <= 1.9576:
                            if f[25] <= 0.3408:
                                if f[64] <= 89.9347:
                                    return 1
                                else:
                                    return 0
                            else:
                                if f[31] <= 0.1721:
                                    if f[6] <= 0.0191:
                                        return 6
                                    else:
                                        return 6
                                else:
                                    return 3
                        else:
                            if f[60] <= 116.5999:
                                if f[29] <= -16.7683:
                                    if f[51] <= 37.5254:
                                        return 3
                                    else:
                                        return 6
                                else:
                                    if f[45] <= 0.2507:
                                        if f[37] <= 0.0555:
                                            if f[20] <= 0.0357:
                                                return 1
                                            else:
                                                return 1
                                        else:
                                            return 1
                                    else:
                                        return 0
                            else:
                                if f[70] <= 0.3852:
                                    if f[18] <= 0.2053:
                                        if f[44] <= 0.2839:
                                            if f[34] <= 0.8037:
                                                return 1
                                            else:
                                                if f[67] <= 81.9205:
                                                    return 0
                                                else:
                                                    return 0
                                        else:
                                            if f[27] <= 158.3681:
                                                if f[10] <= 15424.8348:
                                                    if f[7] <= 79.8154:
                                                        return 6
                                                    else:
                                                        return 0
                                                else:
                                                    return 1
                                            else:
                                                return 3
                                    else:
                                        return 4
                                else:
                                    return 6
                    else:
                        if f[37] <= 0.0106:
                            return 1
                        else:
                            return 1
    else:
        if f[2] <= 0.5179:
            if f[11] <= 70.2368:
                if f[68] <= 51.3164:
                    return 8
                else:
                    if f[35] <= 0.2256:
                        return 0
                    else:
                        return 6
            else:
                if f[51] <= 132.0879:
                    if f[67] <= 97.4922:
                        return 3
                    else:
                        if f[14] <= 0.6204:
                            return 9
                        else:
                            return 9
                else:
                    return 3
        else:
            if f[67] <= 120.7283:
                if f[11] <= 55.2029:
                    if f[30] <= 0.0141:
                        return 7
                    else:
                        return 4
                else:
                    return 8
            else:
                if f[57] <= 0.3184:
                    return 8
                else:
                    return 6


def _tree_5(f):
    if f[1] <= -20.9628:
        if f[70] <= 0.2392:
            if f[29] <= -38.9954:
                return 8
            else:
                if f[36] <= 0.2739:
                    return 8
                else:
                    return 8
        else:
            if f[6] <= 0.2409:
                if f[18] <= 0.0129:
                    if f[42] <= 1.055:
                        if f[39] <= 16.2168:
                            if f[44] <= 0.0033:
                                return 7
                            else:
                                return 7
                        else:
                            return 2
                    else:
                        return 9
                else:
                    if f[62] <= 193.7604:
                        return 0
                    else:
                        return 6
            else:
                if f[15] <= 0.0425:
                    if f[41] <= 1.5357:
                        return 8
                    else:
                        return 8
                else:
                    return 8
    else:
        if f[11] <= 85.6893:
            if f[6] <= 0.1318:
                if f[68] <= 42.5539:
                    if f[34] <= 1.1453:
                        if f[49] <= 0.3145:
                            if f[4] <= 0.071:
                                if f[25] <= 0.2681:
                                    return 6
                                else:
                                    if f[26] <= 67.7769:
                                        if f[10] <= 3704.7589:
                                            if f[35] <= 0.0391:
                                                return 0
                                            else:
                                                return 0
                                        else:
                                            if f[57] <= 0.3004:
                                                return 3
                                            else:
                                                return 0
                                    else:
                                        if f[48] <= 143.6002:
                                            if f[40] <= 0.4577:
                                                return 0
                                            else:
                                                return 0
                                        else:
                                            return 6
                            else:
                                if f[5] <= 0.3278:
                                    if f[4] <= 0.1255:
                                        return 2
                                    else:
                                        if f[60] <= 144.1055:
                                            return 0
                                        else:
                                            return 4
                                else:
                                    return 1
                        else:
                            if f[64] <= 139.7955:
                                if f[66] <= 50.0804:
                                    return 1
                                else:
                                    if f[0] <= 112.0153:
                                        if f[69] <= 0.3229:
                                            return 6
                                        else:
                                            return 6
                                    else:
                                        return 7
                            else:
                                if f[20] <= 0.1098:
                                    return 9
                                else:
                                    return 0
                    else:
                        if f[37] <= 0.0:
                            return 4
                        else:
                            if f[48] <= 122.3027:
                                if f[40] <= 0.5125:
                                    if f[9] <= 0.2693:
                                        return 7
                                    else:
                                        return 7
                                else:
                                    if f[62] <= 71.006:
                                        return 2
                                    else:
                                        return 8
                            else:
                                if f[28] <= 1.1484:
                                    if f[21] <= 66.9133:
                                        if f[5] <= 0.0072:
                                            if f[46] <= 29.7188:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            if f[66] <= 80.0819:
                                                return 9
                                            else:
                                                return 0
                                    else:
                                        if f[39] <= 16.0205:
                                            return 3
                                        else:
                                            return 3
                                else:
                                    return 0
                else:
                    if f[31] <= 0.0022:
                        if f[61] <= 0.2715:
                            if f[40] <= 0.3733:
                                if f[35] <= 0.7988:
                                    return 8
                                else:
                                    return 7
                            else:
                                if f[21] <= -7.5137:
                                    return 2
                                else:
                                    if f[7] <= 71.1949:
                                        if f[65] <= 28.4918:
                                            if f[22] <= 0.9846:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            return 1
                                    else:
                                        if f[60] <= 81.4355:
                                            return 9
                                        else:
                                            return 5
                        else:
                            if f[35] <= 0.4951:
                                if f[63] <= 118.2074:
                                    return 6
                                else:
                                    return 6
                            else:
                                if f[44] <= 0.2576:
                                    if f[17] <= 0.0115:
                                        if f[54] <= 60.1562:
                                            return 1
                                        else:
                                            return 7
                                    else:
                                        if f[25] <= 0.3047:
                                            return 0
                                        else:
                                            if f[20] <= 0.1491:
                                                return 6
                                            else:
                                                return 6
                                else:
                                    return 2
                    else:
                        if f[2] <= 0.0:
                            if f[53] <= 0.2998:
                                if f[14] <= 0.6847:
                                    if f[18] <= 0.0012:
                                        return 8
                                    else:
                                        return 4
                                else:
                                    if f[5] <= 0.0325:
                                        return 2
                                    else:
                                        return 2
                            else:
                                return 6
                        else:
                            if f[28] <= 1.0762:
                                if f[2] <= 0.2038:
                                    if f[9] <= 0.0198:
                                        return 7
                                    else:
                                        if f[30] <= 0.3881:
                                            return 7
                                        else:
                                            if f[6] <= 0.0716:
                                                return 7
                                            else:
                                                return 7
                                else:
                                    return 8
                            else:
                                return 4
            else:
                if f[31] <= 0.1384:
                    if f[1] <= 99.3196:
                        if f[34] <= 1.0362:
                            if f[26] <= 71.3128:
                                if f[4] <= 0.1345:
                                    if f[68] <= 35.4623:
                                        if f[20] <= 0.5577:
                                            return 0
                                        else:
                                            return 1
                                    else:
                                        return 2
                                else:
                                    if f[12] <= 44.1647:
                                        return 4
                                    else:
                                        return 1
                            else:
                                if f[25] <= 0.3604:
                                    if f[67] <= 123.7294:
                                        return 1
                                    else:
                                        if f[39] <= 13.0155:
                                            return 1
                                        else:
                                            return 1
                                else:
                                    return 6
                        else:
                            if f[16] <= 0.2473:
                                if f[65] <= 140.1629:
                                    return 8
                                else:
                                    return 8
                            else:
                                if f[43] <= 1.7798:
                                    if f[19] <= 0.9318:
                                        if f[17] <= 0.1765:
                                            return 2
                                        else:
                                            if f[11] <= 79.9573:
                                                if f[10] <= 2159.2775:
                                                    return 4
                                                else:
                                                    if f[51] <= 140.5913:
                                                        return 2
                                                    else:
                                                        return 0
                                            else:
                                                return 3
                                    else:
                                        if f[23] <= 0.3267:
                                            return 5
                                        else:
                                            if f[63] <= 126.7426:
                                                return 0
                                            else:
                                                return 0
                                else:
                                    if f[62] <= 80.6049:
                                        if f[18] <= 0.0405:
                                            return 1
                                        else:
                                            if f[51] <= 194.5742:
                                                if f[49] <= 0.2342:
                                                    if f[18] <= 0.2975:
                                                        return 2
                                                    else:
                                                        return 2
                                                else:
                                                    return 8
                                            else:
                                                if f[41] <= 1.575:
                                                    return 5
                                                else:
                                                    return 9
                                    else:
                                        if f[66] <= 91.6048:
                                            return 2
                                        else:
                                            if f[11] <= 72.6433:
                                                if f[18] <= 0.1369:
                                                    return 5
                                                else:
                                                    return 5
                                            else:
                                                return 5
                    else:
                        if f[31] <= 0.0015:
                            if f[52] <= 192.1895:
                                return 0
                            else:
                                return 5
                        else:
                            if f[53] <= 0.1564:
                                return 4
                            else:
                                return 5
                else:
                    if f[1] <= 113.24:
                        if f[70] <= 0.2749:
                            if f[18] <= 0.2371:
                                if f[40] <= 0.5354:
                                    return 4
                                else:
                                    if f[13] <= 7.0084:
                                        if f[49] <= 0.1393:
                                            return 4
                                        else:
                                            return 4
                                    else:
                                        if f[41] <= 2.2154:
                                            return 1
                                        else:
                                            return 4
                            else:
                                if f[44] <= 0.3928:
                                    return 4
                                else:
                                    return 2
                        else:
                            if f[28] <= 1.3733:
                                if f[61] <= 0.3135:
                                    if f[12] <= 37.9867:
                                        return 2
                                    else:
                                        return 5
                                else:
                                    if f[25] <= 0.3435:
                                        return 4
                                    else:
                                        return 1
                            else:
                                return 0
                    else:
                        if f[31] <= 0.5679:
                            if f[68] <= 15.6699:
                                return 4
                            else:
                                if f[45] <= 0.5801:
                                    return 4
                                else:
                                    if f[7] <= 212.0522:
                                        return 5
                                    else:
                                        return 5
                        else:
                            return 4
        else:
            if f[70] <= 0.3587:
                if f[3] <= 0.0382:
                    if f[61] <= 0.3359:
                        if f[40] <= 0.5209:
                            if f[40] <= 0.4553:
                                return 7
                            else:
                                if f[53] <= 0.3076:
                                    return 3
                                else:
                                    return 0
                        else:
                            if f[24] <= 0.1377:
                                if f[53] <= 0.3145:
                                    if f[22] <= 0.988:
                                        if f[69] <= 0.1436:
                                            return 9
                                        else:
                                            return 7
                                    else:
                                        if f[37] <= 0.0768:
                                            return 0
                                        else:
                                            return 2
                                else:
                                    if f[29] <= -15.0896:
                                        return 9
                                    else:
                                        return 9
                            else:
                                if f[70] <= 0.3239:
                                    if f[6] <= 0.0128:
                                        return 9
                                    else:
                                        return 9
                                else:
                                    return 9
                    else:
                        if f[69] <= 0.3512:
                            if f[58] <= 67.0029:
                                if f[68] <= 36.1396:
                                    if f[29] <= -0.2681:
                                        return 4
                                    else:
                                        return 0
                                else:
                                    if f[26] <= 82.7691:
                                        return 2
                                    else:
                                        return 7
                            else:
                                return 9
                        else:
                            if f[38] <= 0.6179:
                                if f[43] <= 1.9678:
                                    return 1
                                else:
                                    return 6
                            else:
                                return 7
                else:
                    if f[46] <= 34.2446:
                        if f[6] <= 0.2725:
                            if f[11] <= 117.9724:
                                if f[53] <= 0.3439:
                                    if f[4] <= 0.021:
                                        if f[65] <= 82.8653:
                                            return 0
                                        else:
                                            return 0
                                    else:
                                        if f[65] <= 127.4159:
                                            if f[6] <= 0.2009:
                                                if f[14] <= 0.5536:
                                                    return 4
                                                else:
                                                    return 3
                                            else:
                                                return 9
                                        else:
                                            return 2
                                else:
                                    if f[11] <= 101.522:
                                        if f[63] <= 96.1287:
                                            return 6
                                        else:
                                            return 6
                                    else:
                                        return 0
                            else:
                                if f[65] <= 84.8795:
                                    return 3
                                else:
                                    return 3
                        else:
                            if f[39] <= 54.9629:
                                if f[44] <= 0.3345:
                                    if f[23] <= 0.0918:
                                        return 9
                                    else:
                                        return 9
                                else:
                                    if f[15] <= 0.0093:
                                        if f[52] <= 161.752:
                                            return 4
                                        else:
                                            return 4
                                    else:
                                        if f[33] <= 0.1901:
                                            return 5
                                        else:
                                            return 2
                            else:
                                if f[40] <= 0.55:
                                    return 8
                                else:
                                    if f[63] <= 148.1646:
                                        return 1
                                    else:
                                        return 1
                    else:
                        if f[62] <= 152.1007:
                            if f[63] <= 128.0439:
                                if f[13] <= 51.1857:
                                    if f[50] <= 34.3625:
                                        return 9
                                    else:
                                        if f[38] <= 0.3612:
                                            if f[35] <= 0.1116:
                                                return 3
                                            else:
                                                return 3
                                        else:
                                            return 3
                                else:
                                    if f[4] <= 0.0132:
                                        return 6
                                    else:
                                        return 9
                            else:
                                if f[19] <= 0.742:
                                    if f[29] <= -6.4166:
                                        if f[7] <= 110.0664:
                                            return 2
                                        else:
                                            return 3
                                    else:
                                        if f[37] <= 0.1074:
                                            if f[59] <= 69.9336:
                                                return 9
                                            else:
                                                return 9
                                        else:
                                            return 3
                                else:
                                    if f[7] <= 91.0433:
                                        if f[9] <= 0.1501:
                                            return 0
                                        else:
                                            return 0
                                    else:
                                        if f[9] <= 0.1156:
                                            return 1
                                        else:
                                            if f[25] <= 0.2893:
                                                return 9
                                            else:
                                                return 3
                        else:
                            if f[2] <= 0.0034:
                                if f[63] <= 117.9888:
                                    return 6
                                else:
                                    if f[66] <= 82.9234:
                                        return 2
                                    else:
                                        if f[19] <= 0.6792:
                                            return 3
                                        else:
                                            return 0
                            else:
                                if f[39] <= 82.6282:
                                    if f[56] <= 152.9147:
                                        if f[6] <= 0.0514:
                                            return 3
                                        else:
                                            if f[25] <= 0.3576:
                                                return 3
                                            else:
                                                return 3
                                    else:
                                        return 0
                                else:
                                    return 6
            else:
                if f[6] <= 0.3839:
                    if f[29] <= 7.4053:
                        if f[11] <= 116.9282:
                            if f[41] <= 1.6887:
                                if f[62] <= 170.4792:
                                    if f[24] <= 0.2964:
                                        return 6
                                    else:
                                        return 3
                                else:
                                    return 0
                            else:
                                if f[65] <= 43.2359:
                                    return 7
                                else:
                                    if f[23] <= 0.1267:
                                        return 0
                                    else:
                                        return 1
                        else:
                            if f[69] <= 0.3555:
                                if f[31] <= 0.0156:
                                    return 1
                                else:
                                    if f[31] <= 0.0234:
                                        return 3
                                    else:
                                        return 3
                            else:
                                if f[41] <= 1.5919:
                                    return 6
                                else:
                                    return 9
                    else:
                        if f[11] <= 94.4271:
                            if f[54] <= 31.3422:
                                return 0
                            else:
                                if f[11] <= 90.2522:
                                    return 3
                                else:
                                    return 1
                        else:
                            if f[26] <= 111.6121:
                                if f[14] <= 0.6377:
                                    if f[43] <= 2.2204:
                                        return 6
                                    else:
                                        return 1
                                else:
                                    if f[63] <= 126.1034:
                                        return 1
                                    else:
                                        return 1
                            else:
                                if f[6] <= 0.2634:
                                    if f[53] <= 0.3506:
                                        return 1
                                    else:
                                        return 1
                                else:
                                    return 4
                else:
                    if f[56] <= 111.7861:
                        return 1
                    else:
                        return 4


def _tree_6(f):
    if f[22] <= 0.5197:
        if f[58] <= 100.3127:
            if f[62] <= 130.8555:
                return 7
            else:
                if f[56] <= 188.1707:
                    return 8
                else:
                    return 8
        else:
            return 8
    else:
        if f[7] <= 170.333:
            if f[19] <= 0.7034:
                if f[45] <= 0.0293:
                    if f[11] <= 110.5366:
                        if f[23] <= 0.0232:
                            if f[28] <= 0.9388:
                                if f[19] <= 0.5738:
                                    return 7
                                else:
                                    return 2
                            else:
                                if f[57] <= 0.176:
                                    return 9
                                else:
                                    return 9
                        else:
                            if f[6] <= 0.0313:
                                if f[47] <= 39.3376:
                                    return 7
                                else:
                                    if f[15] <= 0.2663:
                                        return 6
                                    else:
                                        return 6
                            else:
                                if f[67] <= 71.224:
                                    return 2
                                else:
                                    return 1
                    else:
                        return 9
                else:
                    if f[11] <= 91.3672:
                        if f[52] <= 111.252:
                            if f[55] <= 61.9248:
                                return 3
                            else:
                                return 2
                        else:
                            if f[23] <= 0.6458:
                                if f[43] <= 0.8832:
                                    return 4
                                else:
                                    if f[66] <= 164.4427:
                                        if f[57] <= 0.1892:
                                            if f[12] <= 52.5303:
                                                return 4
                                            else:
                                                return 7
                                        else:
                                            if f[46] <= 62.7842:
                                                if f[44] <= 0.3568:
                                                    return 0
                                                else:
                                                    if f[12] <= 45.5128:
                                                        return 9
                                                    else:
                                                        return 1
                                            else:
                                                if f[3] <= 0.0125:
                                                    return 2
                                                else:
                                                    return 3
                                    else:
                                        return 5
                            else:
                                return 2
                    else:
                        if f[62] <= 198.7469:
                            if f[16] <= 0.955:
                                if f[66] <= 101.125:
                                    if f[60] <= 141.9197:
                                        if f[57] <= 0.3291:
                                            if f[48] <= 122.1186:
                                                if f[6] <= 0.1317:
                                                    return 3
                                                else:
                                                    return 9
                                            else:
                                                return 9
                                        else:
                                            if f[4] <= 0.0237:
                                                return 1
                                            else:
                                                return 3
                                    else:
                                        if f[60] <= 169.0234:
                                            if f[24] <= 0.1473:
                                                return 2
                                            else:
                                                return 9
                                        else:
                                            return 3
                                else:
                                    if f[28] <= 1.1506:
                                        if f[57] <= 0.1841:
                                            return 9
                                        else:
                                            if f[43] <= 1.9764:
                                                return 1
                                            else:
                                                if f[5] <= 0.2173:
                                                    return 3
                                                else:
                                                    if f[16] <= 0.6592:
                                                        return 3
                                                    else:
                                                        return 3
                                    else:
                                        if f[3] <= 0.3098:
                                            if f[42] <= 1.0917:
                                                return 9
                                            else:
                                                return 9
                                        else:
                                            return 3
                            else:
                                if f[25] <= 0.3271:
                                    return 7
                                else:
                                    return 6
                        else:
                            if f[29] <= -15.7139:
                                return 3
                            else:
                                return 3
            else:
                if f[57] <= 0.3357:
                    if f[45] <= 0.189:
                        if f[22] <= 0.6375:
                            if f[41] <= 1.8927:
                                return 8
                            else:
                                return 8
                        else:
                            if f[31] <= 0.004:
                                if f[33] <= 0.1855:
                                    if f[57] <= 0.3076:
                                        if f[11] <= 106.293:
                                            if f[30] <= 0.5176:
                                                if f[65] <= 42.9167:
                                                    return 6
                                                else:
                                                    return 6
                                            else:
                                                if f[32] <= 0.093:
                                                    return 8
                                                else:
                                                    return 1
                                        else:
                                            return 9
                                    else:
                                        if f[5] <= 0.0169:
                                            if f[7] <= 55.4404:
                                                return 7
                                            else:
                                                return 2
                                        else:
                                            if f[57] <= 0.3168:
                                                return 0
                                            else:
                                                return 0
                                else:
                                    if f[22] <= 0.9741:
                                        if f[39] <= 7.0109:
                                            if f[70] <= 0.1612:
                                                return 6
                                            else:
                                                return 7
                                        else:
                                            if f[33] <= 0.2817:
                                                return 2
                                            else:
                                                if f[1] <= -20.1631:
                                                    return 8
                                                else:
                                                    return 8
                                    else:
                                        if f[66] <= 56.0145:
                                            if f[40] <= 0.4835:
                                                if f[48] <= 210.9907:
                                                    if f[43] <= 1.3928:
                                                        return 7
                                                    else:
                                                        return 1
                                                else:
                                                    return 2
                                            else:
                                                if f[16] <= 0.9898:
                                                    return 2
                                                else:
                                                    return 2
                                        else:
                                            if f[41] <= 2.4356:
                                                if f[46] <= 20.0439:
                                                    return 2
                                                else:
                                                    if f[29] <= 19.6383:
                                                        if f[3] <= 0.0703:
                                                            if f[2] <= 0.02:
                                                                return 9
                                                            else:
                                                                return 2
                                                        else:
                                                            return 5
                                                    else:
                                                        if f[15] <= 0.2475:
                                                            if f[44] <= 0.0473:
                                                                return 8
                                                            else:
                                                                return 7
                                                        else:
                                                            return 0
                                            else:
                                                if f[38] <= 0.3384:
                                                    return 6
                                                else:
                                                    return 6
                            else:
                                if f[19] <= 1.1706:
                                    if f[4] <= 0.0276:
                                        if f[64] <= 124.8207:
                                            return 9
                                        else:
                                            if f[13] <= 51.1687:
                                                return 7
                                            else:
                                                return 2
                                    else:
                                        if f[0] <= 46.9317:
                                            if f[54] <= 32.7139:
                                                return 4
                                            else:
                                                if f[70] <= 0.2308:
                                                    return 7
                                                else:
                                                    return 7
                                        else:
                                            if f[10] <= 8327.8821:
                                                if f[20] <= 0.0899:
                                                    if f[59] <= 53.1162:
                                                        return 4
                                                    else:
                                                        return 3
                                                else:
                                                    if f[42] <= 1.0554:
                                                        if f[40] <= 0.4999:
                                                            return 6
                                                        else:
                                                            return 6
                                                    else:
                                                        if f[55] <= 84.333:
                                                            return 0
                                                        else:
                                                            if f[17] <= 0.1326:
                                                                return 8
                                                            else:
                                                                return 4
                                            else:
                                                if f[19] <= 0.9638:
                                                    if f[52] <= 125.3643:
                                                        return 9
                                                    else:
                                                        return 3
                                                else:
                                                    return 2
                                else:
                                    if f[7] <= 106.0957:
                                        if f[31] <= 0.0048:
                                            return 7
                                        else:
                                            return 7
                                    else:
                                        return 4
                    else:
                        if f[31] <= 0.0925:
                            if f[4] <= 0.0105:
                                if f[55] <= 144.1952:
                                    if f[9] <= 0.0004:
                                        return 2
                                    else:
                                        if f[1] <= 65.5251:
                                            if f[54] <= 58.8535:
                                                if f[60] <= 94.376:
                                                    return 0
                                                else:
                                                    return 0
                                            else:
                                                return 0
                                        else:
                                            return 1
                                else:
                                    if f[54] <= 11.835:
                                        return 2
                                    else:
                                        return 9
                            else:
                                if f[33] <= 0.291:
                                    if f[63] <= 119.8456:
                                        if f[20] <= 0.1211:
                                            return 6
                                        else:
                                            return 6
                                    else:
                                        if f[15] <= 0.3032:
                                            if f[26] <= 77.443:
                                                if f[1] <= 66.5535:
                                                    if f[17] <= 0.5881:
                                                        return 0
                                                    else:
                                                        return 0
                                                else:
                                                    return 1
                                            else:
                                                if f[16] <= 0.9684:
                                                    if f[4] <= 0.0664:
                                                        return 3
                                                    else:
                                                        return 3
                                                else:
                                                    return 1
                                        else:
                                            return 2
                                else:
                                    if f[67] <= 107.0017:
                                        return 3
                                    else:
                                        if f[52] <= 163.7207:
                                            if f[10] <= 5588.4496:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            return 8
                        else:
                            if f[11] <= 90.0054:
                                if f[62] <= 153.9033:
                                    if f[62] <= 132.546:
                                        if f[43] <= 1.7476:
                                            if f[52] <= 126.9932:
                                                return 7
                                            else:
                                                return 2
                                        else:
                                            return 4
                                    else:
                                        if f[32] <= 0.2285:
                                            return 0
                                        else:
                                            return 5
                                else:
                                    if f[28] <= 1.0087:
                                        return 2
                                    else:
                                        if f[9] <= 0.0:
                                            return 2
                                        else:
                                            return 4
                            else:
                                if f[68] <= 26.834:
                                    return 5
                                else:
                                    if f[38] <= 0.054:
                                        return 4
                                    else:
                                        if f[59] <= 135.6592:
                                            return 3
                                        else:
                                            return 3
                else:
                    if f[64] <= 106.3764:
                        if f[39] <= 39.6369:
                            if f[66] <= 93.3214:
                                if f[68] <= 75.7812:
                                    if f[40] <= 0.3682:
                                        return 1
                                    else:
                                        if f[51] <= 53.5176:
                                            if f[65] <= 39.0653:
                                                return 6
                                            else:
                                                return 0
                                        else:
                                            return 6
                                else:
                                    if f[27] <= 122.2473:
                                        return 7
                                    else:
                                        return 0
                            else:
                                if f[32] <= 0.032:
                                    return 3
                                else:
                                    if f[46] <= 26.9473:
                                        if f[8] <= 0.0122:
                                            return 6
                                        else:
                                            return 6
                                    else:
                                        if f[12] <= 45.2517:
                                            return 3
                                        else:
                                            if f[3] <= 0.1968:
                                                return 1
                                            else:
                                                return 1
                        else:
                            if f[64] <= 96.6342:
                                if f[62] <= 164.6027:
                                    if f[33] <= 0.1552:
                                        return 1
                                    else:
                                        return 1
                                else:
                                    return 0
                            else:
                                if f[54] <= 55.7648:
                                    return 0
                                else:
                                    return 7
                    else:
                        if f[68] <= 22.1475:
                            if f[60] <= 128.6318:
                                if f[12] <= 54.6206:
                                    if f[8] <= 0.0557:
                                        return 1
                                    else:
                                        return 0
                                else:
                                    if f[42] <= 0.9764:
                                        return 6
                                    else:
                                        return 6
                            else:
                                if f[19] <= 0.8752:
                                    if f[63] <= 172.1168:
                                        return 4
                                    else:
                                        return 0
                                else:
                                    if f[23] <= 0.2446:
                                        return 1
                                    else:
                                        if f[43] <= 0.4829:
                                            return 0
                                        else:
                                            return 0
                        else:
                            if f[40] <= 0.4608:
                                if f[63] <= 155.9807:
                                    if f[34] <= 0.8163:
                                        return 6
                                    else:
                                        if f[39] <= 19.4717:
                                            return 7
                                        else:
                                            return 7
                                else:
                                    return 0
                            else:
                                if f[29] <= 0.8981:
                                    if f[21] <= 13.2988:
                                        if f[26] <= 134.6703:
                                            if f[18] <= 0.1811:
                                                if f[63] <= 133.0555:
                                                    return 6
                                                else:
                                                    return 6
                                            else:
                                                return 0
                                        else:
                                            return 9
                                    else:
                                        if f[20] <= 0.2113:
                                            if f[45] <= 0.0425:
                                                return 7
                                            else:
                                                if f[24] <= 0.2223:
                                                    return 1
                                                else:
                                                    return 3
                                        else:
                                            return 6
                                else:
                                    if f[9] <= 0.009:
                                        if f[19] <= 0.8537:
                                            if f[29] <= 17.521:
                                                return 6
                                            else:
                                                return 2
                                        else:
                                            if f[62] <= 154.1555:
                                                return 0
                                            else:
                                                return 8
                                    else:
                                        if f[30] <= 0.177:
                                            if f[31] <= 0.0109:
                                                if f[22] <= 1.078:
                                                    return 0
                                                else:
                                                    return 0
                                            else:
                                                return 1
                                        else:
                                            if f[2] <= 0.1279:
                                                if f[32] <= 0.048:
                                                    if f[36] <= 0.2141:
                                                        return 1
                                                    else:
                                                        return 1
                                                else:
                                                    if f[46] <= 46.3916:
                                                        if f[33] <= 0.0667:
                                                            return 3
                                                        else:
                                                            return 2
                                                    else:
                                                        return 7
                                            else:
                                                return 3
        else:
            if f[31] <= 0.2989:
                if f[27] <= 163.2953:
                    if f[70] <= 0.348:
                        if f[26] <= 87.7063:
                            if f[39] <= 23.9357:
                                if f[48] <= 85.5074:
                                    return 1
                                else:
                                    if f[25] <= 0.3096:
                                        return 4
                                    else:
                                        return 0
                            else:
                                if f[6] <= 0.436:
                                    if f[64] <= 56.2358:
                                        return 1
                                    else:
                                        if f[3] <= 0.4216:
                                            return 2
                                        else:
                                            return 0
                                else:
                                    if f[16] <= 0.6229:
                                        return 8
                                    else:
                                        if f[7] <= 192.5703:
                                            return 4
                                        else:
                                            if f[57] <= 0.3104:
                                                if f[18] <= 0.3469:
                                                    return 5
                                                else:
                                                    return 5
                                            else:
                                                return 0
                        else:
                            if f[68] <= 45.708:
                                if f[13] <= 23.8889:
                                    return 1
                                else:
                                    if f[14] <= 0.5703:
                                        return 3
                                    else:
                                        return 3
                            else:
                                if f[17] <= 0.0388:
                                    return 9
                                else:
                                    return 7
                    else:
                        if f[38] <= 0.0229:
                            return 1
                        else:
                            return 4
                else:
                    if f[10] <= 5145.0978:
                        if f[48] <= 135.1555:
                            if f[49] <= 0.1641:
                                return 5
                            else:
                                return 4
                        else:
                            if f[28] <= 1.1585:
                                return 1
                            else:
                                return 5
                    else:
                        if f[51] <= 143.51:
                            if f[17] <= 0.1294:
                                return 9
                            else:
                                return 3
                        else:
                            if f[0] <= 170.9319:
                                if f[16] <= 0.9166:
                                    return 5
                                else:
                                    return 5
                            else:
                                if f[56] <= 120.7322:
                                    return 1
                                else:
                                    if f[42] <= 1.0538:
                                        return 4
                                    else:
                                        return 8
            else:
                if f[64] <= 187.3913:
                    if f[61] <= 0.3238:
                        if f[26] <= 69.7194:
                            if f[66] <= 232.1981:
                                return 4
                            else:
                                return 4
                        else:
                            return 4
                    else:
                        if f[30] <= 0.1035:
                            return 5
                        else:
                            return 1
                else:
                    return 5


def _tree_7(f):
    if f[1] <= -57.2175:
        if f[11] <= 61.4407:
            return 8
        else:
            if f[6] <= 0.3672:
                return 7
            else:
                return 8
    else:
        if f[7] <= 170.6609:
            if f[19] <= 0.6816:
                if f[17] <= 0.0664:
                    if f[10] <= 5910.1215:
                        if f[2] <= 0.187:
                            if f[7] <= 36.5283:
                                return 7
                            else:
                                if f[48] <= 140.5861:
                                    return 2
                                else:
                                    return 3
                        else:
                            if f[37] <= 0.0027:
                                return 8
                            else:
                                return 8
                    else:
                        if f[25] <= 0.3449:
                            if f[56] <= 177.793:
                                return 9
                            else:
                                return 0
                        else:
                            if f[52] <= 97.5303:
                                if f[42] <= 0.9701:
                                    return 6
                                else:
                                    return 0
                            else:
                                if f[20] <= 0.0857:
                                    return 9
                                else:
                                    return 2
                else:
                    if f[13] <= 25.938:
                        if f[56] <= 104.0273:
                            if f[61] <= 0.3281:
                                return 1
                            else:
                                return 1
                        else:
                            if f[67] <= 144.9906:
                                if f[68] <= 21.5508:
                                    if f[19] <= 0.5916:
                                        return 0
                                    else:
                                        if f[68] <= 15.2051:
                                            return 2
                                        else:
                                            return 2
                                else:
                                    if f[44] <= 0.2161:
                                        return 9
                                    else:
                                        if f[26] <= 68.7526:
                                            return 4
                                        else:
                                            if f[27] <= 129.8173:
                                                return 3
                                            else:
                                                return 3
                            else:
                                if f[24] <= 0.0127:
                                    return 4
                                else:
                                    return 4
                    else:
                        if f[34] <= 1.1482:
                            if f[13] <= 52.1321:
                                if f[26] <= 93.655:
                                    if f[62] <= 192.3527:
                                        if f[11] <= 111.716:
                                            return 6
                                        else:
                                            return 9
                                    else:
                                        return 3
                                else:
                                    if f[69] <= 0.3534:
                                        if f[3] <= 0.0877:
                                            if f[64] <= 96.7642:
                                                return 3
                                            else:
                                                return 3
                                        else:
                                            return 3
                                    else:
                                        return 3
                            else:
                                if f[70] <= 0.2736:
                                    return 9
                                else:
                                    return 3
                        else:
                            if f[56] <= 100.4121:
                                if f[4] <= 0.0144:
                                    return 2
                                else:
                                    return 9
                            else:
                                if f[13] <= 46.9274:
                                    if f[37] <= 0.0131:
                                        return 9
                                    else:
                                        if f[31] <= 0.0012:
                                            return 0
                                        else:
                                            return 3
                                else:
                                    if f[58] <= 75.1899:
                                        return 2
                                    else:
                                        return 4
            else:
                if f[40] <= 0.3955:
                    if f[66] <= 85.5487:
                        if f[3] <= 0.04:
                            if f[12] <= 72.4003:
                                if f[25] <= 0.3369:
                                    return 7
                                else:
                                    if f[59] <= 41.0274:
                                        return 7
                                    else:
                                        return 1
                            else:
                                return 7
                        else:
                            if f[5] <= 0.0015:
                                if f[31] <= 0.0022:
                                    return 0
                                else:
                                    return 0
                            else:
                                if f[1] <= 9.7959:
                                    return 1
                                else:
                                    return 7
                    else:
                        if f[61] <= 0.2939:
                            if f[24] <= 0.0249:
                                return 4
                            else:
                                if f[2] <= 0.0249:
                                    if f[54] <= 58.7391:
                                        return 7
                                    else:
                                        return 7
                                else:
                                    if f[36] <= 0.1829:
                                        return 8
                                    else:
                                        return 2
                        else:
                            if f[69] <= 0.3452:
                                if f[32] <= 0.1433:
                                    if f[34] <= 0.9003:
                                        return 0
                                    else:
                                        return 0
                                else:
                                    return 4
                            else:
                                if f[41] <= 1.4737:
                                    return 1
                                else:
                                    return 6
                else:
                    if f[33] <= 0.1541:
                        if f[29] <= 5.5942:
                            if f[11] <= 116.8461:
                                if f[55] <= 29.1594:
                                    if f[58] <= 28.0352:
                                        return 0
                                    else:
                                        if f[30] <= 0.1191:
                                            return 6
                                        else:
                                            return 7
                                else:
                                    if f[63] <= 118.5051:
                                        if f[63] <= 115.9085:
                                            if f[55] <= 41.9869:
                                                return 6
                                            else:
                                                return 6
                                        else:
                                            return 9
                                    else:
                                        if f[19] <= 1.0273:
                                            if f[67] <= 139.045:
                                                if f[24] <= 0.2842:
                                                    if f[46] <= 29.0332:
                                                        return 0
                                                    else:
                                                        return 6
                                                else:
                                                    if f[36] <= 0.3901:
                                                        return 1
                                                    else:
                                                        return 2
                                            else:
                                                if f[21] <= 25.9795:
                                                    return 9
                                                else:
                                                    return 4
                                        else:
                                            if f[2] <= 0.0046:
                                                if f[18] <= 0.0007:
                                                    return 1
                                                else:
                                                    if f[43] <= 3.0034:
                                                        if f[37] <= 0.0087:
                                                            return 1
                                                        else:
                                                            return 6
                                                    else:
                                                        return 2
                                            else:
                                                if f[3] <= 0.0894:
                                                    return 0
                                                else:
                                                    return 3
                            else:
                                if f[70] <= 0.3472:
                                    if f[68] <= 62.8853:
                                        return 3
                                    else:
                                        return 2
                                else:
                                    if f[45] <= 0.3311:
                                        if f[16] <= 0.9325:
                                            if f[41] <= 1.5851:
                                                return 7
                                            else:
                                                return 9
                                        else:
                                            return 6
                                    else:
                                        return 4
                        else:
                            if f[30] <= 0.2865:
                                if f[54] <= 26.6318:
                                    if f[1] <= 49.8032:
                                        if f[62] <= 115.4427:
                                            return 0
                                        else:
                                            return 0
                                    else:
                                        return 5
                                else:
                                    if f[26] <= 0.0:
                                        return 7
                                    else:
                                        if f[64] <= 123.598:
                                            if f[3] <= 0.0151:
                                                return 6
                                            else:
                                                return 2
                                        else:
                                            if f[24] <= 0.0201:
                                                return 1
                                            else:
                                                if f[37] <= 0.0064:
                                                    return 8
                                                else:
                                                    if f[44] <= 0.3088:
                                                        return 0
                                                    else:
                                                        return 4
                            else:
                                if f[54] <= 57.8705:
                                    if f[0] <= 48.8144:
                                        return 6
                                    else:
                                        if f[25] <= 0.3594:
                                            if f[31] <= 0.1102:
                                                if f[34] <= 0.8928:
                                                    return 1
                                                else:
                                                    if f[30] <= 0.417:
                                                        return 1
                                                    else:
                                                        if f[35] <= 0.5832:
                                                            return 1
                                                        else:
                                                            return 1
                                            else:
                                                return 1
                                        else:
                                            if f[9] <= 0.1003:
                                                if f[70] <= 0.3751:
                                                    return 1
                                                else:
                                                    return 1
                                            else:
                                                return 6
                                else:
                                    if f[19] <= 0.9939:
                                        if f[11] <= 122.6184:
                                            if f[10] <= 10539.8902:
                                                return 2
                                            else:
                                                return 1
                                        else:
                                            return 3
                                    else:
                                        return 5
                    else:
                        if f[31] <= 0.1495:
                            if f[45] <= 0.189:
                                if f[31] <= 0.0044:
                                    if f[34] <= 1.1185:
                                        if f[29] <= -15.5906:
                                            if f[9] <= 0.0623:
                                                if f[17] <= 0.0126:
                                                    return 6
                                                else:
                                                    return 6
                                            else:
                                                return 0
                                        else:
                                            if f[48] <= 71.3262:
                                                return 2
                                            else:
                                                if f[10] <= 4654.3825:
                                                    if f[22] <= 1.0653:
                                                        if f[56] <= 117.6006:
                                                            return 8
                                                        else:
                                                            return 7
                                                    else:
                                                        return 0
                                                else:
                                                    if f[46] <= 90.5:
                                                        if f[22] <= 1.0922:
                                                            return 9
                                                        else:
                                                            return 9
                                                    else:
                                                        return 1
                                    else:
                                        if f[51] <= 76.2881:
                                            if f[41] <= 1.7464:
                                                if f[12] <= 71.21:
                                                    if f[51] <= 65.8532:
                                                        return 2
                                                    else:
                                                        return 2
                                                else:
                                                    return 2
                                            else:
                                                if f[11] <= 74.3323:
                                                    if f[13] <= 27.732:
                                                        return 1
                                                    else:
                                                        if f[60] <= 133.0315:
                                                            return 8
                                                        else:
                                                            return 9
                                                else:
                                                    return 2
                                        else:
                                            if f[0] <= 81.2205:
                                                if f[29] <= 14.7875:
                                                    return 6
                                                else:
                                                    return 1
                                            else:
                                                if f[52] <= 56.2559:
                                                    return 2
                                                else:
                                                    if f[34] <= 1.6173:
                                                        if f[18] <= 0.0825:
                                                            return 8
                                                        else:
                                                            return 8
                                                    else:
                                                        return 7
                                else:
                                    if f[10] <= 7115.6096:
                                        if f[15] <= 0.2036:
                                            if f[20] <= 0.165:
                                                if f[6] <= 0.1223:
                                                    return 8
                                                else:
                                                    return 8
                                            else:
                                                return 7
                                        else:
                                            if f[2] <= 0.0:
                                                return 2
                                            else:
                                                if f[4] <= 0.0623:
                                                    return 7
                                                else:
                                                    return 7
                                    else:
                                        if f[13] <= 40.8489:
                                            if f[46] <= 63.3366:
                                                if f[29] <= 4.605:
                                                    return 5
                                                else:
                                                    return 2
                                            else:
                                                return 0
                                        else:
                                            return 9
                            else:
                                if f[31] <= 0.0176:
                                    if f[25] <= 0.2354:
                                        if f[8] <= 0.0321:
                                            return 2
                                        else:
                                            return 2
                                    else:
                                        if f[9] <= 0.0591:
                                            if f[49] <= 0.1208:
                                                return 0
                                            else:
                                                if f[55] <= 137.6693:
                                                    return 0
                                                else:
                                                    return 0
                                        else:
                                            if f[21] <= -14.7402:
                                                if f[26] <= 52.9426:
                                                    return 0
                                                else:
                                                    return 7
                                            else:
                                                if f[34] <= 0.9883:
                                                    return 6
                                                else:
                                                    return 2
                                else:
                                    if f[52] <= 173.4951:
                                        if f[67] <= 46.3259:
                                            return 7
                                        else:
                                            if f[34] <= 1.0271:
                                                if f[51] <= 122.2783:
                                                    if f[15] <= 0.3032:
                                                        if f[13] <= 11.603:
                                                            return 0
                                                        else:
                                                            return 0
                                                    else:
                                                        return 2
                                                else:
                                                    if f[24] <= 0.0122:
                                                        return 1
                                                    else:
                                                        return 1
                                            else:
                                                if f[28] <= 1.2218:
                                                    if f[7] <= 74.6168:
                                                        return 2
                                                    else:
                                                        return 2
                                                else:
                                                    if f[6] <= 0.2247:
                                                        return 0
                                                    else:
                                                        return 2
                                    else:
                                        if f[49] <= 0.2471:
                                            if f[31] <= 0.0557:
                                                return 1
                                            else:
                                                return 4
                                        else:
                                            return 3
                        else:
                            if f[70] <= 0.2943:
                                if f[5] <= 0.0144:
                                    if f[54] <= 21.125:
                                        return 4
                                    else:
                                        if f[31] <= 0.2128:
                                            return 4
                                        else:
                                            return 4
                                else:
                                    if f[29] <= 16.6787:
                                        return 1
                                    else:
                                        return 8
                            else:
                                if f[16] <= 0.9792:
                                    if f[12] <= 46.7598:
                                        return 4
                                    else:
                                        return 3
                                else:
                                    if f[53] <= 0.2567:
                                        return 0
                                    else:
                                        return 0
        else:
            if f[70] <= 0.3587:
                if f[4] <= 0.313:
                    if f[1] <= 111.8351:
                        if f[45] <= 0.0662:
                            if f[69] <= 0.281:
                                if f[54] <= 37.1465:
                                    return 1
                                else:
                                    return 8
                            else:
                                return 9
                        else:
                            if f[32] <= 0.2456:
                                if f[10] <= 5841.1833:
                                    if f[55] <= 160.7229:
                                        if f[31] <= 0.026:
                                            if f[70] <= 0.2931:
                                                return 0
                                            else:
                                                return 0
                                        else:
                                            return 2
                                    else:
                                        if f[17] <= 0.3215:
                                            return 4
                                        else:
                                            return 4
                                else:
                                    if f[55] <= 190.3555:
                                        if f[18] <= 0.4321:
                                            if f[19] <= 0.7787:
                                                if f[65] <= 157.032:
                                                    if f[29] <= -10.4104:
                                                        return 3
                                                    else:
                                                        return 3
                                                else:
                                                    return 2
                                            else:
                                                if f[54] <= 42.6523:
                                                    if f[23] <= 0.281:
                                                        return 1
                                                    else:
                                                        return 6
                                                else:
                                                    return 5
                                        else:
                                            return 9
                                    else:
                                        if f[7] <= 177.0459:
                                            return 5
                                        else:
                                            return 5
                            else:
                                if f[38] <= 0.0:
                                    return 4
                                else:
                                    if f[9] <= 0.7515:
                                        if f[31] <= 0.1681:
                                            if f[20] <= 0.7705:
                                                if f[10] <= 3230.2942:
                                                    if f[32] <= 0.2852:
                                                        return 5
                                                    else:
                                                        return 5
                                                else:
                                                    if f[46] <= 32.8857:
                                                        return 5
                                                    else:
                                                        return 2
                                            else:
                                                return 1
                                        else:
                                            if f[19] <= 0.8148:
                                                return 5
                                            else:
                                                return 4
                                    else:
                                        return 4
                    else:
                        if f[13] <= 3.2602:
                            return 0
                        else:
                            if f[43] <= 1.6648:
                                return 5
                            else:
                                if f[70] <= 0.2237:
                                    return 5
                                else:
                                    return 4
                else:
                    if f[9] <= 0.0:
                        return 5
                    else:
                        if f[35] <= 0.0068:
                            if f[9] <= 0.1404:
                                if f[53] <= 0.0863:
                                    return 4
                                else:
                                    return 4
                            else:
                                return 4
                        else:
                            if f[12] <= 67.1065:
                                if f[30] <= 0.0631:
                                    return 5
                                else:
                                    return 4
                            else:
                                return 3
            else:
                if f[38] <= 0.0272:
                    if f[28] <= 1.9316:
                        return 1
                    else:
                        return 1
                else:
                    return 4


def _tree_8(f):
    if f[2] <= 0.3682:
        if f[1] <= 93.4603:
            if f[10] <= 6360.7104:
                if f[57] <= 0.2842:
                    if f[31] <= 0.1695:
                        if f[19] <= 1.0423:
                            if f[16] <= 0.6187:
                                if f[29] <= 7.5506:
                                    if f[57] <= 0.1962:
                                        if f[10] <= 1143.6904:
                                            return 4
                                        else:
                                            if f[49] <= 0.2666:
                                                return 2
                                            else:
                                                return 2
                                    else:
                                        return 7
                                else:
                                    if f[55] <= 104.96:
                                        if f[39] <= 80.1175:
                                            if f[25] <= 0.2148:
                                                return 1
                                            else:
                                                return 8
                                        else:
                                            if f[14] <= 0.7473:
                                                return 2
                                            else:
                                                return 2
                                    else:
                                        if f[15] <= 0.1191:
                                            return 8
                                        else:
                                            return 8
                            else:
                                if f[20] <= 0.3626:
                                    if f[8] <= 0.311:
                                        if f[54] <= 95.369:
                                            if f[4] <= 0.1396:
                                                if f[58] <= 14.0425:
                                                    return 1
                                                else:
                                                    if f[24] <= 0.5635:
                                                        if f[12] <= 66.5901:
                                                            if f[59] <= 124.2423:
                                                                if f[43] <= 1.6423:
                                                                    return 2
                                                                else:
                                                                    if f[31] <= 0.001:
                                                                        if f[20] <= 0.276:
                                                                            return 2
                                                                        else:
                                                                            return 2
                                                                    else:
                                                                        return 4
                                                            else:
                                                                if f[29] <= 16.9849:
                                                                    return 5
                                                                else:
                                                                    return 2
                                                        else:
                                                            return 4
                                                    else:
                                                        return 7
                                            else:
                                                return 0
                                        else:
                                            return 5
                                    else:
                                        if f[37] <= 0.0254:
                                            if f[64] <= 190.7109:
                                                return 4
                                            else:
                                                return 0
                                        else:
                                            return 7
                                else:
                                    if f[27] <= 199.8663:
                                        if f[6] <= 0.1751:
                                            return 0
                                        else:
                                            if f[27] <= 124.0765:
                                                if f[7] <= 192.1387:
                                                    return 1
                                                else:
                                                    return 4
                                            else:
                                                if f[26] <= 59.8919:
                                                    if f[33] <= 0.4677:
                                                        return 5
                                                    else:
                                                        return 5
                                                else:
                                                    return 2
                                    else:
                                        return 4
                        else:
                            if f[0] <= 91.8186:
                                if f[31] <= 0.0012:
                                    if f[16] <= 0.1493:
                                        if f[5] <= 0.0:
                                            return 8
                                        else:
                                            return 8
                                    else:
                                        if f[34] <= 1.2431:
                                            if f[17] <= 0.0207:
                                                return 0
                                            else:
                                                return 0
                                        else:
                                            return 2
                                else:
                                    if f[70] <= 0.1449:
                                        if f[64] <= 170.0156:
                                            return 4
                                        else:
                                            return 7
                                    else:
                                        return 7
                            else:
                                if f[45] <= 0.0061:
                                    return 8
                                else:
                                    if f[45] <= 0.4841:
                                        if f[24] <= 0.0117:
                                            if f[27] <= 129.2646:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            if f[41] <= 1.4686:
                                                return 5
                                            else:
                                                return 1
                                    else:
                                        return 0
                    else:
                        if f[2] <= 0.0464:
                            if f[6] <= 0.1455:
                                if f[52] <= 141.4609:
                                    return 9
                                else:
                                    return 0
                            else:
                                if f[41] <= 1.8135:
                                    if f[43] <= 1.34:
                                        return 4
                                    else:
                                        if f[34] <= 1.0865:
                                            return 4
                                        else:
                                            return 2
                                else:
                                    return 4
                        else:
                            return 8
                else:
                    if f[9] <= 0.0496:
                        if f[4] <= 0.0234:
                            if f[23] <= 0.1405:
                                if f[13] <= 35.9667:
                                    if f[34] <= 0.8744:
                                        return 1
                                    else:
                                        if f[3] <= 0.0:
                                            return 7
                                        else:
                                            return 7
                                else:
                                    if f[57] <= 0.334:
                                        return 0
                                    else:
                                        if f[15] <= 0.3144:
                                            return 5
                                        else:
                                            return 6
                            else:
                                if f[68] <= 70.3338:
                                    if f[61] <= 0.3379:
                                        if f[23] <= 0.5842:
                                            return 0
                                        else:
                                            return 0
                                    else:
                                        if f[30] <= 0.0693:
                                            return 0
                                        else:
                                            if f[14] <= 0.6998:
                                                return 7
                                            else:
                                                return 1
                                else:
                                    return 2
                        else:
                            if f[57] <= 0.3135:
                                if f[28] <= 1.2037:
                                    if f[47] <= 57.376:
                                        return 9
                                    else:
                                        return 4
                                else:
                                    return 5
                            else:
                                if f[25] <= 0.3273:
                                    if f[69] <= 0.2678:
                                        return 0
                                    else:
                                        if f[23] <= 0.1973:
                                            return 2
                                        else:
                                            return 2
                                else:
                                    if f[44] <= 0.5969:
                                        if f[26] <= 63.6121:
                                            return 0
                                        else:
                                            return 7
                                    else:
                                        return 6
                    else:
                        if f[53] <= 0.3359:
                            if f[29] <= 7.5803:
                                if f[27] <= 142.9804:
                                    if f[69] <= 0.1391:
                                        return 3
                                    else:
                                        if f[61] <= 0.334:
                                            return 6
                                        else:
                                            return 6
                                else:
                                    if f[30] <= 0.0918:
                                        return 7
                                    else:
                                        return 7
                            else:
                                if f[68] <= 23.9307:
                                    if f[51] <= 123.373:
                                        if f[53] <= 0.2939:
                                            return 0
                                        else:
                                            return 0
                                    else:
                                        if f[33] <= 0.286:
                                            return 1
                                        else:
                                            return 2
                                else:
                                    if f[65] <= 152.8981:
                                        if f[61] <= 0.3359:
                                            return 7
                                        else:
                                            return 0
                                    else:
                                        return 5
                        else:
                            if f[62] <= 96.6272:
                                return 0
                            else:
                                if f[39] <= 50.5566:
                                    return 6
                                else:
                                    return 6
            else:
                if f[40] <= 0.636:
                    if f[29] <= 3.1003:
                        if f[55] <= 30.6426:
                            if f[23] <= 0.0094:
                                return 0
                            else:
                                if f[65] <= 39.3973:
                                    return 7
                                else:
                                    return 7
                        else:
                            if f[53] <= 0.3672:
                                if f[66] <= 121.1708:
                                    if f[25] <= 0.3559:
                                        if f[29] <= -66.189:
                                            if f[1] <= 8.7788:
                                                return 6
                                            else:
                                                return 6
                                        else:
                                            if f[54] <= 27.0732:
                                                if f[40] <= 0.5285:
                                                    if f[18] <= 0.04:
                                                        return 0
                                                    else:
                                                        return 0
                                                else:
                                                    return 1
                                            else:
                                                if f[23] <= 0.0511:
                                                    if f[60] <= 88.2539:
                                                        return 9
                                                    else:
                                                        return 9
                                                else:
                                                    if f[37] <= 0.0358:
                                                        if f[62] <= 141.4113:
                                                            if f[18] <= 0.0998:
                                                                return 7
                                                            else:
                                                                return 9
                                                        else:
                                                            if f[5] <= 0.1089:
                                                                if f[33] <= 0.0856:
                                                                    return 3
                                                                else:
                                                                    return 5
                                                            else:
                                                                return 6
                                                    else:
                                                        if f[20] <= 0.1709:
                                                            if f[56] <= 73.1025:
                                                                return 3
                                                            else:
                                                                return 3
                                                        else:
                                                            return 0
                                    else:
                                        if f[41] <= 1.6238:
                                            if f[6] <= 0.0672:
                                                return 6
                                            else:
                                                return 6
                                        else:
                                            return 2
                                else:
                                    if f[38] <= 0.1034:
                                        if f[59] <= 154.209:
                                            if f[68] <= 17.8992:
                                                return 2
                                            else:
                                                return 4
                                        else:
                                            if f[49] <= 0.3447:
                                                return 3
                                            else:
                                                return 1
                                    else:
                                        if f[21] <= 29.8975:
                                            if f[3] <= 0.1316:
                                                return 7
                                            else:
                                                if f[10] <= 11910.1294:
                                                    return 3
                                                else:
                                                    return 3
                                        else:
                                            if f[47] <= 113.8833:
                                                if f[33] <= 0.144:
                                                    return 9
                                                else:
                                                    return 3
                                            else:
                                                return 4
                            else:
                                if f[18] <= 0.0051:
                                    return 7
                                else:
                                    if f[31] <= 0.0496:
                                        return 6
                                    else:
                                        if f[60] <= 108.4404:
                                            return 6
                                        else:
                                            return 0
                    else:
                        if f[33] <= 0.1045:
                            if f[67] <= 122.2973:
                                if f[57] <= 0.3555:
                                    if f[54] <= 28.583:
                                        if f[16] <= 0.9808:
                                            return 1
                                        else:
                                            return 0
                                    else:
                                        if f[29] <= 10.7459:
                                            return 6
                                        else:
                                            if f[53] <= 0.3545:
                                                return 7
                                            else:
                                                return 7
                                else:
                                    if f[11] <= 96.2375:
                                        if f[45] <= 0.0797:
                                            if f[39] <= 15.2266:
                                                return 7
                                            else:
                                                return 6
                                        else:
                                            return 8
                                    else:
                                        if f[42] <= 1.0027:
                                            if f[54] <= 23.9053:
                                                return 1
                                            else:
                                                return 1
                                        else:
                                            return 0
                            else:
                                if f[42] <= 1.0634:
                                    if f[53] <= 0.3936:
                                        if f[45] <= 0.4241:
                                            if f[51] <= 170.9902:
                                                if f[31] <= 0.1113:
                                                    return 1
                                                else:
                                                    return 1
                                            else:
                                                return 1
                                        else:
                                            return 4
                                    else:
                                        return 0
                                else:
                                    return 4
                        else:
                            if f[4] <= 0.0352:
                                if f[50] <= 79.887:
                                    if f[19] <= 1.0119:
                                        if f[14] <= 0.5841:
                                            return 2
                                        else:
                                            return 2
                                    else:
                                        return 7
                                else:
                                    if f[11] <= 80.2412:
                                        return 7
                                    else:
                                        return 9
                            else:
                                if f[58] <= 50.6762:
                                    if f[31] <= 0.1035:
                                        if f[26] <= 117.5794:
                                            if f[10] <= 10896.117:
                                                if f[34] <= 1.0357:
                                                    return 1
                                                else:
                                                    return 3
                                            else:
                                                return 0
                                        else:
                                            return 2
                                    else:
                                        return 4
                                else:
                                    if f[68] <= 33.0498:
                                        return 2
                                    else:
                                        if f[37] <= 0.0372:
                                            return 3
                                        else:
                                            return 3
                else:
                    if f[17] <= 0.0613:
                        if f[70] <= 0.3467:
                            if f[34] <= 0.8718:
                                return 6
                            else:
                                if f[2] <= 0.0:
                                    return 9
                                else:
                                    return 9
                        else:
                            if f[61] <= 0.3633:
                                return 3
                            else:
                                return 4
                    else:
                        if f[2] <= 0.0143:
                            if f[26] <= 48.6822:
                                return 0
                            else:
                                if f[69] <= 0.2768:
                                    if f[6] <= 0.2079:
                                        if f[29] <= -14.8368:
                                            return 3
                                        else:
                                            return 9
                                    else:
                                        if f[33] <= 0.1812:
                                            return 4
                                        else:
                                            return 2
                                else:
                                    if f[11] <= 118.9997:
                                        if f[45] <= 0.3961:
                                            if f[43] <= 1.9561:
                                                return 6
                                            else:
                                                return 3
                                        else:
                                            return 2
                                    else:
                                        if f[8] <= 0.0844:
                                            return 3
                                        else:
                                            return 1
                        else:
                            if f[3] <= 0.0293:
                                if f[61] <= 0.2979:
                                    return 9
                                else:
                                    return 7
                            else:
                                if f[57] <= 0.2422:
                                    if f[70] <= 0.1966:
                                        return 3
                                    else:
                                        return 9
                                else:
                                    if f[3] <= 0.0764:
                                        if f[12] <= 60.8434:
                                            return 9
                                        else:
                                            if f[57] <= 0.3068:
                                                return 3
                                            else:
                                                return 3
                                    else:
                                        if f[26] <= 95.957:
                                            return 3
                                        else:
                                            return 3
        else:
            if f[4] <= 0.1064:
                if f[27] <= 175.0396:
                    if f[33] <= 0.1682:
                        return 0
                    else:
                        if f[54] <= 18.6104:
                            if f[36] <= 0.0139:
                                return 5
                            else:
                                return 5
                        else:
                            return 2
                else:
                    return 5
            else:
                if f[9] <= 0.0:
                    if f[67] <= 211.2642:
                        return 5
                    else:
                        return 5
                else:
                    if f[54] <= 16.9106:
                        if f[19] <= 0.8953:
                            return 4
                        else:
                            return 0
                    else:
                        if f[46] <= 29.1064:
                            if f[31] <= 0.2678:
                                return 5
                            else:
                                if f[12] <= 57.6216:
                                    if f[13] <= 6.6739:
                                        return 4
                                    else:
                                        return 5
                                else:
                                    return 4
                        else:
                            if f[69] <= 0.3297:
                                if f[58] <= 24.239:
                                    return 5
                                else:
                                    return 5
                            else:
                                return 3
    else:
        if f[22] <= 0.6116:
            if f[65] <= 128.7262:
                return 8
            else:
                if f[3] <= 0.0879:
                    return 8
                else:
                    return 8
        else:
            if f[4] <= 0.0021:
                if f[0] <= 101.8018:
                    if f[55] <= 74.7779:
                        return 0
                    else:
                        return 2
                else:
                    return 8
            else:
                if f[17] <= 0.3208:
                    if f[9] <= 0.0012:
                        return 5
                    else:
                        if f[5] <= 0.0076:
                            return 9
                        else:
                            if f[21] <= 18.4374:
                                return 6
                            else:
                                return 3
                else:
                    return 4


def _tree_9(f):
    if f[28] <= 0.6431:
        if f[67] <= 129.2642:
            return 7
        else:
            if f[69] <= 0.3191:
                if f[23] <= 0.0259:
                    return 8
                else:
                    return 8
            else:
                return 7
    else:
        if f[1] <= 70.5757:
            if f[19] <= 0.6872:
                if f[17] <= 0.0759:
                    if f[11] <= 90.1956:
                        if f[1] <= -41.5808:
                            if f[6] <= 0.2085:
                                return 8
                            else:
                                return 8
                        else:
                            if f[42] <= 1.3528:
                                if f[60] <= 161.4285:
                                    if f[6] <= 0.0164:
                                        if f[46] <= 73.46:
                                            return 7
                                        else:
                                            return 7
                                    else:
                                        if f[41] <= 2.5178:
                                            return 2
                                        else:
                                            return 3
                                else:
                                    return 0
                            else:
                                if f[37] <= 0.0038:
                                    return 8
                                else:
                                    return 9
                    else:
                        if f[57] <= 0.3516:
                            if f[63] <= 110.974:
                                if f[41] <= 1.8529:
                                    if f[11] <= 105.1287:
                                        return 2
                                    else:
                                        return 8
                                else:
                                    return 9
                            else:
                                if f[37] <= 0.0799:
                                    return 9
                                else:
                                    if f[11] <= 113.2307:
                                        return 1
                                    else:
                                        return 9
                        else:
                            if f[4] <= 0.0071:
                                return 0
                            else:
                                return 3
                else:
                    if f[26] <= 57.9217:
                        if f[56] <= 177.0097:
                            if f[68] <= 16.6689:
                                return 0
                            else:
                                if f[68] <= 75.335:
                                    if f[42] <= 1.001:
                                        if f[8] <= 0.0347:
                                            return 1
                                        else:
                                            if f[37] <= 0.0193:
                                                return 2
                                            else:
                                                return 5
                                    else:
                                        if f[7] <= 144.2278:
                                            if f[55] <= 69.4137:
                                                return 0
                                            else:
                                                return 2
                                        else:
                                            return 4
                                else:
                                    return 9
                        else:
                            return 5
                    else:
                        if f[52] <= 152.3914:
                            if f[63] <= 134.2649:
                                if f[64] <= 92.3516:
                                    if f[22] <= 1.4054:
                                        return 9
                                    else:
                                        if f[60] <= 82.6007:
                                            return 4
                                        else:
                                            return 2
                                else:
                                    if f[2] <= 0.0149:
                                        if f[12] <= 56.471:
                                            return 3
                                        else:
                                            return 6
                                    else:
                                        if f[64] <= 107.7223:
                                            return 3
                                        else:
                                            return 3
                            else:
                                if f[41] <= 2.6602:
                                    if f[70] <= 0.1903:
                                        return 2
                                    else:
                                        if f[57] <= 0.2686:
                                            return 9
                                        else:
                                            if f[42] <= 0.9375:
                                                return 8
                                            else:
                                                return 3
                                else:
                                    if f[68] <= 74.1266:
                                        return 9
                                    else:
                                        return 9
                        else:
                            if f[26] <= 80.0695:
                                if f[64] <= 136.2555:
                                    if f[42] <= 1.1195:
                                        return 1
                                    else:
                                        return 3
                                else:
                                    return 4
                            else:
                                if f[17] <= 0.1456:
                                    return 3
                                else:
                                    return 3
            else:
                if f[53] <= 0.3369:
                    if f[22] <= 0.6481:
                        if f[42] <= 1.1614:
                            return 6
                        else:
                            return 8
                    else:
                        if f[4] <= 0.1177:
                            if f[68] <= 27.2919:
                                if f[34] <= 1.1318:
                                    if f[20] <= 0.5807:
                                        if f[4] <= 0.0493:
                                            if f[23] <= 0.679:
                                                if f[10] <= 9323.1696:
                                                    if f[28] <= 1.0052:
                                                        return 0
                                                    else:
                                                        if f[21] <= 38.7547:
                                                            return 0
                                                        else:
                                                            return 0
                                                else:
                                                    return 0
                                            else:
                                                return 2
                                        else:
                                            if f[59] <= 88.6689:
                                                return 6
                                            else:
                                                if f[67] <= 139.0485:
                                                    return 0
                                                else:
                                                    return 1
                                    else:
                                        return 5
                                else:
                                    if f[49] <= 0.173:
                                        if f[25] <= 0.0918:
                                            return 8
                                        else:
                                            if f[50] <= 43.6421:
                                                return 2
                                            else:
                                                return 2
                                    else:
                                        if f[14] <= 0.5603:
                                            return 5
                                        else:
                                            if f[21] <= -6.2505:
                                                return 0
                                            else:
                                                if f[39] <= 44.8828:
                                                    if f[39] <= 24.9312:
                                                        return 1
                                                    else:
                                                        return 2
                                                else:
                                                    return 8
                            else:
                                if f[40] <= 0.4314:
                                    if f[31] <= 0.0042:
                                        if f[42] <= 1.2789:
                                            if f[13] <= 33.6708:
                                                if f[60] <= 100.6201:
                                                    return 6
                                                else:
                                                    if f[46] <= 60.0244:
                                                        return 7
                                                    else:
                                                        return 7
                                            else:
                                                if f[9] <= 0.0517:
                                                    if f[67] <= 54.6811:
                                                        return 0
                                                    else:
                                                        return 0
                                                else:
                                                    return 2
                                        else:
                                            if f[29] <= -18.4646:
                                                return 6
                                            else:
                                                if f[23] <= 0.0029:
                                                    return 8
                                                else:
                                                    return 8
                                    else:
                                        if f[70] <= 0.3334:
                                            if f[67] <= 96.5548:
                                                return 7
                                            else:
                                                return 7
                                        else:
                                            return 2
                                else:
                                    if f[39] <= 20.7459:
                                        if f[18] <= 0.0071:
                                            if f[21] <= 27.1338:
                                                if f[5] <= 0.0164:
                                                    return 7
                                                else:
                                                    return 6
                                            else:
                                                return 9
                                        else:
                                            if f[6] <= 0.0142:
                                                if f[36] <= 0.5879:
                                                    return 0
                                                else:
                                                    return 0
                                            else:
                                                if f[26] <= 72.0133:
                                                    if f[0] <= 88.0496:
                                                        return 5
                                                    else:
                                                        return 0
                                                else:
                                                    if f[52] <= 130.2246:
                                                        if f[42] <= 1.0829:
                                                            if f[7] <= 108.2658:
                                                                return 9
                                                            else:
                                                                return 9
                                                        else:
                                                            if f[1] <= 6.0057:
                                                                return 8
                                                            else:
                                                                return 2
                                                    else:
                                                        if f[23] <= 0.0981:
                                                            return 9
                                                        else:
                                                            if f[42] <= 1.1077:
                                                                return 3
                                                            else:
                                                                return 3
                                    else:
                                        if f[52] <= 172.3066:
                                            if f[69] <= 0.1763:
                                                if f[46] <= 77.3872:
                                                    if f[65] <= 131.8341:
                                                        if f[38] <= 0.6856:
                                                            return 2
                                                        else:
                                                            return 2
                                                    else:
                                                        return 2
                                                else:
                                                    return 8
                                            else:
                                                if f[30] <= 0.6371:
                                                    if f[5] <= 0.3177:
                                                        if f[12] <= 74.81:
                                                            if f[46] <= 66.8447:
                                                                if f[34] <= 1.066:
                                                                    return 0
                                                                else:
                                                                    if f[26] <= 44.2358:
                                                                        return 2
                                                                    else:
                                                                        return 2
                                                            else:
                                                                if f[31] <= 0.0:
                                                                    if f[69] <= 0.2129:
                                                                        return 6
                                                                    else:
                                                                        return 8
                                                                else:
                                                                    if f[30] <= 0.1049:
                                                                        return 2
                                                                    else:
                                                                        return 7
                                                        else:
                                                            if f[46] <= 50.0205:
                                                                return 9
                                                            else:
                                                                return 1
                                                    else:
                                                        if f[22] <= 0.8926:
                                                            return 6
                                                        else:
                                                            return 6
                                                else:
                                                    if f[25] <= 0.3152:
                                                        return 1
                                                    else:
                                                        return 1
                                        else:
                                            if f[18] <= 0.1124:
                                                if f[11] <= 88.4919:
                                                    if f[31] <= 0.021:
                                                        if f[51] <= 39.3216:
                                                            return 2
                                                        else:
                                                            return 6
                                                    else:
                                                        return 4
                                                else:
                                                    return 3
                                            else:
                                                if f[40] <= 0.5906:
                                                    return 5
                                                else:
                                                    return 9
                        else:
                            if f[57] <= 0.3001:
                                if f[31] <= 0.1204:
                                    if f[35] <= 0.4326:
                                        if f[51] <= 180.3561:
                                            if f[33] <= 0.4836:
                                                if f[63] <= 66.8683:
                                                    return 6
                                                else:
                                                    if f[61] <= 0.2344:
                                                        return 9
                                                    else:
                                                        return 2
                                            else:
                                                return 4
                                        else:
                                            return 1
                                    else:
                                        return 7
                                else:
                                    if f[25] <= 0.3115:
                                        if f[67] <= 183.4925:
                                            if f[21] <= -17.1894:
                                                return 4
                                            else:
                                                return 4
                                        else:
                                            return 4
                                    else:
                                        if f[18] <= 0.0627:
                                            return 4
                                        else:
                                            return 3
                            else:
                                if f[5] <= 0.325:
                                    if f[4] <= 0.527:
                                        if f[36] <= 0.0239:
                                            return 5
                                        else:
                                            if f[6] <= 0.0621:
                                                return 6
                                            else:
                                                if f[49] <= 0.2668:
                                                    if f[4] <= 0.3163:
                                                        return 2
                                                    else:
                                                        return 2
                                                else:
                                                    if f[31] <= 0.0354:
                                                        return 1
                                                    else:
                                                        if f[68] <= 31.6258:
                                                            if f[33] <= 0.1826:
                                                                return 4
                                                            else:
                                                                return 0
                                                        else:
                                                            if f[45] <= 0.3827:
                                                                return 3
                                                            else:
                                                                return 3
                                    else:
                                        return 7
                                else:
                                    if f[6] <= 0.199:
                                        return 1
                                    else:
                                        return 1
                else:
                    if f[29] <= 24.7771:
                        if f[66] <= 47.0513:
                            if f[40] <= 0.4364:
                                if f[12] <= 62.8987:
                                    return 7
                                else:
                                    return 7
                            else:
                                if f[25] <= 0.3627:
                                    if f[49] <= 0.3594:
                                        if f[69] <= 0.3504:
                                            return 3
                                        else:
                                            return 0
                                    else:
                                        return 7
                                else:
                                    if f[34] <= 0.7772:
                                        return 6
                                    else:
                                        return 2
                        else:
                            if f[11] <= 119.1335:
                                if f[69] <= 0.3371:
                                    if f[30] <= 0.1591:
                                        if f[0] <= 81.2395:
                                            return 0
                                        else:
                                            return 0
                                    else:
                                        if f[31] <= 0.0271:
                                            if f[52] <= 116.3428:
                                                return 0
                                            else:
                                                return 6
                                        else:
                                            if f[56] <= 119.335:
                                                return 1
                                            else:
                                                return 3
                                else:
                                    if f[31] <= 0.0042:
                                        if f[30] <= 0.5191:
                                            if f[68] <= 86.0615:
                                                if f[56] <= 140.6553:
                                                    if f[41] <= 2.0713:
                                                        return 6
                                                    else:
                                                        return 6
                                                else:
                                                    return 6
                                            else:
                                                return 6
                                        else:
                                            if f[11] <= 91.2651:
                                                if f[57] <= 0.3271:
                                                    return 2
                                                else:
                                                    return 6
                                            else:
                                                if f[51] <= 57.8037:
                                                    return 1
                                                else:
                                                    return 1
                                    else:
                                        if f[41] <= 1.0:
                                            return 0
                                        else:
                                            if f[43] <= 1.777:
                                                if f[60] <= 130.642:
                                                    if f[9] <= 0.0432:
                                                        return 6
                                                    else:
                                                        return 6
                                                else:
                                                    return 0
                                            else:
                                                if f[19] <= 0.9761:
                                                    if f[46] <= 29.0332:
                                                        return 0
                                                    else:
                                                        if f[42] <= 1.0012:
                                                            if f[54] <= 42.7252:
                                                                return 6
                                                            else:
                                                                return 6
                                                        else:
                                                            return 1
                                                else:
                                                    if f[33] <= 0.0918:
                                                        if f[54] <= 37.5117:
                                                            return 1
                                                        else:
                                                            return 1
                                                    else:
                                                        return 4
                            else:
                                if f[70] <= 0.3501:
                                    if f[37] <= 0.0634:
                                        if f[41] <= 1.7382:
                                            return 3
                                        else:
                                            return 3
                                    else:
                                        return 7
                                else:
                                    if f[32] <= 0.0403:
                                        return 9
                                    else:
                                        return 1
                    else:
                        if f[40] <= 0.3483:
                            if f[30] <= 0.5703:
                                return 7
                            else:
                                return 0
                        else:
                            if f[45] <= 0.4028:
                                if f[2] <= 0.0136:
                                    if f[67] <= 60.3562:
                                        return 2
                                    else:
                                        if f[20] <= 0.0785:
                                            if f[9] <= 0.1162:
                                                return 6
                                            else:
                                                if f[16] <= 0.9545:
                                                    return 1
                                                else:
                                                    return 1
                                        else:
                                            return 1
                                else:
                                    if f[35] <= 0.2305:
                                        return 3
                                    else:
                                        if f[57] <= 0.3047:
                                            return 9
                                        else:
                                            return 2
                            else:
                                if f[47] <= 100.7754:
                                    return 0
                                else:
                                    return 0
        else:
            if f[28] <= 1.3255:
                if f[50] <= 43.2813:
                    if f[37] <= 0.0019:
                        return 1
                    else:
                        if f[10] <= 5290.0964:
                            if f[1] <= 135.9398:
                                if f[69] <= 0.2856:
                                    if f[14] <= 0.7081:
                                        return 4
                                    else:
                                        return 4
                                else:
                                    return 4
                            else:
                                return 5
                        else:
                            if f[38] <= 0.0049:
                                if f[63] <= 146.6109:
                                    return 0
                                else:
                                    return 1
                            else:
                                if f[18] <= 0.0999:
                                    return 3
                                else:
                                    if f[51] <= 131.584:
                                        return 4
                                    else:
                                        return 4
                else:
                    if f[12] <= 45.6206:
                        return 5
                    else:
                        return 9
            else:
                if f[1] <= 111.9783:
                    if f[44] <= 0.2565:
                        if f[34] <= 0.9469:
                            if f[10] <= 4175.3466:
                                return 0
                            else:
                                return 1
                        else:
                            if f[50] <= 10.9473:
                                return 2
                            else:
                                if f[28] <= 1.8083:
                                    if f[53] <= 0.2354:
                                        return 5
                                    else:
                                        return 2
                                else:
                                    return 9
                    else:
                        if f[31] <= 0.1169:
                            if f[12] <= 48.4644:
                                return 4
                            else:
                                if f[16] <= 0.974:
                                    return 5
                                else:
                                    return 5
                        else:
                            if f[48] <= 113.324:
                                return 5
                            else:
                                if f[1] <= 104.3122:
                                    return 4
                                else:
                                    return 4
                else:
                    if f[68] <= 20.994:
                        if f[19] <= 0.6825:
                            return 4
                        else:
                            if f[27] <= 154.6167:
                                return 0
                            else:
                                return 5
                    else:
                        if f[36] <= 0.0:
                            return 4
                        else:
                            return 5


def _tree_10(f):
    if f[22] <= 0.8392:
        if f[6] <= 0.2312:
            if f[16] <= 0.0005:
                if f[48] <= 153.5697:
                    return 8
                else:
                    return 8
            else:
                if f[11] <= 134.1:
                    if f[43] <= 1.8472:
                        if f[69] <= 0.0744:
                            return 0
                        else:
                            if f[46] <= 95.4609:
                                return 7
                            else:
                                return 7
                    else:
                        if f[44] <= 0.0649:
                            if f[60] <= 132.304:
                                return 6
                            else:
                                return 0
                        else:
                            if f[35] <= 0.3213:
                                return 2
                            else:
                                return 2
                else:
                    return 9
        else:
            if f[68] <= 70.3439:
                return 8
            else:
                return 8
    else:
        if f[7] <= 205.9418:
            if f[40] <= 0.6516:
                if f[34] <= 0.9678:
                    if f[29] <= 3.231:
                        if f[9] <= 0.0146:
                            if f[30] <= 0.0986:
                                if f[58] <= 37.3994:
                                    if f[9] <= 0.0006:
                                        return 4
                                    else:
                                        if f[13] <= 2.5883:
                                            return 0
                                        else:
                                            return 0
                                else:
                                    return 3
                            else:
                                if f[43] <= 1.8621:
                                    if f[70] <= 0.3033:
                                        return 2
                                    else:
                                        return 0
                                else:
                                    if f[54] <= 37.5117:
                                        return 1
                                    else:
                                        return 5
                        else:
                            if f[2] <= 0.0012:
                                if f[38] <= 0.5327:
                                    if f[31] <= 0.1909:
                                        if f[66] <= 154.939:
                                            if f[57] <= 0.3789:
                                                return 6
                                            else:
                                                return 6
                                        else:
                                            if f[53] <= 0.3516:
                                                return 1
                                            else:
                                                return 6
                                    else:
                                        return 4
                                else:
                                    if f[49] <= 0.3096:
                                        return 4
                                    else:
                                        return 7
                            else:
                                if f[4] <= 0.0473:
                                    if f[40] <= 0.4993:
                                        if f[3] <= 0.0578:
                                            if f[21] <= 35.4937:
                                                return 7
                                            else:
                                                return 6
                                        else:
                                            if f[51] <= 99.416:
                                                return 0
                                            else:
                                                return 0
                                    else:
                                        if f[26] <= 91.6664:
                                            if f[59] <= 108.3423:
                                                return 6
                                            else:
                                                return 6
                                        else:
                                            if f[1] <= 5.0823:
                                                if f[60] <= 97.1373:
                                                    return 9
                                                else:
                                                    return 7
                                            else:
                                                if f[11] <= 115.3296:
                                                    return 6
                                                else:
                                                    return 3
                                else:
                                    if f[50] <= 47.0045:
                                        if f[66] <= 123.7872:
                                            if f[20] <= 0.1714:
                                                if f[24] <= 0.0659:
                                                    return 0
                                                else:
                                                    return 1
                                            else:
                                                return 6
                                        else:
                                            if f[64] <= 90.8615:
                                                return 1
                                            else:
                                                if f[51] <= 124.582:
                                                    return 4
                                                else:
                                                    return 4
                                    else:
                                        if f[7] <= 128.2402:
                                            return 9
                                        else:
                                            if f[42] <= 0.9388:
                                                return 3
                                            else:
                                                return 3
                    else:
                        if f[26] <= 83.3555:
                            if f[4] <= 0.0576:
                                if f[69] <= 0.3504:
                                    if f[7] <= 180.6146:
                                        if f[17] <= 0.1244:
                                            if f[70] <= 0.3374:
                                                return 2
                                            else:
                                                return 0
                                        else:
                                            if f[25] <= 0.2975:
                                                return 0
                                            else:
                                                return 0
                                    else:
                                        return 5
                                else:
                                    if f[6] <= 0.032:
                                        return 7
                                    else:
                                        return 6
                            else:
                                if f[56] <= 83.1758:
                                    if f[50] <= 28.2129:
                                        return 1
                                    else:
                                        return 1
                                else:
                                    if f[68] <= 20.1533:
                                        if f[25] <= 0.3232:
                                            return 1
                                        else:
                                            return 5
                                    else:
                                        if f[61] <= 0.3447:
                                            return 4
                                        else:
                                            return 1
                        else:
                            if f[38] <= 0.2759:
                                if f[57] <= 0.3283:
                                    if f[42] <= 1.0452:
                                        if f[35] <= 0.1152:
                                            return 9
                                        else:
                                            return 3
                                    else:
                                        if f[25] <= 0.3623:
                                            return 1
                                        else:
                                            return 6
                                else:
                                    if f[30] <= 0.2373:
                                        if f[20] <= 0.0837:
                                            return 0
                                        else:
                                            if f[61] <= 0.3617:
                                                return 4
                                            else:
                                                if f[49] <= 0.2314:
                                                    return 1
                                                else:
                                                    return 1
                                    else:
                                        if f[25] <= 0.3604:
                                            if f[9] <= 0.2246:
                                                return 1
                                            else:
                                                if f[20] <= 0.09:
                                                    return 1
                                                else:
                                                    return 1
                                        else:
                                            if f[34] <= 0.7842:
                                                if f[50] <= 33.168:
                                                    return 1
                                                else:
                                                    return 1
                                            else:
                                                if f[53] <= 0.3604:
                                                    return 6
                                                else:
                                                    return 0
                            else:
                                if f[33] <= 0.0241:
                                    if f[58] <= 69.4528:
                                        return 1
                                    else:
                                        return 1
                                else:
                                    if f[68] <= 54.7752:
                                        if f[54] <= 18.6836:
                                            return 0
                                        else:
                                            if f[0] <= 62.2609:
                                                return 6
                                            else:
                                                return 0
                                    else:
                                        if f[22] <= 1.1364:
                                            return 7
                                        else:
                                            return 2
                else:
                    if f[4] <= 0.1368:
                        if f[40] <= 0.455:
                            if f[67] <= 63.7429:
                                if f[4] <= 0.0:
                                    return 8
                                else:
                                    if f[65] <= 14.6689:
                                        return 2
                                    else:
                                        if f[35] <= 0.4418:
                                            return 7
                                        else:
                                            return 7
                            else:
                                if f[27] <= 121.0151:
                                    if f[50] <= 43.8916:
                                        if f[40] <= 0.3579:
                                            return 2
                                        else:
                                            return 2
                                    else:
                                        return 0
                                else:
                                    if f[11] <= 56.9751:
                                        if f[12] <= 53.3747:
                                            if f[46] <= 45.0404:
                                                return 8
                                            else:
                                                return 5
                                        else:
                                            if f[58] <= 31.165:
                                                return 2
                                            else:
                                                return 7
                                    else:
                                        if f[38] <= 0.1487:
                                            return 0
                                        else:
                                            return 1
                        else:
                            if f[34] <= 1.1532:
                                if f[58] <= 17.4727:
                                    if f[27] <= 128.0:
                                        return 2
                                    else:
                                        return 0
                                else:
                                    if f[31] <= 0.0228:
                                        if f[10] <= 5734.2721:
                                            if f[56] <= 95.4633:
                                                if f[13] <= 40.9173:
                                                    return 1
                                                else:
                                                    return 8
                                            else:
                                                if f[18] <= 0.0265:
                                                    if f[16] <= 0.6575:
                                                        return 4
                                                    else:
                                                        return 2
                                                else:
                                                    if f[51] <= 95.1727:
                                                        return 0
                                                    else:
                                                        return 5
                                        else:
                                            if f[70] <= 0.218:
                                                if f[9] <= 0.1721:
                                                    return 9
                                                else:
                                                    return 9
                                            else:
                                                if f[13] <= 35.7934:
                                                    if f[37] <= 0.0449:
                                                        return 2
                                                    else:
                                                        if f[37] <= 0.0547:
                                                            return 6
                                                        else:
                                                            return 6
                                                else:
                                                    if f[33] <= 0.1072:
                                                        return 5
                                                    else:
                                                        if f[40] <= 0.6057:
                                                            return 2
                                                        else:
                                                            return 9
                                    else:
                                        if f[55] <= 45.3911:
                                            return 7
                                        else:
                                            if f[69] <= 0.2812:
                                                if f[31] <= 0.0422:
                                                    return 2
                                                else:
                                                    return 0
                                            else:
                                                if f[17] <= 0.2441:
                                                    return 3
                                                else:
                                                    return 3
                            else:
                                if f[41] <= 1.186:
                                    if f[17] <= 0.2776:
                                        if f[14] <= 0.6802:
                                            return 2
                                        else:
                                            return 2
                                    else:
                                        return 4
                                else:
                                    if f[51] <= 24.3781:
                                        if f[48] <= 193.249:
                                            return 3
                                        else:
                                            return 3
                                    else:
                                        if f[60] <= 57.4275:
                                            if f[32] <= 0.457:
                                                return 1
                                            else:
                                                return 1
                                        else:
                                            if f[7] <= 164.808:
                                                if f[63] <= 81.6957:
                                                    return 7
                                                else:
                                                    if f[10] <= 7191.2381:
                                                        if f[16] <= 0.0857:
                                                            return 5
                                                        else:
                                                            if f[8] <= 0.293:
                                                                if f[31] <= 0.0022:
                                                                    return 2
                                                                else:
                                                                    if f[46] <= 59.5475:
                                                                        if f[40] <= 0.5039:
                                                                            return 2
                                                                        else:
                                                                            return 2
                                                                    else:
                                                                        return 3
                                                            else:
                                                                if f[70] <= 0.1236:
                                                                    return 2
                                                                else:
                                                                    return 7
                                                    else:
                                                        return 5
                                            else:
                                                return 5
                    else:
                        if f[20] <= 0.185:
                            if f[46] <= 32.7637:
                                if f[41] <= 2.16:
                                    return 2
                                else:
                                    return 4
                            else:
                                if f[3] <= 0.0911:
                                    if f[37] <= 0.0628:
                                        if f[52] <= 114.1232:
                                            return 1
                                        else:
                                            if f[16] <= 0.9002:
                                                return 8
                                            else:
                                                return 4
                                    else:
                                        if f[57] <= 0.293:
                                            return 9
                                        else:
                                            return 9
                                else:
                                    if f[27] <= 118.0977:
                                        return 1
                                    else:
                                        return 3
                        else:
                            if f[56] <= 103.499:
                                if f[30] <= 0.7172:
                                    if f[3] <= 0.1602:
                                        return 0
                                    else:
                                        return 1
                                else:
                                    if f[43] <= 2.2467:
                                        return 4
                                    else:
                                        return 8
                            else:
                                if f[10] <= 10122.7884:
                                    if f[42] <= 1.982:
                                        if f[25] <= 0.3284:
                                            if f[68] <= 19.6182:
                                                if f[69] <= 0.1935:
                                                    return 4
                                                else:
                                                    return 1
                                            else:
                                                if f[38] <= 0.4985:
                                                    if f[69] <= 0.293:
                                                        return 4
                                                    else:
                                                        return 4
                                                else:
                                                    return 4
                                        else:
                                            return 0
                                    else:
                                        return 5
                                else:
                                    return 3
            else:
                if f[10] <= 6038.1945:
                    if f[10] <= 611.1317:
                        return 8
                    else:
                        if f[0] <= 149.4351:
                            if f[31] <= 0.1839:
                                if f[21] <= 66.1131:
                                    if f[10] <= 5605.8655:
                                        if f[4] <= 0.1876:
                                            if f[57] <= 0.3232:
                                                if f[15] <= 0.5156:
                                                    if f[19] <= 0.5556:
                                                        if f[13] <= 37.7299:
                                                            return 1
                                                        else:
                                                            return 9
                                                    else:
                                                        if f[39] <= 6.4109:
                                                            return 8
                                                        else:
                                                            if f[41] <= 2.1935:
                                                                return 2
                                                            else:
                                                                return 2
                                                else:
                                                    return 7
                                            else:
                                                if f[5] <= 0.1114:
                                                    return 2
                                                else:
                                                    return 0
                                        else:
                                            return 1
                                    else:
                                        return 6
                                else:
                                    if f[53] <= 0.2207:
                                        return 3
                                    else:
                                        return 4
                            else:
                                if f[60] <= 132.3926:
                                    return 4
                                else:
                                    return 4
                        else:
                            if f[57] <= 0.3004:
                                if f[17] <= 0.1873:
                                    return 5
                                else:
                                    if f[6] <= 0.4966:
                                        return 4
                                    else:
                                        return 4
                            else:
                                return 5
                else:
                    if f[3] <= 0.0691:
                        if f[19] <= 0.6705:
                            if f[61] <= 0.3594:
                                if f[26] <= 145.6353:
                                    if f[14] <= 0.4321:
                                        return 9
                                    else:
                                        if f[62] <= 226.3699:
                                            if f[63] <= 102.5208:
                                                if f[28] <= 0.9602:
                                                    return 9
                                                else:
                                                    return 9
                                            else:
                                                return 9
                                        else:
                                            return 0
                                else:
                                    return 3
                            else:
                                return 1
                        else:
                            if f[57] <= 0.332:
                                if f[50] <= 69.6787:
                                    return 2
                                else:
                                    return 8
                            else:
                                if f[51] <= 43.8286:
                                    return 3
                                else:
                                    return 6
                    else:
                        if f[68] <= 16.2256:
                            if f[70] <= 0.2017:
                                return 2
                            else:
                                return 6
                        else:
                            if f[7] <= 52.9902:
                                return 1
                            else:
                                if f[28] <= 1.1351:
                                    if f[34] <= 1.1102:
                                        return 3
                                    else:
                                        if f[56] <= 110.9199:
                                            return 9
                                        else:
                                            return 3
                                else:
                                    if f[24] <= 0.0278:
                                        if f[17] <= 0.4226:
                                            return 3
                                        else:
                                            return 1
                                    else:
                                        if f[65] <= 97.9323:
                                            if f[3] <= 0.2396:
                                                return 9
                                            else:
                                                return 9
                                        else:
                                            return 3
        else:
            if f[3] <= 0.364:
                if f[17] <= 0.0987:
                    if f[67] <= 198.5028:
                        return 2
                    else:
                        return 8
                else:
                    if f[44] <= 0.3024:
                        return 5
                    else:
                        if f[70] <= 0.2273:
                            if f[35] <= 0.0146:
                                return 4
                            else:
                                return 4
                        else:
                            if f[57] <= 0.315:
                                return 5
                            else:
                                return 4
            else:
                if f[26] <= 85.7849:
                    if f[27] <= 146.8523:
                        if f[43] <= 1.232:
                            return 4
                        else:
                            return 5
                    else:
                        if f[4] <= 0.3194:
                            if f[27] <= 147.7549:
                                return 5
                            else:
                                if f[13] <= 3.2721:
                                    return 5
                                else:
                                    return 5
                        else:
                            if f[50] <= 18.3447:
                                return 5
                            else:
                                return 4
                else:
                    return 1


def _tree_11(f):
    if f[22] <= 0.525:
        if f[53] <= 0.3089:
            return 8
        else:
            return 8
    else:
        if f[7] <= 168.6123:
            if f[19] <= 0.7042:
                if f[68] <= 70.1992:
                    if f[16] <= 0.927:
                        if f[17] <= 0.071:
                            if f[70] <= 0.293:
                                if f[11] <= 90.3817:
                                    return 9
                                else:
                                    return 9
                            else:
                                if f[11] <= 120.1625:
                                    if f[57] <= 0.3577:
                                        if f[50] <= 28.6025:
                                            return 4
                                        else:
                                            return 0
                                    else:
                                        return 6
                                else:
                                    return 9
                        else:
                            if f[33] <= 0.3269:
                                if f[17] <= 0.3103:
                                    if f[58] <= 34.2803:
                                        if f[44] <= 0.4535:
                                            return 3
                                        else:
                                            return 1
                                    else:
                                        if f[39] <= 32.5435:
                                            return 3
                                        else:
                                            if f[9] <= 0.0938:
                                                return 3
                                            else:
                                                return 7
                                else:
                                    if f[10] <= 12469.6058:
                                        if f[68] <= 31.9221:
                                            return 4
                                        else:
                                            return 9
                                    else:
                                        return 3
                            else:
                                if f[51] <= 101.1352:
                                    if f[61] <= 0.2461:
                                        return 2
                                    else:
                                        return 3
                                else:
                                    if f[35] <= 0.1963:
                                        return 9
                                    else:
                                        return 9
                    else:
                        if f[32] <= 0.1343:
                            if f[11] <= 120.2227:
                                if f[31] <= 0.0054:
                                    return 6
                                else:
                                    return 3
                            else:
                                if f[31] <= 0.0178:
                                    return 1
                                else:
                                    return 3
                        else:
                            if f[41] <= 2.8259:
                                if f[36] <= 0.0798:
                                    if f[38] <= 0.0096:
                                        return 1
                                    else:
                                        return 1
                                else:
                                    if f[16] <= 0.9425:
                                        return 9
                                    else:
                                        if f[54] <= 55.3926:
                                            if f[64] <= 111.4382:
                                                return 2
                                            else:
                                                if f[41] <= 1.2956:
                                                    return 2
                                                else:
                                                    return 2
                                        else:
                                            return 5
                            else:
                                if f[14] <= 0.7146:
                                    return 4
                                else:
                                    return 4
                else:
                    if f[12] <= 50.9935:
                        if f[6] <= 0.0263:
                            return 7
                        else:
                            if f[66] <= 75.3002:
                                return 1
                            else:
                                return 9
                    else:
                        if f[17] <= 0.1636:
                            if f[52] <= 175.9355:
                                return 9
                            else:
                                if f[57] <= 0.3155:
                                    return 9
                                else:
                                    return 3
                        else:
                            if f[12] <= 64.4018:
                                return 9
                            else:
                                return 3
            else:
                if f[34] <= 1.0176:
                    if f[10] <= 4706.9172:
                        if f[23] <= 0.2643:
                            if f[68] <= 74.1959:
                                if f[30] <= 0.1147:
                                    if f[22] <= 1.0244:
                                        return 6
                                    else:
                                        if f[26] <= 54.2178:
                                            return 0
                                        else:
                                            return 2
                                else:
                                    if f[58] <= 44.3062:
                                        if f[6] <= 0.0203:
                                            return 7
                                        else:
                                            return 1
                                    else:
                                        if f[57] <= 0.3008:
                                            return 5
                                        else:
                                            return 5
                            else:
                                if f[67] <= 81.0511:
                                    return 0
                                else:
                                    return 8
                        else:
                            if f[25] <= 0.3633:
                                if f[61] <= 0.2646:
                                    if f[5] <= 0.0005:
                                        return 4
                                    else:
                                        return 1
                                else:
                                    return 0
                            else:
                                return 6
                    else:
                        if f[29] <= 15.4304:
                            if f[68] <= 26.1348:
                                if f[52] <= 177.7944:
                                    if f[40] <= 0.4872:
                                        if f[4] <= 0.0089:
                                            return 0
                                        else:
                                            if f[11] <= 95.8742:
                                                if f[59] <= 123.6982:
                                                    if f[13] <= 8.4972:
                                                        return 6
                                                    else:
                                                        return 6
                                                else:
                                                    return 1
                                            else:
                                                return 4
                                    else:
                                        if f[24] <= 0.2327:
                                            if f[58] <= 15.2334:
                                                return 9
                                            else:
                                                if f[9] <= 0.047:
                                                    if f[55] <= 106.0771:
                                                        return 6
                                                    else:
                                                        return 1
                                                else:
                                                    return 6
                                        else:
                                            return 0
                                else:
                                    if f[26] <= 78.0253:
                                        return 0
                                    else:
                                        return 0
                            else:
                                if f[3] <= 0.0829:
                                    if f[38] <= 0.6173:
                                        if f[68] <= 87.4574:
                                            if f[62] <= 104.0089:
                                                if f[34] <= 0.8631:
                                                    return 6
                                                else:
                                                    return 6
                                            else:
                                                if f[33] <= 0.0122:
                                                    if f[22] <= 1.1267:
                                                        return 7
                                                    else:
                                                        return 1
                                                else:
                                                    if f[51] <= 32.7314:
                                                        return 2
                                                    else:
                                                        if f[24] <= 0.0208:
                                                            return 4
                                                        else:
                                                            if f[59] <= 111.0291:
                                                                if f[52] <= 110.1546:
                                                                    return 0
                                                                else:
                                                                    if f[10] <= 14128.3336:
                                                                        if f[40] <= 0.5046:
                                                                            return 6
                                                                        else:
                                                                            return 6
                                                                    else:
                                                                        return 6
                                                            else:
                                                                if f[66] <= 88.3266:
                                                                    return 1
                                                                else:
                                                                    return 4
                                        else:
                                            if f[6] <= 0.0961:
                                                if f[27] <= 128.0:
                                                    return 7
                                                else:
                                                    return 8
                                            else:
                                                return 9
                                    else:
                                        if f[23] <= 0.0796:
                                            if f[62] <= 131.1027:
                                                return 7
                                            else:
                                                return 0
                                        else:
                                            if f[9] <= 0.0261:
                                                return 3
                                            else:
                                                return 6
                                else:
                                    if f[54] <= 31.5002:
                                        if f[1] <= 53.6604:
                                            return 0
                                        else:
                                            return 4
                                    else:
                                        if f[31] <= 0.0066:
                                            return 1
                                        else:
                                            if f[32] <= 0.043:
                                                return 3
                                            else:
                                                if f[48] <= 124.5283:
                                                    return 3
                                                else:
                                                    return 3
                        else:
                            if f[64] <= 96.0604:
                                if f[19] <= 1.2119:
                                    if f[42] <= 1.0339:
                                        if f[70] <= 0.3849:
                                            return 1
                                        else:
                                            return 0
                                    else:
                                        if f[0] <= 116.2476:
                                            if f[61] <= 0.3389:
                                                return 3
                                            else:
                                                return 6
                                        else:
                                            return 1
                                else:
                                    return 7
                            else:
                                if f[63] <= 198.3289:
                                    if f[26] <= 90.3256:
                                        if f[68] <= 53.8402:
                                            return 0
                                        else:
                                            return 4
                                    else:
                                        if f[19] <= 1.05:
                                            if f[25] <= 0.3613:
                                                if f[33] <= 0.0481:
                                                    if f[17] <= 0.3711:
                                                        return 1
                                                    else:
                                                        return 1
                                                else:
                                                    if f[19] <= 0.9712:
                                                        if f[27] <= 159.3257:
                                                            return 7
                                                        else:
                                                            return 3
                                                    else:
                                                        return 0
                                            else:
                                                if f[0] <= 86.0083:
                                                    return 6
                                                else:
                                                    return 6
                                        else:
                                            if f[38] <= 0.2798:
                                                return 7
                                            else:
                                                return 7
                                else:
                                    return 5
                else:
                    if f[1] <= 16.6147:
                        if f[11] <= 68.5059:
                            if f[31] <= 0.0016:
                                if f[55] <= 98.6045:
                                    if f[46] <= 87.5374:
                                        if f[69] <= 0.1194:
                                            if f[43] <= 1.8132:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            if f[50] <= 80.5557:
                                                if f[64] <= 105.0447:
                                                    if f[61] <= 0.291:
                                                        return 1
                                                    else:
                                                        return 1
                                                else:
                                                    if f[39] <= 34.0638:
                                                        return 0
                                                    else:
                                                        return 7
                                            else:
                                                return 8
                                    else:
                                        if f[40] <= 0.5465:
                                            if f[40] <= 0.3325:
                                                return 7
                                            else:
                                                return 7
                                        else:
                                            return 8
                                else:
                                    if f[70] <= 0.152:
                                        return 8
                                    else:
                                        return 2
                            else:
                                if f[9] <= 0.0199:
                                    if f[4] <= 0.0107:
                                        return 7
                                    else:
                                        if f[10] <= 2982.1815:
                                            return 4
                                        else:
                                            return 2
                                else:
                                    if f[67] <= 66.7401:
                                        if f[49] <= 0.3389:
                                            return 7
                                        else:
                                            return 7
                                    else:
                                        return 7
                        else:
                            if f[65] <= 133.2534:
                                if f[51] <= 65.3148:
                                    if f[34] <= 1.0989:
                                        if f[43] <= 3.1711:
                                            if f[51] <= 29.9959:
                                                return 0
                                            else:
                                                return 6
                                        else:
                                            return 2
                                    else:
                                        if f[41] <= 1.7378:
                                            if f[49] <= 0.2246:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            return 2
                                else:
                                    if f[20] <= 0.0928:
                                        return 9
                                    else:
                                        if f[35] <= 0.3584:
                                            return 6
                                        else:
                                            return 7
                            else:
                                if f[18] <= 0.0261:
                                    return 8
                                else:
                                    return 1
                    else:
                        if f[57] <= 0.3291:
                            if f[18] <= 0.0102:
                                if f[4] <= 0.1992:
                                    if f[38] <= 0.2536:
                                        return 2
                                    else:
                                        return 7
                                else:
                                    if f[54] <= 43.4445:
                                        return 4
                                    else:
                                        return 4
                            else:
                                if f[11] <= 72.2657:
                                    if f[43] <= 1.4834:
                                        if f[21] <= -7.5645:
                                            if f[46] <= 24.0137:
                                                return 0
                                            else:
                                                return 5
                                        else:
                                            if f[43] <= 0.5864:
                                                return 1
                                            else:
                                                if f[2] <= 0.0:
                                                    if f[0] <= 67.4177:
                                                        return 2
                                                    else:
                                                        if f[5] <= 0.0007:
                                                            return 2
                                                        else:
                                                            return 2
                                                else:
                                                    return 0
                                    else:
                                        if f[17] <= 0.1057:
                                            if f[15] <= 0.0361:
                                                return 5
                                            else:
                                                return 5
                                        else:
                                            if f[59] <= 92.8463:
                                                if f[58] <= 44.6494:
                                                    if f[18] <= 0.1646:
                                                        return 7
                                                    else:
                                                        return 6
                                                else:
                                                    if f[32] <= 0.1577:
                                                        return 4
                                                    else:
                                                        return 4
                                            else:
                                                if f[4] <= 0.0925:
                                                    if f[68] <= 22.4164:
                                                        return 0
                                                    else:
                                                        return 2
                                                else:
                                                    if f[23] <= 0.1787:
                                                        return 4
                                                    else:
                                                        return 1
                                else:
                                    if f[30] <= 0.332:
                                        if f[42] <= 0.9689:
                                            return 3
                                        else:
                                            if f[58] <= 18.9551:
                                                return 1
                                            else:
                                                if f[20] <= 0.1141:
                                                    return 2
                                                else:
                                                    return 2
                                    else:
                                        if f[62] <= 90.7545:
                                            if f[49] <= 0.3057:
                                                return 4
                                            else:
                                                return 9
                                        else:
                                            if f[3] <= 0.12:
                                                if f[22] <= 1.3165:
                                                    return 2
                                                else:
                                                    return 5
                                            else:
                                                if f[16] <= 0.917:
                                                    return 3
                                                else:
                                                    return 4
                        else:
                            if f[31] <= 0.0139:
                                return 0
                            else:
                                return 0
        else:
            if f[26] <= 83.5514:
                if f[27] <= 173.8996:
                    if f[4] <= 0.2483:
                        if f[58] <= 49.4205:
                            if f[50] <= 17.9277:
                                if f[50] <= 17.2725:
                                    if f[25] <= 0.2676:
                                        if f[10] <= 1579.7069:
                                            return 4
                                        else:
                                            return 4
                                    else:
                                        if f[40] <= 0.5416:
                                            return 0
                                        else:
                                            if f[9] <= 0.0259:
                                                return 5
                                            else:
                                                return 4
                                else:
                                    if f[65] <= 198.3073:
                                        return 2
                                    else:
                                        return 1
                            else:
                                if f[27] <= 125.3885:
                                    return 3
                                else:
                                    if f[18] <= 0.4372:
                                        if f[59] <= 133.959:
                                            return 5
                                        else:
                                            return 5
                                    else:
                                        return 5
                        else:
                            if f[20] <= 0.4988:
                                if f[39] <= 38.3228:
                                    return 9
                                else:
                                    return 2
                            else:
                                return 8
                    else:
                        if f[29] <= -38.571:
                            return 1
                        else:
                            if f[68] <= 20.3057:
                                return 1
                            else:
                                if f[59] <= 129.8242:
                                    return 4
                                else:
                                    return 4
                else:
                    if f[31] <= 0.1558:
                        if f[35] <= 0.0783:
                            return 5
                        else:
                            return 5
                    else:
                        if f[30] <= 0.1285:
                            if f[15] <= 0.0237:
                                if f[65] <= 209.6441:
                                    return 4
                                else:
                                    return 5
                            else:
                                if f[24] <= 0.0057:
                                    return 5
                                else:
                                    return 5
                        else:
                            if f[27] <= 205.454:
                                if f[43] <= 1.8888:
                                    return 4
                                else:
                                    return 4
                            else:
                                return 5
            else:
                if f[61] <= 0.3474:
                    if f[9] <= 0.072:
                        if f[52] <= 173.1371:
                            return 4
                        else:
                            return 4
                    else:
                        if f[68] <= 23.7148:
                            if f[2] <= 0.0089:
                                return 1
                            else:
                                return 5
                        else:
                            if f[35] <= 0.0898:
                                if f[9] <= 0.3866:
                                    if f[52] <= 159.4893:
                                        return 3
                                    else:
                                        return 3
                                else:
                                    return 4
                            else:
                                if f[65] <= 110.4494:
                                    return 7
                                else:
                                    return 9
                else:
                    if f[42] <= 1.0139:
                        if f[16] <= 0.9971:
                            return 1
                        else:
                            return 1
                    else:
                        return 6


def _tree_12(f):
    if f[2] <= 0.691:
        if f[22] <= 3.1757:
            if f[11] <= 92.4182:
                if f[22] <= 1.1279:
                    if f[67] <= 92.3984:
                        if f[40] <= 0.493:
                            if f[31] <= 0.0042:
                                if f[18] <= 0.0088:
                                    if f[52] <= 72.6133:
                                        return 8
                                    else:
                                        if f[54] <= 46.1326:
                                            if f[51] <= 21.0816:
                                                return 2
                                            else:
                                                return 7
                                        else:
                                            if f[12] <= 65.0684:
                                                return 7
                                            else:
                                                return 7
                                else:
                                    if f[9] <= 0.0144:
                                        return 0
                                    else:
                                        if f[33] <= 0.0674:
                                            return 7
                                        else:
                                            if f[41] <= 1.2571:
                                                return 1
                                            else:
                                                return 6
                            else:
                                if f[70] <= 0.3565:
                                    return 7
                                else:
                                    return 2
                        else:
                            if f[33] <= 0.3447:
                                if f[21] <= -9.5026:
                                    if f[20] <= 0.1041:
                                        return 6
                                    else:
                                        if f[57] <= 0.3281:
                                            return 7
                                        else:
                                            return 7
                                else:
                                    if f[15] <= 0.2711:
                                        if f[39] <= 41.4575:
                                            if f[43] <= 1.772:
                                                return 6
                                            else:
                                                return 6
                                        else:
                                            return 2
                                    else:
                                        if f[11] <= 74.5578:
                                            if f[39] <= 10.0752:
                                                return 4
                                            else:
                                                return 2
                                        else:
                                            return 0
                            else:
                                if f[21] <= 16.1602:
                                    if f[70] <= 0.1287:
                                        return 0
                                    else:
                                        if f[50] <= 91.0791:
                                            return 2
                                        else:
                                            return 2
                                else:
                                    if f[19] <= 0.5987:
                                        return 3
                                    else:
                                        if f[49] <= 0.1123:
                                            if f[41] <= 1.581:
                                                return 7
                                            else:
                                                return 7
                                        else:
                                            if f[38] <= 0.5801:
                                                return 8
                                            else:
                                                return 2
                    else:
                        if f[57] <= 0.3094:
                            if f[29] <= -8.9824:
                                if f[54] <= 85.0781:
                                    return 7
                                else:
                                    return 7
                            else:
                                if f[20] <= 0.0945:
                                    return 9
                                else:
                                    if f[63] <= 198.9263:
                                        if f[22] <= 0.9557:
                                            return 8
                                        else:
                                            return 8
                                    else:
                                        return 4
                        else:
                            if f[51] <= 55.9004:
                                return 1
                            else:
                                if f[54] <= 66.1494:
                                    return 9
                                else:
                                    return 0
                else:
                    if f[31] <= 0.1504:
                        if f[34] <= 1.1346:
                            if f[23] <= 0.2017:
                                if f[70] <= 0.3615:
                                    if f[64] <= 68.5163:
                                        if f[16] <= 0.8548:
                                            return 3
                                        else:
                                            return 1
                                    else:
                                        if f[2] <= 0.0219:
                                            if f[8] <= 0.1006:
                                                if f[55] <= 162.4551:
                                                    if f[53] <= 0.3086:
                                                        return 2
                                                    else:
                                                        return 2
                                                else:
                                                    return 4
                                            else:
                                                if f[22] <= 1.3097:
                                                    return 3
                                                else:
                                                    return 5
                                        else:
                                            if f[21] <= 1.3315:
                                                return 8
                                            else:
                                                return 3
                                else:
                                    if f[52] <= 65.7324:
                                        return 3
                                    else:
                                        if f[67] <= 126.9189:
                                            return 1
                                        else:
                                            return 1
                            else:
                                if f[64] <= 126.6094:
                                    if f[29] <= -5.6228:
                                        if f[32] <= 0.1963:
                                            if f[60] <= 140.7185:
                                                if f[40] <= 0.5384:
                                                    return 6
                                                else:
                                                    return 6
                                            else:
                                                return 0
                                        else:
                                            return 1
                                    else:
                                        if f[11] <= 63.1773:
                                            if f[13] <= 15.0747:
                                                return 0
                                            else:
                                                return 0
                                        else:
                                            if f[60] <= 95.0498:
                                                if f[67] <= 135.9098:
                                                    return 1
                                                else:
                                                    return 1
                                            else:
                                                if f[54] <= 36.325:
                                                    if f[41] <= 1.5983:
                                                        if f[29] <= 4.2761:
                                                            return 0
                                                        else:
                                                            return 0
                                                    else:
                                                        return 1
                                                else:
                                                    return 2
                                else:
                                    if f[70] <= 0.2386:
                                        if f[30] <= 0.0645:
                                            return 2
                                        else:
                                            return 0
                                    else:
                                        if f[65] <= 164.1237:
                                            if f[52] <= 88.7457:
                                                return 6
                                            else:
                                                if f[44] <= 0.6244:
                                                    if f[47] <= 130.4111:
                                                        if f[26] <= 72.7685:
                                                            return 0
                                                        else:
                                                            if f[40] <= 0.4693:
                                                                return 0
                                                            else:
                                                                return 0
                                                    else:
                                                        return 0
                                                else:
                                                    return 0
                                        else:
                                            return 1
                        else:
                            if f[3] <= 0.1929:
                                if f[21] <= 1.978:
                                    if f[40] <= 0.5152:
                                        if f[48] <= 113.0156:
                                            return 7
                                        else:
                                            return 7
                                    else:
                                        if f[63] <= 155.9677:
                                            if f[20] <= 0.1388:
                                                if f[54] <= 46.1719:
                                                    return 2
                                                else:
                                                    return 2
                                            else:
                                                return 7
                                        else:
                                            return 0
                                else:
                                    if f[3] <= 0.1838:
                                        if f[59] <= 99.5441:
                                            if f[4] <= 0.0212:
                                                if f[21] <= 45.1089:
                                                    if f[9] <= 0.0121:
                                                        return 2
                                                    else:
                                                        return 2
                                                else:
                                                    return 0
                                            else:
                                                if f[46] <= 35.5918:
                                                    return 9
                                                else:
                                                    return 4
                                        else:
                                            if f[45] <= 0.014:
                                                return 9
                                            else:
                                                if f[26] <= 79.8284:
                                                    return 5
                                                else:
                                                    return 6
                                    else:
                                        return 1
                            else:
                                if f[34] <= 1.4299:
                                    if f[27] <= 168.6703:
                                        if f[4] <= 0.0627:
                                            if f[40] <= 0.5286:
                                                if f[41] <= 1.4598:
                                                    if f[17] <= 0.1311:
                                                        return 2
                                                    else:
                                                        return 2
                                                else:
                                                    return 0
                                            else:
                                                if f[50] <= 14.8193:
                                                    return 2
                                                else:
                                                    return 2
                                        else:
                                            if f[46] <= 30.4057:
                                                return 1
                                            else:
                                                return 3
                                    else:
                                        if f[70] <= 0.2496:
                                            return 5
                                        else:
                                            return 5
                                else:
                                    if f[45] <= 0.0571:
                                        return 1
                                    else:
                                        if f[54] <= 17.4248:
                                            return 2
                                        else:
                                            if f[17] <= 0.2521:
                                                return 5
                                            else:
                                                return 5
                    else:
                        if f[57] <= 0.1948:
                            if f[42] <= 1.7934:
                                if f[14] <= 0.6075:
                                    return 4
                                else:
                                    if f[61] <= 0.1939:
                                        if f[68] <= 25.6279:
                                            return 4
                                        else:
                                            return 4
                                    else:
                                        return 4
                            else:
                                return 5
                        else:
                            if f[66] <= 142.436:
                                if f[57] <= 0.2953:
                                    if f[4] <= 0.1255:
                                        return 2
                                    else:
                                        if f[51] <= 121.386:
                                            if f[46] <= 31.2695:
                                                return 0
                                            else:
                                                if f[21] <= 24.3636:
                                                    return 4
                                                else:
                                                    return 4
                                        else:
                                            return 2
                                else:
                                    if f[43] <= 1.5:
                                        return 0
                                    else:
                                        if f[58] <= 30.1162:
                                            return 6
                                        else:
                                            return 1
                            else:
                                if f[63] <= 182.439:
                                    if f[24] <= 0.0017:
                                        return 1
                                    else:
                                        if f[49] <= 0.3359:
                                            if f[39] <= 37.4404:
                                                return 4
                                            else:
                                                return 4
                                        else:
                                            return 1
                                else:
                                    if f[25] <= 0.2822:
                                        return 5
                                    else:
                                        return 5
            else:
                if f[70] <= 0.3438:
                    if f[17] <= 0.1108:
                        if f[40] <= 0.5292:
                            if f[4] <= 0.0017:
                                if f[18] <= 0.0012:
                                    return 0
                                else:
                                    return 0
                            else:
                                if f[21] <= 17.4742:
                                    if f[2] <= 0.0146:
                                        return 7
                                    else:
                                        return 7
                                else:
                                    return 3
                        else:
                            if f[64] <= 180.4225:
                                if f[14] <= 0.3594:
                                    return 2
                                else:
                                    if f[28] <= 0.7736:
                                        return 6
                                    else:
                                        if f[23] <= 0.0669:
                                            if f[33] <= 0.05:
                                                return 7
                                            else:
                                                if f[5] <= 0.0003:
                                                    return 9
                                                else:
                                                    return 9
                                        else:
                                            if f[69] <= 0.3218:
                                                if f[44] <= 0.1473:
                                                    if f[63] <= 130.5015:
                                                        return 3
                                                    else:
                                                        return 0
                                                else:
                                                    return 2
                                            else:
                                                if f[36] <= 0.1657:
                                                    return 9
                                                else:
                                                    return 9
                            else:
                                return 0
                    else:
                        if f[26] <= 91.1431:
                            if f[19] <= 0.6701:
                                if f[54] <= 32.426:
                                    if f[18] <= 0.0936:
                                        return 3
                                    else:
                                        return 4
                                else:
                                    if f[48] <= 161.1406:
                                        return 9
                                    else:
                                        return 3
                            else:
                                if f[23] <= 0.3594:
                                    if f[44] <= 0.1826:
                                        return 0
                                    else:
                                        if f[36] <= 0.2886:
                                            if f[28] <= 1.0671:
                                                return 6
                                            else:
                                                if f[27] <= 159.4848:
                                                    return 3
                                                else:
                                                    return 5
                                        else:
                                            return 2
                                else:
                                    return 6
                        else:
                            if f[46] <= 26.5465:
                                if f[13] <= 36.4516:
                                    if f[27] <= 156.2997:
                                        if f[22] <= 1.3889:
                                            return 6
                                        else:
                                            return 1
                                    else:
                                        if f[51] <= 138.6162:
                                            return 3
                                        else:
                                            return 3
                                else:
                                    return 9
                            else:
                                if f[62] <= 138.7604:
                                    if f[57] <= 0.2461:
                                        if f[37] <= 0.067:
                                            return 9
                                        else:
                                            return 9
                                    else:
                                        if f[55] <= 111.5703:
                                            return 3
                                        else:
                                            if f[36] <= 0.1619:
                                                if f[3] <= 0.1001:
                                                    return 9
                                                else:
                                                    return 3
                                            else:
                                                return 1
                                else:
                                    if f[19] <= 0.9363:
                                        if f[22] <= 1.0322:
                                            if f[1] <= -0.9141:
                                                return 3
                                            else:
                                                return 3
                                        else:
                                            return 3
                                    else:
                                        return 3
                else:
                    if f[29] <= 4.2868:
                        if f[53] <= 0.3435:
                            if f[47] <= 115.3711:
                                if f[55] <= 38.3174:
                                    return 6
                                else:
                                    if f[53] <= 0.2896:
                                        return 3
                                    else:
                                        if f[58] <= 27.3408:
                                            return 1
                                        else:
                                            return 9
                            else:
                                if f[38] <= 0.0193:
                                    return 5
                                else:
                                    return 4
                        else:
                            if f[12] <= 61.096:
                                if f[17] <= 0.2203:
                                    if f[50] <= 27.1904:
                                        return 0
                                    else:
                                        if f[39] <= 17.3154:
                                            return 1
                                        else:
                                            return 2
                                else:
                                    if f[14] <= 0.5734:
                                        return 4
                                    else:
                                        return 6
                            else:
                                if f[6] <= 0.0686:
                                    return 6
                                else:
                                    return 6
                    else:
                        if f[56] <= 111.5742:
                            if f[45] <= 0.3452:
                                if f[36] <= 0.3123:
                                    if f[70] <= 0.3645:
                                        if f[23] <= 0.1633:
                                            return 1
                                        else:
                                            return 9
                                    else:
                                        if f[61] <= 0.3654:
                                            if f[0] <= 119.2988:
                                                return 1
                                            else:
                                                return 1
                                        else:
                                            return 1
                                else:
                                    return 0
                            else:
                                return 6
                        else:
                            if f[40] <= 0.5362:
                                if f[16] <= 0.9946:
                                    if f[19] <= 0.9596:
                                        return 0
                                    else:
                                        if f[49] <= 0.332:
                                            return 0
                                        else:
                                            return 0
                                else:
                                    return 6
                            else:
                                if f[35] <= 0.6924:
                                    if f[70] <= 0.3658:
                                        if f[44] <= 0.3931:
                                            return 3
                                        else:
                                            return 0
                                    else:
                                        if f[53] <= 0.3475:
                                            return 1
                                        else:
                                            return 1
                                else:
                                    return 7
        else:
            if f[7] <= 204.1834:
                if f[44] <= 0.3281:
                    return 5
                else:
                    if f[10] <= 2301.6312:
                        return 4
                    else:
                        return 4
            else:
                if f[14] <= 0.4927:
                    if f[5] <= 0.0:
                        return 4
                    else:
                        return 4
                else:
                    if f[40] <= 0.7154:
                        if f[40] <= 0.3728:
                            return 4
                        else:
                            if f[11] <= 85.5334:
                                if f[29] <= -16.4075:
                                    if f[36] <= 0.0281:
                                        return 0
                                    else:
                                        return 5
                                else:
                                    if f[1] <= 107.8124:
                                        if f[39] <= 66.4314:
                                            return 8
                                        else:
                                            if f[37] <= 0.048:
                                                return 5
                                            else:
                                                return 5
                                    else:
                                        return 5
                            else:
                                return 1
                    else:
                        if f[6] <= 0.8206:
                            return 5
                        else:
                            return 4
    else:
        if f[52] <= 84.0962:
            return 8
        else:
            return 8


def _tree_13(f):
    if f[22] <= 0.5878:
        if f[33] <= 0.321:
            if f[46] <= 103.2037:
                return 8
            else:
                return 6
        else:
            if f[58] <= 77.7288:
                return 8
            else:
                return 8
    else:
        if f[7] <= 204.8248:
            if f[31] <= 0.1471:
                if f[11] <= 83.1624:
                    if f[23] <= 0.2446:
                        if f[6] <= 0.1507:
                            if f[3] <= 0.0:
                                if f[42] <= 1.0552:
                                    if f[10] <= 1730.3061:
                                        return 4
                                    else:
                                        return 7
                                else:
                                    if f[22] <= 0.9837:
                                        if f[25] <= 0.25:
                                            return 8
                                        else:
                                            return 8
                                    else:
                                        return 2
                            else:
                                if f[40] <= 0.4196:
                                    if f[60] <= 48.6299:
                                        return 6
                                    else:
                                        if f[48] <= 190.4645:
                                            if f[3] <= 0.0456:
                                                if f[17] <= 0.0022:
                                                    return 0
                                                else:
                                                    return 7
                                            else:
                                                if f[61] <= 0.0879:
                                                    return 4
                                                else:
                                                    if f[59] <= 71.8447:
                                                        return 0
                                                    else:
                                                        return 7
                                        else:
                                            return 2
                                else:
                                    if f[70] <= 0.3129:
                                        if f[45] <= 0.0239:
                                            if f[50] <= 100.0078:
                                                if f[49] <= 0.2979:
                                                    if f[20] <= 0.2632:
                                                        if f[56] <= 42.5564:
                                                            return 2
                                                        else:
                                                            return 2
                                                    else:
                                                        return 2
                                                else:
                                                    return 1
                                            else:
                                                return 5
                                        else:
                                            if f[28] <= 1.0519:
                                                if f[9] <= 0.0514:
                                                    if f[25] <= 0.2295:
                                                        if f[57] <= 0.1035:
                                                            return 5
                                                        else:
                                                            return 3
                                                    else:
                                                        if f[13] <= 19.1591:
                                                            return 2
                                                        else:
                                                            return 9
                                                else:
                                                    if f[62] <= 94.2408:
                                                        return 2
                                                    else:
                                                        if f[32] <= 0.4713:
                                                            return 7
                                                        else:
                                                            return 7
                                            else:
                                                if f[43] <= 2.7736:
                                                    if f[62] <= 114.0677:
                                                        return 8
                                                    else:
                                                        return 0
                                                else:
                                                    return 4
                                    else:
                                        if f[68] <= 29.8867:
                                            if f[44] <= 0.4163:
                                                return 1
                                            else:
                                                return 1
                                        else:
                                            if f[42] <= 0.9777:
                                                if f[7] <= 65.1743:
                                                    return 8
                                                else:
                                                    return 2
                                            else:
                                                if f[6] <= 0.016:
                                                    if f[13] <= 17.4838:
                                                        return 0
                                                    else:
                                                        return 7
                                                else:
                                                    if f[39] <= 26.7793:
                                                        return 6
                                                    else:
                                                        return 6
                        else:
                            if f[16] <= 0.3068:
                                if f[47] <= 115.6426:
                                    return 9
                                else:
                                    return 8
                            else:
                                if f[53] <= 0.3232:
                                    if f[27] <= 128.0:
                                        if f[39] <= 28.0024:
                                            if f[56] <= 105.9131:
                                                if f[56] <= 64.3975:
                                                    return 2
                                                else:
                                                    return 7
                                            else:
                                                return 4
                                        else:
                                            if f[31] <= 0.0081:
                                                return 2
                                            else:
                                                return 2
                                    else:
                                        if f[48] <= 131.4896:
                                            if f[38] <= 0.001:
                                                return 4
                                            else:
                                                if f[20] <= 0.7291:
                                                    if f[66] <= 146.0409:
                                                        if f[25] <= 0.2812:
                                                            return 9
                                                        else:
                                                            return 8
                                                    else:
                                                        if f[8] <= 0.0085:
                                                            return 1
                                                        else:
                                                            return 5
                                                else:
                                                    return 2
                                        else:
                                            if f[25] <= 0.1396:
                                                return 4
                                            else:
                                                if f[68] <= 14.8779:
                                                    return 0
                                                else:
                                                    if f[49] <= 0.0938:
                                                        return 5
                                                    else:
                                                        return 5
                                else:
                                    if f[5] <= 0.1108:
                                        if f[43] <= 2.2578:
                                            return 0
                                        else:
                                            if f[63] <= 104.426:
                                                return 3
                                            else:
                                                return 8
                                    else:
                                        if f[23] <= 0.0479:
                                            return 1
                                        else:
                                            return 1
                    else:
                        if f[34] <= 1.1314:
                            if f[4] <= 0.0066:
                                if f[28] <= 1.1224:
                                    if f[0] <= 50.5427:
                                        if f[28] <= 1.06:
                                            return 0
                                        else:
                                            return 0
                                    else:
                                        if f[25] <= 0.2871:
                                            return 1
                                        else:
                                            return 6
                                else:
                                    return 0
                            else:
                                if f[56] <= 110.9434:
                                    if f[66] <= 151.619:
                                        if f[9] <= 0.0547:
                                            if f[37] <= 0.0066:
                                                return 6
                                            else:
                                                return 0
                                        else:
                                            if f[25] <= 0.3525:
                                                return 6
                                            else:
                                                return 6
                                    else:
                                        return 1
                                else:
                                    if f[36] <= 0.1357:
                                        return 0
                                    else:
                                        if f[70] <= 0.2898:
                                            if f[20] <= 0.097:
                                                return 3
                                            else:
                                                if f[9] <= 0.029:
                                                    return 2
                                                else:
                                                    return 2
                                        else:
                                            if f[22] <= 1.0759:
                                                return 7
                                            else:
                                                if f[50] <= 31.6811:
                                                    return 6
                                                else:
                                                    if f[11] <= 70.4368:
                                                        return 0
                                                    else:
                                                        return 0
                        else:
                            if f[5] <= 0.0034:
                                if f[15] <= 0.4417:
                                    if f[47] <= 130.4437:
                                        return 2
                                    else:
                                        return 2
                                else:
                                    return 0
                            else:
                                if f[35] <= 0.4448:
                                    if f[40] <= 0.6776:
                                        if f[4] <= 0.0281:
                                            return 0
                                        else:
                                            if f[8] <= 0.0017:
                                                return 5
                                            else:
                                                return 1
                                    else:
                                        return 2
                                else:
                                    return 7
                else:
                    if f[19] <= 0.6949:
                        if f[17] <= 0.0764:
                            if f[70] <= 0.3501:
                                if f[19] <= 0.6704:
                                    if f[22] <= 0.8945:
                                        if f[40] <= 0.7588:
                                            if f[1] <= -24.4724:
                                                return 9
                                            else:
                                                return 9
                                        else:
                                            return 3
                                    else:
                                        if f[63] <= 75.1079:
                                            return 9
                                        else:
                                            return 9
                                else:
                                    if f[23] <= 0.0583:
                                        return 9
                                    else:
                                        return 0
                            else:
                                if f[1] <= -11.9087:
                                    return 3
                                else:
                                    if f[33] <= 0.0564:
                                        return 6
                                    else:
                                        return 1
                        else:
                            if f[17] <= 0.1619:
                                if f[43] <= 2.6081:
                                    if f[37] <= 0.0746:
                                        if f[32] <= 0.1462:
                                            return 6
                                        else:
                                            return 3
                                    else:
                                        return 2
                                else:
                                    if f[11] <= 99.791:
                                        return 1
                                    else:
                                        if f[33] <= 0.1967:
                                            return 9
                                        else:
                                            return 9
                            else:
                                if f[26] <= 73.9054:
                                    if f[68] <= 13.2148:
                                        return 1
                                    else:
                                        if f[28] <= 1.1209:
                                            return 9
                                        else:
                                            return 2
                                else:
                                    if f[46] <= 29.8154:
                                        return 2
                                    else:
                                        if f[27] <= 135.7168:
                                            if f[15] <= 0.1328:
                                                return 3
                                            else:
                                                return 1
                                        else:
                                            return 3
                    else:
                        if f[70] <= 0.343:
                            if f[31] <= 0.0108:
                                if f[33] <= 0.2292:
                                    if f[50] <= 69.6787:
                                        if f[38] <= 0.5264:
                                            if f[56] <= 127.6439:
                                                if f[4] <= 0.0383:
                                                    if f[58] <= 45.6191:
                                                        return 6
                                                    else:
                                                        if f[40] <= 0.4766:
                                                            return 0
                                                        else:
                                                            return 6
                                                else:
                                                    return 3
                                            else:
                                                if f[56] <= 148.6082:
                                                    return 2
                                                else:
                                                    return 0
                                        else:
                                            if f[33] <= 0.0963:
                                                return 3
                                            else:
                                                return 0
                                    else:
                                        if f[66] <= 82.0037:
                                            if f[18] <= 0.0171:
                                                return 7
                                            else:
                                                return 6
                                        else:
                                            return 9
                                else:
                                    if f[39] <= 13.6135:
                                        if f[43] <= 2.3259:
                                            return 9
                                        else:
                                            return 9
                                    else:
                                        if f[51] <= 65.9199:
                                            if f[5] <= 0.0439:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            return 0
                            else:
                                if f[46] <= 37.4902:
                                    if f[52] <= 167.1963:
                                        if f[28] <= 1.2017:
                                            if f[46] <= 29.2705:
                                                if f[19] <= 0.7398:
                                                    return 6
                                                else:
                                                    return 6
                                            else:
                                                return 0
                                        else:
                                            if f[31] <= 0.0293:
                                                return 2
                                            else:
                                                return 8
                                    else:
                                        if f[8] <= 0.1139:
                                            return 3
                                        else:
                                            return 3
                                else:
                                    if f[5] <= 0.0105:
                                        if f[70] <= 0.228:
                                            return 4
                                        else:
                                            return 2
                                    else:
                                        if f[45] <= 0.1406:
                                            if f[49] <= 0.3242:
                                                if f[12] <= 71.2087:
                                                    return 3
                                                else:
                                                    return 8
                                            else:
                                                return 7
                                        else:
                                            return 3
                        else:
                            if f[29] <= 11.647:
                                if f[33] <= 0.04:
                                    if f[29] <= -17.0071:
                                        if f[19] <= 0.9916:
                                            if f[67] <= 103.8288:
                                                return 6
                                            else:
                                                return 6
                                        else:
                                            return 0
                                    else:
                                        if f[68] <= 69.8316:
                                            if f[48] <= 130.5264:
                                                return 6
                                            else:
                                                if f[23] <= 0.0632:
                                                    return 1
                                                else:
                                                    return 1
                                        else:
                                            if f[2] <= 0.0059:
                                                return 7
                                            else:
                                                return 7
                                else:
                                    if f[53] <= 0.2686:
                                        if f[40] <= 0.4553:
                                            return 3
                                        else:
                                            return 3
                                    else:
                                        if f[5] <= 0.2234:
                                            if f[19] <= 0.9987:
                                                if f[11] <= 118.8256:
                                                    if f[27] <= 102.9672:
                                                        return 2
                                                    else:
                                                        if f[37] <= 0.0085:
                                                            return 3
                                                        else:
                                                            if f[70] <= 0.3634:
                                                                return 6
                                                            else:
                                                                return 6
                                                else:
                                                    return 9
                                            else:
                                                return 0
                                        else:
                                            return 1
                            else:
                                if f[35] <= 0.4752:
                                    if f[25] <= 0.3555:
                                        if f[2] <= 0.0089:
                                            return 1
                                        else:
                                            return 0
                                    else:
                                        if f[26] <= 110.5517:
                                            if f[6] <= 0.0991:
                                                return 0
                                            else:
                                                return 2
                                        else:
                                            if f[38] <= 0.0795:
                                                return 1
                                            else:
                                                return 1
                                else:
                                    if f[60] <= 99.2295:
                                        if f[67] <= 103.5585:
                                            return 1
                                        else:
                                            return 2
                                    else:
                                        if f[1] <= 28.7112:
                                            if f[12] <= 66.3361:
                                                if f[18] <= 0.0133:
                                                    if f[40] <= 0.4635:
                                                        return 7
                                                    else:
                                                        return 7
                                                else:
                                                    return 0
                                            else:
                                                return 2
                                        else:
                                            return 0
            else:
                if f[11] <= 72.2482:
                    if f[70] <= 0.3324:
                        if f[68] <= 16.3008:
                            return 0
                        else:
                            if f[41] <= 1.0622:
                                if f[58] <= 31.1709:
                                    return 1
                                else:
                                    return 4
                            else:
                                if f[55] <= 80.6377:
                                    return 4
                                else:
                                    if f[42] <= 0.7867:
                                        return 2
                                    else:
                                        if f[17] <= 0.8826:
                                            if f[22] <= 1.2557:
                                                return 4
                                            else:
                                                return 4
                                        else:
                                            return 4
                    else:
                        if f[48] <= 110.0566:
                            return 1
                        else:
                            return 5
                else:
                    if f[57] <= 0.3584:
                        if f[20] <= 0.1569:
                            if f[11] <= 92.1479:
                                if f[15] <= 0.1211:
                                    return 4
                                else:
                                    return 7
                            else:
                                if f[54] <= 51.5295:
                                    return 3
                                else:
                                    return 5
                        else:
                            if f[1] <= 72.2795:
                                if f[46] <= 39.1182:
                                    if f[57] <= 0.3357:
                                        if f[66] <= 142.436:
                                            return 2
                                        else:
                                            return 6
                                    else:
                                        return 0
                                else:
                                    return 9
                            else:
                                if f[60] <= 161.7439:
                                    if f[31] <= 0.2826:
                                        return 4
                                    else:
                                        return 4
                                else:
                                    if f[64] <= 152.2223:
                                        return 1
                                    else:
                                        return 4
                    else:
                        if f[1] <= 67.2488:
                            if f[48] <= 149.8652:
                                if f[21] <= 14.8945:
                                    return 1
                                else:
                                    return 6
                            else:
                                if f[67] <= 123.8828:
                                    return 0
                                else:
                                    return 4
                        else:
                            if f[10] <= 15011.4017:
                                return 1
                            else:
                                return 1
        else:
            if f[31] <= 0.3176:
                if f[31] <= 0.0:
                    if f[42] <= 1.5039:
                        return 2
                    else:
                        return 8
                else:
                    if f[57] <= 0.2832:
                        if f[27] <= 164.5862:
                            if f[40] <= 0.6002:
                                if f[26] <= 62.2147:
                                    return 5
                                else:
                                    return 5
                            else:
                                if f[7] <= 213.1807:
                                    return 2
                                else:
                                    return 4
                        else:
                            return 5
                    else:
                        if f[60] <= 145.1416:
                            if f[19] <= 0.8325:
                                return 4
                            else:
                                return 1
                        else:
                            if f[30] <= 0.0161:
                                return 5
                            else:
                                return 0
            else:
                if f[9] <= 0.0:
                    return 5
                else:
                    if f[5] <= 0.0831:
                        if f[64] <= 147.6348:
                            return 4
                        else:
                            return 4
                    else:
                        return 1


def _tree_14(f):
    if f[22] <= 0.546:
        if f[69] <= 0.2567:
            return 8
        else:
            if f[25] <= 0.3195:
                return 6
            else:
                return 8
    else:
        if f[22] <= 3.2858:
            if f[19] <= 0.6935:
                if f[17] <= 0.0854:
                    if f[5] <= 0.0222:
                        if f[68] <= 96.2461:
                            if f[16] <= 0.1812:
                                if f[69] <= 0.0179:
                                    return 8
                                else:
                                    if f[25] <= 0.2734:
                                        return 7
                                    else:
                                        return 7
                            else:
                                if f[23] <= 0.0218:
                                    return 9
                                else:
                                    if f[14] <= 0.7652:
                                        if f[16] <= 0.3572:
                                            return 3
                                        else:
                                            if f[36] <= 0.5039:
                                                return 5
                                            else:
                                                return 7
                                    else:
                                        return 2
                        else:
                            if f[50] <= 109.2625:
                                return 9
                            else:
                                return 9
                    else:
                        if f[49] <= 0.1769:
                            if f[2] <= 0.0249:
                                return 2
                            else:
                                if f[3] <= 0.0442:
                                    return 9
                                else:
                                    return 1
                        else:
                            if f[6] <= 0.0467:
                                if f[63] <= 104.5659:
                                    return 6
                                else:
                                    return 9
                            else:
                                return 9
                else:
                    if f[26] <= 92.8075:
                        if f[64] <= 168.9254:
                            if f[2] <= 0.017:
                                if f[21] <= -34.9925:
                                    return 2
                                else:
                                    if f[69] <= 0.0402:
                                        return 3
                                    else:
                                        if f[67] <= 155.1628:
                                            if f[26] <= 76.773:
                                                if f[38] <= 0.0626:
                                                    return 1
                                                else:
                                                    if f[6] <= 0.0718:
                                                        if f[9] <= 0.0173:
                                                            return 0
                                                        else:
                                                            return 9
                                                    else:
                                                        if f[46] <= 28.29:
                                                            return 2
                                                        else:
                                                            return 4
                                            else:
                                                return 3
                                        else:
                                            if f[30] <= 0.5251:
                                                if f[27] <= 161.43:
                                                    return 4
                                                else:
                                                    return 4
                                            else:
                                                return 5
                            else:
                                if f[9] <= 0.0198:
                                    return 5
                                else:
                                    if f[61] <= 0.2877:
                                        if f[60] <= 98.4099:
                                            return 9
                                        else:
                                            return 9
                                    else:
                                        if f[45] <= 0.2697:
                                            return 3
                                        else:
                                            return 9
                        else:
                            if f[33] <= 0.4285:
                                return 7
                            else:
                                if f[47] <= 91.8975:
                                    return 5
                                else:
                                    return 5
                    else:
                        if f[34] <= 1.1638:
                            if f[33] <= 0.056:
                                if f[36] <= 0.1461:
                                    return 9
                                else:
                                    return 1
                            else:
                                if f[36] <= 0.5271:
                                    if f[13] <= 50.9832:
                                        if f[57] <= 0.1973:
                                            return 3
                                        else:
                                            return 3
                                    else:
                                        return 3
                                else:
                                    return 1
                        else:
                            if f[24] <= 0.0078:
                                return 2
                            else:
                                if f[30] <= 0.3951:
                                    return 3
                                else:
                                    return 9
            else:
                if f[70] <= 0.2955:
                    if f[4] <= 0.1365:
                        if f[22] <= 0.973:
                            if f[70] <= 0.2301:
                                if f[29] <= 13.0267:
                                    if f[49] <= 0.1035:
                                        return 7
                                    else:
                                        if f[32] <= 0.2651:
                                            return 8
                                        else:
                                            return 6
                                else:
                                    if f[2] <= 0.6672:
                                        return 8
                                    else:
                                        return 8
                            else:
                                if f[28] <= 0.9345:
                                    if f[10] <= 2237.5427:
                                        return 7
                                    else:
                                        return 7
                                else:
                                    if f[68] <= 81.7037:
                                        return 0
                                    else:
                                        if f[47] <= 31.0332:
                                            return 9
                                        else:
                                            return 8
                        else:
                            if f[11] <= 75.6909:
                                if f[41] <= 1.1859:
                                    if f[13] <= 38.9547:
                                        if f[40] <= 0.6077:
                                            if f[26] <= 37.7831:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            if f[32] <= 0.2683:
                                                return 5
                                            else:
                                                return 2
                                    else:
                                        if f[46] <= 84.2527:
                                            if f[38] <= 0.1831:
                                                return 2
                                            else:
                                                return 7
                                        else:
                                            return 8
                                else:
                                    if f[68] <= 19.373:
                                        if f[25] <= 0.2939:
                                            if f[35] <= 0.0693:
                                                if f[39] <= 22.7241:
                                                    return 5
                                                else:
                                                    return 5
                                            else:
                                                if f[40] <= 0.4645:
                                                    return 4
                                                else:
                                                    return 2
                                        else:
                                            if f[30] <= 0.6182:
                                                if f[39] <= 16.9272:
                                                    return 0
                                                else:
                                                    return 0
                                            else:
                                                return 8
                                    else:
                                        if f[21] <= 1.6257:
                                            if f[62] <= 75.2567:
                                                if f[14] <= 0.5381:
                                                    return 4
                                                else:
                                                    if f[57] <= 0.2207:
                                                        return 2
                                                    else:
                                                        return 0
                                            else:
                                                if f[16] <= 0.9871:
                                                    if f[52] <= 99.1945:
                                                        return 7
                                                    else:
                                                        return 7
                                                else:
                                                    return 4
                                        else:
                                            if f[40] <= 0.4382:
                                                if f[53] <= 0.2213:
                                                    if f[4] <= 0.0024:
                                                        return 0
                                                    else:
                                                        return 1
                                                else:
                                                    return 6
                                            else:
                                                if f[29] <= 48.3733:
                                                    if f[49] <= 0.2266:
                                                        if f[33] <= 0.6367:
                                                            if f[24] <= 0.1259:
                                                                return 2
                                                            else:
                                                                return 2
                                                        else:
                                                            return 5
                                                    else:
                                                        if f[44] <= 0.0843:
                                                            return 5
                                                        else:
                                                            return 2
                                                else:
                                                    return 8
                            else:
                                if f[45] <= 0.096:
                                    if f[33] <= 0.2865:
                                        if f[45] <= 0.0278:
                                            return 9
                                        else:
                                            if f[44] <= 0.1125:
                                                return 6
                                            else:
                                                return 9
                                    else:
                                        return 2
                                else:
                                    if f[47] <= 75.4548:
                                        if f[42] <= 1.1156:
                                            return 6
                                        else:
                                            return 0
                                    else:
                                        if f[64] <= 161.4616:
                                            if f[41] <= 1.2528:
                                                return 9
                                            else:
                                                if f[31] <= 0.0132:
                                                    return 3
                                                else:
                                                    return 3
                                        else:
                                            return 2
                    else:
                        if f[10] <= 7240.9642:
                            if f[31] <= 0.15:
                                if f[54] <= 29.9369:
                                    if f[54] <= 18.3447:
                                        return 2
                                    else:
                                        return 1
                                else:
                                    if f[62] <= 76.2783:
                                        if f[18] <= 0.009:
                                            return 8
                                        else:
                                            return 0
                                    else:
                                        if f[48] <= 107.7154:
                                            return 7
                                        else:
                                            return 4
                            else:
                                if f[1] <= 114.8335:
                                    if f[62] <= 184.0616:
                                        if f[63] <= 118.578:
                                            return 7
                                        else:
                                            if f[40] <= 0.5596:
                                                if f[20] <= 0.2319:
                                                    return 4
                                                else:
                                                    if f[16] <= 0.9936:
                                                        return 4
                                                    else:
                                                        return 4
                                            else:
                                                if f[29] <= -0.4729:
                                                    return 5
                                                else:
                                                    return 4
                                    else:
                                        return 4
                                else:
                                    return 5
                        else:
                            if f[50] <= 43.5732:
                                if f[37] <= 0.0408:
                                    return 2
                                else:
                                    if f[40] <= 0.5948:
                                        if f[23] <= 0.1792:
                                            return 9
                                        else:
                                            return 3
                                    else:
                                        return 4
                            else:
                                if f[61] <= 0.2256:
                                    return 3
                                else:
                                    return 3
                else:
                    if f[6] <= 0.085:
                        if f[23] <= 0.1556:
                            if f[54] <= 96.1018:
                                if f[59] <= 55.9502:
                                    if f[28] <= 1.0511:
                                        if f[51] <= 13.458:
                                            return 2
                                        else:
                                            if f[0] <= 45.0786:
                                                if f[47] <= 20.8408:
                                                    if f[52] <= 154.9688:
                                                        return 6
                                                    else:
                                                        return 1
                                                else:
                                                    if f[13] <= 42.0669:
                                                        return 7
                                                    else:
                                                        return 7
                                            else:
                                                return 0
                                    else:
                                        return 1
                                else:
                                    if f[62] <= 116.3594:
                                        if f[50] <= 59.3213:
                                            return 6
                                        else:
                                            return 6
                                    else:
                                        if f[29] <= -19.2427:
                                            if f[8] <= 0.1644:
                                                return 6
                                            else:
                                                return 6
                                        else:
                                            if f[53] <= 0.3213:
                                                if f[16] <= 0.2595:
                                                    return 8
                                                else:
                                                    if f[60] <= 128.6328:
                                                        return 3
                                                    else:
                                                        return 2
                                            else:
                                                if f[68] <= 55.5024:
                                                    return 1
                                                else:
                                                    return 1
                            else:
                                if f[1] <= 1.5356:
                                    if f[16] <= 0.0208:
                                        return 7
                                    else:
                                        return 7
                                else:
                                    return 6
                        else:
                            if f[63] <= 132.5283:
                                if f[5] <= 0.0204:
                                    if f[30] <= 0.0846:
                                        return 0
                                    else:
                                        if f[52] <= 120.3008:
                                            if f[24] <= 0.2053:
                                                return 7
                                            else:
                                                return 7
                                        else:
                                            if f[12] <= 55.4515:
                                                return 8
                                            else:
                                                if f[22] <= 1.0482:
                                                    return 1
                                                else:
                                                    return 6
                                else:
                                    if f[61] <= 0.2734:
                                        return 0
                                    else:
                                        if f[61] <= 0.3169:
                                            return 6
                                        else:
                                            if f[50] <= 31.0083:
                                                return 6
                                            else:
                                                if f[38] <= 0.1433:
                                                    return 6
                                                else:
                                                    return 6
                            else:
                                if f[11] <= 117.7992:
                                    if f[40] <= 0.5808:
                                        if f[54] <= 38.7202:
                                            if f[29] <= 5.7857:
                                                if f[54] <= 17.6436:
                                                    return 6
                                                else:
                                                    if f[26] <= 88.4097:
                                                        return 0
                                                    else:
                                                        return 0
                                            else:
                                                return 0
                                        else:
                                            if f[4] <= 0.0175:
                                                if f[10] <= 5458.6667:
                                                    return 0
                                                else:
                                                    return 0
                                            else:
                                                if f[22] <= 1.2005:
                                                    return 2
                                                else:
                                                    return 5
                                    else:
                                        if f[7] <= 47.7158:
                                            return 8
                                        else:
                                            if f[24] <= 0.1362:
                                                return 2
                                            else:
                                                return 6
                                else:
                                    if f[34] <= 0.764:
                                        return 1
                                    else:
                                        return 6
                    else:
                        if f[64] <= 135.9574:
                            if f[70] <= 0.3612:
                                if f[55] <= 160.8848:
                                    if f[34] <= 0.8092:
                                        if f[20] <= 0.2023:
                                            if f[26] <= 116.386:
                                                return 1
                                            else:
                                                return 1
                                        else:
                                            return 6
                                    else:
                                        if f[11] <= 122.8183:
                                            if f[2] <= 0.071:
                                                if f[9] <= 0.0444:
                                                    if f[57] <= 0.3222:
                                                        return 4
                                                    else:
                                                        return 0
                                                else:
                                                    if f[63] <= 126.6875:
                                                        if f[53] <= 0.3441:
                                                            if f[16] <= 0.9181:
                                                                return 6
                                                            else:
                                                                if f[54] <= 25.1431:
                                                                    return 2
                                                                else:
                                                                    return 2
                                                        else:
                                                            if f[67] <= 89.8615:
                                                                return 6
                                                            else:
                                                                return 6
                                                    else:
                                                        if f[18] <= 0.2433:
                                                            if f[45] <= 0.2783:
                                                                return 6
                                                            else:
                                                                return 3
                                                        else:
                                                            return 1
                                            else:
                                                if f[1] <= 14.0032:
                                                    return 0
                                                else:
                                                    return 0
                                        else:
                                            return 3
                                else:
                                    if f[20] <= 0.3552:
                                        if f[7] <= 153.0273:
                                            return 1
                                        else:
                                            return 5
                                    else:
                                        if f[19] <= 0.9014:
                                            return 1
                                        else:
                                            return 1
                            else:
                                if f[29] <= -0.1233:
                                    if f[14] <= 0.6094:
                                        if f[61] <= 0.3623:
                                            return 3
                                        else:
                                            if f[10] <= 19742.1256:
                                                return 6
                                            else:
                                                return 6
                                    else:
                                        if f[41] <= 1.1999:
                                            return 1
                                        else:
                                            return 1
                                else:
                                    if f[34] <= 0.9799:
                                        if f[67] <= 65.5149:
                                            return 7
                                        else:
                                            if f[43] <= 1.2812:
                                                return 0
                                            else:
                                                if f[25] <= 0.3672:
                                                    if f[37] <= 0.0102:
                                                        return 1
                                                    else:
                                                        return 1
                                                else:
                                                    return 1
                                    else:
                                        return 2
                        else:
                            if f[31] <= 0.1102:
                                if f[58] <= 39.6393:
                                    if f[6] <= 0.3127:
                                        if f[28] <= 1.2976:
                                            if f[23] <= 0.4209:
                                                return 0
                                            else:
                                                return 0
                                        else:
                                            return 0
                                    else:
                                        return 5
                                else:
                                    if f[62] <= 89.9606:
                                        return 5
                                    else:
                                        return 9
                            else:
                                if f[51] <= 178.6377:
                                    if f[1] <= 48.2898:
                                        return 3
                                    else:
                                        if f[31] <= 0.3169:
                                            return 4
                                        else:
                                            return 0
                                else:
                                    return 1
        else:
            if f[27] <= 158.1708:
                if f[70] <= 0.2933:
                    if f[31] <= 0.0564:
                        if f[31] <= 0.0018:
                            return 8
                        else:
                            return 5
                    else:
                        if f[11] <= 49.3301:
                            return 4
                        else:
                            return 5
                else:
                    if f[38] <= 0.001:
                        return 1
                    else:
                        return 1
            else:
                if f[7] <= 184.499:
                    return 1
                else:
                    if f[14] <= 0.4523:
                        return 4
                    else:
                        if f[40] <= 0.6702:
                            return 5
                        else:
                            if f[6] <= 0.8084:
                                if f[33] <= 0.4548:
                                    return 5
                                else:
                                    return 5
                            else:
                                return 4


def _tree_15(f):
    if f[2] <= 0.3604:
        if f[7] <= 170.5898:
            if f[19] <= 0.7718:
                if f[3] <= 0.0544:
                    if f[6] <= 0.0426:
                        if f[46] <= 38.4238:
                            if f[25] <= 0.335:
                                return 4
                            else:
                                return 6
                        else:
                            if f[10] <= 7244.8637:
                                if f[19] <= 0.6684:
                                    if f[21] <= 36.1313:
                                        return 7
                                    else:
                                        return 1
                                else:
                                    if f[22] <= 1.0643:
                                        return 2
                                    else:
                                        return 2
                            else:
                                if f[13] <= 19.7329:
                                    if f[12] <= 45.0493:
                                        return 7
                                    else:
                                        return 7
                                else:
                                    if f[61] <= 0.3301:
                                        if f[35] <= 0.4463:
                                            return 1
                                        else:
                                            return 9
                                    else:
                                        if f[1] <= 16.2655:
                                            if f[7] <= 53.6445:
                                                return 6
                                            else:
                                                return 3
                                        else:
                                            return 8
                    else:
                        if f[2] <= 0.0:
                            if f[31] <= 0.0:
                                return 8
                            else:
                                if f[9] <= 0.0082:
                                    return 4
                                else:
                                    return 4
                        else:
                            if f[5] <= 0.3184:
                                if f[11] <= 75.5613:
                                    return 3
                                else:
                                    if f[40] <= 0.8607:
                                        if f[56] <= 153.6825:
                                            if f[41] <= 1.1339:
                                                return 9
                                            else:
                                                if f[9] <= 0.0435:
                                                    return 9
                                                else:
                                                    return 9
                                        else:
                                            return 2
                                    else:
                                        return 3
                            else:
                                if f[17] <= 0.0447:
                                    return 3
                                else:
                                    return 1
                else:
                    if f[26] <= 76.8836:
                        if f[32] <= 0.5015:
                            if f[64] <= 95.0842:
                                if f[41] <= 2.1103:
                                    if f[14] <= 0.613:
                                        return 1
                                    else:
                                        return 1
                                else:
                                    return 9
                            else:
                                if f[57] <= 0.2608:
                                    if f[33] <= 0.5:
                                        if f[34] <= 1.0754:
                                            return 2
                                        else:
                                            return 2
                                    else:
                                        return 4
                                else:
                                    if f[41] <= 2.0703:
                                        if f[65] <= 122.9375:
                                            if f[19] <= 0.7122:
                                                return 0
                                            else:
                                                return 0
                                        else:
                                            return 2
                                    else:
                                        if f[48] <= 146.0059:
                                            return 6
                                        else:
                                            return 3
                        else:
                            return 5
                    else:
                        if f[28] <= 1.2103:
                            if f[29] <= 10.0955:
                                if f[45] <= 0.1071:
                                    return 1
                                else:
                                    if f[2] <= 0.0014:
                                        return 3
                                    else:
                                        if f[70] <= 0.3414:
                                            return 3
                                        else:
                                            return 3
                            else:
                                if f[5] <= 0.1204:
                                    if f[8] <= 0.0393:
                                        if f[37] <= 0.0542:
                                            return 9
                                        else:
                                            return 9
                                    else:
                                        return 3
                                else:
                                    if f[4] <= 0.0544:
                                        return 1
                                    else:
                                        return 3
                        else:
                            if f[16] <= 0.8627:
                                if f[58] <= 42.2412:
                                    return 3
                                else:
                                    return 9
                            else:
                                if f[17] <= 0.2771:
                                    return 2
                                else:
                                    if f[29] <= 11.907:
                                        return 4
                                    else:
                                        return 1
            else:
                if f[49] <= 0.3206:
                    if f[4] <= 0.0747:
                        if f[18] <= 0.022:
                            if f[40] <= 0.3904:
                                if f[51] <= 63.9013:
                                    if f[17] <= 0.0065:
                                        return 7
                                    else:
                                        return 7
                                else:
                                    return 2
                            else:
                                if f[60] <= 84.7573:
                                    if f[58] <= 66.7412:
                                        return 8
                                    else:
                                        return 8
                                else:
                                    if f[33] <= 0.1637:
                                        if f[3] <= 0.0037:
                                            if f[21] <= 35.6816:
                                                return 4
                                            else:
                                                return 9
                                        else:
                                            if f[10] <= 6088.6554:
                                                return 0
                                            else:
                                                return 0
                                    else:
                                        if f[42] <= 1.3425:
                                            if f[21] <= -4.145:
                                                if f[57] <= 0.3047:
                                                    return 7
                                                else:
                                                    return 7
                                            else:
                                                if f[9] <= 0.052:
                                                    if f[15] <= 0.2681:
                                                        return 6
                                                    else:
                                                        if f[52] <= 173.5997:
                                                            return 2
                                                        else:
                                                            return 3
                                                else:
                                                    return 7
                                        else:
                                            if f[33] <= 0.7236:
                                                if f[64] <= 152.9956:
                                                    return 2
                                                else:
                                                    return 2
                                            else:
                                                return 4
                        else:
                            if f[34] <= 1.195:
                                if f[68] <= 39.7266:
                                    if f[39] <= 8.6238:
                                        if f[2] <= 0.0107:
                                            return 3
                                        else:
                                            return 6
                                    else:
                                        if f[29] <= -27.9939:
                                            if f[9] <= 0.002:
                                                return 7
                                            else:
                                                if f[46] <= 22.0608:
                                                    return 6
                                                else:
                                                    return 0
                                        else:
                                            if f[25] <= 0.2941:
                                                if f[21] <= -15.8928:
                                                    return 0
                                                else:
                                                    return 5
                                            else:
                                                if f[30] <= 0.417:
                                                    return 0
                                                else:
                                                    return 0
                                else:
                                    if f[28] <= 0.9575:
                                        return 3
                                    else:
                                        if f[40] <= 0.504:
                                            if f[34] <= 1.065:
                                                return 0
                                            else:
                                                return 1
                                        else:
                                            if f[42] <= 1.1932:
                                                if f[10] <= 6981.1327:
                                                    return 2
                                                else:
                                                    return 2
                                            else:
                                                return 6
                            else:
                                if f[67] <= 92.0918:
                                    if f[35] <= 0.6658:
                                        if f[20] <= 0.5142:
                                            if f[37] <= 0.0298:
                                                return 0
                                            else:
                                                if f[25] <= 0.2671:
                                                    return 7
                                                else:
                                                    return 6
                                        else:
                                            return 5
                                    else:
                                        if f[48] <= 134.1796:
                                            return 7
                                        else:
                                            return 2
                                else:
                                    if f[30] <= 0.2553:
                                        return 2
                                    else:
                                        if f[56] <= 82.2627:
                                            return 2
                                        else:
                                            return 2
                    else:
                        if f[19] <= 1.1671:
                            if f[70] <= 0.3028:
                                if f[20] <= 0.2059:
                                    if f[37] <= 0.0408:
                                        if f[44] <= 0.7055:
                                            if f[69] <= 0.2302:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            return 4
                                    else:
                                        if f[49] <= 0.2476:
                                            return 8
                                        else:
                                            if f[50] <= 43.6973:
                                                return 3
                                            else:
                                                return 3
                                else:
                                    if f[37] <= 0.0011:
                                        return 1
                                    else:
                                        if f[54] <= 37.5771:
                                            if f[36] <= 0.2241:
                                                return 4
                                            else:
                                                return 4
                                        else:
                                            return 7
                            else:
                                if f[26] <= 50.1728:
                                    if f[52] <= 131.9629:
                                        return 0
                                    else:
                                        return 0
                                else:
                                    if f[22] <= 1.7716:
                                        if f[53] <= 0.3252:
                                            if f[55] <= 149.7119:
                                                if f[64] <= 128.1543:
                                                    if f[20] <= 0.1558:
                                                        return 2
                                                    else:
                                                        return 2
                                                else:
                                                    return 5
                                            else:
                                                return 1
                                        else:
                                            return 1
                                    else:
                                        return 6
                        else:
                            if f[22] <= 1.1946:
                                return 7
                            else:
                                if f[68] <= 21.0143:
                                    return 0
                                else:
                                    return 4
                else:
                    if f[29] <= -0.6677:
                        if f[41] <= 1.5366:
                            if f[45] <= 0.27:
                                if f[11] <= 128.7019:
                                    if f[44] <= 0.5501:
                                        if f[32] <= 0.146:
                                            if f[38] <= 0.5161:
                                                return 6
                                            else:
                                                if f[70] <= 0.3601:
                                                    return 0
                                                else:
                                                    return 6
                                        else:
                                            return 6
                                    else:
                                        if f[41] <= 1.1727:
                                            return 7
                                        else:
                                            return 6
                                else:
                                    return 3
                            else:
                                if f[63] <= 135.2692:
                                    if f[61] <= 0.3683:
                                        return 3
                                    else:
                                        return 6
                                else:
                                    if f[64] <= 126.6655:
                                        return 0
                                    else:
                                        return 0
                        else:
                            if f[61] <= 0.3606:
                                if f[2] <= 0.0025:
                                    if f[38] <= 0.5752:
                                        return 6
                                    else:
                                        return 6
                                else:
                                    if f[5] <= 0.0066:
                                        return 3
                                    else:
                                        if f[49] <= 0.3604:
                                            if f[7] <= 89.8232:
                                                return 0
                                            else:
                                                return 6
                                        else:
                                            return 7
                            else:
                                if f[45] <= 0.1958:
                                    if f[23] <= 0.1077:
                                        return 1
                                    else:
                                        return 1
                                else:
                                    if f[65] <= 91.936:
                                        return 8
                                    else:
                                        return 9
                    else:
                        if f[21] <= 6.3899:
                            if f[63] <= 147.8914:
                                if f[41] <= 1.5047:
                                    if f[4] <= 0.0046:
                                        return 0
                                    else:
                                        if f[7] <= 126.2031:
                                            if f[44] <= 0.0883:
                                                return 7
                                            else:
                                                if f[21] <= -42.7144:
                                                    return 7
                                                else:
                                                    return 7
                                        else:
                                            return 0
                                else:
                                    if f[44] <= 0.2719:
                                        if f[58] <= 57.5664:
                                            return 1
                                        else:
                                            return 2
                                    else:
                                        if f[23] <= 0.5393:
                                            return 7
                                        else:
                                            return 6
                            else:
                                if f[20] <= 0.0823:
                                    return 0
                                else:
                                    if f[41] <= 1.4039:
                                        return 0
                                    else:
                                        return 0
                        else:
                            if f[23] <= 0.3179:
                                if f[4] <= 0.021:
                                    if f[50] <= 76.2266:
                                        if f[39] <= 18.6206:
                                            return 0
                                        else:
                                            return 1
                                    else:
                                        return 7
                                else:
                                    if f[2] <= 0.0054:
                                        if f[34] <= 0.8553:
                                            return 1
                                        else:
                                            return 1
                                    else:
                                        return 3
                            else:
                                if f[62] <= 151.2217:
                                    if f[48] <= 121.1318:
                                        if f[33] <= 0.1316:
                                            return 1
                                        else:
                                            return 2
                                    else:
                                        if f[29] <= 30.4131:
                                            if f[28] <= 1.1207:
                                                return 6
                                            else:
                                                return 6
                                        else:
                                            return 1
                                else:
                                    if f[25] <= 0.3641:
                                        if f[58] <= 19.6682:
                                            return 0
                                        else:
                                            return 0
                                    else:
                                        return 5
        else:
            if f[63] <= 177.5238:
                if f[26] <= 90.2235:
                    if f[17] <= 0.4267:
                        if f[45] <= 0.0:
                            if f[7] <= 190.6973:
                                return 8
                            else:
                                return 8
                        else:
                            if f[27] <= 149.6126:
                                if f[50] <= 14.1592:
                                    if f[58] <= 13.9189:
                                        return 1
                                    else:
                                        return 2
                                else:
                                    if f[55] <= 164.4844:
                                        if f[61] <= 0.2558:
                                            return 5
                                        else:
                                            return 0
                                    else:
                                        if f[14] <= 0.6962:
                                            return 1
                                        else:
                                            return 4
                            else:
                                if f[3] <= 0.0988:
                                    return 1
                                else:
                                    if f[19] <= 1.1385:
                                        if f[31] <= 0.1792:
                                            return 5
                                        else:
                                            return 5
                                    else:
                                        return 5
                    else:
                        if f[44] <= 0.3501:
                            if f[61] <= 0.2312:
                                return 5
                            else:
                                return 1
                        else:
                            if f[27] <= 167.3495:
                                if f[40] <= 0.6344:
                                    if f[60] <= 119.0644:
                                        return 4
                                    else:
                                        return 4
                                else:
                                    return 2
                            else:
                                if f[27] <= 174.2167:
                                    return 5
                                else:
                                    return 4
                else:
                    if f[70] <= 0.3523:
                        if f[28] <= 1.2707:
                            if f[62] <= 111.8534:
                                return 6
                            else:
                                return 3
                        else:
                            if f[68] <= 26.98:
                                if f[65] <= 183.3479:
                                    if f[41] <= 1.26:
                                        return 4
                                    else:
                                        return 5
                                else:
                                    return 1
                            else:
                                return 9
                    else:
                        if f[49] <= 0.3154:
                            return 1
                        else:
                            return 1
            else:
                if f[11] <= 85.0359:
                    if f[60] <= 135.0225:
                        if f[31] <= 0.1545:
                            return 5
                        else:
                            return 4
                    else:
                        if f[4] <= 0.3339:
                            return 5
                        else:
                            if f[7] <= 203.7201:
                                return 4
                            else:
                                if f[37] <= 0.0234:
                                    return 5
                                else:
                                    return 5
                else:
                    if f[41] <= 1.3964:
                        return 1
                    else:
                        return 4
    else:
        if f[22] <= 0.6182:
            if f[58] <= 98.4092:
                if f[9] <= 0.0061:
                    if f[24] <= 0.0068:
                        return 8
                    else:
                        return 8
                else:
                    if f[44] <= 0.0024:
                        return 7
                    else:
                        if f[46] <= 83.0166:
                            return 2
                        else:
                            return 9
            else:
                return 8
        else:
            if f[60] <= 42.7568:
                return 6
            else:
                if f[43] <= 2.3771:
                    if f[4] <= 0.1876:
                        if f[0] <= 112.1416:
                            if f[40] <= 0.5615:
                                if f[33] <= 0.24:
                                    return 7
                                else:
                                    return 7
                            else:
                                return 6
                        else:
                            if f[38] <= 0.0667:
                                return 8
                            else:
                                return 8
                    else:
                        return 4
                else:
                    if f[4] <= 0.0347:
                        return 0
                    else:
                        return 3


def _tree_16(f):
    if f[7] <= 168.594:
        if f[40] <= 0.5893:
            if f[25] <= 0.2871:
                if f[55] <= 76.7188:
                    if f[47] <= 45.4532:
                        if f[14] <= 0.8355:
                            if f[44] <= 0.5083:
                                if f[57] <= 0.2584:
                                    if f[33] <= 0.5244:
                                        if f[54] <= 32.751:
                                            return 2
                                        else:
                                            return 2
                                    else:
                                        if f[20] <= 0.0:
                                            return 7
                                        else:
                                            return 8
                                else:
                                    return 0
                            else:
                                if f[21] <= 13.3794:
                                    return 7
                                else:
                                    return 7
                        else:
                            if f[46] <= 28.7322:
                                return 4
                            else:
                                return 2
                    else:
                        if f[5] <= 0.0273:
                            if f[5] <= 0.0026:
                                if f[25] <= 0.1572:
                                    return 7
                                else:
                                    return 7
                            else:
                                return 7
                        else:
                            if f[58] <= 31.5889:
                                return 7
                            else:
                                if f[62] <= 115.218:
                                    return 7
                                else:
                                    return 2
                else:
                    if f[54] <= 50.6362:
                        if f[44] <= 0.7204:
                            if f[19] <= 1.1478:
                                if f[6] <= 0.0225:
                                    return 0
                                else:
                                    if f[2] <= 0.0015:
                                        if f[20] <= 0.1991:
                                            return 2
                                        else:
                                            return 2
                                    else:
                                        if f[61] <= 0.2227:
                                            if f[54] <= 23.4551:
                                                return 2
                                            else:
                                                return 7
                                        else:
                                            return 1
                            else:
                                if f[63] <= 116.3385:
                                    return 6
                                else:
                                    return 0
                        else:
                            if f[43] <= 1.3052:
                                if f[26] <= 55.0192:
                                    return 4
                                else:
                                    return 4
                            else:
                                return 1
                    else:
                        if f[18] <= 0.0:
                            if f[19] <= 0.9995:
                                return 8
                            else:
                                return 8
                        else:
                            if f[13] <= 29.1812:
                                if f[48] <= 176.7021:
                                    return 7
                                else:
                                    return 7
                            else:
                                if f[30] <= 0.0811:
                                    if f[8] <= 0.2046:
                                        return 5
                                    else:
                                        return 5
                                else:
                                    if f[51] <= 107.8445:
                                        return 2
                                    else:
                                        return 8
            else:
                if f[53] <= 0.3447:
                    if f[68] <= 49.168:
                        if f[43] <= 0.9207:
                            if f[19] <= 0.8967:
                                return 1
                            else:
                                if f[28] <= 1.0119:
                                    return 2
                                else:
                                    return 0
                        else:
                            if f[70] <= 0.2011:
                                if f[23] <= 0.2319:
                                    if f[8] <= 0.1441:
                                        return 8
                                    else:
                                        return 2
                                else:
                                    return 1
                            else:
                                if f[29] <= 1.2502:
                                    if f[0] <= 110.491:
                                        if f[29] <= -10.0356:
                                            if f[53] <= 0.333:
                                                if f[63] <= 147.0677:
                                                    if f[4] <= 0.0054:
                                                        return 0
                                                    else:
                                                        if f[64] <= 99.5327:
                                                            return 1
                                                        else:
                                                            if f[1] <= 27.2521:
                                                                return 6
                                                            else:
                                                                return 6
                                                else:
                                                    return 0
                                            else:
                                                return 9
                                        else:
                                            return 2
                                    else:
                                        if f[12] <= 59.1138:
                                            return 4
                                        else:
                                            return 4
                                else:
                                    if f[59] <= 125.0381:
                                        if f[18] <= 0.0017:
                                            return 6
                                        else:
                                            if f[56] <= 80.7792:
                                                if f[70] <= 0.2891:
                                                    return 2
                                                else:
                                                    return 1
                                            else:
                                                if f[25] <= 0.2979:
                                                    return 4
                                                else:
                                                    if f[48] <= 157.3562:
                                                        if f[53] <= 0.2012:
                                                            if f[61] <= 0.2698:
                                                                return 0
                                                            else:
                                                                return 2
                                                        else:
                                                            return 0
                                                    else:
                                                        return 0
                                    else:
                                        if f[35] <= 0.1387:
                                            if f[19] <= 1.1547:
                                                if f[59] <= 175.2875:
                                                    return 1
                                                else:
                                                    return 1
                                            else:
                                                return 4
                                        else:
                                            if f[58] <= 18.7949:
                                                return 2
                                            else:
                                                return 7
                    else:
                        if f[67] <= 60.818:
                            if f[15] <= 0.5547:
                                if f[44] <= 0.0586:
                                    return 0
                                else:
                                    if f[70] <= 0.3548:
                                        if f[26] <= 45.0625:
                                            return 7
                                        else:
                                            return 7
                                    else:
                                        return 7
                            else:
                                return 2
                        else:
                            if f[29] <= -29.6306:
                                if f[64] <= 114.3558:
                                    return 6
                                else:
                                    return 3
                            else:
                                if f[22] <= 1.0424:
                                    if f[55] <= 91.752:
                                        if f[22] <= 0.82:
                                            return 0
                                        else:
                                            return 2
                                    else:
                                        if f[20] <= 0.093:
                                            return 8
                                        else:
                                            return 8
                                else:
                                    if f[26] <= 86.3011:
                                        if f[63] <= 114.6109:
                                            return 9
                                        else:
                                            if f[18] <= 0.0771:
                                                return 2
                                            else:
                                                return 2
                                    else:
                                        if f[61] <= 0.3291:
                                            if f[49] <= 0.3394:
                                                return 1
                                            else:
                                                return 1
                                        else:
                                            return 7
                else:
                    if f[29] <= 3.332:
                        if f[27] <= 168.3015:
                            if f[0] <= 41.6847:
                                if f[51] <= 42.4118:
                                    return 0
                                else:
                                    if f[52] <= 91.6543:
                                        return 7
                                    else:
                                        return 7
                            else:
                                if f[13] <= 19.218:
                                    if f[19] <= 1.1128:
                                        if f[25] <= 0.3818:
                                            if f[43] <= 1.9999:
                                                return 6
                                            else:
                                                if f[65] <= 35.0327:
                                                    return 6
                                                else:
                                                    return 6
                                        else:
                                            return 6
                                    else:
                                        if f[57] <= 0.3619:
                                            return 6
                                        else:
                                            return 0
                                else:
                                    if f[6] <= 0.0708:
                                        if f[50] <= 63.4609:
                                            if f[9] <= 0.1124:
                                                return 6
                                            else:
                                                return 6
                                        else:
                                            return 1
                                    else:
                                        if f[42] <= 1.0313:
                                            if f[22] <= 1.1993:
                                                return 6
                                            else:
                                                return 9
                                        else:
                                            return 3
                        else:
                            return 3
                    else:
                        if f[10] <= 10477.8458:
                            if f[66] <= 28.0692:
                                return 8
                            else:
                                if f[14] <= 0.5871:
                                    if f[58] <= 36.1809:
                                        return 6
                                    else:
                                        return 6
                                else:
                                    if f[68] <= 29.833:
                                        if f[35] <= 0.1436:
                                            return 0
                                        else:
                                            return 0
                                    else:
                                        if f[22] <= 1.1348:
                                            return 7
                                        else:
                                            return 2
                        else:
                            if f[69] <= 0.369:
                                if f[57] <= 0.3389:
                                    return 7
                                else:
                                    if f[21] <= 30.1667:
                                        if f[25] <= 0.3547:
                                            if f[6] <= 0.053:
                                                return 0
                                            else:
                                                return 1
                                        else:
                                            return 3
                                    else:
                                        return 6
                            else:
                                if f[64] <= 113.0483:
                                    return 1
                                else:
                                    if f[12] <= 60.2393:
                                        return 1
                                    else:
                                        return 7
        else:
            if f[16] <= 0.9698:
                if f[17] <= 0.0854:
                    if f[11] <= 76.2889:
                        if f[42] <= 1.364:
                            if f[29] <= -41.0727:
                                return 2
                            else:
                                if f[64] <= 43.3778:
                                    return 1
                                else:
                                    if f[6] <= 0.1025:
                                        if f[31] <= 0.0058:
                                            if f[34] <= 1.0304:
                                                return 6
                                            else:
                                                return 0
                                        else:
                                            return 3
                                    else:
                                        return 7
                        else:
                            if f[16] <= 0.413:
                                return 8
                            else:
                                return 2
                    else:
                        if f[57] <= 0.3262:
                            if f[24] <= 0.0369:
                                if f[46] <= 22.8301:
                                    return 2
                                else:
                                    return 6
                            else:
                                if f[14] <= 0.3869:
                                    return 6
                                else:
                                    if f[9] <= 0.1831:
                                        if f[11] <= 84.7916:
                                            return 9
                                        else:
                                            if f[35] <= 0.8643:
                                                if f[65] <= 84.5905:
                                                    return 9
                                                else:
                                                    if f[57] <= 0.2899:
                                                        return 9
                                                    else:
                                                        return 9
                                            else:
                                                return 9
                                    else:
                                        if f[3] <= 0.0339:
                                            if f[63] <= 110.5869:
                                                return 9
                                            else:
                                                if f[54] <= 75.9141:
                                                    return 9
                                                else:
                                                    return 9
                                        else:
                                            return 3
                        else:
                            if f[55] <= 58.2764:
                                if f[23] <= 0.0383:
                                    return 7
                                else:
                                    if f[27] <= 131.3389:
                                        return 6
                                    else:
                                        return 6
                            else:
                                if f[23] <= 0.0842:
                                    if f[47] <= 92.292:
                                        if f[36] <= 0.126:
                                            return 0
                                        else:
                                            return 3
                                    else:
                                        return 9
                                else:
                                    return 1
                else:
                    if f[11] <= 86.9272:
                        if f[48] <= 96.0234:
                            if f[28] <= 1.0379:
                                return 8
                            else:
                                return 2
                        else:
                            if f[23] <= 0.2211:
                                if f[33] <= 0.2208:
                                    return 1
                                else:
                                    if f[50] <= 75.6357:
                                        return 2
                                    else:
                                        return 3
                            else:
                                if f[10] <= 4315.6267:
                                    if f[47] <= 75.7852:
                                        return 0
                                    else:
                                        return 0
                                else:
                                    return 6
                    else:
                        if f[26] <= 90.0452:
                            if f[46] <= 30.8459:
                                return 6
                            else:
                                if f[65] <= 44.1581:
                                    return 3
                                else:
                                    if f[19] <= 0.6416:
                                        if f[60] <= 154.6008:
                                            return 9
                                        else:
                                            return 9
                                    else:
                                        return 2
                        else:
                            if f[62] <= 130.8073:
                                if f[57] <= 0.25:
                                    if f[45] <= 0.2515:
                                        return 9
                                    else:
                                        return 1
                                else:
                                    if f[36] <= 0.123:
                                        if f[40] <= 0.7683:
                                            return 3
                                        else:
                                            return 3
                                    else:
                                        if f[25] <= 0.3232:
                                            return 2
                                        else:
                                            if f[60] <= 122.0312:
                                                return 1
                                            else:
                                                return 3
                            else:
                                if f[50] <= 29.7844:
                                    return 9
                                else:
                                    if f[68] <= 32.2082:
                                        return 3
                                    else:
                                        return 3
            else:
                if f[53] <= 0.3189:
                    if f[30] <= 0.0791:
                        if f[7] <= 68.1436:
                            if f[26] <= 41.2688:
                                return 8
                            else:
                                if f[59] <= 46.3936:
                                    return 2
                                else:
                                    return 5
                        else:
                            if f[18] <= 0.1094:
                                if f[68] <= 19.1455:
                                    return 0
                                else:
                                    return 4
                            else:
                                return 5
                    else:
                        if f[21] <= 42.5308:
                            if f[14] <= 0.6227:
                                return 4
                            else:
                                if f[42] <= 1.1791:
                                    return 1
                                else:
                                    return 2
                        else:
                            if f[26] <= 58.9886:
                                return 1
                            else:
                                return 3
                else:
                    if f[57] <= 0.3223:
                        if f[16] <= 0.9934:
                            return 3
                        else:
                            if f[55] <= 79.7351:
                                return 0
                            else:
                                return 8
                    else:
                        if f[0] <= 115.9055:
                            if f[41] <= 1.6939:
                                return 6
                            else:
                                if f[1] <= 30.268:
                                    return 6
                                else:
                                    return 6
                        else:
                            return 1
    else:
        if f[16] <= 0.3185:
            if f[12] <= 56.5816:
                return 8
            else:
                return 8
        else:
            if f[61] <= 0.3478:
                if f[10] <= 10913.0029:
                    if f[27] <= 167.0568:
                        if f[3] <= 0.1484:
                            if f[18] <= 0.1182:
                                if f[19] <= 0.6719:
                                    return 4
                                else:
                                    return 4
                            else:
                                return 9
                        else:
                            if f[35] <= 0.0068:
                                if f[31] <= 0.0286:
                                    if f[11] <= 55.4675:
                                        return 5
                                    else:
                                        return 2
                                else:
                                    if f[14] <= 0.8209:
                                        if f[19] <= 0.9786:
                                            if f[25] <= 0.2842:
                                                return 4
                                            else:
                                                if f[37] <= 0.0212:
                                                    return 1
                                                else:
                                                    return 4
                                        else:
                                            return 1
                                    else:
                                        return 5
                            else:
                                if f[31] <= 0.1367:
                                    if f[53] <= 0.1943:
                                        if f[45] <= 0.106:
                                            return 5
                                        else:
                                            return 5
                                    else:
                                        if f[46] <= 19.6797:
                                            return 2
                                        else:
                                            if f[0] <= 162.2307:
                                                if f[56] <= 86.6265:
                                                    return 3
                                                else:
                                                    return 0
                                            else:
                                                if f[53] <= 0.3115:
                                                    return 5
                                                else:
                                                    return 5
                                else:
                                    return 4
                    else:
                        if f[4] <= 0.3123:
                            if f[22] <= 1.4233:
                                return 8
                            else:
                                if f[26] <= 79.929:
                                    if f[11] <= 86.2437:
                                        if f[51] <= 117.0723:
                                            return 5
                                        else:
                                            return 5
                                    else:
                                        if f[9] <= 0.1959:
                                            return 4
                                        else:
                                            return 5
                                else:
                                    if f[45] <= 0.3157:
                                        return 5
                                    else:
                                        return 3
                        else:
                            if f[46] <= 21.8988:
                                if f[22] <= 5.0407:
                                    return 4
                                else:
                                    return 4
                            else:
                                if f[40] <= 0.4433:
                                    return 4
                                else:
                                    if f[33] <= 0.533:
                                        return 5
                                    else:
                                        return 5
                else:
                    if f[14] <= 0.5649:
                        if f[13] <= 39.6422:
                            return 3
                        else:
                            return 3
                    else:
                        if f[35] <= 0.0439:
                            return 1
                        else:
                            return 9
            else:
                if f[63] <= 170.1488:
                    if f[38] <= 0.0229:
                        if f[17] <= 0.5823:
                            return 1
                        else:
                            return 1
                    else:
                        if f[35] <= 0.0078:
                            return 4
                        else:
                            return 1
                else:
                    if f[10] <= 8219.9022:
                        return 5
                    else:
                        return 5


def _tree_17(f):
    if f[1] <= -68.9606:
        if f[11] <= 52.619:
            return 8
        else:
            if f[68] <= 100.742:
                return 7
            else:
                return 8
    else:
        if f[1] <= 63.9614:
            if f[19] <= 0.7638:
                if f[17] <= 0.078:
                    if f[28] <= 0.6988:
                        if f[60] <= 74.6621:
                            return 8
                        else:
                            return 0
                    else:
                        if f[10] <= 5704.7985:
                            if f[13] <= 62.1585:
                                if f[48] <= 141.124:
                                    if f[70] <= 0.2587:
                                        if f[60] <= 144.5967:
                                            return 2
                                        else:
                                            return 2
                                    else:
                                        return 6
                                else:
                                    if f[68] <= 35.2895:
                                        return 0
                                    else:
                                        return 7
                            else:
                                return 9
                        else:
                            if f[33] <= 0.0352:
                                return 7
                            else:
                                if f[61] <= 0.3447:
                                    if f[24] <= 0.0371:
                                        return 2
                                    else:
                                        if f[41] <= 1.2662:
                                            if f[30] <= 0.2557:
                                                return 9
                                            else:
                                                return 2
                                        else:
                                            if f[23] <= 0.1128:
                                                return 9
                                            else:
                                                if f[6] <= 0.0426:
                                                    return 6
                                                else:
                                                    return 9
                                else:
                                    if f[18] <= 0.0039:
                                        return 3
                                    else:
                                        if f[63] <= 111.4184:
                                            return 1
                                        else:
                                            return 9
                else:
                    if f[2] <= 0.0086:
                        if f[3] <= 0.0634:
                            if f[43] <= 2.3025:
                                if f[13] <= 12.3703:
                                    if f[46] <= 38.8154:
                                        return 1
                                    else:
                                        return 4
                                else:
                                    if f[44] <= 0.1535:
                                        return 6
                                    else:
                                        return 9
                            else:
                                if f[43] <= 2.8006:
                                    return 1
                                else:
                                    return 1
                        else:
                            if f[26] <= 66.356:
                                if f[6] <= 0.0774:
                                    if f[65] <= 74.1615:
                                        return 0
                                    else:
                                        return 0
                                else:
                                    if f[23] <= 0.2119:
                                        return 4
                                    else:
                                        return 2
                            else:
                                if f[68] <= 19.9443:
                                    if f[11] <= 103.2798:
                                        return 2
                                    else:
                                        if f[52] <= 123.9834:
                                            return 1
                                        else:
                                            return 0
                                else:
                                    if f[24] <= 0.0735:
                                        if f[22] <= 1.6495:
                                            if f[27] <= 145.4532:
                                                return 6
                                            else:
                                                return 5
                                        else:
                                            return 4
                                    else:
                                        if f[67] <= 52.8864:
                                            return 3
                                        else:
                                            return 3
                    else:
                        if f[11] <= 85.3782:
                            if f[11] <= 73.8489:
                                if f[18] <= 0.1047:
                                    if f[52] <= 67.6533:
                                        return 2
                                    else:
                                        if f[58] <= 23.6123:
                                            return 0
                                        else:
                                            if f[24] <= 0.1351:
                                                return 4
                                            else:
                                                return 3
                                else:
                                    return 5
                            else:
                                if f[51] <= 81.2936:
                                    return 8
                                else:
                                    return 9
                        else:
                            if f[26] <= 97.1218:
                                if f[43] <= 2.5245:
                                    if f[51] <= 103.0768:
                                        if f[1] <= 25.2327:
                                            return 3
                                        else:
                                            return 3
                                    else:
                                        return 2
                                else:
                                    if f[37] <= 0.1055:
                                        if f[21] <= -8.5815:
                                            if f[47] <= 88.552:
                                                return 1
                                            else:
                                                return 9
                                        else:
                                            if f[43] <= 2.8868:
                                                return 9
                                            else:
                                                return 9
                                    else:
                                        return 3
                            else:
                                if f[9] <= 0.1847:
                                    if f[60] <= 151.4619:
                                        return 3
                                    else:
                                        return 3
                                else:
                                    if f[46] <= 41.376:
                                        if f[23] <= 0.146:
                                            return 9
                                        else:
                                            return 9
                                    else:
                                        if f[30] <= 0.5001:
                                            return 3
                                        else:
                                            if f[53] <= 0.2416:
                                                return 9
                                            else:
                                                return 3
            else:
                if f[32] <= 0.14:
                    if f[67] <= 128.2974:
                        if f[29] <= -5.9511:
                            if f[0] <= 42.0269:
                                if f[70] <= 0.3577:
                                    if f[35] <= 0.9321:
                                        if f[61] <= 0.291:
                                            return 7
                                        else:
                                            return 7
                                    else:
                                        return 0
                                else:
                                    if f[26] <= 45.3908:
                                        return 0
                                    else:
                                        return 6
                            else:
                                if f[11] <= 118.6736:
                                    if f[48] <= 187.29:
                                        if f[53] <= 0.2939:
                                            if f[67] <= 65.756:
                                                return 0
                                            else:
                                                return 4
                                        else:
                                            if f[2] <= 0.0699:
                                                if f[40] <= 0.411:
                                                    if f[44] <= 0.2202:
                                                        return 0
                                                    else:
                                                        if f[10] <= 6848.5294:
                                                            return 6
                                                        else:
                                                            return 6
                                                else:
                                                    if f[38] <= 0.4047:
                                                        return 6
                                                    else:
                                                        if f[28] <= 1.0475:
                                                            return 6
                                                        else:
                                                            return 6
                                            else:
                                                if f[3] <= 0.0017:
                                                    return 1
                                                else:
                                                    return 0
                                    else:
                                        if f[38] <= 0.1514:
                                            return 0
                                        else:
                                            return 0
                                else:
                                    if f[41] <= 1.6178:
                                        return 0
                                    else:
                                        if f[26] <= 135.7803:
                                            return 9
                                        else:
                                            return 9
                        else:
                            if f[68] <= 48.6465:
                                if f[25] <= 0.3633:
                                    if f[56] <= 85.2666:
                                        if f[63] <= 101.4455:
                                            return 1
                                        else:
                                            return 1
                                    else:
                                        if f[40] <= 0.5829:
                                            if f[64] <= 96.7798:
                                                if f[25] <= 0.3076:
                                                    return 5
                                                else:
                                                    return 1
                                            else:
                                                if f[7] <= 132.9121:
                                                    if f[5] <= 0.0207:
                                                        if f[39] <= 9.8926:
                                                            return 7
                                                        else:
                                                            if f[55] <= 59.3789:
                                                                return 0
                                                            else:
                                                                return 0
                                                    else:
                                                        if f[40] <= 0.403:
                                                            return 0
                                                        else:
                                                            return 0
                                                else:
                                                    return 3
                                        else:
                                            if f[63] <= 127.4539:
                                                return 1
                                            else:
                                                return 0
                                else:
                                    if f[27] <= 149.9096:
                                        if f[31] <= 0.0049:
                                            return 6
                                        else:
                                            return 0
                                    else:
                                        return 1
                            else:
                                if f[40] <= 0.4794:
                                    if f[18] <= 0.0196:
                                        if f[11] <= 62.445:
                                            return 7
                                        else:
                                            return 7
                                    else:
                                        return 1
                                else:
                                    if f[34] <= 0.764:
                                        if f[21] <= 23.1772:
                                            return 1
                                        else:
                                            return 1
                                    else:
                                        if f[61] <= 0.3135:
                                            return 9
                                        else:
                                            if f[16] <= 0.5989:
                                                if f[54] <= 74.2256:
                                                    return 8
                                                else:
                                                    return 2
                                            else:
                                                if f[21] <= -14.1289:
                                                    return 7
                                                else:
                                                    return 6
                    else:
                        if f[2] <= 0.0046:
                            if f[45] <= 0.4183:
                                if f[49] <= 0.3702:
                                    if f[38] <= 0.1481:
                                        if f[17] <= 0.0991:
                                            return 1
                                        else:
                                            return 1
                                    else:
                                        if f[31] <= 0.0055:
                                            return 1
                                        else:
                                            return 2
                                else:
                                    return 6
                            else:
                                if f[3] <= 0.3474:
                                    return 6
                                else:
                                    return 6
                        else:
                            if f[4] <= 0.1243:
                                if f[13] <= 35.9515:
                                    return 0
                                else:
                                    return 1
                            else:
                                if f[39] <= 32.5647:
                                    if f[13] <= 25.9437:
                                        return 0
                                    else:
                                        return 3
                                else:
                                    return 4
                else:
                    if f[23] <= 0.0017:
                        if f[65] <= 106.7344:
                            if f[29] <= 7.8059:
                                if f[20] <= 0.1084:
                                    return 6
                                else:
                                    return 2
                            else:
                                if f[67] <= 95.4871:
                                    return 8
                                else:
                                    return 8
                        else:
                            return 8
                    else:
                        if f[67] <= 70.2827:
                            if f[25] <= 0.2945:
                                if f[5] <= 0.0:
                                    if f[50] <= 36.4639:
                                        if f[59] <= 19.9079:
                                            return 2
                                        else:
                                            return 2
                                    else:
                                        return 7
                                else:
                                    if f[40] <= 0.4425:
                                        if f[13] <= 52.3135:
                                            return 7
                                        else:
                                            return 7
                                    else:
                                        if f[12] <= 68.7776:
                                            if f[32] <= 0.403:
                                                if f[40] <= 0.4962:
                                                    return 7
                                                else:
                                                    if f[39] <= 19.2749:
                                                        return 4
                                                    else:
                                                        return 2
                                            else:
                                                return 8
                                        else:
                                            if f[7] <= 86.0956:
                                                return 7
                                            else:
                                                return 7
                            else:
                                if f[31] <= 0.002:
                                    if f[40] <= 0.4927:
                                        if f[45] <= 0.0284:
                                            return 1
                                        else:
                                            return 0
                                    else:
                                        if f[70] <= 0.188:
                                            return 8
                                        else:
                                            if f[57] <= 0.2852:
                                                if f[23] <= 0.0488:
                                                    return 2
                                                else:
                                                    return 2
                                            else:
                                                return 0
                                else:
                                    if f[57] <= 0.2646:
                                        return 2
                                    else:
                                        if f[69] <= 0.2763:
                                            return 7
                                        else:
                                            return 7
                        else:
                            if f[57] <= 0.2508:
                                if f[6] <= 0.4593:
                                    if f[16] <= 0.5043:
                                        if f[39] <= 68.1782:
                                            if f[60] <= 117.1904:
                                                return 7
                                            else:
                                                return 0
                                        else:
                                            return 8
                                    else:
                                        if f[70] <= 0.233:
                                            if f[41] <= 1.6536:
                                                if f[24] <= 0.0283:
                                                    return 2
                                                else:
                                                    if f[2] <= 0.0642:
                                                        return 2
                                                    else:
                                                        return 8
                                            else:
                                                if f[43] <= 2.2559:
                                                    if f[19] <= 0.8841:
                                                        return 2
                                                    else:
                                                        return 7
                                                else:
                                                    if f[59] <= 121.4961:
                                                        return 1
                                                    else:
                                                        return 1
                                        else:
                                            if f[15] <= 0.1735:
                                                if f[61] <= 0.252:
                                                    return 5
                                                else:
                                                    if f[10] <= 6238.9632:
                                                        return 4
                                                    else:
                                                        return 1
                                            else:
                                                if f[65] <= 83.4561:
                                                    return 1
                                                else:
                                                    return 1
                                else:
                                    if f[23] <= 0.0349:
                                        return 5
                                    else:
                                        return 8
                            else:
                                if f[23] <= 0.3528:
                                    if f[17] <= 0.2756:
                                        if f[43] <= 2.5361:
                                            if f[67] <= 88.9268:
                                                if f[2] <= 0.0006:
                                                    if f[36] <= 0.1848:
                                                        return 2
                                                    else:
                                                        return 4
                                                else:
                                                    if f[38] <= 0.22:
                                                        return 6
                                                    else:
                                                        return 6
                                            else:
                                                if f[23] <= 0.2454:
                                                    if f[43] <= 2.2896:
                                                        if f[26] <= 65.8116:
                                                            return 8
                                                        else:
                                                            if f[26] <= 88.9959:
                                                                return 7
                                                            else:
                                                                return 9
                                                    else:
                                                        return 1
                                                else:
                                                    return 0
                                        else:
                                            if f[23] <= 0.1357:
                                                return 8
                                            else:
                                                return 2
                                    else:
                                        if f[43] <= 1.7948:
                                            if f[21] <= 13.5205:
                                                return 0
                                            else:
                                                return 6
                                        else:
                                            if f[49] <= 0.2178:
                                                return 4
                                            else:
                                                return 4
                                else:
                                    if f[4] <= 0.071:
                                        return 0
                                    else:
                                        if f[24] <= 0.0463:
                                            return 0
                                        else:
                                            return 2
        else:
            if f[66] <= 215.7433:
                if f[31] <= 0.1364:
                    if f[7] <= 184.0518:
                        if f[10] <= 2265.1308:
                            if f[15] <= 0.0024:
                                if f[20] <= 0.5577:
                                    return 4
                                else:
                                    return 4
                            else:
                                return 2
                        else:
                            if f[39] <= 27.1143:
                                if f[19] <= 0.9479:
                                    return 9
                                else:
                                    if f[15] <= 0.0107:
                                        return 0
                                    else:
                                        return 0
                            else:
                                if f[11] <= 101.0142:
                                    if f[5] <= 0.0061:
                                        if f[47] <= 161.0249:
                                            return 2
                                        else:
                                            return 3
                                    else:
                                        if f[48] <= 147.7295:
                                            return 1
                                        else:
                                            return 4
                                else:
                                    return 3
                    else:
                        if f[53] <= 0.2829:
                            if f[58] <= 13.1074:
                                return 4
                            else:
                                if f[68] <= 20.2295:
                                    return 5
                                else:
                                    return 5
                        else:
                            if f[39] <= 42.2739:
                                if f[1] <= 82.5061:
                                    return 2
                                else:
                                    if f[41] <= 1.2731:
                                        return 5
                                    else:
                                        return 4
                            else:
                                return 1
                else:
                    if f[32] <= 0.0894:
                        if f[67] <= 140.8018:
                            return 6
                        else:
                            if f[37] <= 0.0445:
                                if f[7] <= 165.7539:
                                    return 1
                                else:
                                    return 1
                            else:
                                if f[53] <= 0.3389:
                                    return 9
                                else:
                                    return 4
                    else:
                        if f[9] <= 0.0034:
                            if f[64] <= 172.1875:
                                if f[65] <= 165.6138:
                                    if f[34] <= 1.1745:
                                        return 4
                                    else:
                                        return 2
                                else:
                                    return 1
                            else:
                                return 5
                        else:
                            if f[38] <= 0.1718:
                                if f[10] <= 6026.405:
                                    if f[1] <= 116.4805:
                                        if f[40] <= 0.6164:
                                            return 4
                                        else:
                                            return 4
                                    else:
                                        return 4
                                else:
                                    if f[52] <= 164.4424:
                                        return 3
                                    else:
                                        return 4
                            else:
                                return 4
            else:
                if f[3] <= 0.5574:
                    if f[65] <= 198.4859:
                        if f[55] <= 227.3604:
                            return 5
                        else:
                            return 5
                    else:
                        if f[31] <= 0.3206:
                            return 4
                        else:
                            return 4
                else:
                    if f[63] <= 167.0707:
                        if f[28] <= 1.7597:
                            return 4
                        else:
                            return 5
                    else:
                        return 5


def _tree_18(f):
    if f[22] <= 0.4645:
        return 8
    else:
        if f[7] <= 185.6885:
            if f[11] <= 97.0166:
                if f[68] <= 48.6465:
                    if f[34] <= 1.1312:
                        if f[29] <= 1.135:
                            if f[64] <= 117.9696:
                                if f[22] <= 1.0865:
                                    if f[49] <= 0.2792:
                                        return 0
                                    else:
                                        return 7
                                else:
                                    if f[34] <= 0.9948:
                                        if f[2] <= 0.0034:
                                            return 6
                                        else:
                                            if f[31] <= 0.028:
                                                return 6
                                            else:
                                                return 1
                                    else:
                                        if f[42] <= 1.0962:
                                            return 1
                                        else:
                                            return 3
                            else:
                                if f[63] <= 121.3132:
                                    if f[25] <= 0.3377:
                                        if f[42] <= 0.9294:
                                            return 6
                                        else:
                                            if f[40] <= 0.4885:
                                                if f[60] <= 149.8189:
                                                    return 7
                                                else:
                                                    return 0
                                            else:
                                                return 2
                                    else:
                                        if f[47] <= 114.3069:
                                            return 6
                                        else:
                                            return 6
                                else:
                                    if f[23] <= 0.2616:
                                        if f[2] <= 0.0182:
                                            if f[2] <= 0.0044:
                                                if f[12] <= 46.6131:
                                                    return 6
                                                else:
                                                    if f[14] <= 0.5926:
                                                        return 5
                                                    else:
                                                        return 1
                                            else:
                                                if f[14] <= 0.636:
                                                    return 4
                                                else:
                                                    return 0
                                        else:
                                            return 3
                                    else:
                                        if f[54] <= 15.3154:
                                            return 7
                                        else:
                                            if f[21] <= -6.5772:
                                                return 0
                                            else:
                                                if f[66] <= 66.9723:
                                                    return 0
                                                else:
                                                    return 0
                        else:
                            if f[30] <= 0.583:
                                if f[31] <= 0.1777:
                                    if f[19] <= 0.882:
                                        if f[29] <= 23.3667:
                                            if f[22] <= 1.1386:
                                                return 6
                                            else:
                                                if f[25] <= 0.2949:
                                                    return 1
                                                else:
                                                    if f[14] <= 0.7127:
                                                        return 0
                                                    else:
                                                        return 0
                                        else:
                                            if f[63] <= 140.1488:
                                                return 2
                                            else:
                                                if f[52] <= 172.8094:
                                                    return 1
                                                else:
                                                    return 1
                                    else:
                                        if f[51] <= 104.3857:
                                            if f[35] <= 0.7178:
                                                return 0
                                            else:
                                                return 0
                                        else:
                                            if f[4] <= 0.2917:
                                                if f[3] <= 0.0795:
                                                    return 6
                                                else:
                                                    if f[18] <= 0.5997:
                                                        if f[17] <= 0.4342:
                                                            return 0
                                                        else:
                                                            return 0
                                                    else:
                                                        return 2
                                            else:
                                                return 1
                                else:
                                    if f[70] <= 0.3161:
                                        if f[34] <= 1.0023:
                                            if f[38] <= 0.0073:
                                                return 4
                                            else:
                                                return 4
                                        else:
                                            return 5
                                    else:
                                        if f[4] <= 0.335:
                                            return 5
                                        else:
                                            return 7
                            else:
                                if f[37] <= 0.0109:
                                    if f[42] <= 1.0016:
                                        return 3
                                    else:
                                        return 5
                                else:
                                    if f[69] <= 0.3707:
                                        if f[26] <= 94.3864:
                                            if f[4] <= 0.1188:
                                                return 1
                                            else:
                                                return 1
                                        else:
                                            if f[54] <= 27.6123:
                                                return 0
                                            else:
                                                return 1
                                    else:
                                        return 1
                    else:
                        if f[31] <= 0.1708:
                            if f[60] <= 73.9375:
                                if f[9] <= 0.3699:
                                    return 2
                                else:
                                    if f[33] <= 0.4041:
                                        return 7
                                    else:
                                        if f[6] <= 0.0752:
                                            return 8
                                        else:
                                            return 8
                            else:
                                if f[40] <= 0.4623:
                                    if f[59] <= 73.4785:
                                        if f[31] <= 0.0011:
                                            return 0
                                        else:
                                            if f[39] <= 84.2578:
                                                return 7
                                            else:
                                                return 1
                                    else:
                                        if f[67] <= 123.9181:
                                            return 2
                                        else:
                                            return 5
                                else:
                                    if f[43] <= 1.6363:
                                        if f[41] <= 2.1622:
                                            if f[25] <= 0.1748:
                                                return 1
                                            else:
                                                if f[20] <= 0.189:
                                                    if f[52] <= 207.8682:
                                                        return 2
                                                    else:
                                                        return 3
                                                else:
                                                    if f[28] <= 1.1683:
                                                        if f[14] <= 0.7763:
                                                            return 0
                                                        else:
                                                            return 0
                                                    else:
                                                        if f[66] <= 141.6815:
                                                            return 2
                                                        else:
                                                            return 0
                                        else:
                                            if f[12] <= 55.5485:
                                                if f[27] <= 144.5687:
                                                    return 4
                                                else:
                                                    return 4
                                            else:
                                                return 2
                                    else:
                                        if f[6] <= 0.0917:
                                            if f[4] <= 0.0034:
                                                return 2
                                            else:
                                                if f[7] <= 82.5566:
                                                    return 6
                                                else:
                                                    return 3
                                        else:
                                            if f[16] <= 0.7362:
                                                return 4
                                            else:
                                                if f[20] <= 0.203:
                                                    return 5
                                                else:
                                                    if f[26] <= 65.2742:
                                                        return 5
                                                    else:
                                                        return 5
                        else:
                            if f[6] <= 0.0569:
                                return 0
                            else:
                                if f[5] <= 0.0148:
                                    if f[48] <= 231.8535:
                                        if f[43] <= 1.735:
                                            return 4
                                        else:
                                            return 4
                                    else:
                                        return 5
                                else:
                                    return 8
                else:
                    if f[59] <= 64.3697:
                        if f[19] <= 1.0859:
                            if f[51] <= 15.7637:
                                if f[70] <= 0.2102:
                                    return 2
                                else:
                                    return 2
                            else:
                                if f[0] <= 44.5181:
                                    if f[60] <= 146.302:
                                        if f[42] <= 1.0124:
                                            return 7
                                        else:
                                            return 2
                                    else:
                                        if f[17] <= 0.012:
                                            return 7
                                        else:
                                            return 7
                                else:
                                    if f[42] <= 0.9551:
                                        if f[35] <= 0.5518:
                                            return 6
                                        else:
                                            return 6
                                    else:
                                        if f[45] <= 0.0786:
                                            if f[35] <= 0.4863:
                                                return 2
                                            else:
                                                return 9
                                        else:
                                            if f[46] <= 68.7492:
                                                return 0
                                            else:
                                                return 3
                        else:
                            if f[31] <= 0.0:
                                return 1
                            else:
                                if f[70] <= 0.3574:
                                    return 7
                                else:
                                    return 7
                    else:
                        if f[22] <= 0.6659:
                            if f[63] <= 122.1177:
                                if f[70] <= 0.1565:
                                    return 8
                                else:
                                    return 6
                            else:
                                if f[36] <= 0.0934:
                                    return 8
                                else:
                                    return 8
                        else:
                            if f[19] <= 0.6906:
                                if f[18] <= 0.0214:
                                    if f[9] <= 0.0534:
                                        return 8
                                    else:
                                        return 1
                                else:
                                    if f[56] <= 131.8906:
                                        if f[13] <= 53.1822:
                                            return 9
                                        else:
                                            return 9
                                    else:
                                        return 5
                            else:
                                if f[13] <= 29.7091:
                                    if f[51] <= 44.7969:
                                        return 9
                                    else:
                                        if f[42] <= 1.5653:
                                            if f[2] <= 0.0:
                                                return 1
                                            else:
                                                if f[64] <= 92.6504:
                                                    if f[25] <= 0.3184:
                                                        return 6
                                                    else:
                                                        return 7
                                                else:
                                                    if f[9] <= 0.0178:
                                                        return 7
                                                    else:
                                                        return 7
                                        else:
                                            return 8
                                else:
                                    if f[16] <= 0.1438:
                                        if f[52] <= 149.5511:
                                            return 8
                                        else:
                                            return 6
                                    else:
                                        if f[37] <= 0.003:
                                            if f[21] <= -11.689:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            if f[10] <= 7026.2613:
                                                if f[4] <= 0.0884:
                                                    if f[58] <= 36.9602:
                                                        return 1
                                                    else:
                                                        if f[53] <= 0.1914:
                                                            if f[44] <= 0.0616:
                                                                return 2
                                                            else:
                                                                return 2
                                                        else:
                                                            if f[48] <= 196.585:
                                                                if f[36] <= 0.2045:
                                                                    return 8
                                                                else:
                                                                    return 5
                                                            else:
                                                                return 6
                                                else:
                                                    if f[63] <= 130.6975:
                                                        return 7
                                                    else:
                                                        return 4
                                            else:
                                                if f[26] <= 95.0429:
                                                    if f[0] <= 71.3857:
                                                        return 3
                                                    else:
                                                        return 3
                                                else:
                                                    if f[32] <= 0.0422:
                                                        return 6
                                                    else:
                                                        return 6
            else:
                if f[61] <= 0.3564:
                    if f[17] <= 0.0747:
                        if f[53] <= 0.3701:
                            if f[64] <= 141.476:
                                if f[70] <= 0.3402:
                                    if f[4] <= 0.0002:
                                        if f[36] <= 0.1995:
                                            return 2
                                        else:
                                            return 9
                                    else:
                                        return 9
                                else:
                                    if f[45] <= 0.0:
                                        return 9
                                    else:
                                        if f[66] <= 60.6422:
                                            return 1
                                        else:
                                            return 2
                            else:
                                if f[68] <= 58.9902:
                                    return 0
                                else:
                                    if f[52] <= 167.4453:
                                        if f[59] <= 36.6631:
                                            return 6
                                        else:
                                            return 2
                                    else:
                                        return 9
                        else:
                            if f[62] <= 114.5491:
                                return 3
                            else:
                                return 7
                    else:
                        if f[46] <= 42.8948:
                            if f[70] <= 0.3416:
                                if f[16] <= 0.787:
                                    if f[39] <= 49.4312:
                                        if f[22] <= 1.1526:
                                            return 9
                                        else:
                                            return 9
                                    else:
                                        return 6
                                else:
                                    if f[26] <= 104.2479:
                                        if f[49] <= 0.3154:
                                            if f[45] <= 0.3433:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            if f[32] <= 0.0703:
                                                return 0
                                            else:
                                                if f[53] <= 0.2686:
                                                    return 4
                                                else:
                                                    return 6
                                    else:
                                        if f[44] <= 0.3556:
                                            if f[27] <= 141.6453:
                                                return 6
                                            else:
                                                if f[13] <= 24.0081:
                                                    return 9
                                                else:
                                                    return 3
                                        else:
                                            if f[32] <= 0.1047:
                                                return 3
                                            else:
                                                return 3
                            else:
                                if f[51] <= 103.3408:
                                    if f[21] <= 19.7305:
                                        return 6
                                    else:
                                        if f[54] <= 33.9238:
                                            return 4
                                        else:
                                            return 2
                                else:
                                    if f[2] <= 0.0007:
                                        return 1
                                    else:
                                        return 1
                        else:
                            if f[66] <= 69.006:
                                if f[36] <= 0.2653:
                                    return 9
                                else:
                                    if f[41] <= 1.8734:
                                        if f[13] <= 37.6807:
                                            return 0
                                        else:
                                            return 7
                                    else:
                                        return 2
                            else:
                                if f[19] <= 0.4208:
                                    if f[28] <= 1.1481:
                                        return 9
                                    else:
                                        return 9
                                else:
                                    if f[29] <= 11.4331:
                                        if f[25] <= 0.3689:
                                            if f[21] <= -7.5873:
                                                if f[54] <= 67.8848:
                                                    if f[14] <= 0.4256:
                                                        return 3
                                                    else:
                                                        return 3
                                                else:
                                                    return 9
                                            else:
                                                return 3
                                        else:
                                            return 0
                                    else:
                                        if f[36] <= 0.0618:
                                            return 9
                                        else:
                                            if f[23] <= 0.0862:
                                                return 9
                                            else:
                                                if f[4] <= 0.0266:
                                                    return 1
                                                else:
                                                    return 3
                else:
                    if f[29] <= 7.6761:
                        if f[53] <= 0.3672:
                            if f[30] <= 0.2832:
                                if f[4] <= 0.0248:
                                    return 0
                                else:
                                    if f[23] <= 0.1696:
                                        return 3
                                    else:
                                        return 4
                            else:
                                if f[44] <= 0.1525:
                                    return 6
                                else:
                                    return 1
                        else:
                            if f[20] <= 0.0556:
                                return 6
                            else:
                                if f[11] <= 116.2921:
                                    return 6
                                else:
                                    return 6
                    else:
                        if f[56] <= 107.5566:
                            if f[60] <= 111.7678:
                                return 1
                            else:
                                return 1
                        else:
                            if f[27] <= 137.081:
                                return 6
                            else:
                                if f[37] <= 0.036:
                                    return 1
                                else:
                                    if f[30] <= 0.1741:
                                        return 0
                                    else:
                                        return 4
        else:
            if f[56] <= 175.4062:
                if f[31] <= 0.0505:
                    if f[7] <= 221.1828:
                        if f[57] <= 0.3053:
                            if f[69] <= 0.3208:
                                if f[44] <= 0.2208:
                                    if f[41] <= 1.4783:
                                        if f[19] <= 0.9256:
                                            return 2
                                        else:
                                            return 2
                                    else:
                                        return 3
                                else:
                                    return 5
                            else:
                                return 9
                        else:
                            if f[38] <= 0.057:
                                if f[59] <= 186.8368:
                                    return 1
                                else:
                                    return 1
                            else:
                                return 3
                    else:
                        if f[43] <= 1.2738:
                            return 1
                        else:
                            if f[28] <= 2.585:
                                return 5
                            else:
                                return 5
                else:
                    if f[35] <= 0.008:
                        if f[38] <= 0.0016:
                            if f[41] <= 1.7616:
                                if f[5] <= 0.0005:
                                    return 5
                                else:
                                    return 1
                            else:
                                if f[19] <= 0.8356:
                                    return 4
                                else:
                                    return 4
                        else:
                            if f[65] <= 189.7202:
                                if f[21] <= 57.0228:
                                    if f[24] <= 0.0625:
                                        return 4
                                    else:
                                        if f[20] <= 0.5481:
                                            return 4
                                        else:
                                            return 4
                                else:
                                    return 4
                            else:
                                if f[33] <= 0.2654:
                                    return 4
                                else:
                                    return 5
                    else:
                        if f[55] <= 103.5938:
                            return 2
                        else:
                            if f[45] <= 0.5544:
                                if f[27] <= 163.5641:
                                    if f[68] <= 24.541:
                                        return 1
                                    else:
                                        return 4
                                else:
                                    if f[11] <= 107.2468:
                                        return 5
                                    else:
                                        return 3
                            else:
                                return 5
            else:
                if f[7] <= 197.8506:
                    if f[36] <= 0.0:
                        return 4
                    else:
                        return 0
                else:
                    if f[20] <= 0.4717:
                        return 5
                    else:
                        return 5


def _tree_19(f):
    if f[22] <= 0.4221:
        if f[69] <= 0.3009:
            return 8
        else:
            return 8
    else:
        if f[7] <= 192.2983:
            if f[11] <= 97.5473:
                if f[70] <= 0.2983:
                    if f[31] <= 0.1412:
                        if f[23] <= 0.1716:
                            if f[1] <= -41.52:
                                if f[25] <= 0.23:
                                    return 8
                                else:
                                    return 8
                            else:
                                if f[19] <= 0.8526:
                                    if f[26] <= 110.7756:
                                        if f[52] <= 171.6094:
                                            if f[40] <= 0.6992:
                                                if f[31] <= 0.001:
                                                    if f[42] <= 2.0132:
                                                        if f[8] <= 0.1494:
                                                            return 2
                                                        else:
                                                            return 2
                                                    else:
                                                        return 8
                                                else:
                                                    return 7
                                            else:
                                                if f[11] <= 69.5085:
                                                    return 3
                                                else:
                                                    return 9
                                        else:
                                            if f[27] <= 168.3146:
                                                if f[37] <= 0.0387:
                                                    return 0
                                                else:
                                                    if f[67] <= 68.9657:
                                                        return 7
                                                    else:
                                                        return 3
                                            else:
                                                if f[23] <= 0.032:
                                                    return 2
                                                else:
                                                    return 5
                                    else:
                                        if f[19] <= 0.615:
                                            if f[49] <= 0.0938:
                                                return 9
                                            else:
                                                return 9
                                        else:
                                            return 2
                                else:
                                    if f[59] <= 61.8086:
                                        if f[60] <= 82.749:
                                            if f[23] <= 0.064:
                                                return 8
                                            else:
                                                return 3
                                        else:
                                            if f[65] <= 6.9435:
                                                return 2
                                            else:
                                                if f[40] <= 0.5219:
                                                    if f[13] <= 42.2082:
                                                        if f[50] <= 36.0342:
                                                            if f[1] <= 4.7495:
                                                                return 7
                                                            else:
                                                                return 2
                                                        else:
                                                            return 7
                                                    else:
                                                        return 7
                                                else:
                                                    return 7
                                    else:
                                        if f[25] <= 0.1748:
                                            if f[50] <= 80.2393:
                                                return 7
                                            else:
                                                return 7
                                        else:
                                            if f[22] <= 0.9701:
                                                if f[67] <= 89.1772:
                                                    return 0
                                                else:
                                                    return 8
                                            else:
                                                if f[42] <= 1.498:
                                                    if f[0] <= 115.1491:
                                                        if f[40] <= 0.4137:
                                                            return 7
                                                        else:
                                                            if f[58] <= 42.1953:
                                                                return 8
                                                            else:
                                                                return 1
                                                    else:
                                                        if f[37] <= 0.0123:
                                                            return 8
                                                        else:
                                                            return 4
                                                else:
                                                    if f[17] <= 0.0134:
                                                        return 2
                                                    else:
                                                        return 5
                        else:
                            if f[11] <= 94.9958:
                                if f[29] <= -26.4868:
                                    if f[46] <= 42.0835:
                                        if f[56] <= 138.6568:
                                            return 6
                                        else:
                                            return 6
                                    else:
                                        if f[23] <= 0.1866:
                                            return 4
                                        else:
                                            return 0
                                else:
                                    if f[40] <= 0.5397:
                                        if f[34] <= 1.1894:
                                            if f[43] <= 1.6141:
                                                if f[52] <= 153.142:
                                                    return 0
                                                else:
                                                    return 1
                                            else:
                                                if f[68] <= 29.8428:
                                                    if f[5] <= 0.0246:
                                                        return 7
                                                    else:
                                                        return 0
                                                else:
                                                    if f[64] <= 63.4496:
                                                        return 2
                                                    else:
                                                        return 2
                                        else:
                                            if f[37] <= 0.0188:
                                                if f[70] <= 0.2202:
                                                    return 2
                                                else:
                                                    return 1
                                            else:
                                                if f[59] <= 78.8008:
                                                    if f[70] <= 0.2499:
                                                        return 7
                                                    else:
                                                        return 7
                                                else:
                                                    return 2
                                    else:
                                        if f[53] <= 0.2993:
                                            if f[42] <= 1.009:
                                                return 5
                                            else:
                                                if f[10] <= 1798.3582:
                                                    return 0
                                                else:
                                                    if f[59] <= 147.6886:
                                                        return 2
                                                    else:
                                                        return 2
                                        else:
                                            if f[58] <= 39.0488:
                                                return 0
                                            else:
                                                return 2
                            else:
                                return 6
                    else:
                        if f[63] <= 120.8082:
                            if f[48] <= 126.6621:
                                return 7
                            else:
                                return 1
                        else:
                            if f[69] <= 0.0869:
                                if f[29] <= -0.9731:
                                    return 5
                                else:
                                    return 1
                            else:
                                if f[10] <= 5178.2042:
                                    if f[39] <= 65.6255:
                                        if f[23] <= 0.5078:
                                            if f[46] <= 19.0899:
                                                return 4
                                            else:
                                                return 4
                                        else:
                                            return 0
                                    else:
                                        return 4
                                else:
                                    return 2
                else:
                    if f[54] <= 90.3389:
                        if f[27] <= 132.9543:
                            if f[0] <= 43.3238:
                                if f[39] <= 15.3285:
                                    if f[63] <= 133.472:
                                        return 7
                                    else:
                                        return 7
                                else:
                                    if f[56] <= 127.0283:
                                        if f[56] <= 114.8528:
                                            return 0
                                        else:
                                            return 0
                                    else:
                                        return 6
                            else:
                                if f[47] <= 139.1816:
                                    if f[25] <= 0.329:
                                        if f[55] <= 48.5645:
                                            if f[40] <= 0.6218:
                                                return 6
                                            else:
                                                return 6
                                        else:
                                            if f[10] <= 8112.1843:
                                                if f[33] <= 0.3605:
                                                    if f[27] <= 112.5393:
                                                        if f[22] <= 1.07:
                                                            return 1
                                                        else:
                                                            return 1
                                                    else:
                                                        return 4
                                                else:
                                                    return 3
                                            else:
                                                return 9
                                    else:
                                        if f[27] <= 91.2327:
                                            return 1
                                        else:
                                            if f[11] <= 93.6196:
                                                if f[30] <= 0.0836:
                                                    return 0
                                                else:
                                                    if f[34] <= 1.0265:
                                                        if f[25] <= 0.3375:
                                                            return 6
                                                        else:
                                                            return 6
                                                    else:
                                                        if f[22] <= 1.1688:
                                                            return 7
                                                        else:
                                                            return 6
                                            else:
                                                return 1
                                else:
                                    if f[55] <= 137.4912:
                                        if f[59] <= 79.6701:
                                            return 6
                                        else:
                                            return 1
                                    else:
                                        if f[5] <= 0.1101:
                                            return 4
                                        else:
                                            return 4
                        else:
                            if f[23] <= 0.2636:
                                if f[50] <= 33.29:
                                    if f[60] <= 144.9316:
                                        if f[46] <= 34.8662:
                                            return 1
                                        else:
                                            return 1
                                    else:
                                        return 4
                                else:
                                    if f[3] <= 0.0732:
                                        if f[8] <= 0.0056:
                                            return 6
                                        else:
                                            if f[6] <= 0.0159:
                                                if f[52] <= 164.693:
                                                    return 0
                                                else:
                                                    return 0
                                            else:
                                                if f[64] <= 116.3807:
                                                    if f[57] <= 0.3555:
                                                        return 1
                                                    else:
                                                        return 1
                                                else:
                                                    if f[68] <= 61.377:
                                                        if f[56] <= 129.3262:
                                                            return 7
                                                        else:
                                                            return 0
                                                    else:
                                                        if f[50] <= 82.6533:
                                                            return 2
                                                        else:
                                                            return 6
                                    else:
                                        if f[51] <= 141.541:
                                            if f[10] <= 6898.8998:
                                                if f[12] <= 56.5815:
                                                    return 4
                                                else:
                                                    return 9
                                            else:
                                                if f[60] <= 130.5455:
                                                    return 3
                                                else:
                                                    return 3
                                        else:
                                            if f[50] <= 48.1055:
                                                return 5
                                            else:
                                                return 5
                            else:
                                if f[32] <= 0.0493:
                                    if f[68] <= 21.1045:
                                        return 6
                                    else:
                                        return 1
                                else:
                                    if f[31] <= 0.2073:
                                        if f[7] <= 106.5039:
                                            if f[45] <= 0.2434:
                                                return 7
                                            else:
                                                if f[26] <= 67.6686:
                                                    return 0
                                                else:
                                                    if f[4] <= 0.0538:
                                                        return 0
                                                    else:
                                                        return 0
                                        else:
                                            if f[68] <= 18.8315:
                                                if f[69] <= 0.2769:
                                                    return 5
                                                else:
                                                    if f[46] <= 18.0713:
                                                        return 0
                                                    else:
                                                        return 0
                                            else:
                                                return 1
                                    else:
                                        return 4
                    else:
                        if f[55] <= 94.4199:
                            if f[37] <= 0.0024:
                                return 2
                            else:
                                if f[59] <= 76.9887:
                                    return 7
                                else:
                                    return 7
                        else:
                            return 6
            else:
                if f[57] <= 0.3428:
                    if f[17] <= 0.1172:
                        if f[19] <= 0.7983:
                            if f[17] <= 0.0696:
                                if f[34] <= 0.8236:
                                    return 2
                                else:
                                    if f[41] <= 1.1471:
                                        return 3
                                    else:
                                        if f[61] <= 0.3506:
                                            if f[46] <= 31.6465:
                                                return 9
                                            else:
                                                if f[5] <= 0.3035:
                                                    return 9
                                                else:
                                                    return 9
                                        else:
                                            return 3
                            else:
                                if f[4] <= 0.0217:
                                    if f[25] <= 0.3447:
                                        return 7
                                    else:
                                        return 2
                                else:
                                    return 9
                        else:
                            if f[7] <= 52.9795:
                                return 7
                            else:
                                if f[36] <= 0.3296:
                                    if f[19] <= 0.9537:
                                        return 9
                                    else:
                                        return 0
                                else:
                                    return 6
                    else:
                        if f[2] <= 0.0005:
                            if f[6] <= 0.3835:
                                if f[15] <= 0.2424:
                                    return 1
                                else:
                                    return 2
                            else:
                                if f[15] <= 0.0925:
                                    return 4
                                else:
                                    return 4
                        else:
                            if f[3] <= 0.0796:
                                if f[19] <= 0.5732:
                                    if f[25] <= 0.2441:
                                        return 3
                                    else:
                                        return 9
                                else:
                                    if f[2] <= 0.0637:
                                        if f[41] <= 1.8324:
                                            if f[63] <= 155.3403:
                                                return 0
                                            else:
                                                return 6
                                        else:
                                            return 2
                                    else:
                                        if f[64] <= 88.8239:
                                            return 3
                                        else:
                                            return 3
                            else:
                                if f[29] <= 9.5208:
                                    if f[46] <= 22.465:
                                        if f[5] <= 0.011:
                                            return 6
                                        else:
                                            return 9
                                    else:
                                        if f[61] <= 0.3584:
                                            if f[28] <= 1.0088:
                                                return 3
                                            else:
                                                return 3
                                        else:
                                            return 0
                                else:
                                    if f[5] <= 0.0132:
                                        if f[68] <= 25.459:
                                            return 9
                                        else:
                                            return 9
                                    else:
                                        if f[64] <= 82.6428:
                                            return 1
                                        else:
                                            if f[52] <= 102.3578:
                                                return 9
                                            else:
                                                if f[19] <= 0.7656:
                                                    return 3
                                                else:
                                                    return 3
                else:
                    if f[56] <= 97.5986:
                        if f[29] <= 5.6569:
                            if f[63] <= 86.8962:
                                return 3
                            else:
                                if f[39] <= 22.1416:
                                    return 6
                                else:
                                    return 6
                        else:
                            if f[23] <= 0.0632:
                                return 1
                            else:
                                if f[16] <= 0.9992:
                                    return 1
                                else:
                                    return 1
                    else:
                        if f[29] <= 7.6572:
                            if f[59] <= 66.0713:
                                if f[8] <= 0.0566:
                                    return 7
                                else:
                                    if f[30] <= 0.2783:
                                        return 6
                                    else:
                                        return 6
                            else:
                                if f[10] <= 17137.8549:
                                    if f[33] <= 0.0222:
                                        return 6
                                    else:
                                        if f[43] <= 1.9922:
                                            return 2
                                        else:
                                            if f[59] <= 81.6426:
                                                return 3
                                            else:
                                                return 3
                                else:
                                    if f[29] <= -12.2256:
                                        return 9
                                    else:
                                        return 2
                        else:
                            if f[12] <= 58.7464:
                                if f[42] <= 0.9171:
                                    return 0
                                else:
                                    if f[58] <= 27.6117:
                                        return 1
                                    else:
                                        return 1
                            else:
                                if f[7] <= 41.9541:
                                    return 0
                                else:
                                    if f[11] <= 119.5002:
                                        if f[38] <= 0.0159:
                                            return 1
                                        else:
                                            return 2
                                    else:
                                        if f[10] <= 12475.5009:
                                            return 3
                                        else:
                                            return 3
        else:
            if f[64] <= 166.5884:
                if f[7] <= 226.9973:
                    if f[31] <= 0.1219:
                        if f[61] <= 0.3205:
                            if f[17] <= 0.1294:
                                if f[53] <= 0.2568:
                                    if f[12] <= 40.0677:
                                        return 8
                                    else:
                                        if f[36] <= 0.0149:
                                            return 2
                                        else:
                                            return 2
                                else:
                                    return 9
                            else:
                                if f[40] <= 0.6505:
                                    if f[8] <= 0.0007:
                                        return 4
                                    else:
                                        if f[30] <= 0.1279:
                                            return 8
                                        else:
                                            return 5
                                else:
                                    return 3
                        else:
                            if f[26] <= 89.8809:
                                return 1
                            else:
                                return 1
                    else:
                        if f[35] <= 0.0068:
                            if f[54] <= 17.5781:
                                return 4
                            else:
                                return 4
                        else:
                            if f[11] <= 102.1498:
                                if f[61] <= 0.21:
                                    return 4
                                else:
                                    return 1
                            else:
                                return 3
                else:
                    if f[27] <= 128.0:
                        if f[54] <= 28.1738:
                            return 1
                        else:
                            return 8
                    else:
                        if f[16] <= 0.9995:
                            if f[33] <= 0.2996:
                                if f[3] <= 0.4385:
                                    return 5
                                else:
                                    return 4
                            else:
                                return 5
                        else:
                            return 4
            else:
                if f[12] <= 58.0714:
                    if f[4] <= 0.5831:
                        return 5
                    else:
                        return 5
                else:
                    if f[50] <= 18.3447:
                        return 5
                    else:
                        if f[32] <= 0.2371:
                            return 4
                        else:
                            return 4


def _tree_20(f):
    if f[1] <= -75.3225:
        if f[68] <= 77.1494:
            return 4
        else:
            return 8
    else:
        if f[6] <= 0.3528:
            if f[40] <= 0.4572:
                if f[59] <= 55.9502:
                    if f[4] <= 0.0:
                        if f[6] <= 0.0:
                            return 0
                        else:
                            return 8
                    else:
                        if f[61] <= 0.0723:
                            return 4
                        else:
                            if f[45] <= 0.2102:
                                if f[64] <= 78.9623:
                                    return 7
                                else:
                                    if f[45] <= 0.0089:
                                        return 7
                                    else:
                                        return 7
                            else:
                                return 0
                else:
                    if f[60] <= 141.96:
                        if f[53] <= 0.2578:
                            if f[70] <= 0.2364:
                                if f[47] <= 103.5566:
                                    if f[16] <= 0.8938:
                                        return 2
                                    else:
                                        return 2
                                else:
                                    return 8
                            else:
                                return 7
                        else:
                            if f[62] <= 95.4122:
                                if f[31] <= 0.001:
                                    return 0
                                else:
                                    if f[66] <= 85.7865:
                                        return 7
                                    else:
                                        return 7
                            else:
                                if f[29] <= 28.8457:
                                    if f[9] <= 0.0362:
                                        if f[39] <= 12.4478:
                                            return 0
                                        else:
                                            return 7
                                    else:
                                        if f[11] <= 97.9073:
                                            if f[29] <= 9.9006:
                                                if f[0] <= 99.6003:
                                                    return 6
                                                else:
                                                    return 6
                                            else:
                                                return 6
                                        else:
                                            return 3
                                else:
                                    if f[36] <= 0.0811:
                                        return 1
                                    else:
                                        return 0
                    else:
                        if f[31] <= 0.2403:
                            if f[69] <= 0.1644:
                                if f[51] <= 52.6888:
                                    return 2
                                else:
                                    return 7
                            else:
                                if f[43] <= 1.9255:
                                    if f[67] <= 58.5421:
                                        return 0
                                    else:
                                        return 0
                                else:
                                    if f[9] <= 0.04:
                                        return 0
                                    else:
                                        return 7
                        else:
                            return 4
            else:
                if f[57] <= 0.3428:
                    if f[26] <= 93.8565:
                        if f[10] <= 6286.2789:
                            if f[57] <= 0.2695:
                                if f[44] <= 0.9101:
                                    if f[26] <= 16.8263:
                                        if f[14] <= 0.7928:
                                            return 4
                                        else:
                                            return 8
                                    else:
                                        if f[42] <= 1.081:
                                            if f[23] <= 0.2601:
                                                if f[18] <= 0.1539:
                                                    if f[34] <= 1.0424:
                                                        return 8
                                                    else:
                                                        if f[19] <= 0.68:
                                                            return 9
                                                        else:
                                                            return 2
                                                else:
                                                    if f[26] <= 57.2819:
                                                        return 5
                                                    else:
                                                        return 5
                                            else:
                                                if f[14] <= 0.7094:
                                                    return 1
                                                else:
                                                    return 4
                                        else:
                                            if f[66] <= 98.6659:
                                                if f[33] <= 0.6118:
                                                    if f[54] <= 74.1553:
                                                        if f[32] <= 0.2598:
                                                            if f[46] <= 42.3242:
                                                                return 2
                                                            else:
                                                                return 0
                                                        else:
                                                            return 2
                                                    else:
                                                        return 3
                                                else:
                                                    if f[40] <= 0.5355:
                                                        return 1
                                                    else:
                                                        return 8
                                            else:
                                                if f[57] <= 0.1393:
                                                    if f[47] <= 87.9229:
                                                        return 5
                                                    else:
                                                        if f[0] <= 145.3079:
                                                            return 4
                                                        else:
                                                            return 0
                                                else:
                                                    if f[14] <= 0.7484:
                                                        if f[41] <= 1.4:
                                                            return 2
                                                        else:
                                                            if f[29] <= 15.6638:
                                                                if f[10] <= 3499.4049:
                                                                    return 5
                                                                else:
                                                                    return 0
                                                            else:
                                                                return 4
                                                    else:
                                                        if f[20] <= 0.277:
                                                            return 2
                                                        else:
                                                            return 2
                                else:
                                    if f[29] <= -20.4185:
                                        return 4
                                    else:
                                        return 1
                            else:
                                if f[68] <= 31.4922:
                                    if f[63] <= 104.869:
                                        return 6
                                    else:
                                        if f[6] <= 0.1726:
                                            if f[60] <= 116.209:
                                                if f[27] <= 169.1865:
                                                    return 2
                                                else:
                                                    return 1
                                            else:
                                                if f[40] <= 0.6345:
                                                    if f[63] <= 123.1439:
                                                        return 0
                                                    else:
                                                        return 0
                                                else:
                                                    return 0
                                        else:
                                            if f[37] <= 0.0269:
                                                if f[45] <= 0.3022:
                                                    return 5
                                                else:
                                                    return 5
                                            else:
                                                return 0
                                else:
                                    if f[45] <= 0.002:
                                        if f[42] <= 0.9931:
                                            return 6
                                        else:
                                            return 8
                                    else:
                                        if f[29] <= 24.9947:
                                            if f[37] <= 0.0131:
                                                if f[18] <= 0.0005:
                                                    return 7
                                                else:
                                                    if f[5] <= 0.0005:
                                                        return 0
                                                    else:
                                                        return 2
                                            else:
                                                if f[54] <= 30.86:
                                                    return 7
                                                else:
                                                    return 7
                                        else:
                                            if f[45] <= 0.21:
                                                if f[18] <= 0.0999:
                                                    return 1
                                                else:
                                                    return 2
                                            else:
                                                return 4
                        else:
                            if f[19] <= 0.6789:
                                if f[11] <= 94.9757:
                                    if f[55] <= 61.665:
                                        return 0
                                    else:
                                        return 3
                                else:
                                    if f[56] <= 69.3429:
                                        return 2
                                    else:
                                        if f[38] <= 0.1774:
                                            return 7
                                        else:
                                            return 9
                            else:
                                if f[32] <= 0.1533:
                                    if f[16] <= 0.5:
                                        if f[29] <= -7.0171:
                                            return 9
                                        else:
                                            return 3
                                    else:
                                        if f[29] <= 1.7988:
                                            if f[53] <= 0.29:
                                                return 3
                                            else:
                                                if f[37] <= 0.0166:
                                                    return 2
                                                else:
                                                    if f[36] <= 0.3175:
                                                        return 6
                                                    else:
                                                        return 6
                                        else:
                                            return 0
                                else:
                                    if f[21] <= 36.9737:
                                        if f[28] <= 1.1339:
                                            if f[29] <= -25.3095:
                                                return 2
                                            else:
                                                return 2
                                        else:
                                            return 5
                                    else:
                                        return 4
                    else:
                        if f[17] <= 0.1135:
                            if f[46] <= 31.2365:
                                if f[14] <= 0.5619:
                                    if f[30] <= 0.1113:
                                        return 7
                                    else:
                                        return 6
                                else:
                                    return 2
                            else:
                                if f[7] <= 40.8914:
                                    if f[23] <= 0.0278:
                                        return 7
                                    else:
                                        return 1
                                else:
                                    if f[28] <= 0.9895:
                                        if f[45] <= 0.0288:
                                            if f[40] <= 0.6682:
                                                return 4
                                            else:
                                                return 9
                                        else:
                                            if f[19] <= 0.5224:
                                                return 3
                                            else:
                                                if f[22] <= 0.9597:
                                                    return 0
                                                else:
                                                    return 6
                                    else:
                                        if f[39] <= 95.1665:
                                            if f[48] <= 79.6634:
                                                return 8
                                            else:
                                                if f[17] <= 0.0759:
                                                    if f[43] <= 1.9533:
                                                        return 9
                                                    else:
                                                        return 9
                                                else:
                                                    return 1
                                        else:
                                            return 2
                        else:
                            if f[11] <= 82.4871:
                                if f[64] <= 70.8771:
                                    return 8
                                else:
                                    if f[20] <= 0.2362:
                                        return 9
                                    else:
                                        return 4
                            else:
                                if f[50] <= 35.4277:
                                    if f[26] <= 134.4943:
                                        if f[14] <= 0.4331:
                                            if f[67] <= 70.0512:
                                                return 6
                                            else:
                                                return 1
                                        else:
                                            if f[15] <= 0.271:
                                                return 9
                                            else:
                                                return 2
                                    else:
                                        if f[62] <= 145.0589:
                                            return 5
                                        else:
                                            return 3
                                else:
                                    if f[62] <= 142.7604:
                                        if f[0] <= 103.8213:
                                            if f[41] <= 1.8889:
                                                return 0
                                            else:
                                                return 9
                                        else:
                                            if f[11] <= 141.6215:
                                                return 3
                                            else:
                                                return 3
                                    else:
                                        if f[68] <= 28.1685:
                                            return 3
                                        else:
                                            return 3
                else:
                    if f[43] <= 1.9561:
                        if f[25] <= 0.3449:
                            if f[11] <= 71.0706:
                                if f[58] <= 43.7373:
                                    return 0
                                else:
                                    return 0
                            else:
                                if f[45] <= 0.0288:
                                    return 7
                                else:
                                    if f[30] <= 0.4365:
                                        if f[53] <= 0.3574:
                                            if f[19] <= 0.8246:
                                                if f[4] <= 0.0132:
                                                    return 1
                                                else:
                                                    return 4
                                            else:
                                                return 0
                                        else:
                                            return 6
                                    else:
                                        return 1
                        else:
                            if f[54] <= 73.9746:
                                if f[51] <= 46.5557:
                                    if f[14] <= 0.634:
                                        return 0
                                    else:
                                        return 0
                                else:
                                    if f[49] <= 0.3105:
                                        return 0
                                    else:
                                        if f[31] <= 0.0082:
                                            return 6
                                        else:
                                            if f[41] <= 1.3428:
                                                if f[51] <= 131.9248:
                                                    return 6
                                                else:
                                                    return 1
                                            else:
                                                if f[45] <= 0.5406:
                                                    return 6
                                                else:
                                                    return 6
                            else:
                                return 7
                    else:
                        if f[40] <= 0.66:
                            if f[28] <= 1.0696:
                                if f[29] <= -4.0454:
                                    if f[36] <= 0.3477:
                                        if f[59] <= 135.8018:
                                            if f[38] <= 0.5723:
                                                return 6
                                            else:
                                                return 6
                                        else:
                                            return 1
                                    else:
                                        if f[61] <= 0.3618:
                                            return 2
                                        else:
                                            return 1
                                else:
                                    if f[54] <= 57.6514:
                                        if f[30] <= 0.3418:
                                            if f[17] <= 0.2085:
                                                return 0
                                            else:
                                                return 1
                                        else:
                                            if f[37] <= 0.0109:
                                                return 3
                                            else:
                                                if f[53] <= 0.3213:
                                                    return 0
                                                else:
                                                    if f[38] <= 0.208:
                                                        return 1
                                                    else:
                                                        return 1
                                    else:
                                        if f[41] <= 1.9059:
                                            if f[28] <= 0.9803:
                                                return 6
                                            else:
                                                return 2
                                        else:
                                            return 7
                            else:
                                if f[20] <= 0.1921:
                                    if f[49] <= 0.3711:
                                        if f[56] <= 134.5205:
                                            return 1
                                        else:
                                            return 1
                                    else:
                                        return 0
                                else:
                                    if f[52] <= 124.4434:
                                        return 9
                                    else:
                                        return 2
                        else:
                            if f[35] <= 0.5322:
                                if f[16] <= 0.6645:
                                    return 9
                                else:
                                    if f[62] <= 148.6436:
                                        return 3
                                    else:
                                        return 3
                            else:
                                return 1
        else:
            if f[1] <= 104.2405:
                if f[61] <= 0.3105:
                    if f[58] <= 49.3682:
                        if f[11] <= 129.705:
                            if f[31] <= 0.1213:
                                if f[7] <= 170.9395:
                                    if f[38] <= 0.0112:
                                        return 4
                                    else:
                                        if f[32] <= 0.1694:
                                            return 3
                                        else:
                                            if f[52] <= 116.7539:
                                                return 2
                                            else:
                                                return 8
                                else:
                                    if f[27] <= 129.2646:
                                        if f[10] <= 609.3212:
                                            return 4
                                        else:
                                            if f[3] <= 0.6676:
                                                return 2
                                            else:
                                                return 1
                                    else:
                                        if f[34] <= 1.007:
                                            return 1
                                        else:
                                            if f[49] <= 0.3096:
                                                return 5
                                            else:
                                                return 5
                            else:
                                if f[27] <= 177.3731:
                                    if f[10] <= 6238.9632:
                                        return 4
                                    else:
                                        return 1
                                else:
                                    return 5
                        else:
                            if f[32] <= 0.1125:
                                return 3
                            else:
                                return 3
                    else:
                        if f[42] <= 1.3348:
                            if f[13] <= 43.886:
                                if f[41] <= 1.9688:
                                    return 8
                                else:
                                    return 4
                            else:
                                if f[20] <= 0.2135:
                                    return 2
                                else:
                                    return 9
                        else:
                            if f[43] <= 2.9396:
                                return 8
                            else:
                                return 5
                else:
                    if f[2] <= 0.0045:
                        if f[60] <= 125.8398:
                            if f[52] <= 95.5841:
                                return 1
                            else:
                                return 1
                        else:
                            if f[42] <= 1.0412:
                                if f[10] <= 11118.7469:
                                    if f[21] <= 5.1112:
                                        return 0
                                    else:
                                        return 5
                                else:
                                    return 1
                            else:
                                return 4
                    else:
                        if f[24] <= 0.0198:
                            if f[70] <= 0.3523:
                                if f[54] <= 27.1367:
                                    return 5
                                else:
                                    return 5
                            else:
                                return 1
                        else:
                            if f[9] <= 0.1135:
                                return 4
                            else:
                                return 3
            else:
                if f[3] <= 0.3679:
                    if f[25] <= 0.3086:
                        if f[60] <= 155.8896:
                            return 4
                        else:
                            return 4
                    else:
                        if f[37] <= 0.0016:
                            return 5
                        else:
                            return 5
                else:
                    if f[19] <= 1.3908:
                        if f[21] <= 25.8311:
                            if f[14] <= 0.4169:
                                return 4
                            else:
                                if f[23] <= 0.1628:
                                    return 5
                                else:
                                    return 5
                        else:
                            if f[4] <= 0.124:
                                if f[20] <= 0.7694:
                                    return 5
                                else:
                                    return 2
                            else:
                                return 4
                    else:
                        return 4



def _extract_features(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    b_ch, g_ch, r_ch = cv2.split(image)
    avg_r = float(np.mean(r_ch))
    avg_g = float(np.mean(g_ch))
    avg_b = float(np.mean(b_ch))
    features = []
    features.append(float(np.mean(s)))
    features.append(avg_r - avg_b)
    features.append(float(np.mean((h >= 90) & (h <= 130) & (s > 80))))
    features.append(float(np.mean((h >= 5) & (h <= 20) & (s > 120))))
    features.append(float(np.mean((h >= 20) & (h <= 35) & (s > 100))))
    features.append(float(np.mean((h >= 35) & (h <= 80) & (s > 50))))
    features.append(float(np.mean(s > 180)))
    features.append(float(np.mean(s[16:48, 16:48])))
    features.append(float(np.mean((s < 50) & (v > 180))))
    features.append(float(np.mean(v < 40)))
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    features.append(float(np.var(lap)))
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    horiz_e = float(np.mean(np.abs(sobely)))
    features.append(horiz_e)
    features.append(float(np.std(gray)))
    sat_mask = s > 50
    features.append(float(np.std(h[sat_mask].astype(float))) if np.sum(sat_mask) > 100 else 0.0)
    left = gray[:, :32].astype(float)
    right = gray[:, 32:][:, ::-1].astype(float)
    features.append(1.0 - float(np.mean(np.abs(left - right))) / 128.0)
    features.append(float(np.mean((s < 60) & (v > 150))))
    if np.sum(sat_mask) > 50:
        h_sat = h[sat_mask]
        warm = float(np.sum(h_sat < 30))
        cool = float(np.sum(h_sat > 90))
        features.append(warm / max(warm + cool, 1.0))
    else:
        features.append(0.5)
    features.append(float(np.mean((h >= 15) & (h < 30) & (s > 50))))
    features.append(float(np.mean((h < 15) & (s > 100))))
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    vert_e = float(np.mean(np.abs(sobelx)))
    features.append(vert_e / max(horiz_e, 1.0))
    sat_thresh = (s > 100).astype(np.uint8) * 255
    contours, _ = cv2.findContours(sat_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        perimeter = cv2.arcLength(largest, True)
        features.append(4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0.0)
    else:
        features.append(0.0)
    features.append(float(np.mean(v[:32, :])) - float(np.mean(v[32:, :])))
    features.append(avg_r / max(avg_b, 1.0))
    features.append(float(np.mean((h >= 10) & (h <= 25) & (s >= 40) & (s <= 150))))
    features.append(float(np.mean((gray >= 80) & (gray <= 160) & (s < 60))))
    edges = cv2.Canny(gray, 30, 100)
    features.append(float(np.mean(edges[16:48, 16:48] > 0)))
    warm_region = (h < 30) & (s > 30) & (v > 50)
    if np.sum(warm_region) > 100:
        features.append(float(np.std(lap[warm_region])))
    else:
        features.append(0.0)
    if np.sum(warm_region) > 100:
        features.append(float(np.mean(v[warm_region])))
    else:
        features.append(128.0)
    features.append(avg_r / max(avg_g, 1.0))
    center_gray = float(np.mean(gray[16:48, 16:48]))
    periph_gray = (float(np.mean(gray[:16, :])) + float(np.mean(gray[48:, :])) +
                   float(np.mean(gray[:, :16])) + float(np.mean(gray[:, 48:]))) / 4.0
    features.append(center_gray - periph_gray)
    features.append(float(np.mean(v[48:, :] < 80)))
    features.append(float(np.mean((h >= 20) & (h <= 35) & (s > 80) & (v > 120))))
    features.append(float(np.mean(np.abs(lap) < 5)))
    padded = np.pad(gray, 1, mode='reflect')
    center_p = padded[1:-1, 1:-1].astype(np.int16)
    d_top = np.abs(padded[0:-2, 1:-1].astype(np.int16) - center_p)
    d_bot = np.abs(padded[2:, 1:-1].astype(np.int16) - center_p)
    d_left = np.abs(padded[1:-1, 0:-2].astype(np.int16) - center_p)
    d_right = np.abs(padded[1:-1, 2:].astype(np.int16) - center_p)
    uniform = (d_top < 10) & (d_bot < 10) & (d_left < 10) & (d_right < 10)
    features.append(float(np.mean(uniform)))
    grad_mag = np.sqrt(sobelx**2 + sobely**2)
    grad_mean = float(np.mean(grad_mag))
    grad_std = float(np.std(grad_mag))
    features.append(grad_std / max(grad_mean, 1.0))
    features.append(float(np.mean(s[16:48, 16:48] < 60)))
    features.append(float(np.mean((v > 150) & (s < 80))))
    v_hist = np.histogram(v, bins=4, range=(0, 256))[0].astype(float) / (64 * 64)
    features.append(float(v_hist[0] * v_hist[3]))
    features.append(float(np.mean(s < 40)))
    center_v = float(np.mean(v[16:48, 16:48]))
    border_pixels = np.concatenate([v[:8, :].flatten(), v[56:, :].flatten(),
                                    v[:, :8].flatten(), v[:, 56:].flatten()])
    border_v = float(np.mean(border_pixels))
    features.append(abs(center_v - border_v))
    h_energy = float(np.sum(sobely**2))
    v_energy = float(np.sum(sobelx**2))
    features.append(h_energy / max(h_energy + v_energy, 1.0))
    edge_img = cv2.Canny(gray, 50, 150)
    contours2, _ = cv2.findContours(edge_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours2:
        largest2 = max(contours2, key=cv2.contourArea)
        if len(largest2) >= 5:
            rect = cv2.minAreaRect(largest2)
            w, h_r = rect[1]
            features.append(max(w, h_r) / max(min(w, h_r), 1.0))
        else:
            features.append(1.0)
    else:
        features.append(1.0)
    center_edge = float(np.mean(edges[16:48, 16:48] > 0))
    total_edge = float(np.mean(edges > 0))
    features.append(center_edge / max(total_edge, 0.001))
    sat_pixels = h[s > 50]
    if len(sat_pixels) > 100:
        h_hist_arr = np.histogram(sat_pixels, bins=18, range=(0, 180))[0].astype(float)
        h_hist_arr = h_hist_arr / max(np.sum(h_hist_arr), 1)
        h_hist_arr = h_hist_arr[h_hist_arr > 0]
        features.append(-float(np.sum(h_hist_arr * np.log2(h_hist_arr))))
    else:
        features.append(0.0)
    if len(sat_pixels) > 100:
        features.append(float(np.sum((sat_pixels >= 18) & (sat_pixels <= 38))) / len(sat_pixels))
    else:
        features.append(0.0)
    features.append(float(np.mean((h >= 10) & (h <= 30) & (s > 50) & (v > 100))))
    H2, W2 = 32, 32
    for qi, (r0, c0) in enumerate([(0, 0), (0, W2), (H2, 0), (H2, W2)]):
        r1, c1 = r0 + H2, c0 + W2
        features.append(float(np.mean(h[r0:r1, c0:c1])))
        features.append(float(np.mean(s[r0:r1, c0:c1])))
        features.append(float(np.mean(v[r0:r1, c0:c1])))
        features.append(float(np.mean(edges[r0:r1, c0:c1] > 0)))
    third = 64 // 3
    features.append(float(np.mean(v[:third, :])))
    features.append(float(np.mean(v[third:2*third, :])))
    features.append(float(np.mean(v[2*third:, :])))
    features.append(float(np.mean(s[:third, :])))
    features.append(float(np.mean(s[third:2*third, :])))
    features.append(float(np.mean(s[2*third:, :])))
    features.append(float(np.mean(h[16:48, 16:48])))
    features.append(float(np.mean(edges[:third, :] > 0)))
    features.append(float(np.mean(edges[2*third:, :] > 0)))
    return features
